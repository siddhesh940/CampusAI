import { Providers } from "@/components/providers";
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });

export const metadata: Metadata = {
  title: "CampusAI – Smart Student Onboarding Agent for Engineering Colleges",
  description:
    "Streamline your engineering college's onboarding lifecycle with AI-powered automation — document verification, fee payments, hostel allocation, and more.",
  keywords: [
    "engineering college",
    "onboarding",
    "student",
    "SaaS",
    "education",
    "AI",
    "campus",
  ],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.variable} font-sans antialiased`}>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
