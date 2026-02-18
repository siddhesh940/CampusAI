"use client";

import { Footer } from "@/components/landing/footer";
import { Navbar } from "@/components/landing/navbar";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import { ArrowRight, Calendar } from "lucide-react";
import Link from "next/link";

const posts = [
  {
    title: "How AI is Transforming Student Onboarding in Engineering Colleges",
    excerpt:
      "Discover how intelligent automation can reduce onboarding time from weeks to days while improving student satisfaction.",
    date: "Feb 15, 2026",
    category: "AI & Education",
    slug: "#",
  },
  {
    title: "5 Onboarding Challenges Every Engineering College Faces",
    excerpt:
      "From document chaos to hostel allocation bottlenecks — here are the top pain points and how to solve them.",
    date: "Feb 10, 2026",
    category: "Insights",
    slug: "#",
  },
  {
    title: "Building a Seamless Document Verification Workflow",
    excerpt:
      "Learn how CampusAI automates document uploads, verification, and approval with real-time status tracking.",
    date: "Feb 5, 2026",
    category: "Product",
    slug: "#",
  },
  {
    title: "Case Study: How VJTI Cut Onboarding Time by 85%",
    excerpt:
      "A deep dive into how one of Mumbai's top engineering colleges transformed their onboarding process with CampusAI.",
    date: "Jan 28, 2026",
    category: "Case Study",
    slug: "#",
  },
  {
    title: "The Complete Guide to Fee Payment Automation",
    excerpt:
      "Streamline fee collection, generate receipts automatically, and give students real-time payment status updates.",
    date: "Jan 20, 2026",
    category: "Product",
    slug: "#",
  },
  {
    title: "Why Engineering Colleges Need a Smart Onboarding Agent",
    excerpt:
      "Manual processes, multiple portals, delayed communication — it's time for an intelligent solution.",
    date: "Jan 12, 2026",
    category: "Industry",
    slug: "#",
  },
];

export default function BlogPage() {
  return (
    <main className="min-h-screen">
      <Navbar />

      <section className="relative pt-32 pb-12 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-indigo-50 via-white to-purple-50 dark:from-gray-950 dark:via-gray-900 dark:to-indigo-950" />
        <div className="relative max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h1 className="text-4xl sm:text-5xl font-bold mb-4">
              CampusAI <span className="gradient-text">Blog</span>
            </h1>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Insights, updates, and best practices for student onboarding in
              engineering colleges.
            </p>
          </motion.div>
        </div>
      </section>

      <section className="py-16">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {posts.map((post, i) => (
              <motion.article
                key={post.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: i * 0.1 }}
                viewport={{ once: true }}
                className="glass-card rounded-2xl overflow-hidden group hover:shadow-xl transition-shadow"
              >
                <div className="h-40 gradient-bg opacity-80 flex items-center justify-center">
                  <span className="text-white/60 text-sm font-medium px-3 py-1 rounded-full border border-white/20">
                    {post.category}
                  </span>
                </div>
                <div className="p-6">
                  <div className="flex items-center gap-2 text-xs text-muted-foreground mb-3">
                    <Calendar className="h-3 w-3" />
                    {post.date}
                  </div>
                  <h3 className="font-semibold text-lg mb-2 group-hover:text-primary transition-colors line-clamp-2">
                    {post.title}
                  </h3>
                  <p className="text-sm text-muted-foreground mb-4 line-clamp-3">
                    {post.excerpt}
                  </p>
                  <Link
                    href={post.slug}
                    className="inline-flex items-center gap-1 text-sm text-primary font-medium hover:gap-2 transition-all"
                  >
                    Read More <ArrowRight className="h-3 w-3" />
                  </Link>
                </div>
              </motion.article>
            ))}
          </div>
        </div>
      </section>

      <section className="py-16 bg-muted/30">
        <div className="max-w-3xl mx-auto px-4 text-center">
          <h2 className="text-2xl font-bold mb-4">Stay Updated</h2>
          <p className="text-muted-foreground mb-6">
            Get the latest insights on student onboarding delivered to your
            inbox.
          </p>
          <div className="flex flex-col sm:flex-row gap-3 max-w-md mx-auto">
            <input
              type="email"
              placeholder="you@college.edu"
              className="flex-1 h-12 px-4 rounded-xl border border-input bg-background text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
            />
            <Button variant="gradient" size="lg">
              Subscribe
            </Button>
          </div>
        </div>
      </section>

      <Footer />
    </main>
  );
}
