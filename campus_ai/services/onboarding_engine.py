"""
CampusAI - Onboarding Engine
Rule-based chat engine with knowledge base for student onboarding queries.
"""
import json
import os
from datetime import datetime

from sqlalchemy.orm.session import Session

from typing import List

from database import get_session
from models import ChatHistory, Escalation


KB_PATH: str = os.path.join(os.path.dirname(__file__), "..", "knowledge_base.json")

INTENT_KEYWORDS: dict[str, list[str]] = {
    "fee": ["fee", "fees", "payment", "pay", "tuition", "scholarship", "money", "cost", "amount", "refund", "installment"],
    "documents": ["document", "documents", "marksheet", "certificate", "id proof", "photo", "submit", "verification", "verify", "upload"],
    "hostel": ["hostel", "room", "accommodation", "mess", "laundry", "roommate", "warden"],
    "lms": ["lms", "learning", "moodle", "canvas", "course", "assignment", "login", "portal", "access"],
    "orientation": ["orientation", "induction", "welcome", "schedule", "program", "event"],
    "mentor": ["mentor", "faculty", "advisor", "guidance", "counselor", "counselling"],
    "timetable": ["timetable", "schedule", "class", "lecture", "timing", "slot", "routine"],
    "contacts": ["contact", "phone", "email", "helpdesk", "support", "office", "department", "number"],
    "status": ["status", "progress", "stage", "track", "where am i", "onboarding"],
    "greeting": ["hello", "hi", "hey", "good morning", "good afternoon", "help", "start"]
}


