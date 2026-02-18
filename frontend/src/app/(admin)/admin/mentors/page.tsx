"use client";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import {
    adminService,
    mentorService,
    type MentorAssignment,
} from "@/services/campus-services";
import type { User } from "@/types";
import { Loader2, Plus, Search, Trash2, Users } from "lucide-react";
import { useEffect, useState } from "react";
import { toast } from "sonner";

export default function AdminMentorsPage() {
  const [assignments, setAssignments] = useState<MentorAssignment[]>([]);
  const [students, setStudents] = useState<User[]>([]);
  const [mentors, setMentors] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [showAssignForm, setShowAssignForm] = useState(false);
  const [selectedStudent, setSelectedStudent] = useState("");
  const [selectedMentor, setSelectedMentor] = useState("");
  const [saving, setSaving] = useState(false);
  const [searchFilter, setSearchFilter] = useState("");

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [assignRes, studRes, mentorRes] = await Promise.all([
        mentorService.listAssignments(),
        adminService.listStudents(1, 500),
        adminService.listMentors(),
      ]);
      setAssignments(assignRes.assignments);
      setStudents(studRes.students);
      setMentors(mentorRes.mentors);
    } catch (e: any) {
      toast.error(e.message || "Failed to load data");
    } finally {
      setLoading(false);
    }
  };

  const handleAssign = async () => {
    if (!selectedStudent || !selectedMentor) return;
    setSaving(true);
    try {
      const assignment = await mentorService.assignMentor(
        selectedStudent,
        selectedMentor,
      );
      setAssignments((prev) => [assignment, ...prev]);
      setShowAssignForm(false);
      setSelectedStudent("");
      setSelectedMentor("");
      toast.success("Mentor assigned successfully");
    } catch (e: any) {
      toast.error(e.message || "Failed to assign mentor");
    } finally {
      setSaving(false);
    }
  };

  const handleDeactivate = async (id: string) => {
    try {
      await mentorService.deactivateAssignment(id);
      setAssignments((prev) => prev.filter((a) => a.id !== id));
      toast.success("Assignment deactivated");
    } catch (e: any) {
      toast.error(e.message || "Failed to deactivate");
    }
  };

  const filteredAssignments = searchFilter
    ? assignments.filter(
        (a) =>
          a.student_name?.toLowerCase().includes(searchFilter.toLowerCase()) ||
          a.mentor_name?.toLowerCase().includes(searchFilter.toLowerCase()) ||
          a.student_email?.toLowerCase().includes(searchFilter.toLowerCase()) ||
          a.mentor_email?.toLowerCase().includes(searchFilter.toLowerCase()),
      )
    : assignments;

  // Find unassigned students
  const assignedStudentIds = new Set(assignments.map((a) => a.student_id));
  const unassignedStudents = students.filter(
    (s) => !assignedStudentIds.has(s.id),
  );

  if (loading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-9 w-56" />
        <div className="space-y-3">
          {[1, 2, 3, 4].map((i) => (
            <Skeleton key={i} className="h-20 w-full" />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight flex items-center gap-2">
            <Users className="h-7 w-7 text-primary" />
            Mentor Management
          </h1>
          <p className="text-muted-foreground mt-1">
            Assign mentors to students and manage assignments
          </p>
        </div>
        <Button onClick={() => setShowAssignForm(true)} className="gap-2">
          <Plus className="h-4 w-4" /> Assign Mentor
        </Button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="glass-card p-5">
          <p className="text-sm text-muted-foreground">Total Assignments</p>
          <p className="text-2xl font-bold mt-1">{assignments.length}</p>
        </div>
        <div className="glass-card p-5">
          <p className="text-sm text-muted-foreground">Active Mentors</p>
          <p className="text-2xl font-bold mt-1">{mentors.length}</p>
        </div>
        <div className="glass-card p-5">
          <p className="text-sm text-muted-foreground">Unassigned Students</p>
          <p className="text-2xl font-bold mt-1">{unassignedStudents.length}</p>
        </div>
      </div>

      {/* Assign Form */}
      {showAssignForm && (
        <div className="glass-card p-6">
          <h3 className="font-semibold text-lg mb-4">
            Assign Mentor to Student
          </h3>
          <div className="grid gap-4 md:grid-cols-2">
            <div>
              <label className="text-sm font-medium">Select Student *</label>
              <select
                value={selectedStudent}
                onChange={(e) => setSelectedStudent(e.target.value)}
                className="w-full mt-1 p-2.5 border rounded-lg bg-background text-sm"
                title="Select student"
              >
                <option value="">Choose a student...</option>
                {unassignedStudents.map((s) => (
                  <option key={s.id} value={s.id}>
                    {s.first_name} {s.last_name} ({s.email})
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="text-sm font-medium">Select Mentor *</label>
              <select
                value={selectedMentor}
                onChange={(e) => setSelectedMentor(e.target.value)}
                className="w-full mt-1 p-2.5 border rounded-lg bg-background text-sm"
                title="Select mentor"
              >
                <option value="">Choose a mentor...</option>
                {mentors.map((m) => (
                  <option key={m.id} value={m.id}>
                    {m.first_name} {m.last_name} ({m.email})
                  </option>
                ))}
              </select>
            </div>
          </div>
          <div className="flex gap-3 mt-4">
            <Button variant="outline" onClick={() => setShowAssignForm(false)}>
              Cancel
            </Button>
            <Button
              onClick={handleAssign}
              disabled={saving || !selectedStudent || !selectedMentor}
            >
              {saving && <Loader2 className="h-4 w-4 animate-spin mr-2" />}
              Assign Mentor
            </Button>
          </div>
        </div>
      )}

      {/* Search */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        <Input
          placeholder="Search assignments..."
          className="pl-10"
          onChange={(e) => setSearchFilter(e.target.value)}
        />
      </div>

      {/* Assignment List */}
      <div className="space-y-3">
        {filteredAssignments.length === 0 ? (
          <div className="glass-card p-12 text-center">
            <Users className="h-12 w-12 mx-auto text-muted-foreground mb-3" />
            <h3 className="text-lg font-semibold mb-2">No Assignments</h3>
            <p className="text-muted-foreground">
              Assign mentors to students using the button above.
            </p>
          </div>
        ) : (
          filteredAssignments.map((a) => (
            <div key={a.id} className="glass-card p-5 flex items-center gap-4">
              <div className="h-10 w-10 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0">
                <Users className="h-5 w-5 text-primary" />
              </div>
              <div className="flex-1 min-w-0 grid md:grid-cols-2 gap-2">
                <div>
                  <p className="text-xs text-muted-foreground">Student</p>
                  <p className="font-medium text-sm">
                    {a.student_name || "Unknown"}
                  </p>
                  <p className="text-xs text-muted-foreground">
                    {a.student_email}
                  </p>
                </div>
                <div>
                  <p className="text-xs text-muted-foreground">Mentor</p>
                  <p className="font-medium text-sm">
                    {a.mentor_name || "Unknown"}
                  </p>
                  <p className="text-xs text-muted-foreground">
                    {a.mentor_email}
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <span
                  className={`text-xs px-2.5 py-1 rounded-full font-medium ${
                    a.is_active
                      ? "bg-green-100 text-green-700"
                      : "bg-red-100 text-red-700"
                  }`}
                >
                  {a.is_active ? "Active" : "Inactive"}
                </span>
                {a.is_active && (
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleDeactivate(a.id)}
                    className="text-destructive hover:text-destructive"
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
