"""
CampusAI - Internal Portal Pages
Simulated portal pages for fees, documents, LMS, and hostel.
"""
import sys
import os

from streamlit.delta_generator import DeltaGenerator

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from services.stage_service import get_student_data, update_student_field
from services.reminder_service import resolve_category_reminders


def render_fee_portal() -> None:
    """Render the fee payment portal page."""
    user: sys.Any | None = st.session_state.get("user")
    student_id: sys.Any | None = user.get("student_id") if user else None
    student = get_student_data(student_id) if student_id else None

    st.markdown(
        '<div class="gradient-header">'
        '<h1>💰 Fee Payment Portal</h1>'
        '<p>Secure online fee payment for CampusAI students</p>'
        '</div>',
        unsafe_allow_html=True
    )

    if student and student.get("fee_status") == "paid":
        st.success("Your fee payment has been received and confirmed. No pending dues.")
        st.markdown(
            '<div class="status-card">'
            '<h4 style="color: #6ee7b7;">✅ Payment Receipt</h4>'
            '<p style="color: #9ca3af;">Transaction ID: TXN-2026-' + str(student_id).zfill(6) + '</p>'
            '<p style="color: #9ca3af;">Amount: 1,50,000 INR</p>'
            '<p style="color: #9ca3af;">Status: <span style="color: #10b981;">PAID</span></p>'
            '<p style="color: #9ca3af;">Date: July 2026</p>'
            '</div>',
            unsafe_allow_html=True
        )

        # Show fee breakdown even when paid
        st.markdown("### 📋 Fee Breakdown")
        st.markdown(
            '<div class="status-card">'
            '<table style="width: 100%; color: #d0d0e8; border-collapse: collapse;">'
            '<tr style="border-bottom: 1px solid rgba(99,102,241,0.2);"><td style="padding: 0.5rem;">Tuition Fee</td><td style="text-align: right; padding: 0.5rem;">1,20,000 INR</td></tr>'
            '<tr style="border-bottom: 1px solid rgba(99,102,241,0.2);"><td style="padding: 0.5rem;">Lab Fee</td><td style="text-align: right; padding: 0.5rem;">15,000 INR</td></tr>'
            '<tr style="border-bottom: 1px solid rgba(99,102,241,0.2);"><td style="padding: 0.5rem;">Library Fee</td><td style="text-align: right; padding: 0.5rem;">5,000 INR</td></tr>'
            '<tr style="border-bottom: 1px solid rgba(99,102,241,0.2);"><td style="padding: 0.5rem;">Activity Fee</td><td style="text-align: right; padding: 0.5rem;">10,000 INR</td></tr>'
            '<tr style="border-top: 2px solid #6366f1; font-weight: 700;">'
            '<td style="padding: 0.7rem;">Total</td>'
            '<td style="text-align: right; padding: 0.7rem; color: #a78bfa;">1,50,000 INR</td></tr>'
            '</table>'
            '</div>',
            unsafe_allow_html=True
        )
    else:
        # Payment pending
        st.warning("⚠️ Fee payment is pending. Please complete your payment before the deadline.")

        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("### 📋 Fee Breakdown")
            st.markdown(
                '<div class="status-card">'
                '<table style="width: 100%; color: #d0d0e8; border-collapse: collapse;">'
                '<tr style="border-bottom: 1px solid rgba(99,102,241,0.2);"><td style="padding: 0.5rem;">Tuition Fee</td><td style="text-align: right; padding: 0.5rem;">1,20,000 INR</td></tr>'
                '<tr style="border-bottom: 1px solid rgba(99,102,241,0.2);"><td style="padding: 0.5rem;">Lab Fee</td><td style="text-align: right; padding: 0.5rem;">15,000 INR</td></tr>'
                '<tr style="border-bottom: 1px solid rgba(99,102,241,0.2);"><td style="padding: 0.5rem;">Library Fee</td><td style="text-align: right; padding: 0.5rem;">5,000 INR</td></tr>'
                '<tr style="border-bottom: 1px solid rgba(99,102,241,0.2);"><td style="padding: 0.5rem;">Activity Fee</td><td style="text-align: right; padding: 0.5rem;">10,000 INR</td></tr>'
                '<tr style="border-top: 2px solid #6366f1; font-weight: 700;">'
                '<td style="padding: 0.7rem;">Total</td>'
                '<td style="text-align: right; padding: 0.7rem; color: #a78bfa;">1,50,000 INR</td></tr>'
                '</table>'
                '</div>',
                unsafe_allow_html=True
            )

            st.markdown("### 📌 Important Information")
            info_items: list[tuple[str, str]] = [
                ("⏰ Deadline", "Within 30 days of admission confirmation"),
                ("📦 Installment", "60% at admission, 40% before mid-semester"),
                ("💸 Late Fee", "500 INR per day after deadline"),
                ("🎓 Scholarship", "Merit scholarships for top 10% — up to 50% tuition waiver"),
                ("🔄 Refund Policy", "Full refund within 15 days, 50% within 30 days, none after 30 days"),
            ]
            for label, value in info_items:
                st.markdown(
                    '<div class="status-card" style="display: flex; gap: 1rem; align-items: center;">'
                    '<span style="color: #818cf8; font-weight: 600; min-width: 140px;">' + label + '</span>'
                    '<span style="color: #d0d0e8;">' + value + '</span>'
                    '</div>',
                    unsafe_allow_html=True
                )

        with col2:
            st.markdown("### 💳 Pay Now")
            method: str = st.selectbox("Payment Method", ["UPI", "Net Banking", "Credit Card", "Debit Card", "Demand Draft"], key="pay_method")
            st.markdown("---")
            st.markdown(
                '<div class="status-card" style="text-align: center;">'
                '<p style="color: #9ca3af; font-size: 0.85rem;">Amount Due</p>'
                '<p style="color: #a78bfa; font-size: 2rem; font-weight: 700;">₹1,50,000</p>'
                '</div>',
                unsafe_allow_html=True
            )
            if st.button("Pay Now", key="pay_now_btn", use_container_width=True):
                if student_id:
                    update_student_field(student_id, "fee_status", "paid")
                    resolve_category_reminders(student_id, "fee")
                    st.success("Payment successful! Transaction ID: TXN-2026-" + str(student_id).zfill(6))
                    st.balloons()
                    st.rerun()

    # Contact info
    st.markdown("---")
    st.markdown("### 📞 Need Help?")
    help_c1, help_c2, help_c3 = st.columns(3)
    with help_c1:
        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-icon">📧</div>'
            '<div class="metric-value" style="font-size: 0.9rem;">accounts@campus.edu</div>'
            '<div class="metric-label">Email Support</div>'
            '</div>',
            unsafe_allow_html=True
        )
    with help_c2:
        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-icon">📞</div>'
            '<div class="metric-value" style="font-size: 0.9rem;">Ext: 1100</div>'
            '<div class="metric-label">Phone Support</div>'
            '</div>',
            unsafe_allow_html=True
        )
    with help_c3:
        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-icon">📍</div>'
            '<div class="metric-value" style="font-size: 0.9rem;">Block A, First Floor</div>'
            '<div class="metric-label">Accounts Office</div>'
            '</div>',
            unsafe_allow_html=True
        )

    _render_back_button()


