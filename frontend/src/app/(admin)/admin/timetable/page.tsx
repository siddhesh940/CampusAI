"use client";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import {
    courseService,
    timetableService,
    type Course,
    type ScheduleResponse,
    type Subject,
} from "@/services/campus-services";
import {
    Calendar,
    Clock,
    Loader2,
    MapPin,
    Plus,
    Trash2,
    User,
} from "lucide-react";
import { useEffect, useState } from "react";
import { toast } from "sonner";

const DAYS = [
  { value: "monday", label: "Monday" },
  { value: "tuesday", label: "Tuesday" },
  { value: "wednesday", label: "Wednesday" },
  { value: "thursday", label: "Thursday" },
  { value: "friday", label: "Friday" },
  { value: "saturday", label: "Saturday" },
];

export default function AdminTimetablePage() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [schedules, setSchedules] = useState<ScheduleResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedCourse, setSelectedCourse] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [saving, setSaving] = useState(false);

  const [form, setForm] = useState({
    subject_id: "",
    day_of_week: "monday",
    start_time: "09:00",
    end_time: "10:00",
    room: "",
    instructor: "",
  });

  useEffect(() => {
    loadInitial();
  }, []);

  const loadInitial = async () => {
    try {
      const [courseRes, schedRes] = await Promise.all([
        courseService.listCourses(),
        timetableService.listSchedules(),
      ]);
      setCourses(courseRes.courses);
      setSchedules(schedRes.schedules);
    } catch (e: any) {
      toast.error(e.message || "Failed to load data");
    } finally {
      setLoading(false);
    }
  };

  const loadSubjects = async (courseId: string) => {
    setSelectedCourse(courseId);
    if (!courseId) {
      setSubjects([]);
      return;
    }
    try {
      const res = await courseService.listSubjects(courseId);
      setSubjects(res.subjects);
    } catch (e: any) {
      toast.error(e.message);
    }
  };

  const handleCreate = async () => {
    if (
      !form.subject_id ||
      !form.day_of_week ||
      !form.start_time ||
      !form.end_time
    )
      return;
    setSaving(true);
    try {
      const newSchedule = await timetableService.createSchedule({
        subject_id: form.subject_id,
        day_of_week: form.day_of_week,
        start_time: form.start_time,
        end_time: form.end_time,
        room: form.room || undefined,
        instructor: form.instructor || undefined,
      });
      setSchedules((prev) => [newSchedule, ...prev]);
      setShowForm(false);
      setForm({
        subject_id: "",
        day_of_week: "monday",
        start_time: "09:00",
        end_time: "10:00",
        room: "",
        instructor: "",
      });
      toast.success("Schedule created successfully");
    } catch (e: any) {
      toast.error(e.message || "Failed to create schedule");
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await timetableService.deleteSchedule(id);
      setSchedules((prev) => prev.filter((s) => s.id !== id));
      toast.success("Schedule deleted");
    } catch (e: any) {
      toast.error(e.message);
    }
  };

  // Group schedules by day
  const schedulesByDay: Record<string, ScheduleResponse[]> = {};
  for (const day of DAYS) {
    schedulesByDay[day.value] = schedules
      .filter((s) => s.day_of_week === day.value)
      .sort((a, b) => a.start_time.localeCompare(b.start_time));
  }

  if (loading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-9 w-56" />
        <div className="space-y-3">
          {[1, 2, 3, 4, 5, 6].map((i) => (
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
            <Calendar className="h-7 w-7 text-primary" />
            Timetable Management
          </h1>
          <p className="text-muted-foreground mt-1">
            Create subject schedules for the weekly timetable
          </p>
        </div>
        <Button onClick={() => setShowForm(true)} className="gap-2">
          <Plus className="h-4 w-4" /> Add Schedule
        </Button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="glass-card p-5">
          <p className="text-sm text-muted-foreground">Total Schedules</p>
          <p className="text-2xl font-bold mt-1">{schedules.length}</p>
        </div>
        <div className="glass-card p-5">
          <p className="text-sm text-muted-foreground">Courses</p>
          <p className="text-2xl font-bold mt-1">{courses.length}</p>
        </div>
        <div className="glass-card p-5">
          <p className="text-sm text-muted-foreground">Days with Classes</p>
          <p className="text-2xl font-bold mt-1">
            {DAYS.filter((d) => schedulesByDay[d.value].length > 0).length}
          </p>
        </div>
      </div>

      {/* Create Form */}
      {showForm && (
        <div className="glass-card p-6">
          <h3 className="font-semibold text-lg mb-4">Add Schedule Entry</h3>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            <div>
              <label className="text-sm font-medium">Course</label>
              <select
                value={selectedCourse}
                onChange={(e) => loadSubjects(e.target.value)}
                className="w-full mt-1 p-2.5 border rounded-lg bg-background text-sm"
                title="Select course"
              >
                <option value="">Select course...</option>
                {courses.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.name} ({c.code})
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="text-sm font-medium">Subject *</label>
              <select
                value={form.subject_id}
                onChange={(e) =>
                  setForm({ ...form, subject_id: e.target.value })
                }
                className="w-full mt-1 p-2.5 border rounded-lg bg-background text-sm"
                title="Select subject"
              >
                <option value="">Select subject...</option>
                {subjects.map((s) => (
                  <option key={s.id} value={s.id}>
                    {s.name} ({s.code})
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="text-sm font-medium">Day *</label>
              <select
                value={form.day_of_week}
                onChange={(e) =>
                  setForm({ ...form, day_of_week: e.target.value })
                }
                className="w-full mt-1 p-2.5 border rounded-lg bg-background text-sm"
                title="Select day"
              >
                {DAYS.map((d) => (
                  <option key={d.value} value={d.value}>
                    {d.label}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="text-sm font-medium">Start Time *</label>
              <Input
                type="time"
                value={form.start_time}
                onChange={(e) =>
                  setForm({ ...form, start_time: e.target.value })
                }
                className="mt-1"
              />
            </div>
            <div>
              <label className="text-sm font-medium">End Time *</label>
              <Input
                type="time"
                value={form.end_time}
                onChange={(e) => setForm({ ...form, end_time: e.target.value })}
                className="mt-1"
              />
            </div>
            <div>
              <label className="text-sm font-medium">Room</label>
              <Input
                value={form.room}
                onChange={(e) => setForm({ ...form, room: e.target.value })}
                placeholder="e.g., Room 301"
                className="mt-1"
              />
            </div>
            <div>
              <label className="text-sm font-medium">Instructor</label>
              <Input
                value={form.instructor}
                onChange={(e) =>
                  setForm({ ...form, instructor: e.target.value })
                }
                placeholder="e.g., Dr. Sharma"
                className="mt-1"
              />
            </div>
          </div>
          <div className="flex gap-3 mt-4">
            <Button variant="outline" onClick={() => setShowForm(false)}>
              Cancel
            </Button>
            <Button
              onClick={handleCreate}
              disabled={saving || !form.subject_id}
            >
              {saving && <Loader2 className="h-4 w-4 animate-spin mr-2" />}
              Add Schedule
            </Button>
          </div>
        </div>
      )}

      {/* Weekly Grid */}
      <div className="space-y-3">
        {DAYS.map((day) => (
          <div key={day.value} className="glass-card overflow-hidden">
            <div className="bg-primary/5 px-4 py-2.5 border-b">
              <h3 className="font-semibold text-sm uppercase tracking-wide flex items-center justify-between">
                {day.label}
                <span className="text-xs font-normal text-muted-foreground">
                  {schedulesByDay[day.value].length} classes
                </span>
              </h3>
            </div>
            {schedulesByDay[day.value].length === 0 ? (
              <div className="px-4 py-6 text-center text-sm text-muted-foreground">
                No classes scheduled
              </div>
            ) : (
              <div className="divide-y">
                {schedulesByDay[day.value].map((entry) => (
                  <div
                    key={entry.id}
                    className="px-4 py-3 flex items-center gap-4 hover:bg-muted/30 transition"
                  >
                    <div className="flex items-center gap-2 w-36 flex-shrink-0">
                      <Clock className="h-3.5 w-3.5 text-muted-foreground" />
                      <span className="text-sm font-medium">
                        {entry.start_time?.slice(0, 5)} -{" "}
                        {entry.end_time?.slice(0, 5)}
                      </span>
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="font-medium text-sm truncate">
                        {entry.subject_name || "Subject"}
                      </p>
                      <p className="text-xs text-muted-foreground">
                        {entry.subject_code || ""}
                      </p>
                    </div>
                    {entry.room && (
                      <div className="flex items-center gap-1 text-xs text-muted-foreground">
                        <MapPin className="h-3 w-3" />
                        {entry.room}
                      </div>
                    )}
                    {entry.instructor && (
                      <div className="flex items-center gap-1 text-xs text-muted-foreground">
                        <User className="h-3 w-3" />
                        {entry.instructor}
                      </div>
                    )}
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleDelete(entry.id)}
                      className="text-destructive hover:text-destructive flex-shrink-0"
                    >
                      <Trash2 className="h-3.5 w-3.5" />
                    </Button>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
