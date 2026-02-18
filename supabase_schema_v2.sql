-- ============================================================
-- CampusAI v2 – New Module Schema (Courses, Timetable, Mentoring, Compliance)
-- Run AFTER the base supabase_schema.sql
-- ============================================================

-- ─── NEW ENUMS ─────────────────────────────────────────────

CREATE TYPE enrollment_status AS ENUM ('active', 'dropped');
CREATE TYPE day_of_week AS ENUM ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday');
CREATE TYPE meeting_status AS ENUM ('requested', 'approved', 'rejected', 'completed', 'cancelled');
CREATE TYPE compliance_type AS ENUM ('declaration', 'video', 'document', 'acknowledgement');

-- ─── UPDATE USER ROLE ENUM ────────────────────────────────
-- Add 'mentor' to user_role enum
ALTER TYPE user_role ADD VALUE IF NOT EXISTS 'mentor';

-- ─── 13. COURSES ──────────────────────────────────────────

CREATE TABLE courses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    university_id UUID NOT NULL REFERENCES universities(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(50) NOT NULL,
    description TEXT,
    duration_years INTEGER DEFAULT 4,
    total_credits INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(university_id, code)
);

CREATE INDEX idx_courses_university ON courses(university_id);
CREATE INDEX idx_courses_code ON courses(code);

-- ─── 14. SUBJECTS ─────────────────────────────────────────

CREATE TABLE subjects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    course_id UUID NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    university_id UUID NOT NULL REFERENCES universities(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(50) NOT NULL,
    credits INTEGER DEFAULT 3,
    semester INTEGER DEFAULT 1,
    is_elective BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(university_id, code)
);

CREATE INDEX idx_subjects_course ON subjects(course_id);
CREATE INDEX idx_subjects_university ON subjects(university_id);
CREATE INDEX idx_subjects_semester ON subjects(semester);

-- ─── 15. ENROLLMENTS ──────────────────────────────────────

CREATE TABLE enrollments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    course_id UUID NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    subject_id UUID NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    university_id UUID NOT NULL REFERENCES universities(id) ON DELETE CASCADE,
    status enrollment_status DEFAULT 'active' NOT NULL,
    enrolled_at TIMESTAMPTZ DEFAULT NOW(),
    dropped_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, subject_id)
);

CREATE INDEX idx_enrollments_user ON enrollments(user_id);
CREATE INDEX idx_enrollments_course ON enrollments(course_id);
CREATE INDEX idx_enrollments_subject ON enrollments(subject_id);
CREATE INDEX idx_enrollments_status ON enrollments(status);

-- ─── 16. SUBJECT SCHEDULES (Timetable) ───────────────────

CREATE TABLE subject_schedules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subject_id UUID NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    university_id UUID NOT NULL REFERENCES universities(id) ON DELETE CASCADE,
    day_of_week day_of_week NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    room VARCHAR(100),
    instructor VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_schedules_subject ON subject_schedules(subject_id);
CREATE INDEX idx_schedules_day ON subject_schedules(day_of_week);
CREATE INDEX idx_schedules_university ON subject_schedules(university_id);

-- ─── 17. MENTOR ASSIGNMENTS ──────────────────────────────

CREATE TABLE mentor_assignments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    mentor_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    university_id UUID NOT NULL REFERENCES universities(id) ON DELETE CASCADE,
    is_active BOOLEAN DEFAULT TRUE,
    assigned_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(student_id, mentor_id)
);

CREATE INDEX idx_mentor_assign_student ON mentor_assignments(student_id);
CREATE INDEX idx_mentor_assign_mentor ON mentor_assignments(mentor_id);
CREATE INDEX idx_mentor_assign_university ON mentor_assignments(university_id);

-- ─── 18. MENTOR MEETINGS ─────────────────────────────────

