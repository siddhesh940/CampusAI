"use client";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import { hostelService } from "@/services/campus-services";
import { demoHostelStatus, withDemoFallback } from "@/services/demo-data";
import type { HostelApplication } from "@/types";
import {
    BedDouble,
    Building2,
    CheckCircle2,
    Clock,
    Home,
    Loader2,
    MapPin,
    XCircle,
} from "lucide-react";
import { useEffect, useState } from "react";

const ROOM_TYPES = [
  {
    value: "single",
    label: "Single Room",
    desc: "Private room for one student",
  },
  {
    value: "double",
    label: "Double Sharing",
    desc: "Room shared between two students",
  },
  {
    value: "triple",
    label: "Triple Sharing",
    desc: "Room shared between three students",
  },
];

function StatusBadge({ status }: { status: string }) {
  const cfg: Record<
    string,
    { bg: string; text: string; icon: React.ElementType; label: string }
  > = {
    approved: {
      bg: "bg-green-100 dark:bg-green-900/30",
      text: "text-green-700 dark:text-green-400",
      icon: CheckCircle2,
      label: "Approved",
    },
    pending: {
      bg: "bg-yellow-100 dark:bg-yellow-900/30",
      text: "text-yellow-700 dark:text-yellow-400",
      icon: Clock,
      label: "Pending",
    },
    rejected: {
      bg: "bg-red-100 dark:bg-red-900/30",
      text: "text-red-700 dark:text-red-400",
      icon: XCircle,
      label: "Rejected",
    },
    waitlisted: {
      bg: "bg-blue-100 dark:bg-blue-900/30",
      text: "text-blue-700 dark:text-blue-400",
      icon: Clock,
      label: "Waitlisted",
    },
  };
  const c = cfg[status] || cfg.pending;
  const Icon = c.icon;
  return (
    <span
      className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-sm font-medium ${c.bg} ${c.text}`}
    >
      <Icon className="h-4 w-4" />
      {c.label}
    </span>
  );
}

export default function HostelPage() {
  const [application, setApplication] = useState<HostelApplication | null>(
    null,
  );
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [notApplied, setNotApplied] = useState(false);
  const [error, setError] = useState("");
  const [formError, setFormError] = useState("");

  const [roomType, setRoomType] = useState(ROOM_TYPES[0].value);
  const [specialReq, setSpecialReq] = useState("");

  useEffect(() => {
    withDemoFallback(() => hostelService.getStatus(), demoHostelStatus as any)
      .then((res) => {
        if (res.status === "not_applied") setNotApplied(true);
        else setApplication(res);
      })
      .catch((e) => {
        if (
          e.message?.includes("404") ||
          e.message?.includes("not found") ||
          e.message?.includes("No hostel")
        ) {
          setNotApplied(true);
        } else {
          setError(e.message);
        }
      })
      .finally(() => setLoading(false));
  }, []);

  const handleApply = async () => {
    setSubmitting(true);
    setFormError("");
    try {
      const app = await hostelService.apply({
        room_type_preference: roomType,
        special_requirements: specialReq || undefined,
      });
      setApplication(app);
      setNotApplied(false);
    } catch (e: any) {
      setFormError(e.message);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-9 w-32" />
        <Skeleton className="h-64 rounded-xl" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Hostel</h1>
        <p className="text-muted-foreground">
          Apply for hostel accommodation and track your application.
        </p>
      </div>

      {error && (
        <div className="glass-card p-4 border-red-200 dark:border-red-800">
          <p className="text-red-600 dark:text-red-400 text-sm">{error}</p>
        </div>
      )}

      {/* Application Form */}
      {notApplied && !application && (
        <div className="glass-card p-6">
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Building2 className="h-5 w-5" />
            Apply for Hostel
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
            {ROOM_TYPES.map((rt) => (
              <div
                key={rt.value}
                onClick={() => setRoomType(rt.value)}
                className={`p-4 rounded-xl border-2 cursor-pointer transition-all ${
                  roomType === rt.value
                    ? "border-primary bg-primary/5"
                    : "border-muted hover:border-muted-foreground/30"
                }`}
              >
                <div className="flex items-center gap-2 mb-2">
                  <BedDouble className="h-5 w-5" />
                  <span className="font-medium">{rt.label}</span>
                </div>
                <p className="text-xs text-muted-foreground">{rt.desc}</p>
              </div>
            ))}
          </div>
          <div className="mb-4">
            <label className="text-sm font-medium mb-1.5 block">
              Special Requirements (optional)
            </label>
            <Input
              placeholder="e.g., ground floor, near library..."
              value={specialReq}
              onChange={(e) => setSpecialReq(e.target.value)}
            />
          </div>
          <Button
            onClick={handleApply}
            disabled={submitting}
            variant="gradient"
          >
            {submitting ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin mr-2" /> Submitting...
              </>
            ) : (
              <>
                <Building2 className="h-4 w-4 mr-2" /> Submit Application
              </>
            )}
          </Button>
          {formError && (
            <p className="text-sm text-red-500 mt-2">{formError}</p>
          )}
        </div>
      )}

      {/* Application Status */}
      {application && (
        <div className="glass-card p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-semibold">Application Status</h2>
            <StatusBadge status={application.status} />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-4">
              <div className="flex items-center gap-3 p-3 rounded-lg bg-muted/50">
                <BedDouble className="h-5 w-5 text-muted-foreground" />
                <div>
                  <p className="text-xs text-muted-foreground">
                    Room Type Preference
                  </p>
                  <p className="font-medium capitalize">
                    {(application.room_type || "").replace(/_/g, " ")}
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-3 p-3 rounded-lg bg-muted/50">
                <Clock className="h-5 w-5 text-muted-foreground" />
                <div>
                  <p className="text-xs text-muted-foreground">Applied On</p>
                  <p className="font-medium">
                    {new Date(application.created_at).toLocaleDateString(
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
              {application.preferences && (
                <div className="flex items-start gap-3 p-3 rounded-lg bg-muted/50">
                  <MapPin className="h-5 w-5 text-muted-foreground mt-0.5" />
                  <div>
                    <p className="text-xs text-muted-foreground">
                      Special Requirements
                    </p>
                    <p className="font-medium">{application.preferences}</p>
                  </div>
                </div>
              )}
            </div>

            {application.status === "approved" &&
              application.allocated_room && (
                <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-xl p-5">
                  <h3 className="font-semibold text-green-700 dark:text-green-400 mb-3 flex items-center gap-2">
                    <Home className="h-5 w-5" />
                    Room Allocation
                  </h3>
                  <div className="space-y-2">
                    <p className="text-sm">
                      <span className="text-muted-foreground">Room No:</span>{" "}
                      <span className="font-bold text-lg">
                        {application.allocated_room}
                      </span>
                    </p>
                  </div>
                </div>
              )}

            {application.status === "pending" && (
              <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-xl p-5 flex items-center gap-3">
                <Clock className="h-8 w-8 text-yellow-600 dark:text-yellow-400" />
                <div>
                  <p className="font-medium">Application Under Review</p>
                  <p className="text-sm text-muted-foreground">
                    Your application is being reviewed by the hostel
                    administration. You will be notified once a decision is
                    made.
                  </p>
                </div>
              </div>
            )}

            {application.status === "rejected" && (
              <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl p-5 flex items-center gap-3">
                <XCircle className="h-8 w-8 text-red-600 dark:text-red-400" />
                <div>
                  <p className="font-medium">Application Rejected</p>
                  <p className="text-sm text-muted-foreground">
                    Unfortunately, your hostel application has been rejected.
                    Please contact the administration for more details.
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
