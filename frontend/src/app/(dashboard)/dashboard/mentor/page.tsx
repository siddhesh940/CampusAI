"use client";

import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import {
    mentorService,
    type MentorMeeting,
    type MentorMessage,
    type MentorProfile,
} from "@/services/campus-services";
import {
    Calendar,
    Loader2,
    Mail,
    MessageCircle,
    Send,
    User,
    Video,
} from "lucide-react";
import { useEffect, useRef, useState } from "react";
export default function MentorPage() {
  const [mentor, setMentor] = useState<MentorProfile | null>(null);
  const [messages, setMessages] = useState<MentorMessage[]>([]);
  const [meetings, setMeetings] = useState<MentorMeeting[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [tab, setTab] = useState<"info" | "chat" | "meetings">("info");
  const [newMsg, setNewMsg] = useState("");
  const [sending, setSending] = useState(false);
  const [showBookModal, setShowBookModal] = useState(false);
  const [booking, setBooking] = useState(false);
  const [meetingForm, setMeetingForm] = useState({
    title: "",
    description: "",
    meeting_date: "",
    start_time: "",
    end_time: "",
  });
  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    loadMentor();
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const loadMentor = async () => {
    setLoading(true);
    try {
      const profile = await mentorService.getMyMentor();
      setMentor(profile);
      // Load messages
      if (profile.assignment_id) {
        const [msgRes, mtgRes] = await Promise.all([
          mentorService.getMessages(profile.assignment_id),
          mentorService.listMeetings(),
        ]);
        setMessages(msgRes.messages);
        setMeetings(mtgRes.meetings);
      }
    } catch (e: any) {
      if (e.message?.includes("404")) {
        setError("no_mentor");
      } else {
        setError(e.message);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleSend = async () => {
    if (!newMsg.trim() || !mentor) return;
    setSending(true);
    try {
      const msg = await mentorService.sendMessage(mentor.assignment_id, newMsg);
      setMessages((prev) => [...prev, msg]);
      setNewMsg("");
    } catch (e: any) {
      alert(e.message);
    } finally {
      setSending(false);
    }
  };

  const handleBookMeeting = async () => {
    if (
      !meetingForm.title ||
      !meetingForm.meeting_date ||
      !meetingForm.start_time
    )
      return;
    setBooking(true);
    try {
      const meeting = await mentorService.bookMeeting(meetingForm);
      setMeetings((prev) => [meeting, ...prev]);
      setShowBookModal(false);
      setMeetingForm({
        title: "",
        description: "",
        meeting_date: "",
        start_time: "",
        end_time: "",
      });
    } catch (e: any) {
      alert(e.message);
    } finally {
      setBooking(false);
    }
  };

  const statusColor = (s: string) => {
    switch (s) {
      case "approved":
        return "text-green-600 bg-green-100";
      case "rejected":
      case "cancelled":
        return "text-red-600 bg-red-100";
      case "completed":
        return "text-blue-600 bg-blue-100";
      default:
        return "text-yellow-600 bg-yellow-100";
    }
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-9 w-48" />
        <Skeleton className="h-48 w-full" />
        <Skeleton className="h-64 w-full" />
      </div>
    );
  }

  if (error === "no_mentor") {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center glass-card p-12">
          <User className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
          <h3 className="text-lg font-semibold mb-2">No Mentor Assigned</h3>
          <p className="text-muted-foreground">
            Your mentor will be assigned by the admin. Check back later.
          </p>
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
      <h1 className="text-2xl font-bold flex items-center gap-2">
        <User className="h-6 w-6 text-primary" />
        My Mentor
      </h1>

      {/* Mentor Card */}
      {mentor && (
        <div className="glass-card p-6">
          <div className="flex items-start gap-4">
            <div className="h-14 w-14 rounded-full bg-primary/10 flex items-center justify-center">
              <User className="h-7 w-7 text-primary" />
            </div>
            <div className="flex-1">
              <h2 className="text-xl font-bold">{mentor.mentor_name}</h2>
              <p className="text-muted-foreground flex items-center gap-1 mt-1">
                <Mail className="h-3.5 w-3.5" /> {mentor.mentor_email}
              </p>
              <div className="flex gap-4 mt-3 text-sm">
                <span className="text-muted-foreground">
                  Assigned: {new Date(mentor.assigned_at).toLocaleDateString()}
                </span>
                {mentor.unread_messages > 0 && (
                  <span className="text-primary font-medium">
                    {mentor.unread_messages} unread messages
                  </span>
                )}
              </div>
            </div>
            <Button onClick={() => setShowBookModal(true)} className="gap-2">
              <Video className="h-4 w-4" /> Book Meeting
            </Button>
          </div>
        </div>
      )}

      {/* Tabs */}
      <div className="flex gap-1 bg-muted p-1 rounded-lg w-fit">
        {(["info", "chat", "meetings"] as const).map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`px-4 py-2 text-sm font-medium rounded-md transition ${
              tab === t
                ? "bg-background shadow text-foreground"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            {t === "info" ? "Overview" : t === "chat" ? "Chat" : "Meetings"}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      {tab === "info" && mentor && (
        <div className="grid gap-4 md:grid-cols-2">
          <div className="glass-card p-5">
            <h3 className="font-semibold mb-3 flex items-center gap-2">
              <Calendar className="h-4 w-4 text-primary" /> Upcoming Meetings
            </h3>
            {mentor.upcoming_meetings.length === 0 ? (
              <p className="text-sm text-muted-foreground">
                No upcoming meetings
              </p>
            ) : (
              <div className="space-y-2">
                {mentor.upcoming_meetings.map((m) => (
                  <div key={m.id} className="p-3 bg-muted/50 rounded-lg">
                    <p className="font-medium text-sm">{m.title}</p>
                    <p className="text-xs text-muted-foreground mt-1">
                      {m.meeting_date} at {m.start_time?.slice(0, 5)}
                    </p>
                    <span
                      className={`text-xs px-2 py-0.5 rounded-full mt-1 inline-block ${statusColor(m.status)}`}
                    >
                      {m.status}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>
          <div className="glass-card p-5">
            <h3 className="font-semibold mb-3 flex items-center gap-2">
              <MessageCircle className="h-4 w-4 text-primary" /> Quick Stats
            </h3>
            <div className="space-y-3">
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Total Meetings</span>
                <span className="font-medium">{meetings.length}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Messages</span>
                <span className="font-medium">{messages.length}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Unread</span>
                <span className="font-medium text-primary">
                  {mentor.unread_messages}
                </span>
              </div>
            </div>
          </div>
        </div>
      )}

      {tab === "chat" && mentor && (
        <div className="glass-card flex flex-col h-[500px]">
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {messages.length === 0 ? (
              <div className="flex items-center justify-center h-full text-muted-foreground text-sm">
                No messages yet. Start a conversation!
              </div>
            ) : (
              messages.map((msg) => {
                const isMe = msg.sender_id !== mentor.mentor_id;
                return (
                  <div
                    key={msg.id}
                    className={`flex ${isMe ? "justify-end" : "justify-start"}`}
                  >
                    <div
                      className={`max-w-[70%] px-4 py-2.5 rounded-2xl text-sm ${
                        isMe
                          ? "bg-primary text-primary-foreground rounded-br-md"
                          : "bg-muted rounded-bl-md"
                      }`}
                    >
                      <p>{msg.content}</p>
                      <p
                        className={`text-[10px] mt-1 ${isMe ? "text-primary-foreground/70" : "text-muted-foreground"}`}
                      >
                        {new Date(msg.created_at).toLocaleTimeString([], {
                          hour: "2-digit",
                          minute: "2-digit",
                        })}
                      </p>
                    </div>
                  </div>
                );
              })
            )}
            <div ref={chatEndRef} />
          </div>
          <div className="border-t p-3 flex gap-2">
            <input
              type="text"
              value={newMsg}
              onChange={(e) => setNewMsg(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSend()}
              placeholder="Type a message..."
              className="flex-1 px-4 py-2 rounded-lg border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-primary/30"
            />
            <Button
              onClick={handleSend}
              disabled={sending || !newMsg.trim()}
              size="sm"
            >
              {sending ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Send className="h-4 w-4" />
              )}
            </Button>
          </div>
        </div>
      )}

      {tab === "meetings" && (
        <div className="space-y-3">
          {meetings.length === 0 ? (
            <div className="glass-card p-12 text-center">
              <Calendar className="h-10 w-10 mx-auto text-muted-foreground mb-3" />
              <p className="text-muted-foreground">No meetings yet</p>
            </div>
          ) : (
            meetings.map((m) => (
              <div
                key={m.id}
                className="glass-card p-4 flex items-center gap-4"
              >
                <div className="h-10 w-10 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0">
                  <Video className="h-5 w-5 text-primary" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-sm">{m.title}</p>
                  <p className="text-xs text-muted-foreground mt-0.5">
                    {m.meeting_date} &middot; {m.start_time?.slice(0, 5)}
                    {m.end_time ? ` - ${m.end_time.slice(0, 5)}` : ""}
                  </p>
                </div>
                <span
                  className={`text-xs px-2.5 py-1 rounded-full font-medium ${statusColor(m.status)}`}
                >
                  {m.status}
                </span>
                {m.meeting_link && m.status === "approved" && (
                  <a
                    href={m.meeting_link}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <Button size="sm" variant="outline" className="gap-1">
                      <Video className="h-3 w-3" /> Join
                    </Button>
                  </a>
                )}
              </div>
            ))
          )}
        </div>
      )}

      {/* Book Meeting Modal */}
      {showBookModal && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-background rounded-xl p-6 w-full max-w-md shadow-lg">
            <h3 className="text-lg font-bold mb-4">Book a Meeting</h3>
            <div className="space-y-3">
              <div>
                <label className="text-sm font-medium">Title *</label>
                <input
                  type="text"
                  value={meetingForm.title}
                  onChange={(e) =>
                    setMeetingForm({ ...meetingForm, title: e.target.value })
                  }
                  className="w-full mt-1 px-3 py-2 rounded-lg border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-primary/30"
                  placeholder="Discussion topic"
                />
              </div>
              <div>
                <label className="text-sm font-medium">Description</label>
                <textarea
                  value={meetingForm.description}
                  onChange={(e) =>
                    setMeetingForm({
                      ...meetingForm,
                      description: e.target.value,
                    })
                  }
                  className="w-full mt-1 px-3 py-2 rounded-lg border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-primary/30"
                  rows={2}
                  placeholder="What do you want to discuss?"
                />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-sm font-medium">Date *</label>
                  <input
                    type="date"
                    value={meetingForm.meeting_date}
                    onChange={(e) =>
                      setMeetingForm({
                        ...meetingForm,
                        meeting_date: e.target.value,
                      })
                    }
                    className="w-full mt-1 px-3 py-2 rounded-lg border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-primary/30"
                    title="Meeting date"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium">Start Time *</label>
                  <input
                    type="time"
                    value={meetingForm.start_time}
                    onChange={(e) =>
                      setMeetingForm({
                        ...meetingForm,
                        start_time: e.target.value,
                      })
                    }
                    className="w-full mt-1 px-3 py-2 rounded-lg border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-primary/30"
                    title="Start time"
                  />
                </div>
              </div>
              <div className="flex gap-3 mt-4">
                <Button
                  variant="outline"
                  className="flex-1"
                  onClick={() => setShowBookModal(false)}
                >
                  Cancel
                </Button>
                <Button
                  className="flex-1"
                  onClick={handleBookMeeting}
                  disabled={
                    booking ||
                    !meetingForm.title ||
                    !meetingForm.meeting_date ||
                    !meetingForm.start_time
                  }
                >
                  {booking ? (
                    <Loader2 className="h-4 w-4 animate-spin mr-2" />
                  ) : null}
                  Book Meeting
                </Button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
