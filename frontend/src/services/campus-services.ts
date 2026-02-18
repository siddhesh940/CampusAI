import type {
    ChatMessage,
    Document,
    HostelApplication,
    Payment,
} from "@/types";
import { apiClient } from "./api-client";

// ─── Dashboard ────────────────────────────────────────
export interface DashboardChecklistItem {
  id: string;
  title: string;
  description: string | null;
  category: string;
  order: number;
  is_completed: boolean;
  is_required: boolean;
}

export interface DashboardChecklist {
  items: DashboardChecklistItem[];
  percentage: number;
  total: number;
  completed: number;
}

export interface DashboardSummary {
  documents: {
    total: number;
    approved: number;
    pending: number;
    rejected: number;
    under_review: number;
  };
  payments: {
    status: string;
    total_paid: number;
    total_pending: number;
    count: number;
  };
  hostel: {
    status: string;
    room_type: string | null;
    room_number: string | null;
  };
  lms: {
    status: string;
    lms_id: string | null;
    platform: string;
  };
  onboarding_percentage: number;
  checklist: DashboardChecklist;
  user: {
    name: string;
    email: string;
    role: string;
  };
}

export const dashboardService = {
  async getSummary(): Promise<DashboardSummary> {
    return apiClient.get<DashboardSummary>("/api/v1/dashboard/summary");
  },
};

// ─── Documents ────────────────────────────────────────
export interface DocumentListResponse {
  documents: Document[];
  total: number;
}

export interface DocumentUploadResponse {
  id: string;
  document_type: string;
  file_name: string;
  file_url: string;
  status: string;
  created_at: string;
}

export const documentService = {
  async list(): Promise<DocumentListResponse> {
    return apiClient.get<DocumentListResponse>("/api/v1/documents");
  },

  async upload(
    documentType: string,
    file: File,
  ): Promise<DocumentUploadResponse> {
    const formData = new FormData();
    formData.append("document_type", documentType);
    formData.append("file", file);
    return apiClient.upload<DocumentUploadResponse>(
      "/api/v1/documents/upload",
      formData,
    );
  },

  async review(
    documentId: string,
    status: string,
    rejectionReason?: string,
  ): Promise<Document> {
    return apiClient.put<Document>(`/api/v1/documents/${documentId}/review`, {
      status,
      rejection_reason: rejectionReason,
    });
  },
};

// ─── Payments ─────────────────────────────────────────
export interface PaymentListResponse {
  payments: Payment[];
  total: number;
}

export const paymentService = {
  async list(): Promise<PaymentListResponse> {
    return apiClient.get<PaymentListResponse>("/api/v1/payments");
  },

  async initiate(data: {
    payment_type: string;
    amount: number;
    currency?: string;
    payment_method?: string;
    notes?: string;
  }): Promise<Payment> {
    return apiClient.post<Payment>("/api/v1/payments/initiate", data);
  },

  async verify(paymentId: string): Promise<Payment> {
    return apiClient.post<Payment>(`/api/v1/payments/${paymentId}/verify`);
  },

  getReceiptUrl(paymentId: string): string {
    const baseUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    return `${baseUrl}/api/v1/payments/${paymentId}/receipt`;
  },
};

// ─── Hostel ───────────────────────────────────────────
export const hostelService = {
  async apply(data: {
    room_type_preference: string;
    special_requirements?: string;
  }): Promise<HostelApplication> {
    return apiClient.post<HostelApplication>("/api/v1/hostel/apply", data);
  },

  async getStatus(): Promise<HostelApplication> {
    return apiClient.get<HostelApplication>("/api/v1/hostel/status");
  },

  async allocate(
    applicationId: string,
    data: {
      status: string;
      allocated_room_number?: string;
      allocated_block?: string;
      floor?: number;
      admin_notes?: string;
    },
  ): Promise<HostelApplication> {
    return apiClient.put<HostelApplication>(
      `/api/v1/hostel/${applicationId}/allocate`,
      data,
    );
  },
};

