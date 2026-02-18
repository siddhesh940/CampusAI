"use client";

import { Skeleton } from "@/components/ui/skeleton";
import { apiClient } from "@/services/api-client";
import { Building, IndianRupee, TrendingUp, Users } from "lucide-react";
import { useEffect, useState } from "react";

interface PlatformStats {
  total_universities: number;
  total_students: number;
  total_revenue: number;
  active_plans: number;
}

export default function SuperAdminDashboardPage() {
  const [stats, setStats] = useState<PlatformStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiClient
      .get<PlatformStats>("/api/v1/superadmin/dashboard")
      .then(setStats)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-9 w-48" />
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-28 rounded-xl" />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Platform Overview</h1>
        <p className="text-muted-foreground">
          Manage engineering colleges and monitor platform health.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="glass-card p-5">
          <div className="flex items-start justify-between">
            <div>
              <p className="text-sm font-medium text-muted-foreground">
                Colleges
              </p>
              <p className="text-2xl font-bold mt-1">
                {stats?.total_universities || 0}
              </p>
            </div>
            <div className="p-2.5 rounded-xl bg-blue-500">
              <Building className="h-5 w-5 text-white" />
            </div>
          </div>
        </div>
        <div className="glass-card p-5">
          <div className="flex items-start justify-between">
            <div>
              <p className="text-sm font-medium text-muted-foreground">
                Total Students
              </p>
              <p className="text-2xl font-bold mt-1">
                {stats?.total_students || 0}
              </p>
            </div>
            <div className="p-2.5 rounded-xl bg-purple-500">
              <Users className="h-5 w-5 text-white" />
            </div>
          </div>
        </div>
        <div className="glass-card p-5">
          <div className="flex items-start justify-between">
            <div>
              <p className="text-sm font-medium text-muted-foreground">
                Revenue (MRR)
              </p>
              <p className="text-2xl font-bold mt-1 flex items-center gap-1">
                <IndianRupee className="h-5 w-5" />
                {(stats?.total_revenue || 0).toLocaleString()}
              </p>
            </div>
            <div className="p-2.5 rounded-xl bg-emerald-500">
              <TrendingUp className="h-5 w-5 text-white" />
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <a
          href="/superadmin/universities"
          className="glass-card p-5 hover:shadow-lg transition-shadow"
        >
          <Building className="h-8 w-8 text-blue-500 mb-2" />
          <h3 className="font-semibold">Manage Universities</h3>
          <p className="text-sm text-muted-foreground">
            Add, edit, or deactivate colleges
          </p>
        </a>
        <a
          href="/superadmin/subscriptions"
          className="glass-card p-5 hover:shadow-lg transition-shadow"
        >
          <IndianRupee className="h-8 w-8 text-emerald-500 mb-2" />
          <h3 className="font-semibold">Subscription Plans</h3>
          <p className="text-sm text-muted-foreground">
            Manage pricing and features
          </p>
        </a>
      </div>
    </div>
  );
}
