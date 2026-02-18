"""
CampusAI - Main Application
Production-grade student onboarding platform.
"""
import sys
import os

# Ensure project root is in path
PROJECT_ROOT: str = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Load environment variables from root .env
env_path: str = os.path.join(os.path.dirname(PROJECT_ROOT), ".env")
if os.path.exists(env_path):
    with open(env_path, "r") as ef:
        for line in ef:
            stripped: str = line.strip()
            if stripped and not stripped.startswith("#") and "=" in stripped:
                key_val: list[str] = stripped.split("=", 1)
                os.environ.setdefault(key_val[0].strip(), key_val[1].strip())

import streamlit as st
from database import init_db
from auth import register_user, login_user
from views.dashboard import render_dashboard
from views.onboarding_chat import render_chat
from views.profile import render_profile
from views.admin_panel import render_admin_panel
from views.portals import (
    render_fee_portal, render_document_portal,
    render_lms_portal, render_hostel_portal
)


def load_css() -> None:
    """Load custom CSS styles."""
    css_path: str = os.path.join(PROJECT_ROOT, "static", "styles.css")
    if os.path.exists(css_path):
        with open(css_path, "r") as f:
            st.markdown("<style>" + f.read() + "</style>", unsafe_allow_html=True)


def render_sidebar() -> None:
    """Render the sidebar navigation."""
    user = st.session_state.get("user")

    with st.sidebar:
        # Logo and branding
        st.markdown(
            '<div style="text-align: center; padding: 1rem 0;">'
            '<h1 style="background: linear-gradient(135deg, #667eea, #a78bfa); '
            '-webkit-background-clip: text; -webkit-text-fill-color: transparent; '
            'font-size: 1.8rem; margin: 0;">CampusAI</h1>'
            '<p style="color: #6b7280; font-size: 0.85rem; margin: 0;">Smart Onboarding Platform</p>'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown("---")

        if user:
            # User info
            role_badge_color: str = "#818cf8" if user.get("role") == "student" else "#f59e0b"
            role_label = user.get("role", "").upper()
            st.markdown(
                '<div style="background: rgba(30,30,63,0.5); border-radius: 12px; padding: 1rem; margin-bottom: 1rem;">'
                '<p style="color: #e0e0f0; font-weight: 600; margin: 0;">👤 ' + user.get("name", "") + '</p>'
                '<p style="color: #6b7280; font-size: 0.8rem; margin: 0.3rem 0;">' + user.get("email", "") + '</p>'
                '<span style="background: ' + role_badge_color + '22; color: ' + role_badge_color + '; '
                'padding: 0.15rem 0.6rem; border-radius: 10px; font-size: 0.7rem; font-weight: 600;">'
                + role_label + '</span>'
                '</div>',
                unsafe_allow_html=True
            )

            # Navigation
            st.markdown("### Navigation")

            if user.get("role") == "student":
                nav_items: list[tuple[str, str]] = [
                    ("dashboard", "📊 Dashboard"),
                    ("chat", "💬 AI Assistant"),
                    ("profile", "👤 My Profile"),
                    ("portal_fees", "💰 Fee Portal"),
                    ("portal_documents", "📄 Documents"),
                    ("portal_lms", "💻 LMS Portal"),
                    ("portal_hostel", "🏠 Hostel Portal")
                ]
            else:
                nav_items: list[tuple[str, str]] = [
                    ("admin", "🛡️ Admin Dashboard"),
                    ("profile", "👤 Profile")
                ]

            for page_key, page_label in nav_items:
                current = st.session_state.get("current_page", "dashboard")
                is_active = current == page_key
                btn_type: str = "primary" if is_active else "secondary"
                if st.button(page_label, key="nav_" + page_key, use_container_width=True, type=btn_type):
                    st.session_state["current_page"] = page_key
                    st.rerun()

            st.markdown("---")

            # Logout
            if st.button("🚪 Logout", key="logout_btn", use_container_width=True):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

            # Footer
            st.markdown(
                '<div style="position: fixed; bottom: 1rem; width: 230px; text-align: center;">'
                '<p style="color: #4b5563; font-size: 0.7rem;">CampusAI v2.0</p>'
                '</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div style="text-align: center; padding: 2rem 0;">'
                '<p style="color: #6b7280;">Please login or register to continue</p>'
                '</div>',
                unsafe_allow_html=True
            )


def render_auth_page() -> None:
    """Render login and registration page."""
    st.markdown(
        '<div style="text-align: center; padding: 2rem 0;">'
        '<h1 style="background: linear-gradient(135deg, #667eea, #a78bfa); '
        '-webkit-background-clip: text; -webkit-text-fill-color: transparent; '
        'font-size: 3rem;">CampusAI</h1>'
        '<p style="color: #9ca3af; font-size: 1.1rem;">Smart Student Onboarding Platform</p>'
        '</div>',
        unsafe_allow_html=True
    )

    auth_col1, auth_col2, auth_col3 = st.columns([1, 2, 1])

    with auth_col2:
        auth_tab1, auth_tab2 = st.tabs(["🔐 Login", "📝 Register"])

        with auth_tab1:
            _render_login_form()

        with auth_tab2:
            _render_register_form()

    # Footer info
    st.markdown("<br><br>", unsafe_allow_html=True)
    info_c1, info_c2, info_c3, info_c4 = st.columns(4)
    with info_c1:
        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-icon">🎓</div>'
            '<div style="color: #c4b5fd; font-weight: 600;">Smart Onboarding</div>'
            '<div style="color: #6b7280; font-size: 0.8rem;">Guided step-by-step process</div>'
            '</div>',
            unsafe_allow_html=True
        )
    with info_c2:
        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-icon">📊</div>'
            '<div style="color: #c4b5fd; font-weight: 600;">Track Progress</div>'
            '<div style="color: #6b7280; font-size: 0.8rem;">Real-time status updates</div>'
            '</div>',
            unsafe_allow_html=True
        )
    with info_c3:
        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-icon">💬</div>'
            '<div style="color: #c4b5fd; font-weight: 600;">AI Assistant</div>'
            '<div style="color: #6b7280; font-size: 0.8rem;">Instant answers to queries</div>'
            '</div>',
            unsafe_allow_html=True
        )
    with info_c4:
        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-icon">🔒</div>'
            '<div style="color: #c4b5fd; font-weight: 600;">Secure</div>'
            '<div style="color: #6b7280; font-size: 0.8rem;">Encrypted credentials</div>'
            '</div>',
            unsafe_allow_html=True
        )