// ─── LMS ──────────────────────────────────────────────
export interface LMSStatus {
  id?: string;
  user_id?: string;
  platform: string;
  is_activated: boolean;
  lms_username: string | null;
  lms_id: string | null;
  activated_at: string | null;
}

export const lmsService = {
  async activate(): Promise<LMSStatus> {
    return apiClient.post<LMSStatus>("/api/v1/lms/activate");
  },

  async getStatus(): Promise<LMSStatus> {
    return apiClient.get<LMSStatus>("/api/v1/lms/status");
  },
};

// ─── Chat ─────────────────────────────────────────────
export interface ChatSessionResponse {
  id: string;
  title: string;
  messages: ChatMessage[];
  created_at: string;
  updated_at: string;
}

export interface ChatSessionListResponse {
  sessions: ChatSessionResponse[];
  total: number;
}

export const chatService = {
  async sendMessage(
    message: string,
    sessionId?: string,
  ): Promise<ChatSessionResponse> {
    return apiClient.post<ChatSessionResponse>("/api/v1/chat/message", {
      message,
      session_id: sessionId,
    });
  },

  async getHistory(): Promise<ChatSessionListResponse> {
    return apiClient.get<ChatSessionListResponse>("/api/v1/chat/history");
  },

  async getSession(sessionId: string): Promise<ChatSessionResponse> {
    return apiClient.get<ChatSessionResponse>(
      `/api/v1/chat/session/${sessionId}`,
    );
  },
};

// ─── Onboarding ───────────────────────────────────────
export interface OnboardingProgressResponse {
  id: string;
  overall_progress: number;
  is_completed: boolean;
  completed_at: string | null;
  items: Array<{
    id: string;
    title: string;
    description: string | null;
    category: string;
    order: number;
    is_completed: boolean;
    is_required: boolean;
    deadline: string | null;
    completed_at: string | null;
  }>;
  created_at: string;
}

export const onboardingService = {
  async getProgress(): Promise<OnboardingProgressResponse> {
    return apiClient.get<OnboardingProgressResponse>(
      "/api/v1/onboarding/progress",
    );
  },

  async updateItem(
    itemId: string,
    isCompleted: boolean,
  ): Promise<OnboardingProgressResponse> {
    return apiClient.put<OnboardingProgressResponse>(
      `/api/v1/onboarding/checklist/${itemId}`,
      { is_completed: isCompleted },
    );
  },
};

// ─── User Profile ─────────────────────────────────────
export const userService = {
  async updateProfile(data: {
    first_name?: string;
    last_name?: string;
    phone?: string;
    avatar_url?: string;
  }): Promise<import("@/types").User> {
    return apiClient.put<import("@/types").User>("/api/v1/users/me", data);
  },
};

// ─── Admin ────────────────────────────────────────────
export interface AdminAnalyticsResponse {
  total_students: number;
  onboarding_completed: number;
  pending_documents: number;
  pending_hostel: number;
  total_revenue: number;
  completion_rate: number;
}

export interface StudentListResponse {
  students: import("@/types").User[];
  total: number;
}

export interface PendingDocumentsResponse {
  documents: import("@/types").Document[];
  total: number;
}

