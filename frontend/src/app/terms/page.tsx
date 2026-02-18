import { Footer } from "@/components/landing/footer";
import { Navbar } from "@/components/landing/navbar";

export default function TermsPage() {
  return (
    <main className="min-h-screen">
      <Navbar />

      <section className="pt-32 pb-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 className="text-4xl font-bold mb-2">Terms of Service</h1>
          <p className="text-muted-foreground mb-10">
            Last updated: February 18, 2026
          </p>

          <div className="prose dark:prose-invert max-w-none space-y-6 text-muted-foreground">
            <section>
              <h2 className="text-xl font-semibold text-foreground mb-3">
                1. Acceptance of Terms
              </h2>
              <p>
                By accessing or using CampusAI, you agree to be bound by these
                Terms of Service. If you do not agree, please do not use the
                platform. These terms apply to all users, including students,
                administrators, and college staff.
              </p>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-foreground mb-3">
                2. Description of Service
              </h2>
              <p>
                CampusAI is a smart student onboarding platform for engineering
                colleges. It provides AI-powered onboarding workflows, document
                management, fee payment tracking, hostel allocation, course
                registration, and an AI assistant to guide students throughout
                the onboarding lifecycle.
              </p>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-foreground mb-3">
                3. User Accounts
              </h2>
              <p>
                You are responsible for maintaining the confidentiality of your
                account credentials. You must provide accurate information
                during registration. You agree to notify us immediately of any
                unauthorized use of your account.
              </p>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-foreground mb-3">
                4. Acceptable Use
              </h2>
              <p>
                You agree not to misuse the platform, upload malicious content,
                attempt to access unauthorized data, or interfere with the
                service. Uploaded documents must be genuine and belong to the
                registering student.
              </p>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-foreground mb-3">
                5. Intellectual Property
              </h2>
              <p>
                All content, design, and technology of CampusAI are owned by us.
                You retain ownership of documents and data you upload. By using
                the platform, you grant us a license to process your data for
                service delivery purposes.
              </p>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-foreground mb-3">
                6. Limitation of Liability
              </h2>
              <p>
                CampusAI is provided &quot;as is&quot; without warranties of any
                kind. We are not liable for any indirect, incidental, or
                consequential damages arising from your use of the platform.
              </p>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-foreground mb-3">
                7. Contact
              </h2>
              <p>
                For questions regarding these terms, contact{" "}
                <a
                  href="mailto:legal@campusai.in"
                  className="text-primary hover:underline"
                >
                  legal@campusai.in
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
