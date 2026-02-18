/**
 * Demo / fallback data used when the backend API is unreachable.
 * This lets the frontend showcase the UI on Vercel even without a running backend.
 */

import type {
    ChatSessionListResponse,
    CourseListResponse,
    DashboardSummary,
    EnrollmentListResponse,
    LMSStatus,
    MentorProfile,
    OnboardingProgressResponse,
    SubjectListResponse,
    WeeklyTimetableResponse,
} from "./campus-services";

// ─── Helper ───────────────────────────────────────────
function isDemoMode(): boolean {
  if (typeof window === "undefined") return false;
  const token = localStorage.getItem("access_token") || "";
  return token.endsWith(".demo") || !process.env.NEXT_PUBLIC_API_URL;
}

/**
 * Wrap an async service call so that network errors ("Failed to fetch",
 * TypeError, etc.) fall back to the provided demo data.
 */
export async function withDemoFallback<T>(
  fn: () => Promise<T>,
  fallback: T,
): Promise<T> {
  try {
    return await fn();
  } catch (err: unknown) {
    const msg = err instanceof Error ? err.message.toLowerCase() : String(err);
    if (
      msg.includes("failed to fetch") ||
      msg.includes("networkerror") ||
      msg.includes("network error") ||
      msg.includes("load failed") ||
      msg.includes("fetch") ||
      isDemoMode()
    ) {
      return fallback;
    }
    throw err;
  }
}

// ─── Demo Data ────────────────────────────────────────

export const demoDashboardSummary: DashboardSummary = {
  user: { name: "Demo Student", email: "demo@campusai.app", role: "student" },
  onboarding_percentage: 45,
  documents: {
    total: 4,
    approved: 2,
    pending: 1,
    rejected: 0,
    under_review: 1,
  },
  payments: {
    status: "partial",
    total_paid: 25000,
    total_pending: 75000,
    count: 2,
  },
  hostel: {
    status: "not_applied",
    room_type: null,
    room_number: null,
  },
  lms: {
    status: "inactive",
    lms_id: null,
    platform: "Moodle",
  },
  checklist: {
    items: [
      {
        id: "1",
        title: "Complete Profile",
        description: "Fill in your personal details",
        category: "profile",
        order: 1,
        is_completed: true,
        is_required: true,
      },
      {
        id: "2",
        title: "Upload Documents",
        description: "Upload 10th marksheet, 12th marksheet, Photo, ID proof",
        category: "documents",
        order: 2,
        is_completed: false,
        is_required: true,
      },
      {
        id: "3",
        title: "Pay Fees",
        description: "Complete tuition and hostel payments",
        category: "payments",
        order: 3,
        is_completed: false,
        is_required: true,
      },
      {
        id: "4",
        title: "Apply for Hostel",
        description: "Submit hostel room preference",
        category: "hostel",
        order: 4,
        is_completed: false,
        is_required: false,
      },
      {
        id: "5",
        title: "Activate LMS",
        description: "Get your learning management system credentials",
        category: "lms",
        order: 5,
        is_completed: false,
        is_required: true,
      },
      {
        id: "6",
        title: "Register Courses",
        description: "Enroll in your semester courses",
        category: "courses",
        order: 6,
        is_completed: true,
        is_required: true,
      },
    ],
    percentage: 45,
    total: 6,
    completed: 2,
  },
};

export const demoDocuments = {
  documents: [
    {
      id: "d1",
      user_id: "demo",
      university_id: "demo",
      document_type: "10th_marksheet",
      file_name: "10th_marksheet.pdf",
      file_url: "#",
      status: "approved",
      rejection_reason: null,
      created_at: "2026-01-15T10:30:00Z",
      updated_at: "2026-01-16T08:00:00Z",
    },
    {
      id: "d2",
      user_id: "demo",
      university_id: "demo",
      document_type: "12th_marksheet",
      file_name: "12th_marksheet.pdf",
      file_url: "#",
      status: "approved",
      rejection_reason: null,
      created_at: "2026-01-15T10:35:00Z",
      updated_at: "2026-01-16T08:05:00Z",
    },
    {
      id: "d3",
      user_id: "demo",
      university_id: "demo",
      document_type: "photo",
      file_name: "passport_photo.jpg",
      file_url: "#",
      status: "under_review",
      rejection_reason: null,
      created_at: "2026-02-10T14:00:00Z",
      updated_at: "2026-02-10T14:00:00Z",
    },
    {
      id: "d4",
      user_id: "demo",
      university_id: "demo",
      document_type: "id_proof",
      file_name: "aadhar_card.pdf",
      file_url: "#",
      status: "pending",
      rejection_reason: null,
      created_at: "2026-02-15T09:00:00Z",
      updated_at: "2026-02-15T09:00:00Z",
    },
  ],
  total: 4,
};

