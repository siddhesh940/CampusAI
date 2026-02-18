"""
Chat Service

Handles AI assistant conversations using OpenAI API.
Fetches real user data from DB to provide contextual responses.
Stores conversation history in DB.
"""

import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.models.chat import ChatMessage, ChatSession
from app.models.document import Document, DocumentStatus
from app.models.hostel import HostelApplication
from app.models.lms import LMSActivation
from app.models.payment import Payment, PaymentStatus
from app.models.user import User
from app.schemas.chat import (
    ChatMessageRequest,
    ChatMessageResponse,
    ChatSessionListResponse,
    ChatSessionResponse,
)

settings = get_settings()


async def _build_user_context(db: AsyncSession, user: User) -> str:
    """Fetch real user data from DB and build a context summary for the AI."""
    user_id = user.id
    parts = [f"Student: {user.full_name} ({user.email})"]

    # Documents
    doc_result = await db.execute(select(Document).where(Document.user_id == user_id))
    docs = doc_result.scalars().all()
    if docs:
        doc_lines = []
        for d in docs:
            doc_lines.append(f"  - {d.document_type.replace('_', ' ').title()}: {d.status.value}")
            if d.status == DocumentStatus.REJECTED and d.rejection_reason:
                doc_lines.append(f"    Rejection reason: {d.rejection_reason}")
        parts.append("Documents:\n" + "\n".join(doc_lines))
    else:
        parts.append("Documents: None uploaded yet")

    # Payments
    pay_result = await db.execute(select(Payment).where(Payment.user_id == user_id))
    payments = pay_result.scalars().all()
    if payments:
        paid = sum(p.amount for p in payments if p.status == PaymentStatus.COMPLETED)
        pending = sum(p.amount for p in payments if p.status == PaymentStatus.PENDING)
        parts.append(f"Payments: ₹{paid:,.0f} paid, ₹{pending:,.0f} pending ({len(payments)} transactions)")
    else:
        parts.append("Payments: No payments made yet")

    # Hostel
    hostel_result = await db.execute(select(HostelApplication).where(HostelApplication.user_id == user_id))
    hostel = hostel_result.scalar_one_or_none()
    if hostel:
        h_info = f"Hostel: Status={hostel.status.value}, Preference={hostel.room_type_preference.value}"
        if hostel.allocated_room_number:
            h_info += f", Room={hostel.allocated_room_number}"
        parts.append(h_info)
    else:
        parts.append("Hostel: Not applied yet")

    # LMS
    lms_result = await db.execute(select(LMSActivation).where(LMSActivation.user_id == user_id))
    lms = lms_result.scalar_one_or_none()
    if lms and lms.is_activated:
        parts.append(f"LMS: Activated (ID: {lms.activation_key}, Platform: {lms.platform})")
    else:
        parts.append("LMS: Not activated yet")

    return "\n".join(parts)


async def _get_ai_response(messages: list[dict], user_context: str = "") -> str:
    """Call OpenAI API for a chat completion with real user context."""
    try:
        import openai

        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

        system_prompt = (
            "You are CampusAI Assistant, a helpful AI for university student onboarding. "
            "You help students with document uploads, fee payments, hostel applications, "
            "LMS activation, and general campus queries. "
            "Be concise, friendly, and helpful. "
            "IMPORTANT: You have access to the student's real onboarding data below. "
            "Use this data to give specific, personalized answers instead of generic advice.\n\n"
            f"=== STUDENT DATA ===\n{user_context}\n=== END DATA ==="
        )

        api_messages = [{"role": "system", "content": system_prompt}]
        api_messages.extend(messages[-10:])  # Keep last 10 messages for context

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=api_messages,
            max_tokens=1024,
            temperature=0.7,
        )
        return response.choices[0].message.content or "I'm sorry, I couldn't generate a response."

    except ImportError:
        return _fallback_response(messages[-1]["content"] if messages else "", user_context)
    except Exception as e:
        return _fallback_response(messages[-1]["content"] if messages else "", user_context)


