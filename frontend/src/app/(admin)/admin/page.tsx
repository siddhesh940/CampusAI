"use client";

import { Progress } from "@/components/ui/progress";
import { Skeleton } from "@/components/ui/skeleton";
import {
    adminService,
    type AdminAnalyticsResponse,
} from "@/services/campus-services";
import {
    Building2,
    CheckCircle2,
    FileCheck,
    IndianRupee,
    TrendingUp,
    Users,
} from "lucide-react";
import { useEffect, useState } from "react";

function StatCard({
  title,
  value,
  icon: Icon,
  color,
}: {
  title: string;
  value: string | number;
  icon: React.ElementType;
  color: string;
}) {
  return (
    <div className="glass-card p-5">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-muted-foreground">{title}</p>
          <p className="text-2xl font-bold mt-1">{value}</p>
        </div>
        <div className={`p-2.5 rounded-xl ${color}`}>
          <Icon className="h-5 w-5 text-white" />
        </div>
      </div>
    </div>
  );
}

export default function AdminDashboardPage() {
  const [analytics, setAnalytics] = useState<AdminAnalyticsResponse | null>(
    null,
  );
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    adminService
      .getAnalytics()
      .then(setAnalytics)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-9 w-48" />
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {[1, 2, 3, 4].map((i) => (
            <Skeleton key={i} className="h-28 rounded-xl" />
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="space-y-6">
        <h1 className="text-3xl font-bold tracking-tight">Admin Dashboard</h1>
        <div className="glass-card p-6 border-red-200 dark:border-red-800">
          <p className="text-red-600 dark:text-red-400">{error}</p>
        </div>
      </div>
    );
  }

  if (!analytics) return null;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Admin Dashboard</h1>
        <p className="text-muted-foreground">
          Overview of your college&apos;s onboarding metrics.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Total Students"
          value={analytics.total_students}
          icon={Users}
          color="bg-blue-500"
        />
        <StatCard
          title="Onboarding Complete"
          value={analytics.onboarding_completed}
          icon={CheckCircle2}
          color="bg-green-500"
        />
        <StatCard
          title="Pending Documents"
          value={analytics.pending_documents}
          icon={FileCheck}
          color="bg-yellow-500"
        />
        <StatCard
          title="Total Revenue"
          value={`₹${analytics.total_revenue?.toLocaleString() || 0}`}
          icon={IndianRupee}
          color="bg-emerald-500"
        />
      </div>

      {/* Completion Rate */}
      <div className="glass-card p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold flex items-center gap-2">
            <TrendingUp className="h-5 w-5" />
            Onboarding Completion Rate
          </h2>
          <span className="text-2xl font-bold gradient-text">
            {Math.round(analytics.completion_rate || 0)}%
          </span>
        </div>
        <Progress value={analytics.completion_rate || 0} className="h-3" />
        <p className="text-sm text-muted-foreground mt-2">
          {analytics.onboarding_completed} of {analytics.total_students}{" "}
          students have completed onboarding.
        </p>
      </div>

      {/* Quick Links */}
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4">
        <a
          href="/admin/documents"
          className="glass-card p-5 hover:shadow-lg transition-shadow"
        >
          <FileCheck className="h-8 w-8 text-blue-500 mb-2" />
          <h3 className="font-semibold">Document Review</h3>
          <p className="text-sm text-muted-foreground">
            {analytics.pending_documents} documents awaiting review
          </p>
        </a>
        <a
          href="/admin/students"
          className="glass-card p-5 hover:shadow-lg transition-shadow"
        >
          <Users className="h-8 w-8 text-purple-500 mb-2" />
          <h3 className="font-semibold">Student Management</h3>
          <p className="text-sm text-muted-foreground">
            View and manage {analytics.total_students} students
          </p>
        </a>
        <a
          href="/admin/hostel"
          className="glass-card p-5 hover:shadow-lg transition-shadow"
        >
          <Building2 className="h-8 w-8 text-orange-500 mb-2" />
          <h3 className="font-semibold">Hostel Allocation</h3>
          <p className="text-sm text-muted-foreground">
            {analytics.pending_hostel} pending applications
          </p>
        </a>
        <a
          href="/admin/courses"
          className="glass-card p-5 hover:shadow-lg transition-shadow"
        >
          <CheckCircle2 className="h-8 w-8 text-indigo-500 mb-2" />
          <h3 className="font-semibold">Course Management</h3>
          <p className="text-sm text-muted-foreground">
            Create courses &amp; manage subjects
          </p>
        </a>
        <a
          href="/admin/timetable"
          className="glass-card p-5 hover:shadow-lg transition-shadow"
        >
          <TrendingUp className="h-8 w-8 text-cyan-500 mb-2" />
          <h3 className="font-semibold">Timetable</h3>
          <p className="text-sm text-muted-foreground">
            Set subject schedules for students
          </p>
        </a>
        <a
          href="/admin/mentors"
          className="glass-card p-5 hover:shadow-lg transition-shadow"
        >
          <Users className="h-8 w-8 text-teal-500 mb-2" />
          <h3 className="font-semibold">Mentor Assignments</h3>
          <p className="text-sm text-muted-foreground">
            Assign mentors to students
          </p>
        </a>
        <a
          href="/admin/compliance"
          className="glass-card p-5 hover:shadow-lg transition-shadow"
        >
          <FileCheck className="h-8 w-8 text-rose-500 mb-2" />
          <h3 className="font-semibold">Compliance Training</h3>
          <p className="text-sm text-muted-foreground">
            Manage declarations &amp; training items
          </p>
        </a>
        <a
          href="/admin/lms"
          className="glass-card p-5 hover:shadow-lg transition-shadow"
        >
          <CheckCircle2 className="h-8 w-8 text-amber-500 mb-2" />
          <h3 className="font-semibold">LMS Management</h3>
          <p className="text-sm text-muted-foreground">
            Generate LMS credentials for students
          </p>
        </a>
      </div>
    </div>
  );
}
