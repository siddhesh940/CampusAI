"use client";

import { motion } from "framer-motion";

const steps = [
  {
    step: "01",
    title: "Admission Confirmed",
    description:
      "Student receives their admission letter. The AI agent sends a welcome message and personalized onboarding checklist.",
  },
  {
    step: "02",
    title: "Verify & Pay",
    description:
      "Upload documents for verification, pay fees online, and apply for hostel — the agent tracks every deadline.",
  },
  {
    step: "03",
    title: "Register & Setup",
    description:
      "Register for courses, access your timetable, activate LMS, and complete compliance training — all in one place.",
  },
  {
    step: "04",
    title: "Campus Ready",
    description:
      "Meet your mentor, join student groups, and walk into college fully prepared. The agent stays available all year.",
  },
];

export function HowItWorksSection() {
  return (
    <section id="how-it-works" className="py-24">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold mb-4">
            How <span className="gradient-text">CampusAI</span> Works
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Four simple steps from registration to campus-ready.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {steps.map((step, index) => (
            <motion.div
              key={step.step}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.15 }}
              viewport={{ once: true }}
              className="text-center"
            >
              <div className="text-5xl font-bold gradient-text mb-4">
                {step.step}
              </div>
              <h3 className="text-lg font-semibold mb-2">{step.title}</h3>
              <p className="text-muted-foreground text-sm">
                {step.description}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
