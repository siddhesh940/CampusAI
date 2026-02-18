"use client";

import { motion } from "framer-motion";
import {
    BookOpen,
    Bot,
    Building2,
    Calendar,
    ClipboardCheck,
    CreditCard,
    FileCheck,
    GraduationCap,
    Users,
} from "lucide-react";

const features = [
  {
    icon: FileCheck,
    title: "Document Verification",
    description:
      "Upload, track, and get real-time verification status for all onboarding documents — mark-sheets, ID proofs, and more.",
  },
  {
    icon: CreditCard,
    title: "Fee Payment",
    description:
      "Seamless fee payment tracking with automated receipts, deadline reminders, and installment support.",
  },
  {
    icon: BookOpen,
    title: "Course Registration",
    description:
      "Browse available courses, register for electives, and get your final course list — all guided by the AI agent.",
  },
  {
    icon: Calendar,
    title: "Timetable Access",
    description:
      "Auto-generated personal timetable based on registered courses, sections, and lab batches.",
  },
  {
    icon: GraduationCap,
    title: "LMS Onboarding",
    description:
      "One-click activation of your college LMS account with enrolled courses and study materials ready to go.",
  },
  {
    icon: Building2,
    title: "Hostel Allocation",
    description:
      "Apply for hostel rooms, rank preferences, and track allocation status with instant notifications.",
  },
  {
    icon: Users,
    title: "Mentoring & Guidance",
    description:
      "Get matched with faculty mentors and senior student buddies for a smooth academic transition.",
  },
  {
    icon: ClipboardCheck,
    title: "Compliance Training",
    description:
      "Complete mandatory orientation modules — anti-ragging, code of conduct, lab safety — tracked automatically.",
  },
  {
    icon: Bot,
    title: "AI Onboarding Agent",
    description:
      "24/7 intelligent assistant that answers queries, sends reminders, and guides students through every onboarding step.",
  },
];

export function FeaturesSection() {
  return (
    <section id="features" className="py-24 bg-muted/30">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold mb-4">
            Everything you need for
            <span className="gradient-text"> seamless onboarding</span>
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Covering every step of the student onboarding lifecycle — from
            admission to campus-ready — as described in the engineering college
            onboarding challenge.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              viewport={{ once: true }}
              className="glass-card p-6 hover:shadow-xl transition-shadow"
            >
              <div className="w-12 h-12 gradient-bg rounded-xl flex items-center justify-center mb-4">
                <feature.icon className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-lg font-semibold mb-2">{feature.title}</h3>
              <p className="text-muted-foreground text-sm">
                {feature.description}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
