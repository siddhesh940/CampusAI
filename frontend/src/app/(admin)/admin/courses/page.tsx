"use client";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import {
    courseService,
    type Course,
    type Subject,
} from "@/services/campus-services";
import {
    BookOpen,
    ChevronDown,
    ChevronRight,
    GraduationCap,
    Loader2,
    Plus,
} from "lucide-react";
import { useEffect, useState } from "react";
import { toast } from "sonner";

export default function AdminCoursesPage() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [subjects, setSubjects] = useState<Record<string, Subject[]>>({});
  const [loading, setLoading] = useState(true);
  const [expandedCourse, setExpandedCourse] = useState<string | null>(null);
  const [showCourseForm, setShowCourseForm] = useState(false);
  const [showSubjectForm, setShowSubjectForm] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  const [courseForm, setCourseForm] = useState({
    name: "",
    code: "",
    description: "",
    duration_years: 4,
    total_credits: 0,
  });

  const [subjectForm, setSubjectForm] = useState({
    name: "",
    code: "",
    credits: 3,
    semester: 1,
    is_elective: false,
  });

  useEffect(() => {
    loadCourses();
  }, []);

  const loadCourses = async () => {
    try {
      const res = await courseService.listCourses();
      setCourses(res.courses);
    } catch (e: any) {
      toast.error(e.message || "Failed to load courses");
    } finally {
      setLoading(false);
    }
  };

  const loadSubjects = async (courseId: string) => {
    if (subjects[courseId]) return;
    try {
      const res = await courseService.listSubjects(courseId);
      setSubjects((prev) => ({ ...prev, [courseId]: res.subjects }));
    } catch (e: any) {
      toast.error(e.message);
    }
  };

  const toggleExpand = (courseId: string) => {
    if (expandedCourse === courseId) {
      setExpandedCourse(null);
    } else {
      setExpandedCourse(courseId);
      loadSubjects(courseId);
    }
  };

  const handleCreateCourse = async () => {
    if (!courseForm.name || !courseForm.code) return;
    setSaving(true);
    try {
      const newCourse = await courseService.createCourse(courseForm);
      setCourses((prev) => [newCourse, ...prev]);
      setShowCourseForm(false);
      setCourseForm({
        name: "",
        code: "",
        description: "",
        duration_years: 4,
        total_credits: 0,
      });
      toast.success("Course created successfully");
    } catch (e: any) {
      toast.error(e.message || "Failed to create course");
    } finally {
      setSaving(false);
    }
  };

  const handleCreateSubject = async (courseId: string) => {
    if (!subjectForm.name || !subjectForm.code) return;
    setSaving(true);
    try {
      const newSubject = await courseService.createSubject({
        course_id: courseId,
        ...subjectForm,
      });
      setSubjects((prev) => ({
        ...prev,
        [courseId]: [...(prev[courseId] || []), newSubject],
      }));
      setShowSubjectForm(null);
      setSubjectForm({
        name: "",
        code: "",
        credits: 3,
        semester: 1,
        is_elective: false,
      });
      toast.success("Subject added successfully");
    } catch (e: any) {
      toast.error(e.message || "Failed to create subject");
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-9 w-56" />
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
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
            <GraduationCap className="h-7 w-7 text-primary" />
            Course Management
          </h1>
          <p className="text-muted-foreground mt-1">
            Create and manage courses and subjects
          </p>
        </div>
        <Button onClick={() => setShowCourseForm(true)} className="gap-2">
          <Plus className="h-4 w-4" /> New Course
        </Button>
      </div>

      {/* Create Course Form */}
      {showCourseForm && (
        <div className="glass-card p-6">
          <h3 className="font-semibold text-lg mb-4">Create New Course</h3>
          <div className="grid gap-4 md:grid-cols-2">
            <div>
              <label className="text-sm font-medium">Course Name *</label>
              <Input
                value={courseForm.name}
                onChange={(e) =>
                  setCourseForm({ ...courseForm, name: e.target.value })
                }
                placeholder="e.g., Computer Science Engineering"
                className="mt-1"
              />
            </div>
            <div>
              <label className="text-sm font-medium">Course Code *</label>
              <Input
                value={courseForm.code}
                onChange={(e) =>
                  setCourseForm({ ...courseForm, code: e.target.value })
                }
                placeholder="e.g., CSE"
                className="mt-1"
              />
            </div>
            <div className="md:col-span-2">
              <label className="text-sm font-medium">Description</label>
              <textarea
                value={courseForm.description}
                onChange={(e) =>
                  setCourseForm({ ...courseForm, description: e.target.value })
                }
                className="w-full mt-1 px-3 py-2 rounded-lg border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-primary/30"
                rows={2}
                placeholder="Course description..."
              />
            </div>
            <div>
              <label className="text-sm font-medium">Duration (Years)</label>
              <Input
                type="number"
                value={courseForm.duration_years}
                onChange={(e) =>
                  setCourseForm({
                    ...courseForm,
                    duration_years: Number(e.target.value),
                  })
                }
                className="mt-1"
              />
            </div>
            <div>
              <label className="text-sm font-medium">Total Credits</label>
              <Input
                type="number"
                value={courseForm.total_credits}
                onChange={(e) =>
                  setCourseForm({
                    ...courseForm,
                    total_credits: Number(e.target.value),
                  })
                }
                className="mt-1"
              />
            </div>
          </div>
          <div className="flex gap-3 mt-4">
            <Button variant="outline" onClick={() => setShowCourseForm(false)}>
              Cancel
            </Button>
            <Button
              onClick={handleCreateCourse}
              disabled={saving || !courseForm.name || !courseForm.code}
            >
              {saving && <Loader2 className="h-4 w-4 animate-spin mr-2" />}
              Create Course
            </Button>
          </div>
        </div>
      )}

      {/* Course List */}
      <div className="space-y-3">
        {courses.length === 0 ? (
          <div className="glass-card p-12 text-center">
            <GraduationCap className="h-12 w-12 mx-auto text-muted-foreground mb-3" />
            <h3 className="text-lg font-semibold mb-2">No Courses Yet</h3>
            <p className="text-muted-foreground">
              Create your first course to get started.
            </p>
          </div>
        ) : (
          courses.map((course) => (
            <div key={course.id} className="glass-card overflow-hidden">
              {/* Course Header */}
              <button
                onClick={() => toggleExpand(course.id)}
                className="w-full flex items-center justify-between p-5 text-left hover:bg-muted/30 transition"
              >
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-primary/10">
                    <BookOpen className="h-5 w-5 text-primary" />
                  </div>
                  <div>
                    <h3 className="font-semibold">{course.name}</h3>
                    <p className="text-sm text-muted-foreground">
                      Code: {course.code} · Duration: {course.duration_years}{" "}
                      years · Credits: {course.total_credits}
                    </p>
                  </div>
                </div>
                {expandedCourse === course.id ? (
                  <ChevronDown className="h-5 w-5 text-muted-foreground" />
                ) : (
                  <ChevronRight className="h-5 w-5 text-muted-foreground" />
                )}
              </button>

              {/* Subjects */}
              {expandedCourse === course.id && (
                <div className="border-t px-5 py-4 bg-muted/10">
                  <div className="flex items-center justify-between mb-3">
                    <h4 className="font-medium text-sm">Subjects</h4>
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => setShowSubjectForm(course.id)}
                      className="gap-1"
                    >
                      <Plus className="h-3 w-3" /> Add Subject
                    </Button>
                  </div>

                  {/* Add Subject Form */}
                  {showSubjectForm === course.id && (
                    <div className="bg-background border rounded-lg p-4 mb-4">
                      <div className="grid gap-3 md:grid-cols-2">
                        <div>
                          <label className="text-sm font-medium">
                            Subject Name *
                          </label>
                          <Input
                            value={subjectForm.name}
                            onChange={(e) =>
                              setSubjectForm({
                                ...subjectForm,
                                name: e.target.value,
                              })
                            }
                            placeholder="e.g., Data Structures"
                            className="mt-1"
                          />
                        </div>
                        <div>
                          <label className="text-sm font-medium">
                            Subject Code *
                          </label>
                          <Input
                            value={subjectForm.code}
                            onChange={(e) =>
                              setSubjectForm({
                                ...subjectForm,
                                code: e.target.value,
                              })
                            }
                            placeholder="e.g., CS201"
                            className="mt-1"
                          />
                        </div>
                        <div>
                          <label className="text-sm font-medium">Credits</label>
                          <Input
                            type="number"
                            value={subjectForm.credits}
                            onChange={(e) =>
                              setSubjectForm({
                                ...subjectForm,
                                credits: Number(e.target.value),
                              })
                            }
                            className="mt-1"
                          />
                        </div>
                        <div>
                          <label className="text-sm font-medium">
                            Semester
                          </label>
                          <Input
                            type="number"
                            value={subjectForm.semester}
                            onChange={(e) =>
                              setSubjectForm({
                                ...subjectForm,
                                semester: Number(e.target.value),
                              })
                            }
                            className="mt-1"
                          />
                        </div>
                        <div className="flex items-center gap-2 md:col-span-2">
                          <input
                            type="checkbox"
                            id="is_elective"
                            checked={subjectForm.is_elective}
                            onChange={(e) =>
                              setSubjectForm({
                                ...subjectForm,
                                is_elective: e.target.checked,
                              })
                            }
                            className="rounded"
                          />
                          <label htmlFor="is_elective" className="text-sm">
                            Elective Subject
                          </label>
                        </div>
                      </div>
                      <div className="flex gap-2 mt-3">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => setShowSubjectForm(null)}
                        >
                          Cancel
                        </Button>
                        <Button
                          size="sm"
                          onClick={() => handleCreateSubject(course.id)}
                          disabled={
                            saving || !subjectForm.name || !subjectForm.code
                          }
                        >
                          {saving && (
                            <Loader2 className="h-3 w-3 animate-spin mr-1" />
                          )}
                          Add Subject
                        </Button>
                      </div>
                    </div>
                  )}

                  {/* Subject List */}
                  {subjects[course.id]?.length === 0 ? (
                    <p className="text-sm text-muted-foreground py-4">
                      No subjects added yet.
                    </p>
                  ) : (
                    <div className="space-y-2">
                      {(subjects[course.id] || []).map((sub) => (
                        <div
                          key={sub.id}
                          className="flex items-center justify-between p-3 bg-background rounded-lg border"
                        >
                          <div>
                            <p className="font-medium text-sm">{sub.name}</p>
                            <p className="text-xs text-muted-foreground">
                              {sub.code} · {sub.credits} credits · Sem{" "}
                              {sub.semester}
                              {sub.is_elective ? " · Elective" : ""}
                            </p>
                          </div>
                          <span
                            className={`text-xs px-2 py-0.5 rounded-full ${
                              sub.is_active
                                ? "bg-green-100 text-green-700"
                                : "bg-red-100 text-red-700"
                            }`}
                          >
                            {sub.is_active ? "Active" : "Inactive"}
                          </span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}