def render_document_portal() -> None:
    """Render the document upload portal page."""
    user: sys.Any | None = st.session_state.get("user")
    student_id: sys.Any | None = user.get("student_id") if user else None
    student = get_student_data(student_id) if student_id else None

    st.markdown(
        '<div class="gradient-header">'
        '<h1>📄 Document Verification Portal</h1>'
        '<p>Upload and track your document verification status</p>'
        '</div>',
        unsafe_allow_html=True
    )

    if student and student.get("documents_verified"):
        st.success("All documents have been verified successfully! ✅")

        st.markdown("### ✅ Verified Documents")
        docs: list[tuple[str, str]] = [
            ("10th Marksheet", "Original + 2 copies"),
            ("12th Marksheet", "Original + 2 copies"),
            ("Transfer Certificate", "Original"),
            ("Migration Certificate", "Original"),
            ("Aadhar Card / Government ID", "Photocopy"),
            ("Passport-size Photographs", "6 copies"),
            ("Admission Offer Letter", "Signed copy"),
            ("Medical Fitness Certificate", "Original"),
        ]
        for doc_name, doc_detail in docs:
            st.markdown(
                '<div class="status-card" style="display: flex; justify-content: space-between; align-items: center;">'
                '<div>'
                '<span style="color: #e0e0f0; font-weight: 500;">' + doc_name + '</span>'
                '<span style="color: #6b7280; font-size: 0.8rem; margin-left: 0.8rem;">(' + doc_detail + ')</span>'
                '</div>'
                '<span style="color: #10b981; font-weight: 600;">✅ Verified</span>'
                '</div>',
                unsafe_allow_html=True
            )
    else:
        # Document upload section
        st.warning("⚠️ Documents pending verification. Please upload all required documents.")

        st.markdown("### 📋 Required Documents")
        st.markdown(
            '<div class="status-card">'
            '<p style="color: #9ca3af; font-size: 0.85rem; margin-bottom: 0.8rem;">'
            'Upload all documents in <strong style="color: #a78bfa;">PDF, JPG, or PNG</strong> format (max 5MB each). '
            'Original documents must be presented at the Admissions Office for physical verification.</p>'
            '</div>',
            unsafe_allow_html=True
        )

        docs_required: list[tuple[str, str]] = [
            ("10th Marksheet", "Original + 2 photocopies"),
            ("12th Marksheet", "Original + 2 photocopies"),
            ("Transfer Certificate", "Original from previous institution"),
            ("Migration Certificate", "Original"),
            ("ID Proof (Aadhar Card)", "Photocopy, both sides"),
            ("Passport-size Photographs", "6 copies, white background"),
            ("Admission Offer Letter", "Signed by student and guardian"),
            ("Medical Fitness Certificate", "From registered medical practitioner"),
        ]

        for doc_name, doc_hint in docs_required:
            st.markdown(
                '<p style="color: #c4b5fd; font-weight: 500; margin-bottom: 0.2rem;">' + doc_name
                + ' <span style="color: #6b7280; font-size: 0.8rem;">— ' + doc_hint + '</span></p>',
                unsafe_allow_html=True
            )
            st.file_uploader("Upload " + doc_name, type=["pdf", "jpg", "jpeg", "png"],
                             key="upload_" + doc_name.replace(" ", "_"), label_visibility="collapsed")

        st.markdown("---")
        if st.button("Submit All Documents", key="submit_docs_btn", use_container_width=True):
            if student_id:
                update_student_field(student_id, "documents_verified", True)
                resolve_category_reminders(student_id, "documents")
                st.success("Documents submitted successfully! Verification complete.")
                st.rerun()

    # Additional info
    st.markdown("---")
    st.markdown("### 📌 Submission Guidelines")
    guidelines: list[str] = [
        "Bring originals for physical verification at Block A, Ground Floor",
        "Self-attest all photocopies",
        "Processing takes 3-5 working days after submission",
        "Check status anytime on this portal",
        "Caste & Income certificates required for scholarship applicants",
    ]
    for g: str in guidelines:
        st.markdown(
            '<div class="status-card" style="padding: 0.5rem 1rem;">'
            '<span style="color: #818cf8; margin-right: 0.5rem;">📎</span>'
            '<span style="color: #d0d0e8; font-size: 0.9rem;">' + g + '</span>'
            '</div>',
            unsafe_allow_html=True
        )

    # Contact
    st.markdown("---")
    cnt_c1, cnt_c2 = st.columns(2)
    with cnt_c1:
        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-icon">📧</div>'
            '<div class="metric-value" style="font-size: 0.9rem;">admissions@campus.edu</div>'
            '<div class="metric-label">Admissions Office</div>'
            '</div>',
            unsafe_allow_html=True
        )
    with cnt_c2:
        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-icon">📍</div>'
            '<div class="metric-value" style="font-size: 0.9rem;">Block A, Ground Floor</div>'
            '<div class="metric-label">Ext: 1200</div>'
            '</div>',
            unsafe_allow_html=True
        )

    _render_back_button()


