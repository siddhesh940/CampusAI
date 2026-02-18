"use client";

import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { apiClient } from "@/services/api-client";
import { hostelService } from "@/services/campus-services";
import {
    Building2,
    Home,
    Loader2
} from "lucide-react";
import { useEffect, useState } from "react";

interface HostelApp {
  id: string;
  user_id: string;
  room_type: string;
  status: string;
  preferences?: string;
  allocated_room?: string;
  created_at: string;
}

function StatusBadge({ status }: { status: string }) {
  const cfg: Record<string, { bg: string; text: string }> = {
    approved: {
      bg: "bg-green-100 dark:bg-green-900/30",
      text: "text-green-700 dark:text-green-400",
    },
    pending: {
      bg: "bg-yellow-100 dark:bg-yellow-900/30",
      text: "text-yellow-700 dark:text-yellow-400",
    },
    rejected: {
      bg: "bg-red-100 dark:bg-red-900/30",
      text: "text-red-700 dark:text-red-400",
    },
    waitlisted: {
      bg: "bg-blue-100 dark:bg-blue-900/30",
      text: "text-blue-700 dark:text-blue-400",
    },
  };
  const c = cfg[status] || cfg.pending;
  return (
    <span
      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${c.bg} ${c.text}`}
    >
      {status.charAt(0).toUpperCase() + status.slice(1)}
    </span>
  );
}

export default function AdminHostelPage() {
  const [applications, setApplications] = useState<HostelApp[]>([]);
  const [loading, setLoading] = useState(true);
  const [allocatingId, setAllocatingId] = useState<string | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    apiClient
      .get<{ applications: HostelApp[]; total: number }>(
        "/api/v1/admin/hostel/applications",
      )
      .then((res) => setApplications(res.applications || []))
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  const handleAllocate = async (appId: string) => {
    const room = prompt("Enter room number:");
    if (!room) return;
    const block = prompt("Enter block (e.g. A, B):") || "";
    setAllocatingId(appId);
    try {
      await hostelService.allocate(appId, {
        status: "approved",
        allocated_room_number: room,
        allocated_block: block,
      });
      // Refresh
      const res = await apiClient.get<{
        applications: HostelApp[];
        total: number;
      }>("/api/v1/admin/hostel/applications");
      setApplications(res.applications || []);
    } catch {
      // silent
    } finally {
      setAllocatingId(null);
    }
  };

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
        <h1 className="text-3xl font-bold tracking-tight">Hostel Allocation</h1>
        <p className="text-muted-foreground">
          Manage hostel applications and room allocations.
        </p>
      </div>

      {error && (
        <div className="glass-card p-4 border-red-200 dark:border-red-800">
          <p className="text-red-600 dark:text-red-400 text-sm">{error}</p>
        </div>
      )}

      <div className="glass-card p-6">
        {applications.length === 0 ? (
          <div className="text-center py-12">
            <Building2 className="h-12 w-12 mx-auto text-muted-foreground/50 mb-3" />
            <p className="text-muted-foreground">No hostel applications.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b">
                  <th className="text-left py-3 px-2 font-medium text-muted-foreground">
                    Student ID
                  </th>
                  <th className="text-left py-3 px-2 font-medium text-muted-foreground">
                    Room Type
                  </th>
                  <th className="text-left py-3 px-2 font-medium text-muted-foreground">
                    Preferences
                  </th>
                  <th className="text-left py-3 px-2 font-medium text-muted-foreground">
                    Status
                  </th>
                  <th className="text-left py-3 px-2 font-medium text-muted-foreground">
                    Room
                  </th>
                  <th className="text-left py-3 px-2 font-medium text-muted-foreground">
                    Applied
                  </th>
                  <th className="text-left py-3 px-2 font-medium text-muted-foreground">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody>
                {applications.map((app) => (
                  <tr
                    key={app.id}
                    className="border-b last:border-0 hover:bg-muted/50 transition-colors"
                  >
                    <td className="py-3 px-2 font-mono text-xs">
                      {app.user_id.slice(0, 8)}...
                    </td>
                    <td className="py-3 px-2 capitalize">{app.room_type}</td>
                    <td className="py-3 px-2 text-muted-foreground truncate max-w-[150px]">
                      {app.preferences || "—"}
                    </td>
                    <td className="py-3 px-2">
                      <StatusBadge status={app.status} />
                    </td>
                    <td className="py-3 px-2">
                      {app.allocated_room ? (
                        <span className="flex items-center gap-1 font-medium">
                          <Home className="h-3.5 w-3.5" />
                          {app.allocated_room}
                        </span>
                      ) : (
                        "—"
                      )}
                    </td>
                    <td className="py-3 px-2 text-muted-foreground">
                      {new Date(app.created_at).toLocaleDateString()}
                    </td>
                    <td className="py-3 px-2">
                      {app.status === "pending" && (
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleAllocate(app.id)}
                          disabled={allocatingId === app.id}
                        >
                          {allocatingId === app.id ? (
                            <Loader2 className="h-3 w-3 animate-spin" />
                          ) : (
                            <>
                              <Home className="h-3 w-3 mr-1" /> Allocate
                            </>
                          )}
                        </Button>
                      )}
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
