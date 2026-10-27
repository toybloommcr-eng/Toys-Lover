import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { Container } from "@/components/ui/Container";
import { ElephantDoodle, LionDoodle } from "@/components/brand/Doodles";

export function SaleBanner() {
  return (
    <section className="py-4">
      <Container>
        <div className="relative overflow-hidden rounded-[1.8rem] bg-coral-500 px-6 py-8 text-white shadow-lift sm:px-10 sm:py-10">
          <LionDoodle className="pointer-events-none absolute -left-2 bottom-0 hidden h-32 w-36 sm:block" />
          <ElephantDoodle className="pointer-events-none absolute -right-4 bottom-0 hidden h-32 w-40 sm:block" />
          <div className="relative mx-auto max-w-2xl text-center">
            <p className="mx-auto mb-3 inline-flex rounded-full bg-white/20 px-3 py-1 text-[11px] font-bold uppercase tracking-[0.16em] text-white">
              Limited Time Offer!
            </p>
            <p className="font-display text-3xl font-bold sm:text-5xl">Summer of Play Sale!</p>
            <p className="mt-2 text-sm font-semibold text-white/90 sm:text-xl">Up to 25% OFF Sitewide</p>
            <Link
              href="/sale"
              className="mt-5 inline-flex items-center gap-2 rounded-full bg-white px-6 py-2.5 font-display text-sm font-bold text-coral-600 shadow-soft"
            >
              Shop the Sale
              <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
        </div>
      </Container>
    </section>
  );
}