def _fallback_response(user_message: str, user_context: str = "") -> str:
    """Context-aware rule-based fallback when OpenAI is unavailable."""
    msg = user_message.lower()

    # Parse context for personalized responses
    has_docs = "Documents:" in user_context and "None uploaded" not in user_context
    has_payments = "Payments:" in user_context and "No payments" not in user_context
    has_hostel = "Hostel:" in user_context and "Not applied" not in user_context
    has_lms = "LMS: Activated" in user_context

    if any(w in msg for w in ["document", "upload", "file", "pdf", "marksheet", "aadhar"]):
        if has_docs:
            # Extract document statuses from context
            doc_section = user_context.split("Documents:\n")[1].split("\n\n")[0] if "Documents:\n" in user_context else ""
            return (
                f"Here's the current status of your documents:\n{doc_section}\n\n"
                "If any document was rejected, please re-upload a corrected version. "
                "Go to Dashboard → Documents to upload or view your files."
            )
        return (
            "You haven't uploaded any documents yet. To get started:\n"
            "1. Go to Dashboard → Documents\n"
            "2. Select the document type (10th marksheet, 12th marksheet, Aadhar, photo)\n"
            "3. Upload a PDF, JPG, or PNG (max 5MB)\n"
            "An admin will review your documents once uploaded."
        )
    elif any(w in msg for w in ["status", "progress", "onboarding", "checklist"]):
        status_parts = ["Here's your onboarding status:"]
        status_parts.append(f"📄 Documents: {'Uploaded' if has_docs else 'Not uploaded yet'}")
        status_parts.append(f"💳 Payments: {'Completed' if has_payments else 'Pending'}")
        status_parts.append(f"🏠 Hostel: {'Applied' if has_hostel else 'Not applied'}")
        status_parts.append(f"📚 LMS: {'Activated' if has_lms else 'Not activated'}")
        return "\n".join(status_parts)
    elif any(w in msg for w in ["payment", "fee", "pay", "tuition"]):
        if has_payments:
            pay_line = [l for l in user_context.split("\n") if l.startswith("Payments:")]
            return f"{pay_line[0] if pay_line else 'Payment info available.'}\n\nVisit Dashboard → Payments to view details or make new payments."
        return (
            "No payments recorded yet. Visit Dashboard → Payments to:\n"
            "1. View required fees (tuition, hostel, library, lab)\n"
            "2. Initiate payment\n"
            "3. Download receipts after completion"
        )
    elif any(w in msg for w in ["hostel", "room", "accommodation"]):
        if has_hostel:
            hostel_line = [l for l in user_context.split("\n") if l.startswith("Hostel:")]
            return f"{hostel_line[0] if hostel_line else 'Hostel application found.'}\n\nVisit Dashboard → Hostel for full details."
        return (
            "You haven't applied for hostel yet. Go to Dashboard → Hostel to:\n"
            "1. Choose room type (single, double, or triple)\n"
            "2. Submit your application\n"
            "An admin will review and assign your room."
        )
    elif any(w in msg for w in ["lms", "learning", "course", "moodle"]):
        if has_lms:
            lms_line = [l for l in user_context.split("\n") if l.startswith("LMS:")]
            return f"Your LMS is already activated! {lms_line[0] if lms_line else ''}\n\nYou can access your courses through the LMS portal."
        return (
            "Your LMS is not activated yet. Go to Dashboard → LMS and click 'Activate'. "
            "You'll receive your LMS credentials immediately."
        )
    elif any(w in msg for w in ["hello", "hi", "hey", "greet"]):
        name = user_context.split("(")[0].replace("Student: ", "").strip() if "Student:" in user_context else "there"
        return (
            f"Hello {name}! 👋 I'm your CampusAI Assistant.\n\n"
            "I have access to your real onboarding data and can help with:\n"
            "• Document uploads and verification status\n"
            "• Fee payment tracking\n"
            "• Hostel application status\n"
            "• LMS activation\n\n"
            "Ask me anything specific like 'What's my document status?' or 'Have I paid my fees?'"
        )
    else:
        return (
            "I'm your CampusAI Assistant with access to your real onboarding data! "
            "Try asking:\n"
            "• 'What's my document status?'\n"
            "• 'Have I paid my fees?'\n"
            "• 'What's my hostel application status?'\n"
            "• 'Is my LMS activated?'\n"
            "• 'What's my onboarding progress?'"
        )


