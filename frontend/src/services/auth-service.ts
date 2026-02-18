import type { AuthTokens, LoginRequest, RegisterRequest, User } from "@/types";
import { apiClient } from "./api-client";

export const authService = {
  async login(data: LoginRequest): Promise<AuthTokens> {
    const response = await apiClient.post<AuthTokens>(
      "/api/v1/auth/login",
      data,
    );
    localStorage.setItem("access_token", response.access_token);
    localStorage.setItem("refresh_token", response.refresh_token);
    return response;
  },

  async register(data: RegisterRequest): Promise<{ message: string }> {
    return apiClient.post("/api/v1/auth/register", data);
  },

  async verifyEmail(token: string): Promise<{ message: string }> {
    return apiClient.post("/api/v1/auth/verify-email", { token });
  },

  async getMe(): Promise<User> {
    return apiClient.get<User>("/api/v1/auth/me");
  },

  async logout(): Promise<void> {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    document.cookie = "access_token=; path=/; max-age=0; SameSite=Lax";
  },

  isAuthenticated(): boolean {
    if (typeof window === "undefined") return false;
    return !!localStorage.getItem("access_token");
  },
};
