import { Footer } from "@/components/landing/footer";
import { Navbar } from "@/components/landing/navbar";

export default function PrivacyPage() {
  return (
    <main className="min-h-screen">
      <Navbar />

      <section className="pt-32 pb-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 className="text-4xl font-bold mb-2">Privacy Policy</h1>
          <p className="text-muted-foreground mb-10">
            Last updated: February 18, 2026
          </p>

          <div className="prose dark:prose-invert max-w-none space-y-6 text-muted-foreground">
            <section>
              <h2 className="text-xl font-semibold text-foreground mb-3">
                1. Information We Collect
              </h2>
              <p>
                CampusAI collects information you provide when registering an
                account — including your name, email address, phone number,
                college name, and any documents uploaded during the onboarding
                process. We also collect usage data such as pages visited,
                features used, and device information.
              </p>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-foreground mb-3">
                2. How We Use Your Information
              </h2>
              <p>
                We use your information to provide and improve the CampusAI
                platform, personalize your onboarding experience, communicate
                important updates, process fee payments, and ensure the security
                of your account.
              </p>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-foreground mb-3">
                3. Data Sharing
              </h2>
              <p>
                Your data is shared only with your enrolled engineering
                college&apos;s administration as required for the onboarding
                process. We do not sell your personal data to third parties. We
                may share anonymized, aggregated data for analytics purposes.
              </p>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-foreground mb-3">
                4. Data Security
              </h2>
              <p>
                We implement industry-standard security measures including
                encryption in transit and at rest, role-based access control,
                and regular security audits. College data is isolated using
                multi-tenant architecture.
              </p>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-foreground mb-3">
                5. Your Rights
              </h2>
              <p>
                You have the right to access, correct, or delete your personal
                data. You may also request data portability or object to
                processing. Contact us at privacy@campusai.in for any
                data-related requests.
              </p>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-foreground mb-3">
                6. Contact Us
              </h2>
              <p>
                If you have questions about this Privacy Policy, please contact
                us at{" "}
                <a
                  href="mailto:privacy@campusai.in"
                  className="text-primary hover:underline"
                >
                  privacy@campusai.in
                </a>
                .
              </p>
            </section>
          </div>
        </div>
      </section>

      <Footer />
    </main>
  );
}
