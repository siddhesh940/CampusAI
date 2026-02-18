"""
Dashboard Router

Endpoint: GET /dashboard/summary — aggregated student dashboard data.
Dynamically computes onboarding checklist from real DB state.
"""

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.compliance import ComplianceItem, StudentCompliance
from app.models.course import Enrollment
from app.models.document import Document, DocumentStatus
from app.models.hostel import ApplicationStatus, HostelApplication
from app.models.lms import LMSActivation
from app.models.onboarding import ChecklistItem, OnboardingChecklist
from app.models.payment import Payment, PaymentStatus
from app.models.user import User

router = APIRouter()


def _build_dynamic_checklist(
    docs: list,
    payments: list,
    hostel,
    lms,
    user: User,
    enrollments: list | None = None,
    compliance_done: int = 0,
    compliance_total: int = 0,
) -> dict:
    """Build a dynamic onboarding checklist from actual DB state."""
    items = []

    # 1. Profile completion
    profile_done = bool(user.first_name and user.last_name and user.phone)
    items.append({
        "id": "profile",
        "title": "Complete your profile",
        "description": "Add your name, phone number, and personal details",
        "category": "profile",
        "order": 1,
        "is_completed": profile_done,
        "is_required": True,
    })

    # 2. Document uploads
    required_doc_types = ["10th_marksheet", "12th_marksheet", "aadhar_card", "photo"]
    uploaded_types = {d.document_type for d in docs}
    approved_types = {d.document_type for d in docs if d.status == DocumentStatus.APPROVED}

    docs_uploaded = bool(uploaded_types & set(required_doc_types))
    items.append({
        "id": "documents_upload",
        "title": "Upload required documents",
        "description": f"{len(uploaded_types & set(required_doc_types))}/{len(required_doc_types)} required documents uploaded",
        "category": "documents",
        "order": 2,
        "is_completed": len(uploaded_types & set(required_doc_types)) >= len(required_doc_types),
        "is_required": True,
    })

    all_docs_approved = len(approved_types & set(required_doc_types)) >= len(required_doc_types)
    items.append({
        "id": "documents_approved",
        "title": "Documents verified by admin",
        "description": f"{len(approved_types & set(required_doc_types))}/{len(required_doc_types)} documents approved",
        "category": "documents",
        "order": 3,
        "is_completed": all_docs_approved,
        "is_required": True,
    })

    # 3. Fee payment
    completed_payments = [p for p in payments if p.status == PaymentStatus.COMPLETED]
    has_payment = len(completed_payments) > 0
    total_paid = sum(p.amount for p in completed_payments)
    items.append({
        "id": "payment",
        "title": "Pay admission fees",
        "description": f"₹{total_paid:,.0f} paid" if has_payment else "No payments made yet",
        "category": "payments",
        "order": 4,
        "is_completed": has_payment,
        "is_required": True,
    })

    # 4. Hostel application
    hostel_applied = hostel is not None
    hostel_approved = hostel and hostel.status in (ApplicationStatus.APPROVED, ApplicationStatus.ALLOCATED)
    items.append({
        "id": "hostel",
        "title": "Apply for hostel",
        "description": f"Status: {hostel.status.value}" if hostel else "Not applied yet",
        "category": "hostel",
        "order": 5,
        "is_completed": hostel_applied,
        "is_required": False,
    })

    # 5. LMS activation
    lms_active = lms is not None and lms.is_activated
    items.append({
        "id": "lms",
        "title": "Activate LMS access",
        "description": f"LMS ID: {lms.activation_key}" if lms_active else "Not activated yet",
        "category": "lms",
        "order": 6,
        "is_completed": lms_active,
        "is_required": True,
    })

    # 6. Course enrollment
    enrollment_count = len(enrollments) if enrollments else 0
    items.append({
        "id": "course_enrollment",
        "title": "Enroll in courses",
        "description": f"{enrollment_count} subjects enrolled" if enrollment_count > 0 else "Select your course and subjects",
        "category": "courses",
        "order": 7,
        "is_completed": enrollment_count > 0,
        "is_required": True,
    })

    # 7. Compliance training
    compliance_completed = compliance_done >= compliance_total and compliance_total > 0
    items.append({
        "id": "compliance",
        "title": "Complete compliance training",
        "description": f"{compliance_done}/{compliance_total} items completed" if compliance_total > 0 else "No compliance items configured",
        "category": "compliance",
        "order": 8,
        "is_completed": compliance_completed,
        "is_required": compliance_total > 0,
    })

    # Calculate percentage
    required_items = [i for i in items if i["is_required"]]
    completed_required = [i for i in required_items if i["is_completed"]]
    percentage = round(len(completed_required) / len(required_items) * 100) if required_items else 0

    return {
        "items": items,
        "percentage": percentage,
        "total": len(items),
        "completed": len([i for i in items if i["is_completed"]]),
    }