class ChatService:
    """AI chat business logic."""

    @staticmethod
    async def send_message(
        db: AsyncSession, user: User, data: ChatMessageRequest
    ) -> ChatSessionResponse:
        """Process user message and get AI response."""
        # Get or create session
        session = None
        if data.session_id:
            result = await db.execute(
                select(ChatSession).where(
                    ChatSession.id == data.session_id,
                    ChatSession.user_id == user.id,
                )
            )
            session = result.scalar_one_or_none()

        if not session:
            # Create new session
            title = data.message[:50] + ("..." if len(data.message) > 50 else "")
            session = ChatSession(
                id=uuid.uuid4(),
                user_id=user.id,
                university_id=user.university_id,
                title=title,
            )
            db.add(session)
            await db.flush()

        # Store user message
        user_msg = ChatMessage(
            id=uuid.uuid4(),
            session_id=session.id,
            role="user",
            content=data.message,
        )
        db.add(user_msg)
        await db.flush()

        # Build context from session history
        result = await db.execute(
            select(ChatMessage)
            .where(ChatMessage.session_id == session.id)
            .order_by(ChatMessage.created_at)
        )
        history = result.scalars().all()
        context = [{"role": m.role, "content": m.content} for m in history]

        # Fetch real user data for AI context
        user_context = await _build_user_context(db, user)

        # Get AI response with real data
        ai_response = await _get_ai_response(context, user_context)

        # Store assistant message
        assistant_msg = ChatMessage(
            id=uuid.uuid4(),
            session_id=session.id,
            role="assistant",
            content=ai_response,
        )
        db.add(assistant_msg)
        await db.flush()

        # Reload session with all messages
        result = await db.execute(
            select(ChatSession).where(ChatSession.id == session.id)
        )
        session = result.scalar_one()

        # Build response
        result = await db.execute(
            select(ChatMessage)
            .where(ChatMessage.session_id == session.id)
            .order_by(ChatMessage.created_at)
        )
        messages = result.scalars().all()

        return ChatSessionResponse(
            id=session.id,
            title=session.title,
            messages=[ChatMessageResponse.model_validate(m) for m in messages],
            created_at=session.created_at,
            updated_at=session.updated_at,
        )

    @staticmethod
    async def get_history(
        db: AsyncSession, user: User
    ) -> ChatSessionListResponse:
        """List all chat sessions for a user."""
        result = await db.execute(
            select(ChatSession)
            .where(ChatSession.user_id == user.id)
            .order_by(ChatSession.updated_at.desc())
        )
        sessions = result.scalars().all()

        session_responses = []
        for s in sessions:
            msg_result = await db.execute(
                select(ChatMessage)
                .where(ChatMessage.session_id == s.id)
                .order_by(ChatMessage.created_at)
            )
            messages = msg_result.scalars().all()
            session_responses.append(
                ChatSessionResponse(
                    id=s.id,
                    title=s.title,
                    messages=[ChatMessageResponse.model_validate(m) for m in messages],
                    created_at=s.created_at,
                    updated_at=s.updated_at,
                )
            )

        return ChatSessionListResponse(
            sessions=session_responses,
            total=len(session_responses),
        )

    @staticmethod
    async def get_session(
        db: AsyncSession, user: User, session_id: uuid.UUID
    ) -> ChatSessionResponse:
        """Get a specific chat session with messages."""
        result = await db.execute(
            select(ChatSession).where(
                ChatSession.id == session_id,
                ChatSession.user_id == user.id,
            )
        )
        session = result.scalar_one_or_none()
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat session not found.",
            )

        msg_result = await db.execute(
            select(ChatMessage)
            .where(ChatMessage.session_id == session.id)
            .order_by(ChatMessage.created_at)
        )
        messages = msg_result.scalars().all()

        return ChatSessionResponse(
            id=session.id,
            title=session.title,
            messages=[ChatMessageResponse.model_validate(m) for m in messages],
            created_at=session.created_at,
            updated_at=session.updated_at,
        )