export const demoPayments = {
  payments: [
    {
      id: "p1",
      user_id: "demo",
      university_id: "demo",
      payment_type: "tuition_fee",
      amount: 25000,
      currency: "INR",
      status: "completed",
      payment_method: "upi",
      transaction_id: "TXN_DEMO_001",
      receipt_url: null,
      notes: "Semester 1 tuition fee",
      created_at: "2026-01-20T12:00:00Z",
      updated_at: "2026-01-20T12:05:00Z",
    },
    {
      id: "p2",
      user_id: "demo",
      university_id: "demo",
      payment_type: "hostel_fee",
      amount: 75000,
      currency: "INR",
      status: "pending",
      payment_method: null,
      transaction_id: null,
      receipt_url: null,
      notes: "Hostel annual fee",
      created_at: "2026-02-01T10:00:00Z",
      updated_at: "2026-02-01T10:00:00Z",
    },
  ],
  total: 2,
};

export const demoHostelStatus = {
  id: "",
  user_id: "demo",
  university_id: "demo",
  room_type_preference: "",
  special_requirements: null,
  status: "not_applied",
  allocated_room_number: null,
  allocated_block: null,
  floor: null,
  admin_notes: null,
  created_at: "",
  updated_at: "",
};

export const demoLMSStatus: LMSStatus = {
  platform: "Moodle",
  is_activated: false,
  lms_username: null,
  lms_id: null,
  activated_at: null,
};

export const demoChatSessions: ChatSessionListResponse = {
  sessions: [],
  total: 0,
};

export const demoOnboardingProgress: OnboardingProgressResponse = {
  id: "demo",
  overall_progress: 45,
  is_completed: false,
  completed_at: null,
  items: [
    {
      id: "1",
      title: "Complete Profile",
      description: "Fill in your personal details",
      category: "profile",
      order: 1,
      is_completed: true,
      is_required: true,
      deadline: null,
      completed_at: "2026-01-10T10:00:00Z",
    },
    {
      id: "2",
      title: "Upload Documents",
      description: "Upload required documents",
      category: "documents",
      order: 2,
      is_completed: false,
      is_required: true,
      deadline: "2026-03-01T00:00:00Z",
      completed_at: null,
    },
  ],
  created_at: "2026-01-01T00:00:00Z",
};

export const demoComplianceStatus = {
  items: [
    {
      id: "c1",
      user_id: "demo",
      compliance_item_id: "ci1",
      university_id: "demo",
      is_completed: true,
      completed_at: "2026-01-15T10:00:00Z",
      item_title: "Anti-Ragging Declaration",
      item_type: "declaration",
      item_description: "Sign the anti-ragging declaration form",
      content_url: null,
      is_required: true,
    },
    {
      id: "c2",
      user_id: "demo",
      compliance_item_id: "ci2",
      university_id: "demo",
      is_completed: false,
      completed_at: null,
      item_title: "Code of Conduct Agreement",
      item_type: "agreement",
      item_description: "Read and agree to the student code of conduct",
      content_url: null,
      is_required: true,
    },
    {
      id: "c3",
      user_id: "demo",
      compliance_item_id: "ci3",
      university_id: "demo",
      is_completed: false,
      completed_at: null,
      item_title: "Library Rules Acknowledgement",
      item_type: "acknowledgement",
      item_description: "Acknowledge the library usage guidelines",
      content_url: null,
      is_required: false,
    },
  ],
  total: 3,
  completed: 1,
  required_total: 2,
  required_completed: 1,
  all_required_done: false,
};

