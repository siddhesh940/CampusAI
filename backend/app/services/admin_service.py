"""
Admin Service

Handles admin panel operations: student management, analytics, document review queue.
"""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.document import Document, DocumentStatus
from app.models.hostel import HostelApplication, ApplicationStatus
from app.models.lms import LMSActivation
from app.models.onboarding import OnboardingChecklist
from app.models.payment import Payment, PaymentStatus
from app.models.user import User, UserRole
from app.schemas.document import DocumentListResponse, DocumentResponse
from app.schemas.user import UserListResponse, UserResponse
from app.services.document_service import _doc_to_response


class AdminService:
    """Admin panel business logic."""

    @staticmethod
    async def list_students(
        db: AsyncSession, admin: User, page: int, per_page: int, search: str | None
    ) -> UserListResponse:
        """List students in the admin's university with search and pagination."""
        query = select(User).where(
            User.university_id == admin.university_id,
            User.role == UserRole.STUDENT,
        )
        if search:
            search_filter = f"%{search}%"
            query = query.where(
                (User.email.ilike(search_filter))
                | (User.first_name.ilike(search_filter))
                | (User.last_name.ilike(search_filter))
            )

        # Count total
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar() or 0

        # Paginate
        query = query.offset((page - 1) * per_page).limit(per_page).order_by(User.created_at.desc())
        result = await db.execute(query)
        students = result.scalars().all()

        return UserListResponse(
            users=[UserResponse.model_validate(s) for s in students],
            total=total,
            page=page,
            per_page=per_page,
        )

    @staticmethod
    async def get_analytics(db: AsyncSession, admin: User) -> dict:
        """Get onboarding analytics for the admin's university."""
        uni_id = admin.university_id

        # Total students
        total_result = await db.execute(
            select(func.count()).where(
                User.university_id == uni_id,
                User.role == UserRole.STUDENT,
            )
        )
        total_students = total_result.scalar() or 0

        # Completed onboarding
        completed_result = await db.execute(
            select(func.count()).where(
                OnboardingChecklist.university_id == uni_id,
                OnboardingChecklist.is_completed == True,
            )
        )
        completed = completed_result.scalar() or 0

        # Documents
        docs_total = await db.execute(
            select(func.count()).where(Document.university_id == uni_id)
        )
        docs_approved = await db.execute(
            select(func.count()).where(
                Document.university_id == uni_id,
                Document.status == DocumentStatus.APPROVED,
            )
        )
        docs_pending = await db.execute(
            select(func.count()).where(
                Document.university_id == uni_id,
                Document.status == DocumentStatus.PENDING,
            )
        )

        # Payments
        payments_total = await db.execute(
            select(func.coalesce(func.sum(Payment.amount), 0)).where(
                Payment.university_id == uni_id,
                Payment.status == PaymentStatus.COMPLETED,
            )
        )
        payments_pending = await db.execute(
            select(func.count()).where(
                Payment.university_id == uni_id,
                Payment.status == PaymentStatus.PENDING,
            )
        )

        # Hostel
        hostel_pending = await db.execute(
            select(func.count()).where(
                HostelApplication.university_id == uni_id,
                HostelApplication.status == ApplicationStatus.PENDING,
            )
        )
        hostel_allocated = await db.execute(
            select(func.count()).where(
                HostelApplication.university_id == uni_id,
                HostelApplication.status.in_([ApplicationStatus.APPROVED, ApplicationStatus.ALLOCATED]),
            )
        )

        return {
            "total_students": total_students,
            "onboarding_completed": completed,
            "completion_rate": round((completed / total_students * 100), 1) if total_students > 0 else 0,
            "documents": {
                "total": docs_total.scalar() or 0,
                "approved": docs_approved.scalar() or 0,
                "pending": docs_pending.scalar() or 0,
            },
            "payments": {
                "revenue": float(payments_total.scalar() or 0),
                "pending_count": payments_pending.scalar() or 0,
            },
            "hostel": {
                "pending": hostel_pending.scalar() or 0,
                "allocated": hostel_allocated.scalar() or 0,
            },
        }

    @staticmethod
    async def get_pending_documents(
        db: AsyncSession, admin: User
    ) -> DocumentListResponse:
        """List documents pending review in the admin's university."""
        return await AdminService.get_documents(db, admin, status_filter="pending")

    @staticmethod
    async def get_documents(
        db: AsyncSession,
        admin: User,
        status_filter: str | None = None,
        page: int = 1,
        per_page: int = 50,
        search: str | None = None,
    ) -> DocumentListResponse:
        """List all documents in admin's university with status filtering, pagination, and student info."""
        query = (
            select(Document)
            .options(selectinload(Document.user))
            .where(Document.university_id == admin.university_id)
        )

        # Status filter
        if status_filter and status_filter != "all":
            try:
                doc_status = DocumentStatus(status_filter)
                query = query.where(Document.status == doc_status)
            except ValueError:
                pass  # ignore invalid status

        # Search by student name/email or document type
        if search:
            search_filter = f"%{search}%"
            query = query.join(Document.user).where(
                (User.email.ilike(search_filter))
                | (User.first_name.ilike(search_filter))
                | (User.last_name.ilike(search_filter))
                | (Document.document_type.ilike(search_filter))
                | (Document.file_name.ilike(search_filter))
            )

        # Count total
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar() or 0

        # Paginate and order
        query = query.order_by(Document.created_at.desc()).offset((page - 1) * per_page).limit(per_page)
        result = await db.execute(query)
        docs = result.scalars().all()

        return DocumentListResponse(
            documents=[_doc_to_response(d) for d in docs],
            total=total,
        )

    @staticmethod
    async def get_escalations(db: AsyncSession, admin: User) -> dict:
        """Get escalated issues requiring admin attention."""
        uni_id = admin.university_id

        # Pending documents older than 3 days
        pending_docs = await db.execute(
            select(func.count()).where(
                Document.university_id == uni_id,
                Document.status == DocumentStatus.PENDING,
            )
        )

        # Pending hostel applications
        pending_hostel = await db.execute(
            select(func.count()).where(
                HostelApplication.university_id == uni_id,
                HostelApplication.status == ApplicationStatus.PENDING,
            )
        )

        # Failed payments
        failed_payments = await db.execute(
            select(func.count()).where(
                Payment.university_id == uni_id,
                Payment.status == PaymentStatus.FAILED,
            )
        )

        return {
            "pending_documents": pending_docs.scalar() or 0,
            "pending_hostel_applications": pending_hostel.scalar() or 0,
            "failed_payments": failed_payments.scalar() or 0,
            "total_escalations": (
                (pending_docs.scalar() or 0)
                + (pending_hostel.scalar() or 0)
                + (failed_payments.scalar() or 0)
            ),
        }
