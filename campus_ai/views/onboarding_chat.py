"""
CampusAI - Onboarding Chat Page
Rule-based chat with knowledge base, chat history, and escalation.
"""
import sys
import os

from streamlit.delta_generator import DeltaGenerator

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from datetime import datetime
from services.onboarding_engine import (
    get_response, save_chat_message, get_chat_messages, create_escalation
)
from services.stage_service import get_student_data


def render_chat() -> None:
    """Render the onboarding chat page."""
    user: sys.Any | None = st.session_state.get("user")
    if not user:
        st.error("Please login to access the chat.")
        return

    student_id = user.get("student_id")
    if not student_id:
        st.error("Student profile not found.")
        return

    student = get_student_data(student_id)
    if not student:
        st.error("Could not load student data.")
        return

    # Add user name to student data for personalized responses
    student["name"] = user.get("name", "Student")

    # --- Header ---
    st.markdown(
        '<div class="gradient-header">'
        '<h1>💬 CampusAI Assistant</h1>'
        '<p>Ask anything about your onboarding — fees, documents, LMS, hostel, and more</p>'
        '</div>',
        unsafe_allow_html=True
    )

    # --- Load chat history ---
    if "chat_messages" not in st.session_state:
        stored = get_chat_messages(student_id)
        if stored:
            st.session_state["chat_messages"] = stored
        else:
            welcome_msg = (
                "Hello, " + user.get("name", "") + "! I'm your CampusAI onboarding assistant. "
                "I can help you with:\n\n"
                "- 💰 **Fee Payment** information\n"
                "- 📄 **Document** requirements\n"
                "- 💻 **LMS** activation\n"
                "- 🏠 **Hostel** details\n"
                "- 🎓 **Orientation** schedule\n"
                "- 👨‍🏫 **Mentor** assignment\n"
                "- 📊 **Onboarding Status**\n\n"
                "How can I help you today?"
            )
            st.session_state["chat_messages"] = [{
                "role": "assistant",
                "message": welcome_msg,
                "timestamp": datetime.now().strftime("%I:%M %p, %b %d")
            }]

    # --- Quick Question Buttons ---
    st.markdown("#### Quick Questions")
    qcols: list[DeltaGenerator] = st.columns(4)
    quick_questions: list[tuple[str, DeltaGenerator]] = [
        ("How do I pay fees?", qcols[0]),
        ("What documents needed?", qcols[1]),
        ("How to activate LMS?", qcols[2]),
        ("My onboarding status", qcols[3])
    ]
    for q_text, q_col in quick_questions:
        with q_col:
            if st.button(q_text, key="qq_" + q_text, use_container_width=True):
                _handle_user_message(q_text, student_id, student)

    st.markdown("---")

    # --- Chat Display ---
    # Collect portal navigation buttons from bot messages
    portal_buttons: list[tuple[str, str]] = []

    chat_html = '<div class="chat-container">'
    for msg in st.session_state.get("chat_messages", []):
        role = msg.get("role", "user")
        text = msg.get("message", "")
        timestamp = msg.get("timestamp", "")

        # Extract portal navigation markers before escaping
        import re
        portal_pattern = r'\{\{PORTAL:([a-z_]+):(.+?)\}\}'
        found_portals: list[Any] = re.findall(portal_pattern, text)
        # Only collect portals from the LAST bot message
        if role == "assistant":
            portal_buttons = [(pk, pl) for pk, pl in found_portals]
        # Remove portal markers from display text
        display_text: str = re.sub(portal_pattern, '', text).rstrip('\n')

        # Escape HTML in message
        safe_text: str = display_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        # Convert **bold** to <strong>
        safe_text: str = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', safe_text)
        # Convert *italic* to <em>
        safe_text: str = re.sub(r'\*(.+?)\*', r'<em>\1</em>', safe_text)
        # Convert markdown links [text](url) to clickable <a> tags
        safe_text: str = re.sub(
            r'\[([^\]]+)\]\(([^)]+)\)',
            r'<a href="\2" target="_blank" style="color: #818cf8; text-decoration: underline;">\1</a>',
            safe_text
        )
        # Convert newlines to br
        safe_text: str = safe_text.replace("\n", "<br>")

        if role == "user":
            chat_html += (
                '<div style="display: flex; justify-content: flex-end; margin-bottom: 0.8rem;">'
                '<div class="chat-message chat-user">'
                '<div>' + safe_text + '</div>'
                '<div class="chat-timestamp">' + timestamp + '</div>'
                '</div></div>'
            )
        else:
            chat_html += (
                '<div style="display: flex; justify-content: flex-start; margin-bottom: 0.8rem;">'
                '<div class="chat-message chat-bot">'
                '<div style="font-size: 0.75rem; color: #818cf8; margin-bottom: 0.3rem; font-weight: 600;">🤖 CampusAI</div>'
                '<div>' + safe_text + '</div>'
                '<div class="chat-timestamp">' + timestamp + '</div>'
                '</div></div>'
            )
    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)

    # --- Portal Navigation Buttons ---
    if portal_buttons:
        st.markdown(
            '<div style="background: rgba(99,102,241,0.08); border: 1px solid rgba(99,102,241,0.2); '
            'border-radius: 12px; padding: 0.8rem 1rem; margin: 0.5rem 0 1rem 0;">'
            '<span style="color: #818cf8; font-size: 0.8rem; font-weight: 600;">🔗 Quick Navigation</span>'
            '</div>',
            unsafe_allow_html=True
        )
        btn_cols: list[DeltaGenerator] = st.columns(len(portal_buttons))
        for idx, (page_key, label) in enumerate(portal_buttons):
            with btn_cols[idx]:
                if st.button(label, key="portal_nav_" + page_key + "_" + str(idx), use_container_width=True):
                    st.session_state["current_page"] = page_key
                    st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Input Area ---
    input_col, btn_col = st.columns([5, 1])
    with input_col:
        user_input: str = st.text_input(
            "Message",
            placeholder="Ask about your onboarding...",
            key="chat_input",
            label_visibility="collapsed"
        )
    with btn_col:
        send_clicked: bool = st.button("Send ➤", key="send_btn", use_container_width=True)

    if send_clicked and user_input:
        _handle_user_message(user_input, student_id, student)

    # --- Escalation ---
    st.markdown("---")
    with st.expander("⚠️ Need more help? Escalate to an advisor"):
        esc_subject: str = st.text_input("Subject", placeholder="Brief subject of your issue", key="esc_subject")
        esc_message: str = st.text_area("Describe your issue", placeholder="Provide details about what you need help with...", key="esc_message")
        if st.button("Submit Escalation", key="esc_submit"):
            if esc_subject and esc_message:
                success: bool = create_escalation(student_id, esc_subject, esc_message)
                if success:
                    st.success("Escalation submitted! An advisor will contact you soon.")
                else:
                    st.error("Failed to submit escalation. Please try again.")
            else:
                st.warning("Please fill in both subject and description.")


def _handle_user_message(message, student_id, student) -> sys.NoReturn:
    """Process user message and generate response."""
    timestamp: str = datetime.now().strftime("%I:%M %p, %b %d")

    # Add user message
    st.session_state["chat_messages"].append({
        "role": "user",
        "message": message,
        "timestamp": timestamp
    })
    save_chat_message(student_id, "user", message)

    # Generate response
    response = get_response(message, student)

    # Add bot response
    st.session_state["chat_messages"].append({
        "role": "assistant",
        "message": response,
        "timestamp": timestamp
    })
    save_chat_message(student_id, "assistant", response)

    st.rerun()