export const demoCourses: CourseListResponse = {
  courses: [
    {
      id: "cr1",
      university_id: "demo",
      name: "B.Tech Computer Science",
      code: "BTCS",
      description: "Bachelor of Technology in Computer Science & Engineering",
      duration_years: 4,
      total_credits: 160,
      is_active: true,
      created_at: "2025-06-01T00:00:00Z",
    },
    {
      id: "cr2",
      university_id: "demo",
      name: "B.Tech Information Technology",
      code: "BTIT",
      description: "Bachelor of Technology in Information Technology",
      duration_years: 4,
      total_credits: 160,
      is_active: true,
      created_at: "2025-06-01T00:00:00Z",
    },
  ],
  total: 2,
};

export const demoSubjects: SubjectListResponse = {
  subjects: [
    {
      id: "s1",
      course_id: "cr1",
      university_id: "demo",
      name: "Data Structures & Algorithms",
      code: "CS201",
      credits: 4,
      semester: 3,
      is_elective: false,
      is_active: true,
      created_at: "2025-06-01T00:00:00Z",
    },
    {
      id: "s2",
      course_id: "cr1",
      university_id: "demo",
      name: "Database Management Systems",
      code: "CS202",
      credits: 3,
      semester: 3,
      is_elective: false,
      is_active: true,
      created_at: "2025-06-01T00:00:00Z",
    },
    {
      id: "s3",
      course_id: "cr1",
      university_id: "demo",
      name: "Machine Learning",
      code: "CS301",
      credits: 4,
      semester: 5,
      is_elective: true,
      is_active: true,
      created_at: "2025-06-01T00:00:00Z",
    },
  ],
  total: 3,
};

export const demoEnrollments: EnrollmentListResponse = {
  enrollments: [
    {
      id: "e1",
      user_id: "demo",
      course_id: "cr1",
      subject_id: "s1",
      university_id: "demo",
      status: "enrolled",
      enrolled_at: "2026-01-10T10:00:00Z",
      subject_name: "Data Structures & Algorithms",
      subject_code: "CS201",
      course_name: "B.Tech Computer Science",
    },
    {
      id: "e2",
      user_id: "demo",
      course_id: "cr1",
      subject_id: "s2",
      university_id: "demo",
      status: "enrolled",
      enrolled_at: "2026-01-10T10:00:00Z",
      subject_name: "Database Management Systems",
      subject_code: "CS202",
      course_name: "B.Tech Computer Science",
    },
  ],
  total: 2,
  course_name: "B.Tech Computer Science",
};

export const demoWeeklyTimetable: WeeklyTimetableResponse = {
  days: [
    {
      day: "Monday",
      entries: [
        {
          schedule_id: "t1",
          subject_name: "Data Structures & Algorithms",
          subject_code: "CS201",
          start_time: "09:00",
          end_time: "10:30",
          room: "LH-101",
          instructor: "Dr. Sharma",
        },
        {
          schedule_id: "t2",
          subject_name: "Database Management Systems",
          subject_code: "CS202",
          start_time: "11:00",
          end_time: "12:30",
          room: "LH-203",
          instructor: "Prof. Patil",
        },
      ],
    },
    {
      day: "Tuesday",
      entries: [
        {
          schedule_id: "t3",
          subject_name: "Machine Learning",
          subject_code: "CS301",
          start_time: "10:00",
          end_time: "11:30",
          room: "LH-105",
          instructor: "Dr. Kulkarni",
        },
      ],
    },
    {
      day: "Wednesday",
      entries: [
        {
          schedule_id: "t4",
          subject_name: "Data Structures & Algorithms",
          subject_code: "CS201",
          start_time: "09:00",
          end_time: "10:30",
          room: "Lab-A1",
          instructor: "Dr. Sharma",
        },
        {
          schedule_id: "t5",
          subject_name: "Database Management Systems",
          subject_code: "CS202",
          start_time: "14:00",
          end_time: "15:30",
          room: "LH-203",
          instructor: "Prof. Patil",
        },
      ],
    },
    {
      day: "Thursday",
      entries: [
        {
          schedule_id: "t6",
          subject_name: "Machine Learning",
          subject_code: "CS301",
          start_time: "10:00",
          end_time: "11:30",
          room: "Lab-B2",
          instructor: "Dr. Kulkarni",
        },
      ],
    },
    {
      day: "Friday",
      entries: [
        {
          schedule_id: "t7",
          subject_name: "Data Structures & Algorithms",
          subject_code: "CS201",
          start_time: "09:00",
          end_time: "10:30",
          room: "LH-101",
          instructor: "Dr. Sharma",
        },
      ],
    },
  ],
  total_subjects: 3,
  total_hours: 12,
};