@router.get(
    "/summary",
    summary="Student dashboard summary",
)
async def dashboard_summary(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Return aggregated dashboard data:
    - document_count and statuses
    - payment_status
    - hostel_status
    - lms_status
    - onboarding_percentage (dynamically computed)
    """
    user_id = current_user.id

    # Documents
    doc_result = await db.execute(
        select(Document).where(Document.user_id == user_id)
    )
    docs = doc_result.scalars().all()
    doc_total = len(docs)
    doc_approved = sum(1 for d in docs if d.status == DocumentStatus.APPROVED)
    doc_pending = sum(1 for d in docs if d.status == DocumentStatus.PENDING)
    doc_rejected = sum(1 for d in docs if d.status == DocumentStatus.REJECTED)
    doc_under_review = sum(1 for d in docs if d.status == DocumentStatus.UNDER_REVIEW)

    # Payments
    pay_result = await db.execute(
        select(Payment).where(Payment.user_id == user_id)
    )
    payments = pay_result.scalars().all()
    total_paid = sum(p.amount for p in payments if p.status == PaymentStatus.COMPLETED)
    total_pending = sum(p.amount for p in payments if p.status == PaymentStatus.PENDING)
    payment_status = "completed" if payments and all(
        p.status == PaymentStatus.COMPLETED for p in payments
    ) else ("pending" if payments else "none")

    # Hostel
    hostel_result = await db.execute(
        select(HostelApplication).where(HostelApplication.user_id == user_id)
    )
    hostel = hostel_result.scalar_one_or_none()
    hostel_status = hostel.status.value if hostel else "not_applied"

    # LMS
    lms_result = await db.execute(
        select(LMSActivation).where(LMSActivation.user_id == user_id)
    )
    lms = lms_result.scalar_one_or_none()
    lms_status = "activated" if lms and lms.is_activated else "inactive"

    # Enrollments
    enroll_result = await db.execute(
        select(Enrollment).where(
            Enrollment.user_id == user_id,
            Enrollment.status == "active",
        )
    )
    enrollments = enroll_result.scalars().all()

    # Compliance
    compliance_total_result = await db.execute(
        select(func.count()).where(
            ComplianceItem.university_id == current_user.university_id,
            ComplianceItem.is_active == True,
            ComplianceItem.is_required == True,
        )
    )
    compliance_total = compliance_total_result.scalar() or 0

    compliance_done_result = await db.execute(
        select(func.count()).where(
            StudentCompliance.user_id == user_id,
            StudentCompliance.is_completed == True,
            StudentCompliance.compliance_item_id.in_(
                select(ComplianceItem.id).where(
                    ComplianceItem.university_id == current_user.university_id,
                    ComplianceItem.is_active == True,
                    ComplianceItem.is_required == True,
                )
            ),
        )
    )
    compliance_done = compliance_done_result.scalar() or 0

    # Dynamic checklist
    checklist = _build_dynamic_checklist(
        docs, payments, hostel, lms, current_user,
        enrollments=list(enrollments),
        compliance_done=compliance_done,
        compliance_total=compliance_total,
    )

    return {
        "documents": {
            "total": doc_total,
            "approved": doc_approved,
            "pending": doc_pending,
            "rejected": doc_rejected,
            "under_review": doc_under_review,
        },
        "payments": {
            "status": payment_status,
            "total_paid": total_paid,
            "total_pending": total_pending,
            "count": len(payments),
        },
        "hostel": {
            "status": hostel_status,
            "room_type": hostel.room_type_preference.value if hostel else None,
            "room_number": hostel.allocated_room_number if hostel else None,
        },
        "lms": {
            "status": lms_status,
            "lms_id": lms.activation_key if lms else None,
            "platform": lms.platform if lms else "Moodle",
        },
        "onboarding_percentage": checklist["percentage"],
        "checklist": checklist,
        "user": {
            "name": current_user.full_name,
            "email": current_user.email,
            "role": current_user.role.value,
        },
    }
