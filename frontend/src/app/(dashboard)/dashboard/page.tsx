"use client";

import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Skeleton } from "@/components/ui/skeleton";
import {
    dashboardService,
    type DashboardSummary,
} from "@/services/campus-services";
import {
    ArrowRight,
    BookOpen,
    Building2,
    CheckCircle2,
    Clock,
    CreditCard,
    FileText,
} from "lucide-react";
import Link from "next/link";
import { useEffect, useState } from "react";

function StatCard({
  title,
  value,
  subtitle,
  icon: Icon,
  href,
  color,
}: {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: React.ElementType;
  href: string;
  color: string;
}) {
  return (
    <Link href={href} className="block group">
      <div className="glass-card p-5 hover:shadow-lg transition-all group-hover:border-primary/30">
        <div className="flex items-start justify-between">
          <div>
            <p className="text-sm font-medium text-muted-foreground">{title}</p>
            <p className="text-2xl font-bold mt-1">{value}</p>
            {subtitle && (
              <p className="text-xs text-muted-foreground mt-1">{subtitle}</p>
            )}
          </div>
          <div className={`p-2.5 rounded-xl ${color}`}>
            <Icon className="h-5 w-5 text-white" />
          </div>
        </div>
        <div className="flex items-center gap-1 mt-3 text-xs text-primary opacity-0 group-hover:opacity-100 transition-opacity">
          View details <ArrowRight className="h-3 w-3" />
        </div>
      </div>
    </Link>
  );
}

function ChecklistStatusIcon({ completed }: { completed: boolean }) {
  if (completed) return <CheckCircle2 className="h-4 w-4 text-green-500" />;
  return <Clock className="h-4 w-4 text-yellow-500" />;
}

const CATEGORY_LINKS: Record<string, string> = {
  profile: "/dashboard/profile",
  documents: "/dashboard/documents",
  payments: "/dashboard/payments",
  hostel: "/dashboard/hostel",
  lms: "/dashboard/lms",
  courses: "/dashboard/courses",
  compliance: "/dashboard/compliance",
  timetable: "/dashboard/timetable",
  mentor: "/dashboard/mentor",
};

export default function DashboardPage() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    dashboardService
      .getSummary()
      .then(setSummary)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="space-y-6">
        <div>
          <Skeleton className="h-9 w-48 mb-2" />
          <Skeleton className="h-4 w-72" />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {[1, 2, 3, 4].map((i) => (
            <Skeleton key={i} className="h-32 rounded-xl" />
          ))}
        </div>
        <Skeleton className="h-64 rounded-xl" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="space-y-6">
        <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
        <div className="glass-card p-6 border-red-200 dark:border-red-800">
          <p className="text-red-600 dark:text-red-400">{error}</p>
          <Button
            variant="outline"
            size="sm"
            className="mt-3"
            onClick={() => window.location.reload()}
          >
            Try again
          </Button>
        </div>
      </div>
    );
  }

  if (!summary) return null;

  const checklist = summary.checklist;
  const docSubtitle = (() => {
    const parts: string[] = [];
    if (summary.documents.pending > 0)
      parts.push(`${summary.documents.pending} pending`);
    if (summary.documents.under_review > 0)
      parts.push(`${summary.documents.under_review} under review`);
    if (summary.documents.rejected > 0)
      parts.push(`${summary.documents.rejected} rejected`);
    if (parts.length === 0) {
      return summary.documents.total > 0 ? "All reviewed" : "No documents yet";
    }
    return parts.join(", ");
  })();

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold tracking-tight">
          Welcome back, {summary.user.name}
        </h1>
        <p className="text-muted-foreground">
          Track your onboarding progress and manage your tasks.
        </p>
      </div>

      {/* Onboarding Progress */}
      <div className="glass-card p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold">Onboarding Progress</h2>
          <span className="text-2xl font-bold gradient-text">
            {summary.onboarding_percentage}%
          </span>
        </div>
        <Progress value={summary.onboarding_percentage} className="h-3" />
        <p className="text-sm text-muted-foreground mt-2">
          {summary.onboarding_percentage === 100
            ? "All onboarding steps completed! You're all set."
            : `${100 - summary.onboarding_percentage}% remaining — keep going!`}
        </p>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Documents"
          value={`${summary.documents.approved}/${summary.documents.total}`}
          subtitle={docSubtitle}
          icon={FileText}
          href="/dashboard/documents"
          color="bg-blue-500"
        />
        <StatCard
          title="Payments"
          value={`₹${summary.payments.total_paid.toLocaleString()}`}
          subtitle={
            summary.payments.total_pending > 0
              ? `₹${summary.payments.total_pending.toLocaleString()} pending`
              : summary.payments.count > 0
                ? "All paid"
                : "No payments yet"
          }
          icon={CreditCard}
          href="/dashboard/payments"
          color="bg-emerald-500"
        />
        <StatCard
          title="Hostel"
          value={
            summary.hostel.status === "not_applied"
              ? "Not Applied"
              : summary.hostel.status.charAt(0).toUpperCase() +
                summary.hostel.status.slice(1)
          }
          subtitle={
            summary.hostel.room_number
              ? `Room ${summary.hostel.room_number}`
              : summary.hostel.room_type || "Apply now"
          }
          icon={Building2}
          href="/dashboard/hostel"
          color="bg-purple-500"
        />
        <StatCard
          title="LMS"
          value={summary.lms.status === "activated" ? "Active" : "Inactive"}
          subtitle={
            summary.lms.lms_id
              ? `ID: ${summary.lms.lms_id}`
              : summary.lms.platform || "Activate now"
          }
          icon={BookOpen}
          href="/dashboard/lms"
          color="bg-orange-500"
        />
      </div>

      {/* Dynamic Checklist (computed from DB state) */}
      {checklist && checklist.items.length > 0 && (
        <div className="glass-card p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold">Onboarding Checklist</h2>
            <span className="text-sm text-muted-foreground">
              {checklist.completed}/{checklist.total} completed
            </span>
          </div>
          <div className="space-y-3">
            {checklist.items
              .sort((a, b) => a.order - b.order)
              .map((item) => (
                <Link
                  key={item.id}
                  href={CATEGORY_LINKS[item.category] || "/dashboard"}
                  className="flex items-center gap-3 p-3 rounded-lg hover:bg-muted/50 transition-colors"
                >
                  <div
                    className={`flex-shrink-0 h-5 w-5 rounded-full border-2 flex items-center justify-center transition-colors ${
                      item.is_completed
                        ? "bg-green-500 border-green-500"
                        : "border-muted-foreground/50"
                    }`}
                  >
                    {item.is_completed && (
                      <CheckCircle2 className="h-3.5 w-3.5 text-white" />
                    )}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p
                      className={`text-sm font-medium ${
                        item.is_completed
                          ? "line-through text-muted-foreground"
                          : ""
                      }`}
                    >
                      {item.title}
                    </p>
                    {item.description && (
                      <p className="text-xs text-muted-foreground truncate">
                        {item.description}
                      </p>
                    )}
                  </div>
                  {item.is_required && !item.is_completed && (
                    <span className="text-xs bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400 px-2 py-0.5 rounded-full">
                      Required
                    </span>
                  )}
                  <ChecklistStatusIcon completed={item.is_completed} />
                </Link>
              ))}
          </div>
        </div>
      )}
    </div>
  );
}
