"use client";

import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import {
    BookOpen,
    Building2,
    Calendar,
    ChevronLeft,
    CreditCard,
    FileText,
    GraduationCap,
    LayoutDashboard,
    MessageCircle,
    ShieldCheck,
    User,
    Users,
} from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";

interface SidebarProps {
  variant?: "student" | "admin" | "superadmin";
}

const studentLinks = [
  { label: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  { label: "Documents", href: "/dashboard/documents", icon: FileText },
  { label: "Payments", href: "/dashboard/payments", icon: CreditCard },
  { label: "Courses", href: "/dashboard/courses", icon: GraduationCap },
  { label: "Timetable", href: "/dashboard/timetable", icon: Calendar },
  { label: "Hostel", href: "/dashboard/hostel", icon: Building2 },
  { label: "LMS", href: "/dashboard/lms", icon: BookOpen },
  { label: "Mentor", href: "/dashboard/mentor", icon: Users },
  { label: "Compliance", href: "/dashboard/compliance", icon: ShieldCheck },
  { label: "AI Chat", href: "/dashboard/chat", icon: MessageCircle },
  { label: "Profile", href: "/dashboard/profile", icon: User },
];

const adminLinks = [
  { label: "Dashboard", href: "/admin", icon: LayoutDashboard },
  { label: "Students", href: "/admin/students", icon: Users },
  { label: "Documents", href: "/admin/documents", icon: FileText },
  { label: "Courses", href: "/admin/courses", icon: GraduationCap },
  { label: "Timetable", href: "/admin/timetable", icon: Calendar },
  { label: "Hostel", href: "/admin/hostel", icon: Building2 },
  { label: "Mentors", href: "/admin/mentors", icon: Users },
  { label: "Compliance", href: "/admin/compliance", icon: ShieldCheck },
  { label: "LMS", href: "/admin/lms", icon: BookOpen },
  { label: "Payments", href: "/admin/payments", icon: CreditCard },
];

const superAdminLinks = [
  { label: "Dashboard", href: "/superadmin", icon: LayoutDashboard },
  {
    label: "Colleges",
    href: "/superadmin/colleges",
    icon: GraduationCap,
  },
  {
    label: "Subscriptions",
    href: "/superadmin/subscriptions",
    icon: CreditCard,
  },
];

export function Sidebar({ variant = "student" }: SidebarProps) {
  const pathname = usePathname();
  const [collapsed, setCollapsed] = useState(false);

  const links =
    variant === "superadmin"
      ? superAdminLinks
      : variant === "admin"
        ? adminLinks
        : studentLinks;

  return (
    <aside
      className={cn(
        "h-screen sticky top-0 border-r bg-card flex flex-col transition-all duration-300",
        collapsed ? "w-16" : "w-64",
      )}
    >
      {/* Logo */}
      <div className="h-16 flex items-center gap-2 px-4 border-b">
        <GraduationCap className="h-6 w-6 text-primary flex-shrink-0" />
        {!collapsed && <span className="font-bold text-lg">CampusAI</span>}
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto py-4 px-2 space-y-1">
        {links.map((link) => {
          const isActive =
            pathname === link.href ||
            (link.href !== "/dashboard" &&
              link.href !== "/admin" &&
              link.href !== "/superadmin" &&
              pathname.startsWith(link.href));

          return (
            <Link
              key={link.href}
              href={link.href}
              className={cn(
                "flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors",
                isActive
                  ? "bg-primary/10 text-primary"
                  : "text-muted-foreground hover:bg-muted hover:text-foreground",
              )}
            >
              <link.icon className="h-4 w-4 flex-shrink-0" />
              {!collapsed && link.label}
            </Link>
          );
        })}
      </nav>

      {/* Collapse toggle */}
      <div className="border-t p-2">
        <Button
          variant="ghost"
          size="sm"
          className="w-full justify-center"
          onClick={() => setCollapsed(!collapsed)}
        >
          <ChevronLeft
            className={cn(
              "h-4 w-4 transition-transform",
              collapsed && "rotate-180",
            )}
          />
        </Button>
      </div>
    </aside>
  );
}
