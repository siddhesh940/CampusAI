"use client";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import { adminService } from "@/services/campus-services";
import {
  BookOpen,
  CheckCircle2,
  Key,
  Loader2,
  Search,
  XCircle,
} from "lucide-react";
import { useEffect, useState } from "react";
import { toast } from "sonner";

interface LMSEntry {
  id: string;
  user_id: string;
  platform: string;
  is_activated: boolean;
  lms_username: string | null;
  activation_key: string | null;
  activated_at: string | null;
  student_name: string;
  student_email: string;
}

export default function AdminLMSPage() {
  const [activations, setActivations] = useState<LMSEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [generatingFor, setGeneratingFor] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const res = await adminService.listLMSActivations();
      setActivations(res.activations);
    } catch (e: any) {
      toast.error(e.message || "Failed to load LMS data");
    } finally {
      setLoading(false);
    }
  };

  const handleGenerate = async (userId: string) => {
    setGeneratingFor(userId);
    try {
      const result = await adminService.generateLMSCredentials(userId);
      setActivations((prev) =>
        prev.map((a) =>
          a.user_id === userId
            ? {
                ...a,
                lms_username: result.lms_username,
                activation_key: result.activation_key,
                is_activated: result.is_activated,
              }
            : a,
        ),
      );
      toast.success("LMS credentials generated successfully");
    } catch (e: any) {
      toast.error(e.message || "Failed to generate credentials");
    } finally {
      setGeneratingFor(null);
    }
  };

  const filtered = searchQuery
    ? activations.filter(
        (a) =>
          a.student_name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
          a.student_email?.toLowerCase().includes(searchQuery.toLowerCase()),
      )
    : activations;

  const activeCount = activations.filter((a) => a.is_activated).length;

  if (loading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-9 w-56" />
        <div className="grid grid-cols-3 gap-4">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-24" />
          ))}
        </div>
        <div className="space-y-3">
          {[1, 2, 3, 4].map((i) => (
            <Skeleton key={i} className="h-16 w-full" />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold tracking-tight flex items-center gap-2">
          <BookOpen className="h-7 w-7 text-primary" />
          LMS Management
        </h1>
        <p className="text-muted-foreground mt-1">
          Generate and manage LMS credentials for students
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="glass-card p-5">
          <p className="text-sm text-muted-foreground">Total Students</p>
          <p className="text-2xl font-bold mt-1">{activations.length}</p>
        </div>
        <div className="glass-card p-5">
          <p className="text-sm text-muted-foreground">Activated</p>
          <p className="text-2xl font-bold mt-1 text-green-600">
            {activeCount}
          </p>
        </div>
        <div className="glass-card p-5">
          <p className="text-sm text-muted-foreground">Pending</p>
          <p className="text-2xl font-bold mt-1 text-yellow-600">
            {activations.length - activeCount}
          </p>
        </div>
      </div>

      {/* Search */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        <Input
          placeholder="Search students..."
          className="pl-10"
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </div>

      {/* Table */}
      <div className="glass-card overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b bg-muted/30">
                <th className="text-left p-4 font-medium">Student</th>
                <th className="text-left p-4 font-medium">Platform</th>
                <th className="text-left p-4 font-medium">LMS Username</th>
                <th className="text-left p-4 font-medium">Activation Key</th>
                <th className="text-left p-4 font-medium">Status</th>
                <th className="text-left p-4 font-medium">Actions</th>
              </tr>
            </thead>
            <tbody>
              {filtered.length === 0 ? (
                <tr>
                  <td colSpan={6} className="p-8 text-center text-muted-foreground">
                    No LMS entries found.
                  </td>
                </tr>
              ) : (
                filtered.map((entry) => (
                  <tr key={entry.id || entry.user_id} className="border-b hover:bg-muted/20">
                    <td className="p-4">
                      <p className="font-medium">{entry.student_name}</p>
                      <p className="text-xs text-muted-foreground">
                        {entry.student_email}
                      </p>
                    </td>
                    <td className="p-4">{entry.platform}</td>
                    <td className="p-4 font-mono text-xs">
                      {entry.lms_username || "—"}
                    </td>
                    <td className="p-4 font-mono text-xs">
                      {entry.activation_key || "—"}
                    </td>
                    <td className="p-4">
                      {entry.is_activated ? (
                        <span className="inline-flex items-center gap-1 text-xs px-2.5 py-1 rounded-full bg-green-100 text-green-700 font-medium">
                          <CheckCircle2 className="h-3 w-3" /> Active
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1 text-xs px-2.5 py-1 rounded-full bg-yellow-100 text-yellow-700 font-medium">
                          <XCircle className="h-3 w-3" /> Inactive
                        </span>
                      )}
                    </td>
                    <td className="p-4">
                      {!entry.is_activated && (
                        <Button
                          size="sm"
                          variant="outline"
                          className="gap-1"
                          onClick={() => handleGenerate(entry.user_id)}
                          disabled={generatingFor === entry.user_id}
                        >
                          {generatingFor === entry.user_id ? (
                            <Loader2 className="h-3 w-3 animate-spin" />
                          ) : (
                            <Key className="h-3 w-3" />
                          )}
                          Generate
                        </Button>
                      )}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