export const demoMentorProfile: MentorProfile = {
  mentor_id: "m1",
  mentor_name: "Dr. Rajesh Kumar",
  mentor_email: "rajesh.kumar@campusai.app",
  assignment_id: "a1",
  is_active: true,
  assigned_at: "2026-01-05T10:00:00Z",
  upcoming_meetings: [
    {
      id: "mt1",
      assignment_id: "a1",
      student_id: "demo",
      mentor_id: "m1",
      university_id: "demo",
      title: "Weekly Check-in",
      description: "Discuss semester progress and any issues",
      meeting_date: "2026-02-20T00:00:00Z",
      start_time: "14:00",
      end_time: "14:30",
      status: "scheduled",
      meeting_link: "https://meet.google.com/demo",
      notes: null,
      mentor_name: "Dr. Rajesh Kumar",
      student_name: "Demo Student",
      created_at: "2026-02-15T10:00:00Z",
    },
  ],
  unread_messages: 2,
};

export const demoMentorMeetings = {
  meetings: [
    {
      id: "mt1",
      assignment_id: "a1",
      student_id: "demo",
      mentor_id: "m1",
      university_id: "demo",
      title: "Weekly Check-in",
      description: "Discuss semester progress",
      meeting_date: "2026-02-20T00:00:00Z",
      start_time: "14:00",
      end_time: "14:30",
      status: "scheduled",
      meeting_link: "https://meet.google.com/demo",
      notes: null,
      mentor_name: "Dr. Rajesh Kumar",
      student_name: "Demo Student",
      created_at: "2026-02-15T10:00:00Z",
    },
    {
      id: "mt2",
      assignment_id: "a1",
      student_id: "demo",
      mentor_id: "m1",
      university_id: "demo",
      title: "Course Selection Guidance",
      description: "Help with elective selection for next semester",
      meeting_date: "2026-02-10T00:00:00Z",
      start_time: "15:00",
      end_time: "15:30",
      status: "completed",
      meeting_link: null,
      notes: "Selected Machine Learning as elective",
      mentor_name: "Dr. Rajesh Kumar",
      student_name: "Demo Student",
      created_at: "2026-02-08T10:00:00Z",
    },
  ],
  total: 2,
};

export const demoUser = {
  id: "demo",
  email: "demo@campusai.app",
  first_name: "Demo",
  last_name: "Student",
  phone: "+91 9876543210",
  role: "student" as const,
  university_id: "demo",
  is_active: true,
  is_email_verified: true,
  created_at: "2026-01-01T00:00:00Z",
  last_login_at: "2026-02-18T08:00:00Z",
};

export const demoMentorMessages = {
  messages: [
    {
      id: "msg1",
      assignment_id: "a1",
      sender_id: "m1",
      content: "Welcome! Feel free to reach out if you need any guidance.",
      is_read: true,
      sender_name: "Dr. Rajesh Kumar",
      created_at: "2026-01-05T11:00:00Z",
    },
    {
      id: "msg2",
      assignment_id: "a1",
      sender_id: "m1",
      content: "Don't forget to submit your documents before the deadline!",
      is_read: false,
      sender_name: "Dr. Rajesh Kumar",
      created_at: "2026-02-14T09:00:00Z",
    },
  ],
  total: 2,
};
