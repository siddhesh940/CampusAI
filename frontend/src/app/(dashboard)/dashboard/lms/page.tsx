"use client";

import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { lmsService, type LMSStatus } from "@/services/campus-services";
import { demoLMSStatus, withDemoFallback } from "@/services/demo-data";
import {
    BookOpen,
    Calendar,
    CheckCircle2,
    Copy,
    ExternalLink,
    Hash,
    Loader2,
    User,
    Zap,
} from "lucide-react";
import { useEffect, useState } from "react";

export default function LMSPage() {
  const [status, setStatus] = useState<LMSStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [activating, setActivating] = useState(false);
  const [error, setError] = useState("");
  const [copied, setCopied] = useState("");

  useEffect(() => {
    withDemoFallback(() => lmsService.getStatus(), demoLMSStatus)
      .then(setStatus)
      .catch((e) => {
        if (!e.message?.includes("404")) {
          setError(e.message);
        }
      })
      .finally(() => setLoading(false));
  }, []);

  const handleActivate = async () => {
    setActivating(true);
    setError("");
    try {
      const s = await lmsService.activate();
      setStatus(s);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setActivating(false);
    }
  };

  const copyToClipboard = (text: string, field: string) => {
    navigator.clipboard.writeText(text);
    setCopied(field);
    setTimeout(() => setCopied(""), 2000);
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-9 w-40" />
        <Skeleton className="h-64 rounded-xl" />
      </div>
    );
  }

  const isActive = status?.is_activated;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">LMS Access</h1>
        <p className="text-muted-foreground">
          Activate and manage your Learning Management System access.
        </p>
      </div>

      {error && (
        <div className="glass-card p-4 border-red-200 dark:border-red-800">
          <p className="text-red-600 dark:text-red-400 text-sm">{error}</p>
        </div>
      )}

      <div className="glass-card p-6">
        {/* Not activated */}
        {!isActive && (
          <div className="text-center py-12">
            <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-primary/10 mb-6">
              <BookOpen className="h-10 w-10 text-primary" />
            </div>
            <h2 className="text-2xl font-bold mb-2">Activate Your LMS</h2>
            <p className="text-muted-foreground max-w-md mx-auto mb-6">
              Get instant access to your Learning Management System. Your
              credentials will be generated automatically.
            </p>
            <Button
              onClick={handleActivate}
              disabled={activating}
              variant="gradient"
              size="lg"
            >
              {activating ? (
                <>
                  <Loader2 className="h-5 w-5 animate-spin mr-2" />{" "}
                  Activating...
                </>
              ) : (
                <>
                  <Zap className="h-5 w-5 mr-2" /> Activate LMS
                </>
              )}
            </Button>
          </div>
        )}

        {/* Activated */}
        {isActive && status && (
          <div>
            <div className="flex items-center gap-3 mb-6">
              <div className="p-2.5 rounded-xl bg-green-500">
                <CheckCircle2 className="h-6 w-6 text-white" />
              </div>
              <div>
                <h2 className="text-xl font-bold">LMS Activated</h2>
                <p className="text-sm text-muted-foreground">
                  Your learning platform is ready to use
                </p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* LMS ID */}
              <div className="flex items-center gap-3 p-4 rounded-xl bg-muted/50">
                <Hash className="h-5 w-5 text-muted-foreground" />
                <div className="flex-1">
                  <p className="text-xs text-muted-foreground">LMS ID</p>
                  <p className="font-mono font-bold">{status.lms_id}</p>
                </div>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => copyToClipboard(status.lms_id || "", "id")}
                >
                  {copied === "id" ? (
                    <CheckCircle2 className="h-4 w-4 text-green-500" />
                  ) : (
                    <Copy className="h-4 w-4" />
                  )}
                </Button>
              </div>

              {/* Username */}
              <div className="flex items-center gap-3 p-4 rounded-xl bg-muted/50">
                <User className="h-5 w-5 text-muted-foreground" />
                <div className="flex-1">
                  <p className="text-xs text-muted-foreground">LMS Username</p>
                  <p className="font-mono font-bold">{status.lms_username}</p>
                </div>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() =>
                    copyToClipboard(status.lms_username || "", "user")
                  }
                >
                  {copied === "user" ? (
                    <CheckCircle2 className="h-4 w-4 text-green-500" />
                  ) : (
                    <Copy className="h-4 w-4" />
                  )}
                </Button>
              </div>

              {/* Platform */}
              <div className="flex items-center gap-3 p-4 rounded-xl bg-muted/50">
                <BookOpen className="h-5 w-5 text-muted-foreground" />
                <div>
                  <p className="text-xs text-muted-foreground">Platform</p>
                  <p className="font-medium">{status.platform}</p>
                </div>
              </div>

              {/* Activated Date */}
              {status.activated_at && (
                <div className="flex items-center gap-3 p-4 rounded-xl bg-muted/50">
                  <Calendar className="h-5 w-5 text-muted-foreground" />
                  <div>
                    <p className="text-xs text-muted-foreground">
                      Activated On
                    </p>
                    <p className="font-medium">
                      {new Date(status.activated_at).toLocaleDateString(
                        "en-IN",
                        {
                          day: "numeric",
                          month: "long",
                          year: "numeric",
                        },
                      )}
                    </p>
                  </div>
                </div>
              )}
            </div>

            <div className="mt-6 p-4 rounded-xl bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800">
              <p className="text-sm text-blue-700 dark:text-blue-400">
                <strong>Tip:</strong> Use your LMS Username and the password
                sent to your email to log into {status.platform}.
              </p>
            </div>

            <div className="mt-4">
              <Button variant="outline" asChild>
                <a href="#" target="_blank" rel="noopener noreferrer">
                  <ExternalLink className="h-4 w-4 mr-2" />
                  Open {status.platform}
                </a>
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
