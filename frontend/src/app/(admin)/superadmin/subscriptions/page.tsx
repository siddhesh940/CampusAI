"use client";

import { Skeleton } from "@/components/ui/skeleton";
import { apiClient } from "@/services/api-client";
import type { SubscriptionPlan } from "@/types";
import { CheckCircle2, CreditCard, Users } from "lucide-react";
import { useEffect, useState } from "react";

export default function SuperAdminSubscriptionsPage() {
  const [plans, setPlans] = useState<SubscriptionPlan[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    apiClient
      .get<{ plans: SubscriptionPlan[] }>("/api/v1/superadmin/plans")
      .then((res) => setPlans(res.plans || []))
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-9 w-48" />
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-48 rounded-xl" />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Subscriptions</h1>
        <p className="text-muted-foreground">
          Manage subscription plans and billing.
        </p>
      </div>

      {error && (
        <div className="glass-card p-4 border-red-200 dark:border-red-800">
          <p className="text-red-600 dark:text-red-400 text-sm">{error}</p>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {plans.map((plan) => (
          <div key={plan.id} className="glass-card p-6 flex flex-col">
            <div className="flex items-center gap-2 mb-3">
              <CreditCard className="h-5 w-5 text-primary" />
              <h3 className="font-bold text-lg">{plan.name}</h3>
            </div>
            <p className="text-3xl font-bold mb-1">
              \u20B9{plan.price_monthly.toLocaleString()}
              <span className="text-sm font-normal text-muted-foreground">
                /mo
              </span>
            </p>
            <div className="flex items-center gap-1.5 text-sm text-muted-foreground mb-4">
              <Users className="h-4 w-4" />
              Up to {plan.max_students.toLocaleString()} students
            </div>
            <div className="flex-1 space-y-2">
              {Object.entries(plan.features || {}).map(([key, enabled]) => (
                <div key={key} className="flex items-center gap-2 text-sm">
                  <CheckCircle2
                    className={`h-4 w-4 ${enabled ? "text-green-500" : "text-muted-foreground/30"}`}
                  />
                  <span
                    className={
                      enabled ? "" : "text-muted-foreground line-through"
                    }
                  >
                    {key
                      .replace(/_/g, " ")
                      .replace(/\b\w/g, (l) => l.toUpperCase())}
                  </span>
                </div>
              ))}
            </div>
            <div
              className={`mt-4 text-center py-1.5 rounded-full text-xs font-medium ${
                plan.is_active
                  ? "bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400"
                  : "bg-gray-100 dark:bg-gray-800 text-gray-600"
              }`}
            >
              {plan.is_active ? "Active" : "Inactive"}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
