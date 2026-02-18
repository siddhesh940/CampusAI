"use client";

import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import {
  timetableService,
  type WeeklyTimetableResponse,
} from "@/services/campus-services";
import {
  Calendar,
  Clock,
  Download,
  MapPin,
  User,
  BookOpen,
} from "lucide-react";
import { useEffect, useState } from "react";

const DAY_LABELS: Record<string, string> = {
  monday: "Monday",
  tuesday: "Tuesday",
  wednesday: "Wednesday",
  thursday: "Thursday",
  friday: "Friday",
  saturday: "Saturday",
};

export default function TimetablePage() {
  const [timetable, setTimetable] = useState<WeeklyTimetableResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    timetableService
      .getWeekly()
      .then(setTimetable)
      .catch((e: any) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  const handleDownloadPDF = () => {
    if (!timetable) return;
    // Generate printable timetable
    const printWindow = window.open("", "_blank");
    if (!printWindow) return;

    let html = `<!DOCTYPE html><html><head><title>Weekly Timetable</title>
    <style>
      body { font-family: Arial, sans-serif; padding: 20px; }
      h1 { text-align: center; color: #1a1a2e; }
      table { width: 100%; border-collapse: collapse; margin-top: 20px; }
      th, td { border: 1px solid #ddd; padding: 10px; text-align: left; font-size: 13px; }
      th { background-color: #1a1a2e; color: white; }
      .empty { color: #999; font-style: italic; }
      .stats { display: flex; gap: 30px; margin-top: 10px; font-size: 14px; color: #555; }
      @media print { body { padding: 0; } }
    </style></head><body>
    <h1>📅 Weekly Timetable</h1>
    <div class="stats">
      <span><strong>Subjects:</strong> ${timetable.total_subjects}</span>
      <span><strong>Total Hours:</strong> ${timetable.total_hours}h/week</span>
    </div>
    <table><thead><tr><th>Day</th><th>Time</th><th>Subject</th><th>Code</th><th>Room</th><th>Instructor</th></tr></thead><tbody>`;

    for (const day of timetable.days) {
      if (day.entries.length === 0) {
        html += `<tr><td><strong>${DAY_LABELS[day.day]}</strong></td><td colspan="5" class="empty">No classes</td></tr>`;
      } else {
        day.entries.forEach((entry, i) => {
          html += `<tr>
            ${i === 0 ? `<td rowspan="${day.entries.length}"><strong>${DAY_LABELS[day.day]}</strong></td>` : ""}
            <td>${entry.start_time} - ${entry.end_time}</td>
            <td>${entry.subject_name}</td>
            <td>${entry.subject_code}</td>
            <td>${entry.room || "-"}</td>
            <td>${entry.instructor || "-"}</td>
          </tr>`;
        });
      }
    }
    html += `</tbody></table></body></html>`;
    printWindow.document.write(html);
    printWindow.document.close();
    printWindow.print();
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-9 w-48" />
        <div className="grid gap-4">
          {[...Array(6)].map((_, i) => (
            <Skeleton key={i} className="h-24 w-full" />
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <p className="text-destructive mb-2">{error}</p>
          <Button onClick={() => window.location.reload()}>Retry</Button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold flex items-center gap-2">
            <Calendar className="h-6 w-6 text-primary" />
            Weekly Timetable
          </h1>
          <p className="text-muted-foreground mt-1">
            Your class schedule based on enrolled subjects
          </p>
        </div>
        {timetable && timetable.total_subjects > 0 && (
          <Button onClick={handleDownloadPDF} variant="outline" className="gap-2">
            <Download className="h-4 w-4" />
            Download PDF
          </Button>
        )}
      </div>

      {/* Stats */}
      {timetable && (
        <div className="grid grid-cols-2 gap-4">
          <div className="glass-card p-4 flex items-center gap-3">
            <div className="p-2 rounded-lg bg-primary/10">
              <BookOpen className="h-5 w-5 text-primary" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Enrolled Subjects</p>
              <p className="text-xl font-bold">{timetable.total_subjects}</p>
            </div>
          </div>
          <div className="glass-card p-4 flex items-center gap-3">
            <div className="p-2 rounded-lg bg-orange-500/10">
              <Clock className="h-5 w-5 text-orange-500" />
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Hours/Week</p>
              <p className="text-xl font-bold">{timetable.total_hours}h</p>
            </div>
          </div>
        </div>
      )}

      {/* Timetable Grid */}
      {timetable && timetable.total_subjects === 0 ? (
        <div className="glass-card p-12 text-center">
          <Calendar className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
          <h3 className="text-lg font-semibold mb-2">No Timetable Available</h3>
          <p className="text-muted-foreground">
            Enroll in subjects from the Courses page to see your timetable.
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {timetable?.days.map((day) => (
            <div key={day.day} className="glass-card overflow-hidden">
              <div className="bg-primary/5 px-4 py-2.5 border-b">
                <h3 className="font-semibold text-sm uppercase tracking-wide">
                  {DAY_LABELS[day.day]}
                </h3>
              </div>
              {day.entries.length === 0 ? (
                <div className="px-4 py-6 text-center text-sm text-muted-foreground">
                  No classes scheduled
                </div>
              ) : (
                <div className="divide-y">
                  {day.entries.map((entry) => (
                    <div
                      key={entry.schedule_id}
                      className="px-4 py-3 flex items-center gap-4 hover:bg-muted/30 transition"
                    >
                      <div className="flex items-center gap-2 w-36 flex-shrink-0">
                        <Clock className="h-3.5 w-3.5 text-muted-foreground" />
                        <span className="text-sm font-medium">
                          {entry.start_time?.slice(0, 5)} - {entry.end_time?.slice(0, 5)}
                        </span>
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="font-medium text-sm truncate">
                          {entry.subject_name}
                        </p>
                        <p className="text-xs text-muted-foreground">
                          {entry.subject_code}
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
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
