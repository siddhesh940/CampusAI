"""
CampusAI - Stage Service
Calculates and updates onboarding stages based on student progress.
"""
from database import get_session
from models import Student


STAGE_NAMES: dict[int, str] = {
    1: "Admission Confirmation",
    2: "Document Verification",
    3: "Academic Setup",
    4: "Campus Integration"
}

STAGE_DESCRIPTIONS: dict[int, str] = {
    1: "Complete fee payment to progress",
    2: "Submit and verify all required documents",
    3: "Activate LMS and register for courses",
    4: "Complete orientation and campus integration"
}


def calculate_stage(student_data) -> int:
    """Calculate onboarding stage from student data dict."""
    if student_data.get("fee_status") != "paid":
        return 1

    if not student_data.get("documents_verified"):
        return 2

    if not student_data.get("lms_activated"):
        return 3

    return 4


def get_stage_progress(stage) -> int:
    """Get progress percentage for a stage."""
    progress_map: dict[int, int] = {1: 25, 2: 50, 3: 75, 4: 100}
    return progress_map.get(stage, 0)


def get_stage_name(stage) -> str:
    """Get human-readable stage name."""
    return STAGE_NAMES.get(stage, "Unknown")


def get_stage_description(stage) -> str:
    """Get stage description."""
    return STAGE_DESCRIPTIONS.get(stage, "")


def get_pending_tasks(student_data):
    """Get list of pending tasks for a student."""
    tasks = []

    if student_data.get("fee_status") != "paid":
        tasks.append({
            "task": "Pay Admission Fee",
            "category": "fee",
            "priority": "high",
            "icon": "💰"
        })

    if not student_data.get("documents_verified"):
        tasks.append({
            "task": "Submit & Verify Documents",
            "category": "documents",
            "priority": "high",
            "icon": "📄"
        })

    if not student_data.get("lms_activated"):
        tasks.append({
            "task": "Activate LMS Account",
            "category": "lms",
            "priority": "medium",
            "icon": "💻"
        })

    if not student_data.get("orientation_completed"):
        tasks.append({
            "task": "Complete Orientation",
            "category": "orientation",
            "priority": "medium",
            "icon": "🎓"
        })

    if not student_data.get("mentor_assigned"):
        tasks.append({
            "task": "Get Mentor Assignment",
            "category": "mentor",
            "priority": "low",
            "icon": "👨‍🏫"
        })

    return tasks


def update_student_stage(student_id) -> bool:
    """Recalculate and update student's onboarding stage."""
    session = get_session()
    try:
        student = session.query(Student).filter(Student.id == student_id).first()
        if not student:
            return False

        data = {
            "fee_status": student.fee_status,
            "documents_verified": student.documents_verified,
            "lms_activated": student.lms_activated,
            "orientation_completed": student.orientation_completed,
            "mentor_assigned": student.mentor_assigned
        }
        new_stage: int = calculate_stage(data)
        student.onboarding_stage = new_stage
        session.commit()
        return True
    except Exception:
        session.rollback()
        return False
    finally:
        session.close()


def get_student_data(student_id):
    """Get full student data as dict."""
    session = get_session()
    try:
        student = session.query(Student).filter(Student.id == student_id).first()
        if not student:
            return None
        return {
            "id": student.id,
            "user_id": student.user_id,
            "branch": student.branch or "",
            "year": student.year or 1,
            "hostel_preference": student.hostel_preference or "none",
            "fee_status": student.fee_status or "unpaid",
            "documents_verified": bool(student.documents_verified),
            "lms_activated": bool(student.lms_activated),
            "orientation_completed": bool(student.orientation_completed),
            "mentor_assigned": student.mentor_assigned or "",
            "phone": student.phone or "",
            "address": student.address or "",
            "onboarding_stage": student.onboarding_stage or 1
        }
    finally:
        session.close()


def update_student_field(student_id, field_name, value) -> bool:
    """Update a specific student field."""
    session = get_session()
    try:
        student = session.query(Student).filter(Student.id == student_id).first()
        if not student:
            return False
        setattr(student, field_name, value)
        # Recalculate stage
        data = {
            "fee_status": student.fee_status,
            "documents_verified": student.documents_verified,
            "lms_activated": student.lms_activated,
            "orientation_completed": student.orientation_completed,
            "mentor_assigned": student.mentor_assigned
        }
        student.onboarding_stage = calculate_stage(data)
        session.commit()
        return True
    except Exception:
        session.rollback()
        return False
    finally:
        session.close()