def render_lms_portal() -> None:
    """Render the LMS activation portal page."""
    user: sys.Any | None = st.session_state.get("user")
    student_id: sys.Any | None = user.get("student_id") if user else None
    student = get_student_data(student_id) if student_id else None

    st.markdown(
        '<div class="gradient-header">'
        '<h1>💻 Learning Management System</h1>'
        '<p>Access course materials, assignments, and academic resources</p>'
        '</div>',
        unsafe_allow_html=True
    )

    if student and student.get("lms_activated"):
        st.success("Your LMS account is active! ✅")

        # Quick stats
        stat_c1, stat_c2, stat_c3, stat_c4 = st.columns(4)
        with stat_c1:
            st.markdown(
                '<div class="metric-card">'
                '<div class="metric-icon">📚</div>'
                '<div class="metric-value">5</div>'
                '<div class="metric-label">Enrolled Courses</div>'
                '</div>',
                unsafe_allow_html=True
            )
        with stat_c2:
            st.markdown(
                '<div class="metric-card">'
                '<div class="metric-icon">📝</div>'
                '<div class="metric-value">12</div>'
                '<div class="metric-label">Pending Assignments</div>'
                '</div>',
                unsafe_allow_html=True
            )
        with stat_c3:
            st.markdown(
                '<div class="metric-card">'
                '<div class="metric-icon">🎥</div>'
                '<div class="metric-value">48</div>'
                '<div class="metric-label">Video Lectures</div>'
                '</div>',
                unsafe_allow_html=True
            )
        with stat_c4:
            st.markdown(
                '<div class="metric-card">'
                '<div class="metric-icon">💬</div>'
                '<div class="metric-value">3</div>'
                '<div class="metric-label">Forum Discussions</div>'
                '</div>',
                unsafe_allow_html=True
            )

        st.markdown("### 📚 Enrolled Courses")
        courses: list[tuple[str, str, str, str]] = [
            ("CS101", "Data Structures & Algorithms", "Prof. Sharma", "Mon/Wed/Fri 9:00 AM"),
            ("CS102", "Database Management Systems", "Prof. Gupta", "Tue/Thu 10:30 AM"),
            ("CS103", "Operating Systems", "Prof. Patel", "Mon/Wed 2:00 PM"),
            ("MA201", "Engineering Mathematics III", "Prof. Singh", "Tue/Thu/Sat 8:00 AM"),
            ("HS101", "Professional Communication", "Prof. Verma", "Fri 3:00 PM"),
        ]
        for code, name, prof, schedule in courses:
            st.markdown(
                '<div class="status-card" style="display: flex; justify-content: space-between; align-items: center;">'
                '<div style="display: flex; align-items: center; gap: 1rem;">'
                '<span style="background: rgba(99,102,241,0.2); color: #a78bfa; padding: 0.3rem 0.6rem; '
                'border-radius: 6px; font-weight: 700; font-size: 0.85rem;">' + code + '</span>'
                '<div>'
                '<span style="color: #e0e0f0; font-weight: 500;">' + name + '</span><br>'
                '<span style="color: #6b7280; font-size: 0.8rem;">' + prof + ' | ' + schedule + '</span>'
                '</div></div>'
                '<span style="color: #10b981; font-size: 0.8rem;">Active</span>'
                '</div>',
                unsafe_allow_html=True
            )

        # LMS Features
        st.markdown("---")
        st.markdown("### 🛠️ LMS Features")
        features: list[tuple[str, str]] = [
            ("📖 Course Materials", "Lecture notes, slides, reference books"),
            ("📝 Assignments", "Submit assignments online, track deadlines"),
            ("📊 Online Quizzes", "Take quizzes and view instant results"),
            ("🎥 Video Lectures", "Recorded lectures available 24/7"),
            ("💬 Discussion Forum", "Interact with classmates and faculty"),
            ("📈 Grade Tracker", "View grades and academic progress"),
        ]
        feat_cols: list[DeltaGenerator] = st.columns(3)
        for idx, (feat_name, feat_desc) in enumerate(features):
            with feat_cols[idx % 3]:
                st.markdown(
                    '<div class="metric-card">'
                    '<div style="color: #c4b5fd; font-weight: 600; font-size: 0.9rem;">' + feat_name + '</div>'
                    '<div style="color: #6b7280; font-size: 0.8rem; margin-top: 0.3rem;">' + feat_desc + '</div>'
                    '</div>',
                    unsafe_allow_html=True
                )

    else:
        st.markdown("### 🔐 Activate Your LMS Account")
        st.info("Complete the steps below to activate your LMS and get access to all course materials.")

        # Steps
        steps: list[tuple[str, str, str]] = [
            ("1️⃣", "Verify Student ID", "Your student ID is auto-filled below"),
            ("2️⃣", "Set LMS Password", "Minimum 8 characters, 1 uppercase, 1 number"),
            ("3️⃣", "Complete Profile", "Your profile is auto-synced from registration"),
            ("4️⃣", "Auto-Enroll", "You will be enrolled in all semester courses automatically"),
        ]
        step_cols: list[DeltaGenerator] = st.columns(4)
        for idx, (icon, title, desc) in enumerate(steps):
            with step_cols[idx]:
                st.markdown(
                    '<div class="metric-card" style="text-align: center;">'
                    '<div style="font-size: 1.5rem;">' + icon + '</div>'
                    '<div style="color: #c4b5fd; font-weight: 600; font-size: 0.85rem; margin-top: 0.3rem;">' + title + '</div>'
                    '<div style="color: #6b7280; font-size: 0.75rem; margin-top: 0.3rem;">' + desc + '</div>'
                    '</div>',
                    unsafe_allow_html=True
                )

        st.markdown("---")
        act_c1, act_c2 = st.columns([2, 1])
        with act_c1:
            st.markdown(
                '<div class="status-card">'
                '<p style="color: #9ca3af; font-size: 0.85rem;">Student ID</p>'
                '<p style="color: #a78bfa; font-size: 1.2rem; font-weight: 700;">' + str(student_id or "N/A") + '</p>'
                '</div>',
                unsafe_allow_html=True
            )
            lms_password: str = st.text_input("Set LMS Password", type="password", key="lms_pass",
                                         help="Min 8 characters, 1 uppercase letter, 1 number")
            lms_confirm: str = st.text_input("Confirm Password", type="password", key="lms_confirm")

        with act_c2:
            st.markdown("### 📱 Mobile App")
            st.markdown(
                '<div class="status-card" style="text-align: center;">'
                '<div style="font-size: 2rem;">📱</div>'
                '<p style="color: #c4b5fd; font-weight: 600;">Campus LMS App</p>'
                '<p style="color: #6b7280; font-size: 0.8rem;">Available on iOS & Android</p>'
                '<p style="color: #9ca3af; font-size: 0.75rem; margin-top: 0.5rem;">'
                'Download after activation to access courses on the go</p>'
                '</div>',
                unsafe_allow_html=True
            )

        if st.button("🚀 Activate LMS Account", key="activate_lms_btn", use_container_width=True):
            if not lms_password or len(lms_password) < 8:
                st.error("Password must be at least 8 characters.")
            elif lms_password != lms_confirm:
                st.error("Passwords do not match.")
            elif student_id:
                update_student_field(student_id, "lms_activated", True)
                resolve_category_reminders(student_id, "lms")
                st.success("LMS account activated successfully! You are now enrolled in 5 courses.")
                st.balloons()
                st.rerun()

    # Support info
    st.markdown("---")
    st.markdown("### 📞 IT Support")
    sup_c1, sup_c2, sup_c3 = st.columns(3)
    with sup_c1:
        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-icon">📧</div>'
            '<div class="metric-value" style="font-size: 0.9rem;">it@campus.edu</div>'
            '<div class="metric-label">Email</div>'
            '</div>',
            unsafe_allow_html=True
        )
    with sup_c2:
        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-icon">📞</div>'
            '<div class="metric-value" style="font-size: 0.9rem;">Ext: 2200</div>'
            '<div class="metric-label">Phone</div>'
            '</div>',
            unsafe_allow_html=True
        )
    with sup_c3:
        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-icon">🕐</div>'
            '<div class="metric-value" style="font-size: 0.9rem;">Mon-Fri, 9AM-6PM</div>'
            '<div class="metric-label">Support Hours</div>'
            '</div>',
            unsafe_allow_html=True
        )

    _render_back_button()


