"""
CampusAI - Admin Panel Page
Admin dashboard with analytics, student management, and escalation handling.
"""
import sys
import os
from typing import List, Tuple

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm.session import Session
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
from database import get_session
from models import Student, User, Escalation


def render_admin_panel() -> None:
    """Render the admin dashboard."""
    user: sys.Any | None = st.session_state.get("user")
    if not user or user.get("role") != "admin":
        st.error("Access denied. Admin privileges required.")
        return

    # --- Header ---
    st.markdown(
        '<div class="gradient-header">'
        '<h1>🛡️ Admin Dashboard</h1>'
        '<p>Student management, analytics, and escalation handling</p>'
        '</div>',
        unsafe_allow_html=True
    )

    # --- Load Stats ---
    stats = _get_admin_stats()

    # --- KPI Row ---
    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-icon">👥</div>'
            '<div class="metric-value">' + str(stats["total_students"]) + '</div>'
            '<div class="metric-label">Total Students</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-icon">💰</div>'
            '<div class="metric-value">' + str(stats["fee_paid"]) + '</div>'
            '<div class="metric-label">Fees Paid</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-icon">📄</div>'
            '<div class="metric-value">' + str(stats["docs_verified"]) + '</div>'
            '<div class="metric-label">Docs Verified</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-icon">💻</div>'
            '<div class="metric-value">' + str(stats["lms_active"]) + '</div>'
            '<div class="metric-label">LMS Active</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with c5:
        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-icon">⚠️</div>'
            '<div class="metric-value">' + str(stats["pending_escalations"]) + '</div>'
            '<div class="metric-label">Escalations</div>'
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Tabs ---
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Analytics", "👥 Students", "⚠️ Escalations", "📋 Reports"])

    with tab1:
        _render_analytics(stats)

    with tab2:
        _render_student_list()

    with tab3:
        _render_escalations()

    with tab4:
        _render_reports(stats)


def _get_admin_stats():
    """Get all admin statistics."""
    session: Session = get_session()
    try:
        total: int = session.query(Student).count()
        fee_paid: int = session.query(Student).filter(Student.fee_status == "paid").count()
        fee_unpaid: int = total - fee_paid
        docs_v: int = session.query(Student).filter(Student.documents_verified == True).count()
        docs_p: int = total - docs_v
        lms_a: int = session.query(Student).filter(Student.lms_activated == True).count()
        lms_i: int = total - lms_a
        orient_c: int = session.query(Student).filter(Student.orientation_completed == True).count()

        stage_1: int = session.query(Student).filter(Student.onboarding_stage == 1).count()
        stage_2: int = session.query(Student).filter(Student.onboarding_stage == 2).count()
        stage_3: int = session.query(Student).filter(Student.onboarding_stage == 3).count()
        stage_4: int = session.query(Student).filter(Student.onboarding_stage == 4).count()

        pending_esc: int = session.query(Escalation).filter(Escalation.status == "pending").count()
        total_esc: int = session.query(Escalation).count()

        # Branch distribution
        branches: List[Row[Tuple[str]]] = session.query(Student.branch).all()
        branch_counts = {}
        for row in branches:
            b = row[0] if row[0] else "Not Set"
            branch_counts[b] = branch_counts.get(b, 0) + 1

        return {
            "total_students": total,
            "fee_paid": fee_paid,
            "fee_unpaid": fee_unpaid,
            "docs_verified": docs_v,
            "docs_pending": docs_p,
            "lms_active": lms_a,
            "lms_inactive": lms_i,
            "orientation_completed": orient_c,
            "stage_1": stage_1,
            "stage_2": stage_2,
            "stage_3": stage_3,
            "stage_4": stage_4,
            "pending_escalations": pending_esc,
            "total_escalations": total_esc,
            "branch_counts": branch_counts
        }
    finally:
        session.close()


