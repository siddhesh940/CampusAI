"""
CampusAI - Student Profile Page
View and edit profile, update onboarding tasks.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from services.stage_service import (
    get_student_data, update_student_field, get_stage_name
)
from services.reminder_service import resolve_category_reminders


BRANCHES: list[str] = [
    "Computer Science", "Information Technology",
    "Electronics & Communication", "Electrical Engineering",
    "Mechanical Engineering", "Civil Engineering",
    "Chemical Engineering", "Biotechnology",
    "Aerospace Engineering", "Data Science"
]


def render_profile() -> None:
    """Render the student profile page."""
    user = st.session_state.get("user")
    if not user:
        st.error("Please login to access your profile.")
        return

    student_id = user.get("student_id")
    if not student_id:
        st.error("Student profile not found.")
        return

    student = get_student_data(student_id)
    if not student:
        st.error("Could not load student data.")
        return

    # --- Profile Header ---
    stage = student.get("onboarding_stage", 1)
    stage_name: str = get_stage_name(stage)

    st.markdown(
        '<div class="profile-header">'
        '<div class="profile-avatar">👤</div>'
        '<h2 style="color: white; margin: 0;">' + user.get("name", "Student") + '</h2>'
        '<p style="color: rgba(255,255,255,0.7); margin: 0.3rem 0;">' + user.get("email", "") + '</p>'
        '<span class="stage-badge stage-' + str(stage) + '">' + stage_name + '</span>'
        '</div>',
        unsafe_allow_html=True
    )

    # --- Tabs ---
    tab1, tab2, tab3 = st.tabs(["📋 Profile Details", "✅ Onboarding Actions", "⚙️ Settings"])

    with tab1:
        _render_profile_details(student, student_id)

    with tab2:
        _render_onboarding_actions(student, student_id)

    with tab3:
        _render_settings(user)


def _render_profile_details(student, student_id) -> None:
    """Render editable profile details."""
    st.markdown("### Academic Information")

    col1, col2 = st.columns(2)
    with col1:
        current_branch = student.get("branch", "")
        branch_idx = 0
        if current_branch in BRANCHES:
            branch_idx: int = BRANCHES.index(current_branch)
        branch: str = st.selectbox("Branch", BRANCHES, index=branch_idx, key="prof_branch")

    with col2:
        year = st.selectbox("Year", [1, 2, 3, 4], index=student.get("year", 1) - 1, key="prof_year")

    st.markdown("### Personal Information")
    col3, col4 = st.columns(2)
    with col3:
        phone: str | None = st.text_input("Phone", value=student.get("phone", ""), key="prof_phone")
    with col4:
        hostel_options: list[str] = ["none", "single", "double", "triple"]
        current_hostel = student.get("hostel_preference", "none")
        hostel_idx = 0
        if current_hostel in hostel_options:
            hostel_idx: int = hostel_options.index(current_hostel)
        hostel: str = st.selectbox("Hostel Preference", hostel_options, index=hostel_idx, key="prof_hostel")

    address: str | None = st.text_area("Address", value=student.get("address", ""), key="prof_address")

    if st.button("💾 Save Profile", key="save_profile", use_container_width=True):
        update_student_field(student_id, "branch", branch)
        update_student_field(student_id, "year", year)
        update_student_field(student_id, "phone", phone)
        update_student_field(student_id, "hostel_preference", hostel)
        update_student_field(student_id, "address", address)
        st.success("Profile updated successfully!")
        st.rerun()

    # --- Current Status Summary ---
    st.markdown("---")
    st.markdown("### 📊 Current Status")

    status_items = [
        ("Fee Payment", "paid" if student.get("fee_status") == "paid" else "unpaid",
         "#10b981" if student.get("fee_status") == "paid" else "#ef4444"),
        ("Documents", "Verified" if student.get("documents_verified") else "Pending",
         "#10b981" if student.get("documents_verified") else "#ef4444"),
        ("LMS Account", "Active" if student.get("lms_activated") else "Inactive",
         "#10b981" if student.get("lms_activated") else "#ef4444"),
        ("Orientation", "Completed" if student.get("orientation_completed") else "Pending",
         "#10b981" if student.get("orientation_completed") else "#ef4444"),
        ("Mentor", student.get("mentor_assigned") or "Not Assigned",
         "#10b981" if student.get("mentor_assigned") else "#f59e0b")
    ]

    for label, value, color in status_items:
        st.markdown(
            '<div class="status-card" style="display: flex; justify-content: space-between; align-items: center;">'
            '<span style="color: #e0e0f0; font-weight: 500;">' + label + '</span>'
            '<span style="color: ' + color + '; font-weight: 600;">' + value.upper() + '</span>'
            '</div>',
            unsafe_allow_html=True
        )


def _render_onboarding_actions(student, student_id) -> None:
    """Render onboarding action buttons."""
    st.markdown("### Complete Your Onboarding")
    st.markdown("Use these actions to update your onboarding status:")

    st.markdown("---")

    # Fee Payment
    st.markdown("#### 💰 Fee Payment")
    if student.get("fee_status") == "paid":
        st.success("Fee has been paid ✅")
    else:
        st.warning("Fee payment is pending")
        fee_col1, fee_col2 = st.columns([3, 1])
        with fee_col1:
            st.markdown("Complete your fee payment through the payment portal, then confirm here.")
        with fee_col2:
            if st.button("Confirm Payment", key="confirm_fee"):
                update_student_field(student_id, "fee_status", "paid")
                resolve_category_reminders(student_id, "fee")
                st.success("Fee payment confirmed!")
                st.rerun()

    st.markdown("---")

    # Documents
    st.markdown("#### 📄 Document Verification")
    if student.get("documents_verified"):
        st.success("Documents verified ✅")
    else:
        st.warning("Documents pending verification")
        doc_col1, doc_col2 = st.columns([3, 1])
        with doc_col1:
            st.markdown("Upload your documents on the portal, then mark as submitted.")
        with doc_col2:
            if st.button("Mark Submitted", key="confirm_docs"):
                update_student_field(student_id, "documents_verified", True)
                resolve_category_reminders(student_id, "documents")
                st.success("Documents marked as submitted!")
                st.rerun()

    st.markdown("---")

    # LMS
    st.markdown("#### 💻 LMS Activation")
    if student.get("lms_activated"):
        st.success("LMS activated ✅")
    else:
        st.warning("LMS account not yet activated")
        lms_col1, lms_col2 = st.columns([3, 1])
        with lms_col1:
            st.markdown("Visit the LMS portal and activate your account, then confirm here.")
        with lms_col2:
            if st.button("Confirm Activation", key="confirm_lms"):
                update_student_field(student_id, "lms_activated", True)
                resolve_category_reminders(student_id, "lms")
                st.success("LMS account activated!")
                st.rerun()

    st.markdown("---")

    # Orientation
    st.markdown("#### 🎓 Orientation Program")
    if student.get("orientation_completed"):
        st.success("Orientation completed ✅")
    else:
        st.info("Attend the orientation program and confirm completion")
        orient_col1, orient_col2 = st.columns([3, 1])
        with orient_col1:
            st.markdown("Complete the orientation program, then mark as done.")
        with orient_col2:
            if st.button("Mark Complete", key="confirm_orientation"):
                update_student_field(student_id, "orientation_completed", True)
                resolve_category_reminders(student_id, "orientation")
                st.success("Orientation marked as completed!")
                st.rerun()


def _render_settings(user) -> None:
    """Render account settings."""
    st.markdown("### Account Settings")

    st.markdown(
        '<div class="status-card">'
        '<p style="color: #9ca3af; margin: 0;">Name</p>'
        '<p style="color: #e0e0f0; font-weight: 600; margin: 0;">' + user.get("name", "") + '</p>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="status-card">'
        '<p style="color: #9ca3af; margin: 0;">Email</p>'
        '<p style="color: #e0e0f0; font-weight: 600; margin: 0;">' + user.get("email", "") + '</p>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="status-card">'
        '<p style="color: #9ca3af; margin: 0;">Role</p>'
        '<p style="color: #e0e0f0; font-weight: 600; margin: 0;">' + user.get("role", "").upper() + '</p>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="status-card">'
        '<p style="color: #9ca3af; margin: 0;">Member Since</p>'
        '<p style="color: #e0e0f0; font-weight: 600; margin: 0;">' + user.get("created_at", "")[:10] + '</p>'
        '</div>',
        unsafe_allow_html=True
    )
