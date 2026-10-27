import { Leaf, Lock, RotateCcw, Truck } from "lucide-react";
import { Container } from "@/components/ui/Container";

const badges = [
  { icon: Truck, title: "Free Shipping", text: "On orders over £60" },
  { icon: RotateCcw, title: "Easy Returns", text: "14-day hassle-free returns" },
  { icon: Lock, title: "Secure Checkout", text: "100% safe & secure payments" },
  { icon: Leaf, title: "Sustainably Made", text: "Eco-friendly toys and packaging" },
];

export function TrustBadges() {
  return (
    <section className="border-y border-cream-200 bg-white py-8">
      <Container>
        <div className="grid grid-cols-2 gap-6 lg:grid-cols-4">
          {badges.map((badge) => (
            <div key={badge.title} className="flex items-start gap-3">
              <badge.icon className="mt-0.5 h-8 w-8 shrink-0 text-teal-600" strokeWidth={1.6} aria-hidden />
              <div>
                <h3 className="font-display text-sm font-bold text-ink-800">{badge.title}</h3>
                <p className="text-xs leading-relaxed text-ink-500">{badge.text}</p>
              </div>
            </div>
          ))}
        </div>
      </Container>
    </section>
  );
}