def _render_login_form() -> None:
    """Render login form."""
    st.markdown("### Welcome Back")
    email: str = st.text_input("Email", placeholder="you@campus.edu", key="login_email")
    password: str = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")

    if st.button("Login", key="login_btn", use_container_width=True):
        success, result = login_user(email, password)
        if success:
            st.session_state["user"] = result
            if result.get("role") == "admin":
                st.session_state["current_page"] = "admin"
            else:
                st.session_state["current_page"] = "dashboard"
            st.rerun()
        else:
            st.error(result)


def _render_register_form() -> None:
    """Render registration form."""
    st.markdown("### Create Account")
    name: str = st.text_input("Full Name", placeholder="Enter your full name", key="reg_name")
    email: str = st.text_input("Email", placeholder="you@campus.edu", key="reg_email")
    password: str = st.text_input("Password", type="password", placeholder="Min 6 characters", key="reg_password")
    confirm: str = st.text_input("Confirm Password", type="password", placeholder="Re-enter password", key="reg_confirm")

    role: str = st.radio("I am a", ["Student", "Admin"], key="reg_role", horizontal=True)
    role_value: str = role.lower()

    admin_code: str = ""
    if role_value == "admin":
        admin_code: str = st.text_input("Admin Registration Code", type="password", key="reg_admin_code",
                                    placeholder="Enter admin code")

    if st.button("Create Account", key="register_btn", use_container_width=True):
        if password != confirm:
            st.error("Passwords do not match.")
        else:
            success, message = register_user(name, email, password, role_value, admin_code)
            if success:
                st.success(message)
            else:
                st.error(message)


def route_page() -> None:
    """Route to the correct page based on session state."""
    page = st.session_state.get("current_page", "dashboard")
    user = st.session_state.get("user")

    if not user:
        render_auth_page()
        return

    if page == "dashboard":
        render_dashboard()
    elif page == "chat":
        render_chat()
    elif page == "profile":
        render_profile()
    elif page == "admin":
        render_admin_panel()
    elif page == "portal_fees":
        render_fee_portal()
    elif page == "portal_documents":
        render_document_portal()
    elif page == "portal_lms":
        render_lms_portal()
    elif page == "portal_hostel":
        render_hostel_portal()
    else:
        render_dashboard()


def main() -> None:
    """Application entry point."""
    st.set_page_config(
        page_title="CampusAI - Smart Onboarding",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Initialize database
    init_db()

    # Load CSS
    load_css()

    # Render sidebar
    render_sidebar()

    # Route to page
    route_page()


if __name__ == "__main__":
    main()
