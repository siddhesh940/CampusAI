"use client";

import { Footer } from "@/components/landing/footer";
import { Navbar } from "@/components/landing/navbar";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import { ArrowRight, MapPin } from "lucide-react";
import Link from "next/link";

const openings = [
  {
    title: "Full-Stack Developer",
    department: "Engineering",
    location: "Remote / Mumbai",
    type: "Full-time",
  },
  {
    title: "AI/ML Engineer",
    department: "AI Team",
    location: "Remote / Pune",
    type: "Full-time",
  },
  {
    title: "Product Designer (UI/UX)",
    department: "Design",
    location: "Remote",
    type: "Full-time",
  },
  {
    title: "DevOps Engineer",
    department: "Infrastructure",
    location: "Remote / Bangalore",
    type: "Full-time",
  },
  {
    title: "Customer Success Manager",
    department: "Sales",
    location: "Mumbai",
    type: "Full-time",
  },
];

export default function CareersPage() {
  return (
    <main className="min-h-screen">
      <Navbar />

      <section className="relative pt-32 pb-16 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-indigo-50 via-white to-purple-50 dark:from-gray-950 dark:via-gray-900 dark:to-indigo-950" />
        <div className="relative max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h1 className="text-4xl sm:text-5xl font-bold mb-4">
              Join the <span className="gradient-text">CampusAI</span> Team
            </h1>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Help us transform student onboarding for engineering colleges
              across India. We&apos;re building something impactful — come be a
              part of it.
            </p>
          </motion.div>
        </div>
      </section>

      <section className="py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-2xl font-bold mb-8">
            Open Positions{" "}
            <span className="text-muted-foreground font-normal text-lg">
              ({openings.length})
            </span>
          </h2>
          <div className="space-y-4">
            {openings.map((job, i) => (
              <motion.div
                key={job.title}
                initial={{ opacity: 0, y: 10 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: i * 0.1 }}
                viewport={{ once: true }}
                className="glass-card rounded-xl p-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4 hover:shadow-lg transition-shadow"
              >
                <div>
                  <h3 className="font-semibold text-lg">{job.title}</h3>
                  <div className="flex flex-wrap items-center gap-3 mt-2 text-sm text-muted-foreground">
                    <span className="px-2 py-0.5 rounded-full bg-primary/10 text-primary text-xs font-medium">
                      {job.department}
                    </span>
                    <span className="flex items-center gap-1">
                      <MapPin className="h-3 w-3" /> {job.location}
                    </span>
                    <span>{job.type}</span>
                  </div>
                </div>
                <Button variant="outline" size="sm" className="flex-shrink-0">
                  Apply <ArrowRight className="ml-1 h-3 w-3" />
                </Button>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      <section className="py-16 bg-muted/30">
        <div className="max-w-3xl mx-auto px-4 text-center">
          <h2 className="text-2xl font-bold mb-4">
            Don&apos;t see the right role?
          </h2>
          <p className="text-muted-foreground mb-6">
            We&apos;re always looking for talented people. Send us your resume
            and we&apos;ll reach out when something fits.
          </p>
          <Button variant="gradient" size="lg" asChild>
            <Link href="/contact">Get in Touch</Link>
          </Button>
        </div>
      </section>

      <Footer />
    </main>
  );
}
