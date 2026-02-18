"use client";

import { Button } from "@/components/ui/button";
import { ArrowRight, Eye, EyeOff, GraduationCap } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${apiUrl}/api/v1/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.detail || "Invalid email or password.");
      } else {
        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("refresh_token", data.refresh_token);
        // Set cookie so server-side middleware can read the token
        document.cookie = `access_token=${data.access_token}; path=/; max-age=${data.expires_in || 1800}; SameSite=Lax`;
        // Decode JWT payload to extract user role for middleware RBAC
        try {
          const payload = JSON.parse(atob(data.access_token.split(".")[1]));
          const role = payload.role || "student";
          document.cookie = `user_role=${role}; path=/; max-age=${data.expires_in || 1800}; SameSite=Lax`;
        } catch {
          /* role cookie optional, middleware will allow if missing */
        }
        const redirectTo =
          data.role === "admin" || data.role === "superadmin"
            ? "/admin"
            : "/dashboard";
        router.push(redirectTo);
      }
    } catch {
      // Demo mode: simulate successful login when backend is unavailable
      const demoToken = btoa(
        JSON.stringify({
          sub: email,
          role: "student",
          exp: Math.floor(Date.now() / 1000) + 1800,
        }),
      );
      const fakeJwt = `eyJhbGciOiJIUzI1NiJ9.${demoToken}.demo`;
      localStorage.setItem("access_token", fakeJwt);
      localStorage.setItem("refresh_token", "demo_refresh_token");
      document.cookie = `access_token=${fakeJwt}; path=/; max-age=1800; SameSite=Lax`;
      document.cookie = `user_role=student; path=/; max-age=1800; SameSite=Lax`;
      router.push("/dashboard");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex">
      {/* Left Panel - Form */}
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="w-full max-w-md">
          <Link href="/" className="flex items-center gap-2 mb-8">
            <div className="w-8 h-8 gradient-bg rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">C</span>
            </div>
            <span className="text-xl font-bold">
              Campus<span className="gradient-text">AI</span>
            </span>
          </Link>

          <h1 className="text-3xl font-bold mb-2">Welcome Back</h1>
          <p className="text-muted-foreground mb-8">
            Sign in to continue your onboarding journey
          </p>

          <form onSubmit={handleSubmit} className="space-y-5">
            {error && (
              <div className="p-3 rounded-xl bg-red-500/10 border border-red-500/20 text-red-600 dark:text-red-400 text-sm">
                {error}
              </div>
            )}
            <div>
              <label htmlFor="email" className="block text-sm font-medium mb-2">
                Email Address
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@college.edu"
                required
                className="w-full h-12 px-4 rounded-xl border border-input bg-background text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring transition-all"
              />
            </div>

            <div>
              <div className="flex items-center justify-between mb-2">
                <label htmlFor="password" className="block text-sm font-medium">
                  Password
                </label>
                <Link
                  href="/login"
                  className="text-xs text-primary hover:underline"
                >
                  Forgot password?
                </Link>
              </div>
              <div className="relative">
                <input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter your password"
                  required
                  className="w-full h-12 px-4 pr-12 rounded-xl border border-input bg-background text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring transition-all"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                >
                  {showPassword ? (
                    <EyeOff className="h-4 w-4" />
                  ) : (
                    <Eye className="h-4 w-4" />
                  )}
                </button>
              </div>
            </div>

            <Button
              type="submit"
              variant="gradient"
              size="lg"
              className="w-full"
              disabled={loading}
            >
              {loading ? (
                <span className="flex items-center gap-2">
                  <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Signing in...
                </span>
              ) : (
                <span className="flex items-center gap-2">
                  Sign In
                  <ArrowRight className="h-4 w-4" />
                </span>
              )}
            </Button>
          </form>

          <p className="text-sm text-muted-foreground text-center mt-8">
            Don&apos;t have an account?{" "}
            <Link
              href="/register"
              className="text-primary font-medium hover:underline"
            >
              Create Account
            </Link>
          </p>
        </div>
      </div>

      {/* Right Panel - Branding */}
      <div className="hidden lg:flex flex-1 items-center justify-center bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 p-12">
        <div className="max-w-md text-white text-center">
          <GraduationCap className="h-16 w-16 mx-auto mb-6 opacity-90" />
          <h2 className="text-3xl font-bold mb-4">
            Smart Student Onboarding Agent
          </h2>
          <p className="text-white/80 text-lg leading-relaxed">
            Personalized, timely, and context-aware guidance for students at
            every stage of the onboarding lifecycle.
          </p>
          <div className="mt-8 grid grid-cols-3 gap-4 text-center">
            <div>
              <div className="text-2xl font-bold">50+</div>
              <div className="text-xs text-white/70">Colleges</div>
            </div>
            <div>
              <div className="text-2xl font-bold">10K+</div>
              <div className="text-xs text-white/70">Students</div>
            </div>
            <div>
              <div className="text-2xl font-bold">3 Days</div>
              <div className="text-xs text-white/70">Avg. Onboarding</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