def load_knowledge_base():
    """Load FAQ knowledge base from JSON."""
    try:
        with open(KB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def detect_intent(message) -> str:
    """Detect user intent from message using keyword matching."""
    lower_msg = message.lower().strip()

    best_intent = "unknown"
    best_score = 0

    for intent_name, keywords in INTENT_KEYWORDS.items():
        score = 0
        for kw in keywords:
            if kw in lower_msg:
                score += 1
        if score > best_score:
            best_score: int = score
            best_intent: str = intent_name

    if best_score == 0:
        return "unknown"
    return best_intent


def get_response(message, student_data):
    """Generate a response based on intent and student context."""
    intent: str = detect_intent(message)
    kb = load_knowledge_base()

    if intent == "greeting":
        name = student_data.get("name", "Student")
        stage = student_data.get("onboarding_stage", 1)
        return (
            "Hello, " + name + "! Welcome to CampusAI. "
            "You are currently at Stage " + str(stage) + " of your onboarding. "
            "How can I help you today? You can ask about fees, documents, LMS, hostel, orientation, or your onboarding status."
        )

    if intent == "fee":
        return _build_fee_response(kb, student_data)

    if intent == "documents":
        return _build_documents_response(kb, student_data)

    if intent == "hostel":
        return _build_hostel_response(kb, student_data)

    if intent == "lms":
        return _build_lms_response(kb, student_data)

    if intent == "orientation":
        return _build_orientation_response(kb, student_data)

    if intent == "mentor":
        return _build_mentor_response(kb, student_data)

    if intent == "timetable":
        return _build_timetable_response(kb)

    if intent == "contacts":
        return _build_contacts_response(kb)

    if intent == "status":
        return _build_status_response(student_data)

    return (
        "I can help you with:\n\n"
        "- **Fee Payment** — Payment options, deadlines, scholarships\n"
        "- **Documents** — Required documents and verification\n"
        "- **LMS Access** — Activate your learning portal\n"
        "- **Hostel** — Room types, facilities, application\n"
        "- **Orientation** — Schedule and details\n"
        "- **Mentor** — Faculty mentor assignment\n"
        "- **Timetable** — Class schedule info\n"
        "- **Contacts** — Department contacts\n\n"
        "Please ask your question and I'll provide detailed guidance!"
    )


def _build_fee_response(kb, student_data) -> str:
    """Build fee-related response."""
    fee_data = kb.get("fees", {})
    status = student_data.get("fee_status", "unpaid")

    if status == "paid":
        return "Your fee payment has been confirmed. No pending payments at this time."

    parts: list[str] = ["**Fee Payment Information**\n"]

    total = fee_data.get("tuition_fee", "")
    if total:
        parts.append("**Tuition Fee:** " + total)

    hostel_fee = fee_data.get("hostel_fee", "")
    if hostel_fee:
        parts.append("**Hostel Fee:** " + hostel_fee)

    methods = fee_data.get("payment_methods", [])
    if methods:
        parts.append("\n**Payment Methods:** " + ", ".join(methods))

    deadline = fee_data.get("deadline", "")
    if deadline:
        parts.append("\n**Deadline:** " + deadline)

    installment = fee_data.get("installment_plan", "")
    if installment:
        parts.append("**Installment Plan:** " + installment)

    scholarship = fee_data.get("scholarship_info", "")
    if scholarship:
        parts.append("\n**Scholarship:** " + scholarship)

    refund = fee_data.get("refund_policy", "")
    if refund:
        parts.append("**Refund Policy:** " + refund)

    late_fee = fee_data.get("late_fee", "")
    if late_fee:
        parts.append("**Late Fee:** " + late_fee)

    contact = fee_data.get("contact", "")
    if contact:
        parts.append("\n**Contact:** " + contact)

    parts.append("\n\n⚠️ *Your fee is currently unpaid. Please complete payment to proceed with onboarding.*")
    parts.append("\n👉 **Click the button below to pay your fees online.**")
    parts.append("{{PORTAL:portal_fees:💰 Open Fee Portal}}")
    return "\n".join(parts)


def _build_documents_response(kb, student_data) -> str:
    """Build documents-related response."""
    doc_data = kb.get("documents", {})
    verified = student_data.get("documents_verified", False)

    if verified:
        return "All your documents have been verified successfully."

    parts: list[str] = ["**Document Requirements**\n"]

    required = doc_data.get("required_documents", [])
    if required:
        parts.append("**Required Documents:**")
        for doc in required:
            parts.append("  - " + doc)

    submission = doc_data.get("submission_method", "")
    if submission:
        parts.append("\n**How to Submit:** " + submission)

    processing = doc_data.get("processing_time", "")
    if processing:
        parts.append("**Processing Time:** " + processing)

    contact = doc_data.get("contact", "")
    if contact:
        parts.append("**Contact:** " + contact)

    parts.append("\n👉 **Upload your documents on the Document Portal below.**")
    parts.append("{{PORTAL:portal_documents:📄 Open Document Portal}}")
    return "\n".join(parts)


def _build_hostel_response(kb, student_data) -> str:
    """Build hostel-related response."""
    hostel_data = kb.get("hostel", {})
    parts: list[str] = ["**Hostel Information**\n"]

    room_types = hostel_data.get("room_types", {})
    if room_types:
        parts.append("**Room Types & Pricing:**")
        for rtype, price in room_types.items():
            parts.append("  - **" + rtype.title() + ":** " + str(price))

    facilities = hostel_data.get("facilities", [])
    if facilities:
        parts.append("\n**Facilities:** " + ", ".join(facilities))

    contact = hostel_data.get("contact", "")
    if contact:
        parts.append("**Contact:** " + contact)

    allotment = hostel_data.get("allotment", "")
    if allotment:
        parts.append("**Allotment:** " + allotment)

    rules = hostel_data.get("rules", "")
    if rules:
        parts.append("**Rules:** " + rules)

    parts.append("\n👉 **Apply for hostel accommodation on the Hostel Portal below.**")
    parts.append("{{PORTAL:portal_hostel:🏠 Open Hostel Portal}}")
    return "\n".join(parts)


def _build_lms_response(kb, student_data):
    """Build LMS-related response."""
    lms_data = kb.get("lms", {})
    activated = student_data.get("lms_activated", False)

    if activated:
        return (
            "Your LMS account is already activated! ✅\n\n"
            "**Platform:** " + lms_data.get("platform", "Campus LMS") + "\n"
            "**Mobile App:** " + lms_data.get("mobile_app", "Available") + "\n\n"
            "Access your courses, assignments, and materials on the LMS Portal.\n\n"
            "If you face any issues, contact: " + lms_data.get("contact", "IT Support") + "\n"
            "{{PORTAL:portal_lms:💻 Open LMS Portal}}"
        )

    parts: list[str] = ["**LMS Activation Guide**\n"]

    parts.append("**Platform:** " + lms_data.get("platform", "Campus LMS"))

    features = lms_data.get("features", [])
    if features:
        parts.append("**Features:** " + ", ".join(features))

    steps = lms_data.get("activation_steps", [])
    if steps:
        parts.append("\n**Steps to Activate:**")
        for idx, step in enumerate(steps):
            parts.append("  " + str(idx + 1) + ". " + step)

    parts.append("\n**Support Hours:** " + lms_data.get("support_hours", "Mon-Fri, 9 AM - 6 PM"))

    contact = lms_data.get("contact", "")
    if contact:
        parts.append("**Support:** " + contact)

    parts.append("\n👉 **Activate your LMS account on the portal below.**")
    parts.append("{{PORTAL:portal_lms:💻 Open LMS Portal}}")
    return "\n".join(parts)


def _build_orientation_response(kb, student_data) -> str:
    """Build orientation-related response."""
    orient_data = kb.get("orientation", {})
    completed = student_data.get("orientation_completed", False)

    if completed:
        return "You have already completed the orientation program."

    parts: list[str] = ["**Orientation Program**\n"]

    schedule = orient_data.get("schedule", "")
    if schedule:
        parts.append("**Schedule:** " + schedule)

    venue = orient_data.get("venue", "")
    if venue:
        parts.append("**Venue:** " + venue)

    items = orient_data.get("what_to_bring", [])
    if items:
        parts.append("\n**What to Bring:**")
        for item in items:
            parts.append("  - " + item)

    contact = orient_data.get("contact", "")
    if contact:
        parts.append("\n**Contact:** " + contact)

    return "\n".join(parts)


def _build_mentor_response(kb, student_data):
    """Build mentor-related response."""
    mentor_data = kb.get("mentor", {})
    assigned = student_data.get("mentor_assigned", "")

    if assigned:
        return "Your assigned mentor is **" + assigned + "**. Please schedule a meeting during office hours."

    parts: list[str] = ["**Faculty Mentor Program**\n"]

    about = mentor_data.get("about", "")
    if about:
        parts.append(about)

    contact = mentor_data.get("contact", "")
    if contact:
        parts.append("\n**Contact:** " + contact)

    parts.append("\n*Mentor assignment is in progress. You will be notified once assigned.*")
    return "\n".join(parts)


def _build_timetable_response(kb) -> str:
    """Build timetable-related response."""
    tt_data = kb.get("timetable", {})
    parts: list[str] = ["**Timetable Information**\n"]

    class_timings = tt_data.get("class_timings", "")
    if class_timings:
        parts.append("**Class Timings:** " + class_timings)

    info = tt_data.get("info", "")
    if info:
        parts.append("\n" + info)

    info_note = tt_data.get("info_note", "")
    if info_note:
        parts.append("\n📌 " + info_note)

    contact = tt_data.get("contact", "")
    if contact:
        parts.append("\n**Contact:** " + contact)

    parts.append("\n{{PORTAL:dashboard:📊 Go to Dashboard}}")
    return "\n".join(parts)


def _build_contacts_response(kb) -> str:
    """Build contacts response."""
    contacts_data = kb.get("contacts", {})
    parts: list[str] = ["**Campus Contact Directory**\n"]

    for dept, info in contacts_data.items():
        dept_name = dept.replace("_", " ").title()
        parts.append("**" + dept_name + "**")
        if isinstance(info, dict):
            for key, val in info.items():
                parts.append("  " + key.title() + ": " + str(val))
        else:
            parts.append("  " + str(info))
        parts.append("")

    return "\n".join(parts)


def _build_status_response(student_data) -> str:
    """Build onboarding status response."""
    stage = student_data.get("onboarding_stage", 1)
    stage_names: dict[int, str] = {
        1: "Admission Confirmation",
        2: "Document Verification",
        3: "Academic Setup",
        4: "Campus Integration"
    }

    parts: list[str] = ["**Your Onboarding Status**\n"]
    parts.append("**Current Stage:** " + str(stage) + " — " + stage_names.get(stage, ""))
    parts.append("**Progress:** " + str(stage * 25) + "%\n")

    parts.append("**Checklist:**")
    fee_ok = student_data.get("fee_status") == "paid"
    doc_ok = student_data.get("documents_verified", False)
    lms_ok = student_data.get("lms_activated", False)
    orient_ok = student_data.get("orientation_completed", False)

    parts.append(("  ✅" if fee_ok else "  ❌") + " Fee Payment")
    parts.append(("  ✅" if doc_ok else "  ❌") + " Document Verification")
    parts.append(("  ✅" if lms_ok else "  ❌") + " LMS Activation")
    parts.append(("  ✅" if orient_ok else "  ❌") + " Orientation")

    return "\n".join(parts)


def save_chat_message(student_id, role, message) -> None:
    """Save a chat message to history."""
    session: Session = get_session()
    try:
        entry = ChatHistory(
            student_id=student_id,
            role=role,
            message=message,
            timestamp=datetime.utcnow()
        )
        session.add(entry)
        session.commit()
    except Exception:
        session.rollback()
    finally:
        session.close()


def get_chat_messages(student_id, limit=50):
    """Get recent chat messages for a student."""
    session: Session = get_session()
    try:
        messages: List[ChatHistory] = session.query(ChatHistory).filter(
            ChatHistory.student_id == student_id
        ).order_by(ChatHistory.timestamp.asc()).limit(limit).all()

        result = []
        for msg in messages:
            result.append({
                "role": msg.role,
                "message": msg.message,
                "timestamp": msg.timestamp.strftime("%I:%M %p, %b %d") if msg.timestamp else ""
            })
        return result
    finally:
        session.close()


def create_escalation(student_id, subject, message) -> bool:
    """Create an escalation request."""
    session: Session = get_session()
    try:
        esc = Escalation(
            student_id=student_id,
            subject=subject,
            message=message,
            status="pending",
            created_at=datetime.utcnow()
        )
        session.add(esc)
        session.commit()
        return True
    except Exception:
        session.rollback()
        return False
    finally:
        session.close()
