// ─── User ───
export enum UserRole {
  STUDENT = "student",
  ADMIN = "admin",
  SUPERADMIN = "superadmin",
  MENTOR = "mentor",
}

export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  phone?: string;
  avatar_url?: string;
  role: UserRole;
  university_id?: string;
  is_active: boolean;
  is_email_verified: boolean;
  created_at: string;
  last_login_at?: string;
}

// ─── Auth ───
export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  phone?: string;
  university_slug?: string;
  college_name?: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

// ─── University ───
export interface University {
  id: string;
  name: string;
  slug: string;
  logo_url?: string;
  domain?: string;
  is_active: boolean;
  subscription_plan_id?: string;
  created_at: string;
}

export interface SubscriptionPlan {
  id: string;
  name: string;
  max_students: number;
  price_monthly: number;
  features: Record<string, boolean>;
  is_active: boolean;
}

// ─── Onboarding ───
export interface ChecklistItem {
  id: string;
  title: string;
  description?: string;
  order: number;
  is_completed: boolean;
  completed_at?: string;
}

export interface OnboardingProgress {
  checklist_id: string;
  total_items: number;
  completed_items: number;
  percentage: number;
  items: ChecklistItem[];
}

// ─── Documents ───
export enum DocumentStatus {
  PENDING = "pending",
  UNDER_REVIEW = "under_review",
  APPROVED = "approved",
  REJECTED = "rejected",
}

export interface Document {
  id: string;
  user_id: string;
  document_type: string;
  file_url: string;
  file_name: string;
  file_size: number;
  mime_type: string;
  status: DocumentStatus;
  rejection_reason?: string;
  reviewed_by?: string;
  reviewed_at?: string;
  created_at: string;
  uploaded_at?: string; // alias kept for compat
  student_name?: string;
  student_email?: string;
}

// ─── Payments ───
export enum PaymentStatus {
  PENDING = "pending",
  COMPLETED = "completed",
  FAILED = "failed",
  REFUNDED = "refunded",
}

export interface Payment {
  id: string;
  user_id: string;
  amount: number;
  currency: string;
  payment_type: string;
  status: PaymentStatus;
  transaction_id?: string;
  gateway_response?: Record<string, unknown>;
  created_at: string;
}

// ─── Hostel ───
export enum RoomType {
  SINGLE = "single",
  DOUBLE = "double",
  TRIPLE = "triple",
}

export enum ApplicationStatus {
  PENDING = "pending",
  APPROVED = "approved",
  REJECTED = "rejected",
  WAITLISTED = "waitlisted",
}

export interface HostelApplication {
  id: string;
  user_id: string;
  room_type: RoomType;
  preferences?: string;
  status: ApplicationStatus;
  allocated_room?: string;
  created_at: string;
}

// ─── LMS ───
export interface LMSActivation {
  id: string;
  user_id: string;
  platform: string;
  is_activated: boolean;
  activation_date?: string;
  lms_user_id?: string;
}

// ─── Chat ───
export interface ChatMessage {
  id: string;
  session_id: string;
  role: "user" | "assistant";
  content: string;
  created_at: string;
}

export interface ChatSession {
  id: string;
  user_id: string;
  title?: string;
  created_at: string;
  updated_at: string;
}

// ─── API Response ───
export interface ApiResponse<T> {
  data: T;
  message?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}

// ─── Admin Analytics ───
export interface AdminAnalytics {
  total_students: number;
  onboarding_completed: number;
  pending_documents: number;
  pending_hostel: number;
  revenue: number;
  completion_rate: number;
}
