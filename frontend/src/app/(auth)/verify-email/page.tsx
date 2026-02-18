"use client";

import { Button } from "@/components/ui/button";
import { CheckCircle, Mail } from "lucide-react";
import Link from "next/link";

export default function VerifyEmailPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-50 via-white to-purple-50 dark:from-gray-950 dark:via-gray-900 dark:to-indigo-950 p-4">
      <div className="glass-card p-10 w-full max-w-md text-center rounded-2xl">
        <div className="w-16 h-16 gradient-bg rounded-full flex items-center justify-center mx-auto mb-6">
          <Mail className="h-8 w-8 text-white" />
        </div>
        <h1 className="text-2xl font-bold mb-3">Check Your Email</h1>
        <p className="text-muted-foreground mb-6 leading-relaxed">
          We&apos;ve sent a verification link to your email address. Please
          click the link to verify your account and complete registration.
        </p>

        <div className="glass-card p-4 rounded-xl mb-6 text-left">
          <div className="flex items-start gap-3">
            <CheckCircle className="h-5 w-5 text-green-500 mt-0.5 flex-shrink-0" />
            <div className="text-sm text-muted-foreground">
              <p className="font-medium text-foreground mb-1">Next Steps</p>
              <ul className="space-y-1">
                <li>1. Open your email inbox</li>
                <li>2. Click the verification link</li>
                <li>3. You&apos;ll be redirected to login</li>
              </ul>
            </div>
          </div>
        </div>

        <div className="space-y-3">
          <Button variant="gradient" className="w-full" asChild>
            <Link href="/login">Go to Login</Link>
          </Button>
          <p className="text-xs text-muted-foreground">
            Didn&apos;t receive the email?{" "}
            <button className="text-primary hover:underline font-medium">
              Resend verification email
            </button>
          </p>
        </div>
      </div>
    </div>
  );
}