export const adminService = {
  async getAnalytics(): Promise<AdminAnalyticsResponse> {
    return apiClient.get<AdminAnalyticsResponse>("/api/v1/admin/analytics");
  },

  async listStudents(
    page = 1,
    limit = 20,
    search?: string,
  ): Promise<StudentListResponse> {
    const params = new URLSearchParams({
      page: String(page),
      limit: String(limit),
    });
    if (search) params.set("search", search);
    return apiClient.get<StudentListResponse>(
      `/api/v1/admin/students?${params}`,
    );
  },

  async getPendingDocuments(): Promise<PendingDocumentsResponse> {
    return apiClient.get<PendingDocumentsResponse>(
      "/api/v1/admin/documents/pending",
    );
  },

  async getDocuments(
    status?: string,
    page = 1,
    perPage = 50,
    search?: string,
  ): Promise<PendingDocumentsResponse> {
    const params = new URLSearchParams({
      page: String(page),
      per_page: String(perPage),
    });
    if (status && status !== "all") params.set("status", status);
    if (search) params.set("search", search);
    return apiClient.get<PendingDocumentsResponse>(
      `/api/v1/admin/documents?${params}`,
    );
  },

  // ── Hostel admin ──
  async listHostelApplications(
    status?: string,
  ): Promise<{
    applications: import("@/types").HostelApplication[];
    total: number;
  }> {
    const params = status && status !== "all" ? `?status=${status}` : "";
    return apiClient.get(`/api/v1/admin/hostel${params}`);
  },

  // ── LMS admin ──
  async listLMSActivations(): Promise<{
    activations: Array<{
      id: string;
      user_id: string;
      platform: string;
      is_activated: boolean;
      lms_username: string | null;
      activation_key: string | null;
      activated_at: string | null;
      student_name: string;
      student_email: string;
    }>;
    total: number;
  }> {
    return apiClient.get("/api/v1/admin/lms");
  },

  async generateLMSCredentials(userId: string): Promise<{
    id: string;
    lms_username: string;
    activation_key: string;
    is_activated: boolean;
  }> {
    return apiClient.post("/api/v1/admin/lms/generate", { user_id: userId });
  },

  // ── Mentors list for admin ──
  async listMentors(): Promise<{
    mentors: import("@/types").User[];
    total: number;
  }> {
    return apiClient.get("/api/v1/admin/mentors");
  },

  // ── Payments admin ──
  async listPayments(
    status?: string,
    page = 1,
    perPage = 50,
  ): Promise<{
    payments: import("@/types").Payment[];
    total: number;
  }> {
    const params = new URLSearchParams({
      page: String(page),
      per_page: String(perPage),
    });
    if (status && status !== "all") params.set("status", status);
    return apiClient.get(`/api/v1/admin/payments?${params}`);
  },
};

// ─── Course Registration ──────────────────────────────
export interface Course {
  id: string;
  university_id: string;
  name: string;
  code: string;
  description: string | null;
  duration_years: number;
  total_credits: number;
  is_active: boolean;
  created_at: string;
}

export interface Subject {
  id: string;
  course_id: string;
  university_id: string;
  name: string;
  code: string;
  credits: number;
  semester: number;
  is_elective: boolean;
  is_active: boolean;
  created_at: string;
}

export interface Enrollment {
  id: string;
  user_id: string;
  course_id: string;
  subject_id: string;
  university_id: string;
  status: string;
  enrolled_at: string;
  subject_name?: string;
  subject_code?: string;
  course_name?: string;
}

export interface CourseListResponse {
  courses: Course[];
  total: number;
}
export interface SubjectListResponse {
  subjects: Subject[];
  total: number;
}
export interface EnrollmentListResponse {
  enrollments: Enrollment[];
  total: number;
  course_name?: string;
}

export const courseService = {
  async listCourses(): Promise<CourseListResponse> {
    return apiClient.get<CourseListResponse>("/api/v1/courses/");
  },
  async getCourse(id: string): Promise<Course> {
    return apiClient.get<Course>(`/api/v1/courses/${id}`);
  },
  async createCourse(data: {
    name: string;
    code: string;
    description?: string;
    duration_years?: number;
    total_credits?: number;
  }): Promise<Course> {
    return apiClient.post<Course>("/api/v1/courses/", data);
  },
  async listSubjects(courseId?: string): Promise<SubjectListResponse> {
    const params = courseId ? `?course_id=${courseId}` : "";
    return apiClient.get<SubjectListResponse>(
      `/api/v1/courses/subjects/list${params}`,
    );
  },
  async createSubject(data: {
    course_id: string;
    name: string;
    code: string;
    credits?: number;
    semester?: number;
    is_elective?: boolean;
  }): Promise<Subject> {
    return apiClient.post<Subject>("/api/v1/courses/subjects", data);
  },
  async enroll(
    courseId: string,
    subjectIds: string[],
  ): Promise<EnrollmentListResponse> {
    return apiClient.post<EnrollmentListResponse>("/api/v1/courses/enroll", {
      course_id: courseId,
      subject_ids: subjectIds,
    });
  },
  async dropSubject(subjectId: string): Promise<EnrollmentListResponse> {
    return apiClient.post<EnrollmentListResponse>("/api/v1/courses/drop", {
      subject_id: subjectId,
    });
  },
  async getEnrollments(): Promise<EnrollmentListResponse> {
    return apiClient.get<EnrollmentListResponse>(
      "/api/v1/courses/enrollments/me",
    );
  },
};

