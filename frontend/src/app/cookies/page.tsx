import { Footer } from "@/components/landing/footer";
import { Navbar } from "@/components/landing/navbar";

export default function CookiesPage() {
  return (
    <main className="min-h-screen">
      <Navbar />

      <section className="pt-32 pb-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 className="text-4xl font-bold mb-2">Cookie Policy</h1>
          <p className="text-muted-foreground mb-10">
            Last updated: February 18, 2026
          </p>

          <div className="prose dark:prose-invert max-w-none space-y-6 text-muted-foreground">
            <section>
              <h2 className="text-xl font-semibold text-foreground mb-3">
                1. What Are Cookies
              </h2>
              <p>
                Cookies are small text files stored on your device when you
                visit a website. They help us provide a better browsing
                experience, remember your preferences, and analyze how you use
                CampusAI.
              </p>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-foreground mb-3">
                2. Cookies We Use
              </h2>
              <ul className="list-disc pl-6 space-y-2">
                <li>
                  <strong className="text-foreground">
                    Essential Cookies:
                  </strong>{" "}
                  Required for the platform to function — authentication,
                  session management, and security tokens.
                </li>
                <li>
                  <strong className="text-foreground">
                    Preference Cookies:
                  </strong>{" "}
                  Remember your settings like theme (light/dark mode) and
                  language preferences.
                </li>
                <li>
                  <strong className="text-foreground">
                    Analytics Cookies:
                  </strong>{" "}
                  Help us understand how users interact with the platform so we
                  can improve the experience.
                </li>
              </ul>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-foreground mb-3">
                3. Third-Party Cookies
              </h2>
              <p>
                We may use third-party services (such as analytics providers)
                that set their own cookies. These are governed by the respective
                third party&apos;s privacy policy.
              </p>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-foreground mb-3">
                4. Managing Cookies
              </h2>
              <p>
                You can control cookies through your browser settings. Disabling
                essential cookies may affect the functionality of CampusAI. Most
                browsers allow you to block or delete cookies from specific
                websites.
              </p>
            </section>

            <section>
              <h2 className="text-xl font-semibold text-foreground mb-3">
                5. Contact
              </h2>
              <p>
                If you have questions about our cookie practices, contact{" "}
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
