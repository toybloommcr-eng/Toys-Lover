import { Mail } from "lucide-react";
import { Container } from "@/components/ui/Container";
import { NewsletterForm } from "@/components/home/NewsletterForm";
import { BirdDoodle } from "@/components/brand/Doodles";

export function Newsletter() {
  return (
    <section className="bg-teal-700 py-10 text-white">
      <Container>
        <div className="relative overflow-hidden rounded-[1.6rem] bg-teal-800 px-6 py-8 sm:px-10">
          <BirdDoodle className="pointer-events-none absolute bottom-2 right-6 hidden h-16 w-20 sm:block" />
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="heading-glow-light font-display text-3xl font-extrabold sm:text-4xl lg:text-5xl">
              Let’s Stay in Touch!
            </h2>
            <p className="mt-2 text-sm text-teal-100">
              Sign up for exclusive offers, new arrivals, and learning tips for your little ones.
            </p>
            <div className="mt-5">
              <NewsletterForm compact />
            </div>
          </div>
        </div>
      </Container>
    </section>
  );
}