// ─── Timetable ────────────────────────────────────────
export interface TimetableEntry {
  schedule_id: string;
  subject_name: string;
  subject_code: string;
  start_time: string;
  end_time: string;
  room: string | null;
  instructor: string | null;
}

export interface TimetableDayResponse {
  day: string;
  entries: TimetableEntry[];
}

export interface WeeklyTimetableResponse {
  days: TimetableDayResponse[];
  total_subjects: number;
  total_hours: number;
}

export interface ScheduleResponse {
  id: string;
  subject_id: string;
  university_id: string;
  day_of_week: string;
  start_time: string;
  end_time: string;
  room: string | null;
  instructor: string | null;
  subject_name?: string;
  subject_code?: string;
  created_at: string;
}

export const timetableService = {
  async getWeekly(): Promise<WeeklyTimetableResponse> {
    return apiClient.get<WeeklyTimetableResponse>("/api/v1/timetable/weekly");
  },
  async listSchedules(
    subjectId?: string,
  ): Promise<{ schedules: ScheduleResponse[]; total: number }> {
    const params = subjectId ? `?subject_id=${subjectId}` : "";
    return apiClient.get(`/api/v1/timetable/schedules${params}`);
  },
  async createSchedule(data: {
    subject_id: string;
    day_of_week: string;
    start_time: string;
    end_time: string;
    room?: string;
    instructor?: string;
  }): Promise<ScheduleResponse> {
    return apiClient.post<ScheduleResponse>(
      "/api/v1/timetable/schedules",
      data,
    );
  },
  async deleteSchedule(id: string): Promise<void> {
    return apiClient.delete(`/api/v1/timetable/schedules/${id}`);
  },
};

// ─── Mentoring ────────────────────────────────────────
export interface MentorProfile {
  mentor_id: string;
  mentor_name: string;
  mentor_email: string;
  assignment_id: string;
  is_active: boolean;
  assigned_at: string;
  upcoming_meetings: MentorMeeting[];
  unread_messages: number;
}

export interface MentorMeeting {
  id: string;
  assignment_id: string;
  student_id: string;
  mentor_id: string;
  university_id: string;
  title: string;
  description: string | null;
  meeting_date: string;
  start_time: string;
  end_time: string | null;
  status: string;
  meeting_link: string | null;
  notes: string | null;
  mentor_name?: string;
  student_name?: string;
  created_at: string;
}

export interface MentorMessage {
  id: string;
  assignment_id: string;
  sender_id: string;
  content: string;
  is_read: boolean;
  sender_name?: string;
  created_at: string;
}

export interface MentorAssignment {
  id: string;
  student_id: string;
  mentor_id: string;
  university_id: string;
  is_active: boolean;
  assigned_at: string;
  mentor_name?: string;
  mentor_email?: string;
  student_name?: string;
  student_email?: string;
}

