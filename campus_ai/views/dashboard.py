"""
CampusAI - Student Dashboard Page
Main dashboard with progress, reminders, and quick actions.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import plotly.graph_objects as go
from services.stage_service import (
    get_student_data, get_stage_name, get_stage_progress,
    get_pending_tasks, get_stage_description
)
from services.reminder_service import generate_reminders, get_active_reminders


def render_dashboard() -> None:
    """Render the student dashboard."""
    user = st.session_state.get("user")
    if not user:
        st.error("Please login to access the dashboard.")
        return

    student_id = user.get("student_id")
    if not student_id:
        st.error("Student profile not found.")
        return

    student = get_student_data(student_id)
    if not student:
        st.error("Could not load student data.")
        return

    # Generate reminders
    generate_reminders(student_id)

    # --- Welcome Header ---
    st.markdown(
        '<div class="gradient-header">'
        '<h1>Welcome back, ' + user.get("name", "Student") + '!</h1>'
        '<p>Track your onboarding progress and complete pending tasks</p>'
        '</div>',
        unsafe_allow_html=True
    )

    # --- KPI Metrics Row ---
    stage = student.get("onboarding_stage", 1)
    progress: int = get_stage_progress(stage)
    pending = get_pending_tasks(student)
    reminders = get_active_reminders(student_id)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-icon">📊</div>'
            '<div class="metric-value">' + str(stage) + '/4</div>'
            '<div class="metric-label">Current Stage</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-icon">📈</div>'
            '<div class="metric-value">' + str(progress) + '%</div>'
            '<div class="metric-label">Progress</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-icon">📋</div>'
            '<div class="metric-value">' + str(len(pending)) + '</div>'
            '<div class="metric-label">Pending Tasks</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-icon">🔔</div>'
            '<div class="metric-value">' + str(len(reminders)) + '</div>'
            '<div class="metric-label">Reminders</div>'
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Progress Bar ---
    stage_name: str = get_stage_name(stage)
    stage_desc: str = get_stage_description(stage)
    bar_width = str(progress)

    st.markdown(
        '<div class="progress-container">'
        '<h3 style="color: #e0e0ff; margin-bottom: 0.8rem;">Onboarding Progress</h3>'
        '<div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">'
        '<span class="stage-badge stage-' + str(stage) + '">' + stage_name + '</span>'
        '<span style="color: #a78bfa; font-weight: 600;">' + bar_width + '%</span>'
        '</div>'
        '<div class="progress-bar-bg">'
        '<div class="progress-bar-fill" style="width: ' + bar_width + '%;"></div>'
        '</div>'
        '<div class="progress-label">'
        '<span>Stage ' + str(stage) + ' of 4</span>'
        '<span>' + stage_desc + '</span>'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Two Column Layout ---
    left_col, right_col = st.columns([3, 2])

    with left_col:
        # Pending Tasks
        st.markdown("### 📋 Pending Tasks")
        if not pending:
            st.markdown(
                '<div class="reminder-alert-success" style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(6, 78, 59, 0.05)); '
                'border-left: 4px solid #10b981; border-radius: 0 12px 12px 0; padding: 1rem 1.25rem; color: #6ee7b7;">'
                '🎉 All tasks completed! You are fully onboarded.</div>',
                unsafe_allow_html=True
            )
        else:
            for task in pending:
                icon = task.get("icon", "📌")
                name = task.get("task", "")
                priority = task.get("priority", "medium")
                priority_color: str = "#ef4444" if priority == "high" else "#f59e0b" if priority == "medium" else "#6b7280"
                st.markdown(
                    '<div class="status-card" style="display: flex; align-items: center; justify-content: space-between;">'
                    '<div>'
                    '<span style="font-size: 1.3rem; margin-right: 0.8rem;">' + icon + '</span>'
                    '<span style="color: #e0e0f0; font-weight: 500;">' + name + '</span>'
                    '</div>'
                    '<span style="background: ' + priority_color + '22; color: ' + priority_color + '; '
                    'padding: 0.2rem 0.8rem; border-radius: 12px; font-size: 0.75rem; font-weight: 600; text-transform: uppercase;">'
                    + priority + '</span>'
                    '</div>',
                    unsafe_allow_html=True
                )

    with right_col:
        # Reminders
        st.markdown("### 🔔 Active Reminders")
        if not reminders:
            st.markdown(
                '<div style="color: #6ee7b7; padding: 1rem;">No active reminders</div>',
                unsafe_allow_html=True
            )
        else:
            for rem in reminders:
                urgent_class: str = "font-weight: 700;" if rem.get("urgent") else ""
                days = rem.get("days_left", 0)
                days_text: str = str(days) + " days left" if days > 0 else "Overdue!"
                days_color: str = "#ef4444" if days < 3 else "#f59e0b" if days < 7 else "#6ee7b7"
                st.markdown(
                    '<div class="reminder-alert">'
                    '<div style="display: flex; justify-content: space-between; align-items: center;">'
                    '<span style="' + urgent_class + '">' + rem.get("message", "") + '</span>'
                    '</div>'
                    '<div style="margin-top: 0.5rem; font-size: 0.8rem; color: ' + days_color + ';">⏰ ' + days_text + '</div>'
                    '</div>',
                    unsafe_allow_html=True
                )

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Quick Actions ---
    st.markdown("### ⚡ Quick Actions")
    qa1, qa2, qa3, qa4 = st.columns(4)

    with qa1:
        st.markdown(
            '<div class="quick-action">'
            '<div class="quick-action-icon">💰</div>'
            '<div class="quick-action-label">Pay Fees</div>'
            '</div>',
            unsafe_allow_html=True
        )
        if st.button("Pay Now", key="qa_fee", use_container_width=True):
            st.session_state["current_page"] = "portal_fees"
            st.rerun()

    with qa2:
        st.markdown(
            '<div class="quick-action">'
            '<div class="quick-action-icon">📄</div>'
            '<div class="quick-action-label">Upload Documents</div>'
            '</div>',
            unsafe_allow_html=True
        )
        if st.button("Upload", key="qa_docs", use_container_width=True):
            st.session_state["current_page"] = "portal_documents"
            st.rerun()

    with qa3:
        st.markdown(
            '<div class="quick-action">'
            '<div class="quick-action-icon">💻</div>'
            '<div class="quick-action-label">Activate LMS</div>'
            '</div>',
            unsafe_allow_html=True
        )
        if st.button("Activate", key="qa_lms", use_container_width=True):
            st.session_state["current_page"] = "portal_lms"
            st.rerun()

    with qa4:
        st.markdown(
            '<div class="quick-action">'
            '<div class="quick-action-icon">🏠</div>'
            '<div class="quick-action-label">Hostel Application</div>'
            '</div>',
            unsafe_allow_html=True
        )
        if st.button("Apply", key="qa_hostel", use_container_width=True):
            st.session_state["current_page"] = "portal_hostel"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Onboarding Stage Visual ---
    st.markdown("### 🗺️ Onboarding Journey")
    stages_html = '<div style="display: flex; gap: 1rem; flex-wrap: wrap;">'
    stage_items: list[tuple[int, str, str]] = [
        (1, "Admission Confirmation", "💳"),
        (2, "Document Verification", "📑"),
        (3, "Academic Setup", "🎓"),
        (4, "Campus Integration", "🏫")
    ]
    for s_num, s_name, s_icon in stage_items:
        if s_num < stage:
            bg = "rgba(16, 185, 129, 0.15)"
            border = "rgba(16, 185, 129, 0.4)"
            color = "#6ee7b7"
            status_text = "✅ Completed"
        elif s_num == stage:
            bg = "rgba(99, 102, 241, 0.15)"
            border = "rgba(99, 102, 241, 0.4)"
            color = "#a78bfa"
            status_text = "🔄 In Progress"
        else:
            bg = "rgba(55, 55, 90, 0.3)"
            border = "rgba(55, 55, 90, 0.3)"
            color = "#6b7280"
            status_text = "⏳ Upcoming"

        stages_html += (
            '<div style="flex: 1; min-width: 200px; background: ' + bg + '; border: 1px solid ' + border + '; '
            'border-radius: 12px; padding: 1.2rem; text-align: center;">'
            '<div style="font-size: 2rem;">' + s_icon + '</div>'
            '<div style="color: ' + color + '; font-weight: 600; margin: 0.5rem 0;">' + s_name + '</div>'
            '<div style="font-size: 0.8rem; color: ' + color + ';">' + status_text + '</div>'
            '</div>'
        )
    stages_html += '</div>'
    st.markdown(stages_html, unsafe_allow_html=True)

    # --- Onboarding Checklist Donut Chart ---
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📊 Completion Overview")

    completed_count = 0
    total_count = 5
    if student.get("fee_status") == "paid":
        completed_count += 1
    if student.get("documents_verified"):
        completed_count += 1
    if student.get("lms_activated"):
        completed_count += 1
    if student.get("orientation_completed"):
        completed_count += 1
    if student.get("mentor_assigned"):
        completed_count += 1

    remaining: int = total_count - completed_count

    fig = go.Figure(data=[go.Pie(
        labels=["Completed", "Pending"],
        values=[completed_count, remaining],
        hole=0.65,
        marker=dict(colors=["#6366f1", "#1e1e3f"]),
        textinfo="label+value",
        textfont=dict(color="white", size=14)
    )])
    fig.update_layout(
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=300,
        margin=dict(l=20, r=20, t=20, b=20),
        annotations=[dict(
            text=str(completed_count) + "/" + str(total_count),
            x=0.5, y=0.5, font_size=28,
            font_color="#a78bfa",
            showarrow=False
        )]
    )
    st.plotly_chart(fig, use_container_width=True)
