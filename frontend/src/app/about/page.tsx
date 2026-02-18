"use client";

import { Footer } from "@/components/landing/footer";
import { Navbar } from "@/components/landing/navbar";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import { GraduationCap, Target, Users, Zap } from "lucide-react";
import Link from "next/link";

const values = [
  {
    icon: Target,
    title: "Student-First",
    description:
      "Every feature is designed to simplify the student experience from day one.",
  },
  {
    icon: Zap,
    title: "AI-Powered",
    description:
      "Intelligent automation that answers queries and guides students 24/7.",
  },
  {
    icon: Users,
    title: "College-Centric",
    description:
      "Built specifically for the workflows and needs of engineering colleges.",
  },
];

export default function AboutPage() {
  return (
    <main className="min-h-screen">
      <Navbar />

      {/* Hero */}
      <section className="relative pt-32 pb-20 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-indigo-50 via-white to-purple-50 dark:from-gray-950 dark:via-gray-900 dark:to-indigo-950" />
        <div className="relative max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <GraduationCap className="h-16 w-16 mx-auto text-primary mb-6" />
            <h1 className="text-4xl sm:text-5xl font-bold mb-6">
              About <span className="gradient-text">CampusAI</span>
            </h1>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
              We&apos;re building the future of student onboarding for
              engineering colleges — replacing fragmented manual processes with
              a single AI-powered platform.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Mission */}
      <section className="py-20">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
            >
              <h2 className="text-3xl font-bold mb-4">Our Mission</h2>
              <p className="text-muted-foreground leading-relaxed mb-4">
                Engineering colleges manage a complex student onboarding
                lifecycle — from admission through the first academic year.
                Students struggle with fragmented information about document
                verification, fee payments, course registration, hostel
                allocation, and compliance training.
              </p>
              <p className="text-muted-foreground leading-relaxed">
                CampusAI solves this with an intelligent onboarding agent that
                provides personalized, timely, and context-aware guidance at
                every stage. We reduce onboarding from weeks to days while
                cutting administrative workload by 80%.
              </p>
            </motion.div>
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
              className="glass-card p-8 rounded-2xl"
            >
              <div className="grid grid-cols-2 gap-6 text-center">
                <div>
                  <div className="text-3xl font-bold gradient-text">50+</div>
                  <div className="text-sm text-muted-foreground mt-1">
                    Engineering Colleges
                  </div>
                </div>
                <div>
                  <div className="text-3xl font-bold gradient-text">
                    10,000+
                  </div>
                  <div className="text-sm text-muted-foreground mt-1">
                    Students Onboarded
                  </div>
                </div>
                <div>
                  <div className="text-3xl font-bold gradient-text">80%</div>
                  <div className="text-sm text-muted-foreground mt-1">
                    Less Admin Work
                  </div>
                </div>
                <div>
                  <div className="text-3xl font-bold gradient-text">3 Days</div>
                  <div className="text-sm text-muted-foreground mt-1">
                    Avg. Onboarding
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Values */}
      <section className="py-20 bg-muted/30">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12">
            Our <span className="gradient-text">Values</span>
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            {values.map((v, i) => (
              <motion.div
                key={v.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: i * 0.15 }}
                viewport={{ once: true }}
                className="glass-card p-6 text-center"
              >
                <div className="w-12 h-12 gradient-bg rounded-xl flex items-center justify-center mx-auto mb-4">
                  <v.icon className="w-6 h-6 text-white" />
                </div>
                <h3 className="font-semibold text-lg mb-2">{v.title}</h3>
                <p className="text-sm text-muted-foreground">{v.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20">
        <div className="max-w-3xl mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-4">
            Want to transform your college&apos;s onboarding?
          </h2>
          <p className="text-muted-foreground mb-8">
            Get started with CampusAI today — free for up to 500 students.
          </p>
          <Button variant="gradient" size="lg" asChild>
            <Link href="/register">Get Started Free</Link>
          </Button>
        </div>
      </section>

      <Footer />
    </main>
  );
}