export const mentorService = {
  async getMyMentor(): Promise<MentorProfile> {
    return apiClient.get<MentorProfile>("/api/v1/mentor/me");
  },
  async getMyStudents(): Promise<{
    assignments: MentorAssignment[];
    total: number;
  }> {
    return apiClient.get("/api/v1/mentor/students");
  },
  async bookMeeting(data: {
    title: string;
    description?: string;
    meeting_date: string;
    start_time: string;
    end_time?: string;
    meeting_link?: string;
  }): Promise<MentorMeeting> {
    return apiClient.post<MentorMeeting>("/api/v1/mentor/meetings", data);
  },
  async updateMeeting(
    meetingId: string,
    data: { status: string; notes?: string; meeting_link?: string },
  ): Promise<MentorMeeting> {
    return apiClient.put<MentorMeeting>(
      `/api/v1/mentor/meetings/${meetingId}`,
      data,
    );
  },
  async listMeetings(): Promise<{ meetings: MentorMeeting[]; total: number }> {
    return apiClient.get("/api/v1/mentor/meetings");
  },
  async sendMessage(
    assignmentId: string,
    content: string,
  ): Promise<MentorMessage> {
    return apiClient.post<MentorMessage>(
      `/api/v1/mentor/${assignmentId}/messages`,
      { content },
    );
  },
  async getMessages(
    assignmentId: string,
  ): Promise<{ messages: MentorMessage[]; total: number }> {
    return apiClient.get(`/api/v1/mentor/${assignmentId}/messages`);
  },
  async assignMentor(
    studentId: string,
    mentorId: string,
  ): Promise<MentorAssignment> {
    return apiClient.post<MentorAssignment>("/api/v1/mentor/assign", {
      student_id: studentId,
      mentor_id: mentorId,
    });
  },
  async listAssignments(): Promise<{
    assignments: MentorAssignment[];
    total: number;
  }> {
    return apiClient.get("/api/v1/mentor/assignments");
  },
  async deactivateAssignment(id: string): Promise<void> {
    return apiClient.delete(`/api/v1/mentor/assignments/${id}`);
  },
};

// ─── Compliance ───────────────────────────────────────
export interface ComplianceItem {
  id: string;
  university_id: string;
  title: string;
  description: string | null;
  compliance_type: string;
  content_url: string | null;
  order: number;
  is_required: boolean;
  is_active: boolean;
  created_at: string;
}

export interface StudentComplianceStatus {
  id: string;
  user_id: string;
  compliance_item_id: string;
  university_id: string;
  is_completed: boolean;
  completed_at: string | null;
  item_title?: string;
  item_type?: string;
  item_description?: string;
  content_url?: string;
  is_required: boolean;
}

export interface ComplianceStatusResponse {
  items: StudentComplianceStatus[];
  total: number;
  completed: number;
  required_total: number;
  required_completed: number;
  all_required_done: boolean;
}

export const complianceService = {
  async listItems(): Promise<{ items: ComplianceItem[]; total: number }> {
    return apiClient.get("/api/v1/compliance/items");
  },
  async createItem(data: {
    title: string;
    description?: string;
    compliance_type: string;
    content_url?: string;
    order?: number;
    is_required?: boolean;
  }): Promise<ComplianceItem> {
    return apiClient.post<ComplianceItem>("/api/v1/compliance/items", data);
  },
  async updateItem(
    itemId: string,
    data: {
      title?: string;
      description?: string;
      compliance_type?: string;
      content_url?: string;
      order?: number;
      is_required?: boolean;
      is_active?: boolean;
    },
  ): Promise<ComplianceItem> {
    return apiClient.put<ComplianceItem>(
      `/api/v1/compliance/items/${itemId}`,
      data,
    );
  },
  async deleteItem(itemId: string): Promise<void> {
    return apiClient.delete(`/api/v1/compliance/items/${itemId}`);
  },
  async submitCompliance(
    complianceItemId: string,
  ): Promise<StudentComplianceStatus> {
    return apiClient.post<StudentComplianceStatus>(
      "/api/v1/compliance/submit",
      { compliance_item_id: complianceItemId },
    );
  },
  // Alias for backward compat
  async submit(complianceItemId: string): Promise<StudentComplianceStatus> {
    return this.submitCompliance(complianceItemId);
  },
  async getStatus(): Promise<ComplianceStatusResponse> {
    return apiClient.get<ComplianceStatusResponse>("/api/v1/compliance/status");
  },
};

// Type alias used by compliance page
export type ComplianceStatus = StudentComplianceStatus;