def _render_analytics(stats) -> None:
    """Render analytics charts."""
    st.markdown("### 📊 Onboarding Analytics")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        # Stage Distribution
        st.markdown("#### Stage Distribution")
        fig_stage = go.Figure(data=[go.Bar(
            x=["Stage 1", "Stage 2", "Stage 3", "Stage 4"],
            y=[stats["stage_1"], stats["stage_2"], stats["stage_3"], stats["stage_4"]],
            marker_color=["#ef4444", "#f59e0b", "#3b82f6", "#10b981"],
            text=[stats["stage_1"], stats["stage_2"], stats["stage_3"], stats["stage_4"]],
            textposition="auto",
            textfont=dict(color="white", size=14)
        )])
        fig_stage.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=350,
            margin=dict(l=40, r=20, t=20, b=40),
            xaxis=dict(color="#9ca3af", gridcolor="rgba(99,102,241,0.1)"),
            yaxis=dict(color="#9ca3af", gridcolor="rgba(99,102,241,0.1)")
        )
        st.plotly_chart(fig_stage, use_container_width=True)

    with chart_col2:
        # Fee Status Pie
        st.markdown("#### Fee Payment Status")
        fig_fee = go.Figure(data=[go.Pie(
            labels=["Paid", "Unpaid"],
            values=[stats["fee_paid"], stats["fee_unpaid"]],
            hole=0.5,
            marker=dict(colors=["#10b981", "#ef4444"]),
            textinfo="label+percent",
            textfont=dict(color="white", size=13)
        )])
        fig_fee.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=350,
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=False
        )
        st.plotly_chart(fig_fee, use_container_width=True)

    chart_col3, chart_col4 = st.columns(2)

    with chart_col3:
        # Document Verification
        st.markdown("#### Document Verification")
        fig_doc = go.Figure(data=[go.Pie(
            labels=["Verified", "Pending"],
            values=[stats["docs_verified"], stats["docs_pending"]],
            hole=0.5,
            marker=dict(colors=["#6366f1", "#374151"]),
            textinfo="label+percent",
            textfont=dict(color="white", size=13)
        )])
        fig_doc.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=350,
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=False
        )
        st.plotly_chart(fig_doc, use_container_width=True)

    with chart_col4:
        # Branch Distribution
        st.markdown("#### Branch Distribution")
        branch_data = stats.get("branch_counts", {})
        if branch_data:
            branch_names = list(branch_data.keys())
            branch_values = list(branch_data.values())
            fig_branch = go.Figure(data=[go.Bar(
                x=branch_names,
                y=branch_values,
                marker_color="#818cf8",
                text=branch_values,
                textposition="auto",
                textfont=dict(color="white", size=12)
            )])
            fig_branch.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=350,
                margin=dict(l=40, r=20, t=20, b=60),
                xaxis=dict(color="#9ca3af", tickangle=-45, gridcolor="rgba(99,102,241,0.1)"),
                yaxis=dict(color="#9ca3af", gridcolor="rgba(99,102,241,0.1)")
            )
            st.plotly_chart(fig_branch, use_container_width=True)
        else:
            st.info("No branch data available yet.")


def _render_student_list() -> None:
    """Render searchable student list."""
    st.markdown("### 👥 Student Directory")

    # Search and filters
    search_col, filter_col1, filter_col2 = st.columns([2, 1, 1])
    with search_col:
        search_query: str = st.text_input("🔍 Search by name or email", key="admin_search")
    with filter_col1:
        stage_filter: str = st.selectbox("Filter by Stage", ["All", "Stage 1", "Stage 2", "Stage 3", "Stage 4"], key="admin_stage_filter")
    with filter_col2:
        fee_filter: str = st.selectbox("Filter by Fee", ["All", "Paid", "Unpaid"], key="admin_fee_filter")

    # Get students
    session: Session = get_session()
    try:
        query: RowReturningQuery[Tuple[Student, User]] = session.query(Student, User).join(User, Student.user_id == User.id)

        if search_query:
            search_pattern: str = "%" + search_query + "%"
            query: RowReturningQuery[Tuple[Student, User]] = query.filter(
                (User.name.ilike(search_pattern)) | (User.email.ilike(search_pattern))
            )

        if stage_filter != "All":
            stage_num = int(stage_filter.split(" ")[1])
            query: RowReturningQuery[Tuple[Student, User]] = query.filter(Student.onboarding_stage == stage_num)

        if fee_filter == "Paid":
            query: RowReturningQuery[Tuple[Student, User]] = query.filter(Student.fee_status == "paid")
        elif fee_filter == "Unpaid":
            query: RowReturningQuery[Tuple[Student, User]] = query.filter(Student.fee_status != "paid")

        results: List[Row[Tuple[Student, User]]] = query.all()

        if not results:
            st.info("No students found matching your criteria.")
            return

        st.markdown("**" + str(len(results)) + " students found**")

        # Build table
        table_html = (
            '<table class="styled-table">'
            '<thead><tr>'
            '<th>Name</th><th>Email</th><th>Branch</th><th>Stage</th>'
            '<th>Fee</th><th>Docs</th><th>LMS</th>'
            '</tr></thead><tbody>'
        )

        for student, u in results:
            stage = student.onboarding_stage or 1
            stage_class: str = "stage-" + str(stage)
            fee_color: str = "#10b981" if student.fee_status == "paid" else "#ef4444"
            doc_color: str = "#10b981" if student.documents_verified else "#ef4444"
            lms_color: str = "#10b981" if student.lms_activated else "#ef4444"

            table_html += (
                '<tr>'
                '<td>' + (u.name or "") + '</td>'
                '<td>' + (u.email or "") + '</td>'
                '<td>' + (student.branch or "Not Set") + '</td>'
                '<td><span class="stage-badge ' + stage_class + '">Stage ' + str(stage) + '</span></td>'
                '<td style="color: ' + fee_color + ';">' + ("Paid" if student.fee_status == "paid" else "Unpaid") + '</td>'
                '<td style="color: ' + doc_color + ';">' + ("Yes" if student.documents_verified else "No") + '</td>'
                '<td style="color: ' + lms_color + ';">' + ("Yes" if student.lms_activated else "No") + '</td>'
                '</tr>'
            )

        table_html += '</tbody></table>'
        st.markdown(table_html, unsafe_allow_html=True)

    finally:
        session.close()


