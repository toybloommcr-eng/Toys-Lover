import { getBestSellers } from "@/lib/data/products";
import { Hero } from "@/components/home/Hero";
import { SquishyLane } from "@/components/home/SquishyLane";
import { CategoryTiles } from "@/components/home/CategoryTiles";
import { LearningBenefits } from "@/components/home/LearningBenefits";
import { TrustBadges } from "@/components/home/TrustBadges";
import { Newsletter } from "@/components/home/Newsletter";
import { BestSellers } from "@/components/home/BestSellers";
import { GlowHeading } from "@/components/home/GlowHeading";
import { Container } from "@/components/ui/Container";

export default function HomePage() {
  const bestsellers = getBestSellers().slice(0, 10);

  return (
    <>
      <Hero />
      <SquishyLane />
      <CategoryTiles title="Shop by Category" eyebrow="All aisles" />

      <section id="trending" className="content-visibility-auto bg-cream-50 py-12">
        <Container>
          <GlowHeading eyebrow="Parents pick these first" title="Best Sellers" />
          <div className="mt-8">
            <BestSellers products={bestsellers} />
          </div>
        </Container>
      </section>

      <div className="content-visibility-auto">
        <LearningBenefits />
      </div>
      <TrustBadges />
      <Newsletter />
    </>
  );
}