def render_hostel_portal() -> None:
    """Render the hostel application portal page."""
    user: sys.Any | None = st.session_state.get("user")
    student_id: sys.Any | None = user.get("student_id") if user else None
    student = get_student_data(student_id) if student_id else None

    st.markdown(
        '<div class="gradient-header">'
        '<h1>🏠 Hostel Application Portal</h1>'
        '<p>Apply for campus accommodation and manage your hostel preferences</p>'
        '</div>',
        unsafe_allow_html=True
    )

    # Room types info
    st.markdown("### 🛏️ Available Room Types")
    room_col1, room_col2, room_col3 = st.columns(3)

    with room_col1:
        st.markdown(
            '<div class="metric-card" style="text-align: center;">'
            '<div class="metric-icon">🛏️</div>'
            '<div class="metric-value" style="font-size: 1.5rem;">Single</div>'
            '<div class="metric-label" style="font-size: 1.1rem; color: #a78bfa;">₹12,000/month</div>'
            '<div style="color: #9ca3af; font-size: 0.8rem; margin-top: 0.5rem;">Private room</div>'
            '<div style="color: #9ca3af; font-size: 0.8rem;">Attached bathroom</div>'
            '<div style="color: #9ca3af; font-size: 0.8rem;">Study desk & wardrobe</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with room_col2:
        st.markdown(
            '<div class="metric-card" style="text-align: center;">'
            '<div class="metric-icon">🛏️🛏️</div>'
            '<div class="metric-value" style="font-size: 1.5rem;">Double</div>'
            '<div class="metric-label" style="font-size: 1.1rem; color: #a78bfa;">₹8,000/month</div>'
            '<div style="color: #9ca3af; font-size: 0.8rem; margin-top: 0.5rem;">Shared room (2 students)</div>'
            '<div style="color: #9ca3af; font-size: 0.8rem;">Common bathroom</div>'
            '<div style="color: #9ca3af; font-size: 0.8rem;">Individual desks</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with room_col3:
        st.markdown(
            '<div class="metric-card" style="text-align: center;">'
            '<div class="metric-icon">🛏️🛏️🛏️</div>'
            '<div class="metric-value" style="font-size: 1.5rem;">Triple</div>'
            '<div class="metric-label" style="font-size: 1.1rem; color: #a78bfa;">₹5,000/month</div>'
            '<div style="color: #9ca3af; font-size: 0.8rem; margin-top: 0.5rem;">3-sharing room</div>'
            '<div style="color: #9ca3af; font-size: 0.8rem;">Common bathroom</div>'
            '<div style="color: #9ca3af; font-size: 0.8rem;">Shared wardrobe</div>'
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown("---")

    current_pref = student.get("hostel_preference", "none") if student else "none"
    if current_pref and current_pref != "none":
        st.success("Hostel application submitted! Preference: " + current_pref.title() + " Room")
        st.markdown(
            '<div class="status-card">'
            '<h4 style="color: #6ee7b7;">📋 Application Status</h4>'
            '<p style="color: #d0d0e8;"><strong>Room Type:</strong> ' + current_pref.title() + '</p>'
            '<p style="color: #d0d0e8;"><strong>Status:</strong> <span style="color: #fbbf24;">Processing</span></p>'
            '<p style="color: #9ca3af; font-size: 0.85rem;">Room allotment is on first-come-first-served basis. '
            'You will be notified via email once your room is assigned.</p>'
            '</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown("### 📝 Apply for Hostel")
        st.info("Room allotment is on first-come-first-served basis. Apply within 7 days of admission confirmation.")

        app_c1, app_c2 = st.columns([2, 1])
        with app_c1:
            room_pref: str = st.selectbox("Room Preference", ["single", "double", "triple"],
                                     format_func=lambda x: x.title() + " Room", key="hostel_room_pref")
            food_pref: str = st.selectbox("Food Preference", ["Veg", "Non-Veg", "Jain"], key="hostel_food_pref")
            special: str = st.text_area("Special Requirements (if any)", placeholder="Medical conditions, accessibility needs, etc.",
                                   key="hostel_special")
        with app_c2:
            price_map: dict[str, str] = {"single": "12,000", "double": "8,000", "triple": "5,000"}
            st.markdown(
                '<div class="status-card" style="text-align: center;">'
                '<p style="color: #9ca3af; font-size: 0.85rem;">Monthly Rent</p>'
                '<p style="color: #a78bfa; font-size: 2rem; font-weight: 700;">₹' + price_map.get(room_pref, "0") + '</p>'
                '<p style="color: #6b7280; font-size: 0.8rem;">+ Mess charges included</p>'
                '</div>',
                unsafe_allow_html=True
            )

        if st.button("Submit Application", key="hostel_apply_btn", use_container_width=True):
            if student_id:
                update_student_field(student_id, "hostel_preference", room_pref)
                st.success("Hostel application submitted! You'll be notified about room allotment.")
                st.rerun()

    # Facilities
    st.markdown("---")
    st.markdown("### ✅ Hostel Facilities")
    facilities_data: list[tuple[str, str]] = [
        ("📶 Wi-Fi", "High-speed internet in all rooms and common areas"),
        ("👕 Laundry", "In-house laundry service"),
        ("🍽️ Mess", "3 meals daily — Breakfast, Lunch, Dinner"),
        ("🔒 24/7 Security", "CCTV surveillance and guard patrol"),
        ("🎮 Common Room", "TV, carrom, table tennis, indoor games"),
        ("🏋️ Gym", "Fully equipped fitness center"),
        ("📖 Study Hall", "Quiet study rooms open 24/7"),
        ("🚿 Hot Water", "24-hour hot water supply"),
    ]
    fac_cols: list[DeltaGenerator] = st.columns(4)
    for idx, (fac_name, fac_desc) in enumerate(facilities_data):
        with fac_cols[idx % 4]:
            st.markdown(
                '<div class="metric-card" style="text-align: center; min-height: 120px;">'
                '<div style="color: #c4b5fd; font-weight: 600; font-size: 0.85rem;">' + fac_name + '</div>'
                '<div style="color: #6b7280; font-size: 0.75rem; margin-top: 0.3rem;">' + fac_desc + '</div>'
                '</div>',
                unsafe_allow_html=True
            )

    # Rules
    st.markdown("---")
    st.markdown("### 📋 Hostel Rules")
    rules: list[str] = [
        "No guests allowed after 10:00 PM",
        "Mess Timings: Breakfast 7-9 AM | Lunch 12-2 PM | Dinner 7-9 PM",
        "Ragging is strictly prohibited — zero tolerance policy",
        "Maintain silence in study areas and corridors after 10 PM",
        "Report maintenance issues to the hostel office immediately",
    ]
    for rule: str in rules:
        st.markdown(
            '<div class="status-card" style="padding: 0.5rem 1rem;">'
            '<span style="color: #f59e0b; margin-right: 0.5rem;">⚡</span>'
            '<span style="color: #d0d0e8; font-size: 0.9rem;">' + rule + '</span>'
            '</div>',
            unsafe_allow_html=True
        )

    # Contact
    st.markdown("---")
    cnt_c1, cnt_c2 = st.columns(2)
    with cnt_c1:
        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-icon">📧</div>'
            '<div class="metric-value" style="font-size: 0.9rem;">hostel@campus.edu</div>'
            '<div class="metric-label">Hostel Office</div>'
            '</div>',
            unsafe_allow_html=True
        )
    with cnt_c2:
        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-icon">📍</div>'
            '<div class="metric-value" style="font-size: 0.9rem;">Hostel Block, Ground Floor</div>'
            '<div class="metric-label">Ext: 3300</div>'
            '</div>',
            unsafe_allow_html=True
        )

    _render_back_button()


def _render_back_button() -> None:
    """Render back to dashboard button."""
    st.markdown("---")
    if st.button("← Back to Dashboard", key="back_to_dash_" + str(id(render_fee_portal))):
        st.session_state["current_page"] = "dashboard"
        st.rerun()
