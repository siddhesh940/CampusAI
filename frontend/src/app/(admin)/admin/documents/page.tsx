"use client";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import { adminService, documentService } from "@/services/campus-services";
import type { Document } from "@/types";
import {
    AlertTriangle,
    CheckCircle2,
    Clock,
    Eye,
    FileSearch,
    FileText,
    Filter,
    Loader2,
    Search,
    XCircle,
} from "lucide-react";
import { useCallback, useEffect, useState } from "react";

const STATUS_TABS = [
  { value: "all", label: "All", icon: FileText },
  { value: "pending", label: "Pending", icon: Clock },
  { value: "under_review", label: "Under Review", icon: FileSearch },
  { value: "approved", label: "Approved", icon: CheckCircle2 },
  { value: "rejected", label: "Rejected", icon: XCircle },
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
    under_review: {
      bg: "bg-blue-100 dark:bg-blue-900/30",
      text: "text-blue-700 dark:text-blue-400",
      icon: FileSearch,
      label: "Under Review",
    },
    rejected: {
      bg: "bg-red-100 dark:bg-red-900/30",
      text: "text-red-700 dark:text-red-400",
      icon: XCircle,
      label: "Rejected",
    },
  };
  const c = cfg[status] || cfg.pending;
  const Icon = c.icon;
  return (
    <span
      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${c.bg} ${c.text}`}
    >
      <Icon className="h-3 w-3" />
      {c.label}
    </span>
  );
}

function RejectModal({
  open,
  onClose,
  onConfirm,
  loading,
}: {
  open: boolean;
  onClose: () => void;
  onConfirm: (reason: string) => void;
  loading: boolean;
}) {
  const [reason, setReason] = useState("");

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
      <div className="bg-background border rounded-xl shadow-2xl w-full max-w-md mx-4 p-6">
        <div className="flex items-center gap-3 mb-4">
          <div className="p-2 rounded-full bg-red-100 dark:bg-red-900/30">
            <AlertTriangle className="h-5 w-5 text-red-600" />
          </div>
          <div>
            <h3 className="text-lg font-semibold">Reject Document</h3>
            <p className="text-sm text-muted-foreground">
              Please provide a reason for rejection.
            </p>
          </div>
        </div>
        <textarea
          value={reason}
          onChange={(e) => setReason(e.target.value)}
          placeholder="Enter rejection reason (required)..."
          className="w-full h-24 rounded-lg border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring resize-none"
          autoFocus
        />
        <div className="flex gap-2 mt-4 justify-end">
          <Button variant="outline" onClick={onClose} disabled={loading}>
            Cancel
          </Button>
          <Button
            variant="destructive"
            onClick={() => onConfirm(reason)}
            disabled={!reason.trim() || loading}
          >
            {loading ? (
              <Loader2 className="h-4 w-4 animate-spin mr-2" />
            ) : (
              <XCircle className="h-4 w-4 mr-2" />
            )}
            Reject Document
          </Button>
        </div>
      </div>
    </div>
  );
}

export default function AdminDocumentsPage() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [reviewingId, setReviewingId] = useState<string | null>(null);
  const [error, setError] = useState("");
  const [activeTab, setActiveTab] = useState("all");
  const [searchQuery, setSearchQuery] = useState("");
  const [rejectModalDoc, setRejectModalDoc] = useState<string | null>(null);

  const fetchDocs = useCallback(async () => {
    setLoading(true);
    try {
      const res = await adminService.getDocuments(
        activeTab,
        1,
        50,
        searchQuery || undefined,
      );
      setDocuments(res.documents || []);
      setTotal(res.total || 0);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, [activeTab, searchQuery]);

  useEffect(() => {
    fetchDocs();
  }, [fetchDocs]);

  const [searchTimeout, setSearchTimeout] = useState<NodeJS.Timeout | null>(
    null,
  );
  const handleSearchChange = (value: string) => {
    if (searchTimeout) clearTimeout(searchTimeout);
    const timeout = setTimeout(() => {
      setSearchQuery(value);
    }, 400);
    setSearchTimeout(timeout);
  };

  const handleReview = async (
    docId: string,
    status: string,
    reason?: string,
  ) => {
    setReviewingId(docId);
    try {
      await documentService.review(docId, status, reason);
      setRejectModalDoc(null);
      await fetchDocs();
    } catch (e: any) {
      setError(e.message || "Failed to update document status");
    } finally {
      setReviewingId(null);
    }
  };

  const getFileUrl = (url: string) => {
    if (!url) return "#";
    if (url.startsWith("http")) return url;
    const base = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    return `${base}${url}`;
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Document Review</h1>
        <p className="text-muted-foreground">
          Review, approve, or reject student document submissions.{" "}
          {total > 0 && `(${total} total)`}
        </p>
      </div>

      {error && (
        <div className="glass-card p-4 border-red-200 dark:border-red-800">
          <p className="text-red-600 dark:text-red-400 text-sm">{error}</p>
          <Button
            variant="ghost"
            size="sm"
            className="mt-1"
            onClick={() => setError("")}
          >
            Dismiss
          </Button>
        </div>
      )}

      {/* Status Filter Tabs + Search */}
      <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
        <div className="flex gap-1 bg-muted/50 p-1 rounded-lg overflow-x-auto">
          {STATUS_TABS.map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.value}
                onClick={() => setActiveTab(tab.value)}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-sm font-medium transition-colors whitespace-nowrap ${
                  activeTab === tab.value
                    ? "bg-background shadow-sm text-foreground"
                    : "text-muted-foreground hover:text-foreground"
                }`}
              >
                <Icon className="h-3.5 w-3.5" />
                {tab.label}
              </button>
            );
          })}
        </div>
        <div className="relative w-full sm:w-72">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search student or document..."
            className="pl-9"
            onChange={(e) => handleSearchChange(e.target.value)}
          />
        </div>
      </div>

      {/* Documents Table */}
      <div className="glass-card p-6">
        {loading ? (
          <div className="space-y-3">
            {[1, 2, 3, 4].map((i) => (
              <Skeleton key={i} className="h-14 rounded-lg" />
            ))}
          </div>
        ) : documents.length === 0 ? (
          <div className="text-center py-12">
            <Filter className="h-12 w-12 mx-auto text-muted-foreground/50 mb-3" />
            <p className="text-lg font-medium">No documents found</p>
            <p className="text-muted-foreground text-sm">
              {activeTab === "all"
                ? "No documents have been submitted yet."
                : `No ${activeTab.replace("_", " ")} documents.`}
            </p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b">
                  <th className="text-left py-3 px-2 font-medium text-muted-foreground">
                    Student
                  </th>
                  <th className="text-left py-3 px-2 font-medium text-muted-foreground">
                    Document Type
                  </th>
                  <th className="text-left py-3 px-2 font-medium text-muted-foreground">
                    File
                  </th>
                  <th className="text-left py-3 px-2 font-medium text-muted-foreground">
                    Status
                  </th>
                  <th className="text-left py-3 px-2 font-medium text-muted-foreground">
                    Submitted
                  </th>
                  <th className="text-left py-3 px-2 font-medium text-muted-foreground">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody>
                {documents.map((doc) => (
                  <tr
                    key={doc.id}
                    className="border-b last:border-0 hover:bg-muted/50 transition-colors"
                  >
                    <td className="py-3 px-2">
                      <div>
                        <p className="font-medium text-sm">
                          {doc.student_name || "Unknown Student"}
                        </p>
                        <p className="text-xs text-muted-foreground">
                          {doc.student_email || doc.user_id.slice(0, 8) + "..."}
                        </p>
                      </div>
                    </td>
                    <td className="py-3 px-2 capitalize">
                      {doc.document_type.replace(/_/g, " ")}
                    </td>
                    <td className="py-3 px-2">
                      <div className="flex items-center gap-2">
                        <FileText className="h-4 w-4 text-muted-foreground" />
                        <span className="truncate max-w-[150px]">
                          {doc.file_name}
                        </span>
                      </div>
                    </td>
                    <td className="py-3 px-2">
                      <StatusBadge status={doc.status} />
                      {doc.status === "rejected" && doc.rejection_reason && (
                        <p
                          className="text-xs text-red-500 mt-1 max-w-[200px] truncate"
                          title={doc.rejection_reason}
                        >
                          {doc.rejection_reason}
                        </p>
                      )}
                    </td>
                    <td className="py-3 px-2 text-muted-foreground text-xs">
                      {doc.created_at
                        ? new Date(doc.created_at).toLocaleDateString("en-IN", {
                            day: "2-digit",
                            month: "short",
                            year: "numeric",
                          })
                        : "\u2014"}
                    </td>
                    <td className="py-3 px-2">
                      <div className="flex gap-1.5 items-center">
                        <a
                          href={getFileUrl(doc.file_url)}
                          target="_blank"
                          rel="noopener noreferrer"
                          title="Preview document"
                        >
                          <Button size="sm" variant="ghost">
                            <Eye className="h-3.5 w-3.5" />
                          </Button>
                        </a>

                        {doc.status === "pending" && (
                          <Button
                            size="sm"
                            variant="outline"
                            className="text-blue-600 border-blue-300 hover:bg-blue-50 dark:hover:bg-blue-900/20"
                            onClick={() => handleReview(doc.id, "under_review")}
                            disabled={reviewingId === doc.id}
                          >
                            {reviewingId === doc.id ? (
                              <Loader2 className="h-3 w-3 animate-spin" />
                            ) : (
                              <>
                                <FileSearch className="h-3 w-3 mr-1" />
                                Review
                              </>
                            )}
                          </Button>
                        )}

                        {(doc.status === "pending" ||
                          doc.status === "under_review") && (
                          <Button
                            size="sm"
                            variant="outline"
                            className="text-green-600 border-green-300 hover:bg-green-50 dark:hover:bg-green-900/20"
                            onClick={() => handleReview(doc.id, "approved")}
                            disabled={reviewingId === doc.id}
                          >
                            {reviewingId === doc.id ? (
                              <Loader2 className="h-3 w-3 animate-spin" />
                            ) : (
                              <>
                                <CheckCircle2 className="h-3 w-3 mr-1" />
                                Approve
                              </>
                            )}
                          </Button>
                        )}

                        {(doc.status === "pending" ||
                          doc.status === "under_review") && (
                          <Button
                            size="sm"
                            variant="outline"
                            className="text-red-600 border-red-300 hover:bg-red-50 dark:hover:bg-red-900/20"
                            onClick={() => setRejectModalDoc(doc.id)}
                            disabled={reviewingId === doc.id}
                          >
                            <XCircle className="h-3 w-3 mr-1" />
                            Reject
                          </Button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Rejection Modal */}
      <RejectModal
        open={!!rejectModalDoc}
        onClose={() => setRejectModalDoc(null)}
        onConfirm={(reason) => {
          if (rejectModalDoc) handleReview(rejectModalDoc, "rejected", reason);
        }}
        loading={reviewingId === rejectModalDoc}
      />
    </div>
  );
}
