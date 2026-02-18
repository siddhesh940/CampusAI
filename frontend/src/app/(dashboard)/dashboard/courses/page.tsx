"use client";

import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import {
    courseService,
    type Course,
    type Enrollment,
    type Subject,
} from "@/services/campus-services";
import {
    CheckCircle2,
    GraduationCap,
    Loader2,
    Plus,
    Trash2,
} from "lucide-react";
import { useEffect, useState } from "react";
export default function CoursesPage() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [enrollments, setEnrollments] = useState<Enrollment[]>([]);
  const [selectedCourse, setSelectedCourse] = useState("");
  const [selectedSubjects, setSelectedSubjects] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [enrolling, setEnrolling] = useState(false);
  const [error, setError] = useState("");
  const [courseName, setCourseName] = useState("");

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [courseRes, enrollRes] = await Promise.all([
        courseService.listCourses(),
        courseService.getEnrollments(),
      ]);
      setCourses(courseRes.courses);
      setEnrollments(enrollRes.enrollments);
      setCourseName(enrollRes.course_name || "");
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const loadSubjects = async (courseId: string) => {
    setSelectedCourse(courseId);
    setSelectedSubjects([]);
    if (!courseId) {
      setSubjects([]);
      return;
    }
    try {
      const res = await courseService.listSubjects(courseId);
      setSubjects(res.subjects);
    } catch (e: any) {
      setError(e.message);
    }
  };

  const toggleSubject = (id: string) => {
    setSelectedSubjects((prev) =>
      prev.includes(id) ? prev.filter((s) => s !== id) : [...prev, id],
    );
  };

  const handleEnroll = async () => {
    if (!selectedCourse || selectedSubjects.length === 0) return;
    setEnrolling(true);
    setError("");
    try {
      const res = await courseService.enroll(selectedCourse, selectedSubjects);
      setEnrollments(res.enrollments);
      setCourseName(res.course_name || "");
      setSelectedSubjects([]);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setEnrolling(false);
    }
  };

  const handleDrop = async (subjectId: string) => {
    try {
      const res = await courseService.dropSubject(subjectId);
      setEnrollments(res.enrollments);
    } catch (e: any) {
      setError(e.message);
    }
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-9 w-64" />
        <div className="grid gap-4 md:grid-cols-2">
          <Skeleton className="h-48" />
          <Skeleton className="h-48" />
        </div>
      </div>
    );
  }

  const enrolledIds = new Set(enrollments.map((e) => e.subject_id));

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <GraduationCap className="h-7 w-7 text-primary" />
        <h1 className="text-2xl font-bold">Course Registration</h1>
      </div>

      {error && (
        <div className="bg-destructive/10 text-destructive p-3 rounded-lg text-sm">
          {error}
        </div>
      )}

      {/* Enrollment Summary */}
      {enrollments.length > 0 && (
        <div className="glass-card p-5">
          <h2 className="font-semibold text-lg mb-3 flex items-center gap-2">
            <CheckCircle2 className="h-5 w-5 text-green-500" />
            Enrolled Subjects {courseName && `- ${courseName}`}
          </h2>
          <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
            {enrollments.map((e) => (
              <div
                key={e.id}
                className="flex items-center justify-between p-3 bg-muted/50 rounded-lg"
              >
                <div>
                  <p className="font-medium text-sm">{e.subject_name}</p>
                  <p className="text-xs text-muted-foreground">
                    {e.subject_code}
                  </p>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => handleDrop(e.subject_id)}
                  className="text-destructive hover:text-destructive"
                >
                  <Trash2 className="h-4 w-4" />
                </Button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Course Selection */}
      <div className="glass-card p-5">
        <h2 className="font-semibold text-lg mb-4">Select Course & Subjects</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Course</label>
            <select
              value={selectedCourse}
              onChange={(e) => loadSubjects(e.target.value)}
              className="w-full p-2.5 border rounded-lg bg-background text-sm"
              title="Select course"
            >
              <option value="">Select a course...</option>
              {courses.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name} ({c.code})
                </option>
              ))}
            </select>
          </div>

          {subjects.length > 0 && (
            <div>
              <label className="block text-sm font-medium mb-2">
                Subjects (select multiple)
              </label>
              <div className="grid gap-2 md:grid-cols-2">
                {subjects.map((s) => {
                  const isEnrolled = enrolledIds.has(s.id);
                  const isSelected = selectedSubjects.includes(s.id);
                  return (
                    <button
                      key={s.id}
                      onClick={() => !isEnrolled && toggleSubject(s.id)}
                      disabled={isEnrolled}
                      className={`flex items-center gap-3 p-3 rounded-lg border text-left transition-colors ${
                        isEnrolled
                          ? "bg-green-50 border-green-200 opacity-60 dark:bg-green-900/20"
                          : isSelected
                            ? "bg-primary/10 border-primary"
                            : "hover:bg-muted/50"
                      }`}
                    >
                      <div
                        className={`w-5 h-5 rounded flex items-center justify-center border ${
                          isEnrolled || isSelected
                            ? "bg-primary border-primary text-white"
                            : ""
                        }`}
                      >
                        {(isEnrolled || isSelected) && (
                          <CheckCircle2 className="h-3 w-3" />
                        )}
                      </div>
                      <div className="flex-1">
                        <p className="font-medium text-sm">{s.name}</p>
                        <p className="text-xs text-muted-foreground">
                          {s.code} · {s.credits} credits · Sem {s.semester}
                          {s.is_elective ? " · Elective" : ""}
                        </p>
                      </div>
                      {isEnrolled && (
                        <span className="text-xs text-green-600 font-medium">
                          Enrolled
                        </span>
                      )}
                    </button>
                  );
                })}
              </div>
            </div>
          )}

          {selectedSubjects.length > 0 && (
            <Button
              onClick={handleEnroll}
              disabled={enrolling}
              className="w-full"
            >
              {enrolling ? (
                <Loader2 className="h-4 w-4 animate-spin mr-2" />
              ) : (
                <Plus className="h-4 w-4 mr-2" />
              )}
              Enroll in {selectedSubjects.length} Subject(s)
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
