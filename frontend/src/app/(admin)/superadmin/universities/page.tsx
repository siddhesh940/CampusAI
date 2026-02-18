"use client";

import { Skeleton } from "@/components/ui/skeleton";
import { apiClient } from "@/services/api-client";
import type { University } from "@/types";
import { Building, CheckCircle2, Globe, XCircle } from "lucide-react";
import { useEffect, useState } from "react";

export default function SuperAdminCollegesPage() {
  const [universities, setUniversities] = useState<University[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    apiClient
      .get<{ universities: University[]; total: number }>(
        "/api/v1/superadmin/universities",
      )
      .then((res) => setUniversities(res.universities || []))
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-9 w-48" />
        <Skeleton className="h-64 rounded-xl" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">
          Engineering Colleges
        </h1>
        <p className="text-muted-foreground">
          Manage all registered engineering colleges on the platform.
        </p>
      </div>

      {error && (
        <div className="glass-card p-4 border-red-200 dark:border-red-800">
          <p className="text-red-600 dark:text-red-400 text-sm">{error}</p>
        </div>
      )}

      <div className="glass-card p-6">
        {universities.length === 0 ? (
          <div className="text-center py-12">
            <Building className="h-12 w-12 mx-auto text-muted-foreground/50 mb-3" />
            <p className="text-muted-foreground">
              No universities registered yet.
            </p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b">
                  <th className="text-left py-3 px-2 font-medium text-muted-foreground">
                    Name
                  </th>
                  <th className="text-left py-3 px-2 font-medium text-muted-foreground">
                    Slug
                  </th>
                  <th className="text-left py-3 px-2 font-medium text-muted-foreground">
                    Domain
                  </th>
                  <th className="text-left py-3 px-2 font-medium text-muted-foreground">
                    Status
                  </th>
                  <th className="text-left py-3 px-2 font-medium text-muted-foreground">
                    Created
                  </th>
                </tr>
              </thead>
              <tbody>
                {universities.map((u) => (
                  <tr
                    key={u.id}
                    className="border-b last:border-0 hover:bg-muted/50 transition-colors"
                  >
                    <td className="py-3 px-2 font-medium">
                      <div className="flex items-center gap-2">
                        {u.logo_url ? (
                          <img
                            src={u.logo_url}
                            alt=""
                            className="h-6 w-6 rounded"
                          />
                        ) : (
                          <Building className="h-4 w-4 text-muted-foreground" />
                        )}
                        {u.name}
                      </div>
                    </td>
                    <td className="py-3 px-2 font-mono text-xs text-muted-foreground">
                      {u.slug}
                    </td>
                    <td className="py-3 px-2">
                      {u.domain ? (
                        <span className="flex items-center gap-1 text-muted-foreground">
                          <Globe className="h-3.5 w-3.5" />
                          {u.domain}
                        </span>
                      ) : (
                        "—"
                      )}
                    </td>
                    <td className="py-3 px-2">
                      {u.is_active ? (
                        <span className="inline-flex items-center gap-1 text-xs text-green-600 dark:text-green-400">
                          <CheckCircle2 className="h-3 w-3" /> Active
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1 text-xs text-red-500">
                          <XCircle className="h-3 w-3" /> Inactive
                        </span>
                      )}
                    </td>
                    <td className="py-3 px-2 text-muted-foreground">
                      {new Date(u.created_at).toLocaleDateString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
