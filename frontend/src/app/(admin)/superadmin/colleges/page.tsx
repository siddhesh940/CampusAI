"use client";

import { redirect } from "next/navigation";

// Redirect to universities page (same content)
export default function SuperAdminCollegesRedirect() {
  redirect("/superadmin/universities");
}