CREATE TABLE mentor_meetings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    assignment_id UUID NOT NULL REFERENCES mentor_assignments(id) ON DELETE CASCADE,
    student_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    mentor_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    university_id UUID NOT NULL REFERENCES universities(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    meeting_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME,
    status meeting_status DEFAULT 'requested' NOT NULL,
    meeting_link VARCHAR(512),
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_meetings_assignment ON mentor_meetings(assignment_id);
CREATE INDEX idx_meetings_student ON mentor_meetings(student_id);
CREATE INDEX idx_meetings_mentor ON mentor_meetings(mentor_id);
CREATE INDEX idx_meetings_status ON mentor_meetings(status);
CREATE INDEX idx_meetings_date ON mentor_meetings(meeting_date);

-- ─── 19. MENTOR MESSAGES ─────────────────────────────────

CREATE TABLE mentor_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    assignment_id UUID NOT NULL REFERENCES mentor_assignments(id) ON DELETE CASCADE,
    sender_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_mentor_messages_assignment ON mentor_messages(assignment_id);
CREATE INDEX idx_mentor_messages_sender ON mentor_messages(sender_id);
CREATE INDEX idx_mentor_messages_unread ON mentor_messages(assignment_id, is_read) WHERE is_read = FALSE;

-- ─── 20. COMPLIANCE ITEMS ─────────────────────────────────

CREATE TABLE compliance_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    university_id UUID NOT NULL REFERENCES universities(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    compliance_type compliance_type NOT NULL,
    content_url VARCHAR(512),
    "order" INTEGER DEFAULT 0,
    is_required BOOLEAN DEFAULT TRUE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_compliance_items_university ON compliance_items(university_id);
CREATE INDEX idx_compliance_items_type ON compliance_items(compliance_type);

-- ─── 21. STUDENT COMPLIANCE STATUS ────────────────────────

CREATE TABLE student_compliance (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    compliance_item_id UUID NOT NULL REFERENCES compliance_items(id) ON DELETE CASCADE,
    university_id UUID NOT NULL REFERENCES universities(id) ON DELETE CASCADE,
    is_completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, compliance_item_id)
);

CREATE INDEX idx_student_compliance_user ON student_compliance(user_id);
CREATE INDEX idx_student_compliance_item ON student_compliance(compliance_item_id);

-- ─── ROW LEVEL SECURITY (New Tables) ──────────────────────

ALTER TABLE courses ENABLE ROW LEVEL SECURITY;
ALTER TABLE subjects ENABLE ROW LEVEL SECURITY;
ALTER TABLE enrollments ENABLE ROW LEVEL SECURITY;
ALTER TABLE subject_schedules ENABLE ROW LEVEL SECURITY;
ALTER TABLE mentor_assignments ENABLE ROW LEVEL SECURITY;
ALTER TABLE mentor_meetings ENABLE ROW LEVEL SECURITY;
ALTER TABLE mentor_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE compliance_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE student_compliance ENABLE ROW LEVEL SECURITY;

-- Courses & Subjects: everyone in the university can view
CREATE POLICY "Users can view courses" ON courses FOR SELECT
    USING (university_id IN (SELECT university_id FROM users WHERE id = auth.uid()));

CREATE POLICY "Users can view subjects" ON subjects FOR SELECT
    USING (university_id IN (SELECT university_id FROM users WHERE id = auth.uid()));

-- Admin can manage courses & subjects
CREATE POLICY "Admin can manage courses" ON courses FOR ALL
    USING (university_id IN (
        SELECT university_id FROM users WHERE id = auth.uid() AND role IN ('admin', 'superadmin')
    ));

CREATE POLICY "Admin can manage subjects" ON subjects FOR ALL
    USING (university_id IN (
        SELECT university_id FROM users WHERE id = auth.uid() AND role IN ('admin', 'superadmin')
    ));

-- Enrollments: students see only their own
CREATE POLICY "Students view own enrollments" ON enrollments FOR SELECT
    USING (user_id = auth.uid());

CREATE POLICY "Students can enroll" ON enrollments FOR INSERT
    WITH CHECK (user_id = auth.uid());

CREATE POLICY "Students can update own enrollments" ON enrollments FOR UPDATE
    USING (user_id = auth.uid());

CREATE POLICY "Admin can manage enrollments" ON enrollments FOR ALL
    USING (university_id IN (
        SELECT university_id FROM users WHERE id = auth.uid() AND role IN ('admin', 'superadmin')
    ));

-- Schedules: visible to enrolled students and admins
CREATE POLICY "Users can view schedules" ON subject_schedules FOR SELECT
    USING (university_id IN (SELECT university_id FROM users WHERE id = auth.uid()));

CREATE POLICY "Admin can manage schedules" ON subject_schedules FOR ALL
    USING (university_id IN (
        SELECT university_id FROM users WHERE id = auth.uid() AND role IN ('admin', 'superadmin')
    ));

-- Mentor Assignments: students see their own, mentors see assigned, admin sees all
CREATE POLICY "Students view own mentor" ON mentor_assignments FOR SELECT
    USING (student_id = auth.uid());

CREATE POLICY "Mentors view assigned students" ON mentor_assignments FOR SELECT
    USING (mentor_id = auth.uid());

CREATE POLICY "Admin manage mentor assignments" ON mentor_assignments FOR ALL
    USING (university_id IN (
        SELECT university_id FROM users WHERE id = auth.uid() AND role IN ('admin', 'superadmin')
    ));

-- Mentor Meetings: participants can view
CREATE POLICY "Meeting participants can view" ON mentor_meetings FOR SELECT
    USING (student_id = auth.uid() OR mentor_id = auth.uid());

CREATE POLICY "Students can request meetings" ON mentor_meetings FOR INSERT
    WITH CHECK (student_id = auth.uid());

CREATE POLICY "Mentors can update meetings" ON mentor_meetings FOR UPDATE
    USING (mentor_id = auth.uid());

CREATE POLICY "Admin manage meetings" ON mentor_meetings FOR ALL
    USING (university_id IN (
        SELECT university_id FROM users WHERE id = auth.uid() AND role IN ('admin', 'superadmin')
    ));

-- Mentor Messages: assignment participants can view/send
CREATE POLICY "Message participants can view" ON mentor_messages FOR SELECT
    USING (assignment_id IN (
        SELECT id FROM mentor_assignments WHERE student_id = auth.uid() OR mentor_id = auth.uid()
    ));

CREATE POLICY "Users can send messages" ON mentor_messages FOR INSERT
    WITH CHECK (sender_id = auth.uid() AND assignment_id IN (
        SELECT id FROM mentor_assignments WHERE student_id = auth.uid() OR mentor_id = auth.uid()
    ));

-- Compliance: all students can view items, manage own status
CREATE POLICY "Users view compliance items" ON compliance_items FOR SELECT
    USING (university_id IN (SELECT university_id FROM users WHERE id = auth.uid()));

CREATE POLICY "Admin manage compliance items" ON compliance_items FOR ALL
    USING (university_id IN (
        SELECT university_id FROM users WHERE id = auth.uid() AND role IN ('admin', 'superadmin')
    ));

CREATE POLICY "Students view own compliance status" ON student_compliance FOR SELECT
    USING (user_id = auth.uid());

CREATE POLICY "Students can submit compliance" ON student_compliance FOR INSERT
    WITH CHECK (user_id = auth.uid());

CREATE POLICY "Students can update compliance" ON student_compliance FOR UPDATE
    USING (user_id = auth.uid());

-- ─── UPDATED_AT TRIGGERS (New Tables) ─────────────────────

CREATE TRIGGER set_updated_at_courses BEFORE UPDATE ON courses FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER set_updated_at_subjects BEFORE UPDATE ON subjects FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER set_updated_at_enrollments BEFORE UPDATE ON enrollments FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER set_updated_at_schedules BEFORE UPDATE ON subject_schedules FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER set_updated_at_mentor_assignments BEFORE UPDATE ON mentor_assignments FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER set_updated_at_mentor_meetings BEFORE UPDATE ON mentor_meetings FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER set_updated_at_compliance_items BEFORE UPDATE ON compliance_items FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER set_updated_at_student_compliance BEFORE UPDATE ON student_compliance FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ─── SEED DEFAULT COMPLIANCE ITEMS ────────────────────────
-- These will be created per-university via admin panel.
-- Below is an example for reference:

-- INSERT INTO compliance_items (university_id, title, description, compliance_type, "order", is_required) VALUES
--     ('<uni-id>', 'Anti-Ragging Declaration', 'I hereby declare that I will not participate in any form of ragging...', 'declaration', 1, true),
--     ('<uni-id>', 'Code of Conduct', 'I have read and agree to abide by the institutional code of conduct.', 'acknowledgement', 2, true),
--     ('<uni-id>', 'Orientation Video', 'Watch the complete campus orientation video.', 'video', 3, true),
--     ('<uni-id>', 'Anti-Sexual Harassment Policy', 'I acknowledge the anti-sexual harassment policy.', 'declaration', 4, true);
