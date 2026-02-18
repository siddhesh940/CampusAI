"use client";

import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import {
    complianceService,
    type ComplianceStatus,
} from "@/services/campus-services";
import { demoComplianceStatus, withDemoFallback } from "@/services/demo-data";
import {
    CheckCircle2,
    Circle,
    ExternalLink,
    FileCheck,
    Loader2,
    PlayCircle,
    ShieldCheck,
} from "lucide-react";
import { useEffect, useState } from "react";

export default function CompliancePage() {
  const [items, setItems] = useState<ComplianceStatus[]>([]);
  const [stats, setStats] = useState({
    total: 0,
    completed: 0,
    required_total: 0,
    required_completed: 0,
    all_required_done: false,
  });
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState<string | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    loadCompliance();
  }, []);

  const loadCompliance = async () => {
    try {
      const res = await withDemoFallback(
        () => complianceService.getStatus(),
        demoComplianceStatus as any,
      );
      setItems(res.items);
      setStats({
        total: res.total,
        completed: res.completed,
        required_total: res.required_total,
        required_completed: res.required_completed,
        all_required_done: res.all_required_done,
      });
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (itemId: string) => {
    setSubmitting(itemId);
    setError("");
    try {
      await complianceService.submit(itemId);
      await loadCompliance();
    } catch (e: any) {
      setError(e.message);
    } finally {
      setSubmitting(null);
    }
  };

  const getIcon = (type: string) => {
    switch (type) {
      case "declaration":
        return ShieldCheck;
      case "video":
        return PlayCircle;
      case "document":
        return FileCheck;
      default:
        return ShieldCheck;
    }
  };

  const getTypeLabel = (type: string) => {
    switch (type) {
      case "declaration":
        return "Declaration";
      case "video":
        return "Video";
      case "document":
        return "Document";
      case "acknowledgement":
        return "Acknowledgement";
      default:
        return type;
    }
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-9 w-56" />
        <div className="grid gap-4">
          {[1, 2, 3, 4].map((i) => (
            <Skeleton key={i} className="h-24 w-full" />
          ))}
        </div>
      </div>
    );
  }

  const progressPercent =
    stats.required_total > 0
      ? Math.round((stats.required_completed / stats.required_total) * 100)
      : 0;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold">Compliance Training</h1>
        <p className="text-muted-foreground mt-1">
          Complete all required compliance items to proceed with onboarding
        </p>
      </div>

      {/* Progress Card */}
      <div className="glass-card p-6">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <ShieldCheck className="h-5 w-5 text-primary" />
            <span className="font-semibold">Compliance Progress</span>
          </div>
          <span className="text-sm font-medium">
            {stats.required_completed}/{stats.required_total} Required
          </span>
        </div>
        <div className="w-full bg-muted rounded-full h-3">
          <div
            className={`bg-primary h-3 rounded-full transition-all duration-500 w-[${progressPercent}%]`}
          />
        </div>
        <div className="flex items-center justify-between mt-2">
          <span className="text-sm text-muted-foreground">
            {stats.completed} of {stats.total} total items completed
          </span>
          {stats.all_required_done && (
            <span className="flex items-center gap-1 text-sm text-green-600 font-medium">
              <CheckCircle2 className="h-4 w-4" />
              All required items done!
            </span>
          )}
        </div>
      </div>

      {error && (
        <div className="bg-red-50 text-red-600 p-4 rounded-lg text-sm">
          {error}
        </div>
      )}

      {/* Compliance Items */}
      <div className="space-y-3">
        {items.map((item) => {
          const Icon = getIcon(item.item_type || "declaration");
          const isProcessing = submitting === item.compliance_item_id;

          return (
            <div
              key={item.id}
              className={`glass-card p-5 transition-all ${
                item.is_completed ? "border-green-200 bg-green-50/30" : ""
              }`}
            >
              <div className="flex items-start gap-4">
                {/* Status icon */}
                <div
                  className={`mt-0.5 flex-shrink-0 ${item.is_completed ? "text-green-600" : "text-muted-foreground"}`}
                >
                  {item.is_completed ? (
                    <CheckCircle2 className="h-6 w-6" />
                  ) : (
                    <Circle className="h-6 w-6" />
                  )}
                </div>

                {/* Content */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <h3 className="font-semibold">{item.item_title}</h3>
                    {item.is_required && (
                      <span className="text-xs bg-red-100 text-red-700 px-2 py-0.5 rounded-full">
                        Required
                      </span>
                    )}
                    <span className="text-xs bg-muted px-2 py-0.5 rounded-full">
                      {getTypeLabel(item.item_type || "")}
                    </span>
                  </div>
                  {item.item_description && (
                    <p className="text-sm text-muted-foreground mt-1">
                      {item.item_description}
                    </p>
                  )}
                  {item.content_url && !item.is_completed && (
                    <a
                      href={item.content_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 text-sm text-primary hover:underline mt-2"
                    >
                      <ExternalLink className="h-3.5 w-3.5" />
                      View Content
                    </a>
                  )}
                  {item.is_completed && item.completed_at && (
                    <p className="text-xs text-green-600 mt-1">
                      Completed on{" "}
                      {new Date(item.completed_at).toLocaleDateString()}
                    </p>
                  )}
                </div>

                {/* Action */}
                <div className="flex-shrink-0">
                  {item.is_completed ? (
                    <span className="text-sm text-green-600 font-medium">
                      Done
                    </span>
                  ) : (
                    <Button
                      size="sm"
                      onClick={() => handleSubmit(item.compliance_item_id)}
                      disabled={isProcessing}
                    >
                      {isProcessing ? (
                        <Loader2 className="h-4 w-4 animate-spin mr-1" />
                      ) : (
                        <Icon className="h-4 w-4 mr-1" />
                      )}
                      {item.item_type === "declaration"
                        ? "I Agree"
                        : item.item_type === "video"
                          ? "Mark Watched"
                          : "Acknowledge"}
                    </Button>
                  )}
                </div>
              </div>
            </div>
          );
        })}

        {items.length === 0 && (
          <div className="text-center py-12 text-muted-foreground">
            <ShieldCheck className="h-12 w-12 mx-auto mb-3 opacity-40" />
            <p>No compliance items configured yet.</p>
          </div>
        )}
      </div>
    </div>
  );
}