def _render_escalations() -> None:
    """Render escalation requests."""
    st.markdown("### ⚠️ Escalation Requests")

    session: Session = get_session()
    try:
        escalations: List[Row[Tuple[Escalation, Student, User]]] = session.query(Escalation, Student, User).join(
            Student, Escalation.student_id == Student.id
        ).join(
            User, Student.user_id == User.id
        ).order_by(Escalation.created_at.desc()).all()

        if not escalations:
            st.info("No escalation requests.")
            return

        pending_count: int = sum(1 for e, s, u in escalations if e.status == "pending")
        st.markdown("**" + str(pending_count) + " pending** out of " + str(len(escalations)) + " total")

        for esc, student, u in escalations:
            status_class: str = "escalation-pending" if esc.status == "pending" else "escalation-resolved"
            status_icon: str = "🔴" if esc.status == "pending" else "🟢"
            created = esc.created_at.strftime("%b %d, %Y %I:%M %p") if esc.created_at else ""

            st.markdown(
                '<div class="' + status_class + '">'
                '<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">'
                '<strong>' + status_icon + ' ' + (esc.subject or "General Query") + '</strong>'
                '<span style="font-size: 0.8rem;">' + created + '</span>'
                '</div>'
                '<p style="margin: 0.3rem 0;">From: <strong>' + (u.name or "") + '</strong> (' + (u.email or "") + ')</p>'
                '<p style="margin: 0.3rem 0;">' + (esc.message or "") + '</p>'
                '</div>',
                unsafe_allow_html=True
            )

            if esc.status == "pending":
                resp_key: str = "esc_resp_" + str(esc.id)
                response: str = st.text_input("Response", key=resp_key, placeholder="Type your response...")
                resolve_col1, resolve_col2 = st.columns([1, 1])
                with resolve_col1:
                    if st.button("Resolve", key="resolve_" + str(esc.id)):
                        esc.status = "resolved"
                        esc.admin_response = response or "Resolved by admin"
                        esc.resolved_at = datetime.utcnow()
                        session.commit()
                        st.success("Escalation resolved!")
                        st.rerun()
                st.markdown("---")

    finally:
        session.close()


def _render_reports(stats) -> None:
    """Render summary reports."""
    st.markdown("### 📋 Summary Report")

    total = stats["total_students"]
    if total == 0:
        st.info("No students registered yet.")
        return

    # Completion rates
    fee_rate = round(stats["fee_paid"] / total * 100) if total > 0 else 0
    doc_rate = round(stats["docs_verified"] / total * 100) if total > 0 else 0
    lms_rate = round(stats["lms_active"] / total * 100) if total > 0 else 0
    orient_rate = round(stats["orientation_completed"] / total * 100) if total > 0 else 0

    # Completion bar chart
    fig = go.Figure(data=[go.Bar(
        x=["Fee Payment", "Documents", "LMS Activation", "Orientation"],
        y=[fee_rate, doc_rate, lms_rate, orient_rate],
        marker_color=["#10b981", "#6366f1", "#3b82f6", "#f59e0b"],
        text=[str(fee_rate) + "%", str(doc_rate) + "%", str(lms_rate) + "%", str(orient_rate) + "%"],
        textposition="auto",
        textfont=dict(color="white", size=14)
    )])
    fig.update_layout(
        title=dict(text="Completion Rates", font=dict(color="#e0e0f0")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=400,
        yaxis=dict(range=[0, 100], color="#9ca3af", gridcolor="rgba(99,102,241,0.1)", title="Percentage"),
        xaxis=dict(color="#9ca3af"),
        margin=dict(l=40, r=20, t=50, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)

    # Summary metrics
    st.markdown("---")
    st.markdown("#### Key Metrics")

    metrics_html: str = (
        '<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem;">'
        '<div class="status-card"><strong>Total Registered:</strong> ' + str(total) + '</div>'
        '<div class="status-card"><strong>Fully Onboarded (Stage 4):</strong> ' + str(stats["stage_4"]) + '</div>'
        '<div class="status-card"><strong>Fee Collection Rate:</strong> ' + str(fee_rate) + '%</div>'
        '<div class="status-card"><strong>Document Completion:</strong> ' + str(doc_rate) + '%</div>'
        '<div class="status-card"><strong>LMS Activation:</strong> ' + str(lms_rate) + '%</div>'
        '<div class="status-card"><strong>Pending Escalations:</strong> ' + str(stats["pending_escalations"]) + '</div>'
        '</div>'
    )
    st.markdown(metrics_html, unsafe_allow_html=True)
