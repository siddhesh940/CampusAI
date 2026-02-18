"use client";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import { documentService } from "@/services/campus-services";
import type { Document } from "@/types";
import {
    CheckCircle2,
    Clock,
    Download,
    FileSearch,
    FileText,
    Loader2,
    Upload,
    XCircle,
} from "lucide-react";
import { useEffect, useRef, useState } from "react";

const DOC_TYPES = [
  { value: "10th_marksheet", label: "10th Marksheet" },
  { value: "12th_marksheet", label: "12th Marksheet" },
  { value: "aadhar_card", label: "Aadhar Card" },
  { value: "photo", label: "Passport Photo" },
  { value: "transfer_certificate", label: "Transfer Certificate" },
  { value: "income_certificate", label: "Income Certificate" },
  { value: "caste_certificate", label: "Caste Certificate" },
  { value: "other", label: "Other Document" },
];

const STATUS_LABELS: Record<string, string> = {
  pending: "Pending",
  under_review: "Under Review",
  approved: "Approved",
  rejected: "Rejected",
};

function StatusBadge({ status }: { status: string }) {
  const cfg: Record<
    string,
    { bg: string; text: string; icon: React.ElementType }
  > = {
    approved: {
      bg: "bg-green-100 dark:bg-green-900/30",
      text: "text-green-700 dark:text-green-400",
      icon: CheckCircle2,
    },
    under_review: {
      bg: "bg-blue-100 dark:bg-blue-900/30",
      text: "text-blue-700 dark:text-blue-400",
      icon: FileSearch,
    },
    pending: {
      bg: "bg-yellow-100 dark:bg-yellow-900/30",
      text: "text-yellow-700 dark:text-yellow-400",
      icon: Clock,
    },
    rejected: {
      bg: "bg-red-100 dark:bg-red-900/30",
      text: "text-red-700 dark:text-red-400",
      icon: XCircle,
    },
  };
  const c = cfg[status] || cfg.pending;
  const Icon = c.icon;
  return (
    <span
      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${c.bg} ${c.text}`}
    >
      <Icon className="h-3 w-3" />
      {STATUS_LABELS[status] || status}
    </span>
  );
}

export default function DocumentsPage() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");
  const [uploadError, setUploadError] = useState("");
  const [selectedType, setSelectedType] = useState(DOC_TYPES[0].value);
  const fileRef = useRef<HTMLInputElement>(null);

  const fetchDocs = async () => {
    try {
      const res = await documentService.list();
      setDocuments(res.documents || []);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocs();
  }, []);

  const handleUpload = async () => {
    const file = fileRef.current?.files?.[0];
    if (!file) {
      setUploadError("Please select a file");
      return;
    }
    setUploading(true);
    setUploadError("");
    try {
      await documentService.upload(selectedType, file);
      if (fileRef.current) fileRef.current.value = "";
      await fetchDocs();
    } catch (e: any) {
      setUploadError(e.message);
    } finally {
      setUploading(false);
    }
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-9 w-40" />
        <Skeleton className="h-32 rounded-xl" />
        <Skeleton className="h-64 rounded-xl" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Documents</h1>
        <p className="text-muted-foreground">
          Upload and manage your onboarding documents.
        </p>
      </div>

      {/* Upload Section */}
      <div className="glass-card p-6">
        <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
          <Upload className="h-5 w-5" />
          Upload Document
        </h2>
        <div className="flex flex-col sm:flex-row gap-3">
          <select
            value={selectedType}
            onChange={(e) => setSelectedType(e.target.value)}
            title="Document type"
            aria-label="Document type"
            className="flex h-10 rounded-lg border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          >
            {DOC_TYPES.map((t) => (
              <option key={t.value} value={t.value}>
                {t.label}
              </option>
            ))}
          </select>
          <Input
            ref={fileRef}
            type="file"
            accept=".pdf,.jpg,.jpeg,.png"
            className="flex-1"
          />
          <Button
            onClick={handleUpload}
            disabled={uploading}
            variant="gradient"
          >
            {uploading ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin mr-2" />
                Uploading...
              </>
            ) : (
              <>
                <Upload className="h-4 w-4 mr-2" />
                Upload
              </>
            )}
          </Button>
        </div>
        {uploadError && (
          <p className="text-sm text-red-500 mt-2">{uploadError}</p>
        )}
        <p className="text-xs text-muted-foreground mt-2">
          Accepted formats: PDF, JPG, PNG. Max size: 5MB.
        </p>
      </div>

      {/* Error */}
      {error && (
        <div className="glass-card p-4 border-red-200 dark:border-red-800">
          <p className="text-red-600 dark:text-red-400 text-sm">{error}</p>
        </div>
      )}

      {/* Documents List */}
      <div className="glass-card p-6">
        <h2 className="text-lg font-semibold mb-4">Your Documents</h2>
        {documents.length === 0 ? (
          <div className="text-center py-12">
            <FileText className="h-12 w-12 mx-auto text-muted-foreground/50 mb-3" />
            <p className="text-muted-foreground">No documents uploaded yet.</p>
            <p className="text-sm text-muted-foreground">
              Upload your first document above to get started.
            </p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b">
                  <th className="text-left py-3 px-2 font-medium text-muted-foreground">
                    Type
                  </th>
                  <th className="text-left py-3 px-2 font-medium text-muted-foreground">
                    File Name
                  </th>
                  <th className="text-left py-3 px-2 font-medium text-muted-foreground">
                    Status
                  </th>
                  <th className="text-left py-3 px-2 font-medium text-muted-foreground">
                    Uploaded
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
                      <span className="capitalize">
                        {doc.document_type.replace(/_/g, " ")}
                      </span>
                    </td>
                    <td className="py-3 px-2">
                      <div className="flex items-center gap-2">
                        <FileText className="h-4 w-4 text-muted-foreground" />
                        <span className="truncate max-w-[200px]">
                          {doc.file_name}
                        </span>
                      </div>
                    </td>
                    <td className="py-3 px-2">
                      <StatusBadge status={doc.status} />
                      {doc.status === "rejected" && doc.rejection_reason && (
                        <p className="text-xs text-red-500 mt-1">
                          {doc.rejection_reason}
                        </p>
                      )}
                    </td>
                    <td className="py-3 px-2 text-muted-foreground">
                      {doc.created_at
                        ? new Date(doc.created_at).toLocaleDateString()
                        : "—"}
                    </td>
                    <td className="py-3 px-2">
                      <a
                        href={
                          doc.file_url?.startsWith("http")
                            ? doc.file_url
                            : `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}${doc.file_url}`
                        }
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-1 text-primary hover:underline text-xs"
                      >
                        <Download className="h-3 w-3" />
                        View
                      </a>
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
