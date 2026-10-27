import { Award, Brain, Hand, Palette, Users } from "lucide-react";
import { Container } from "@/components/ui/Container";
import { GlowHeading } from "@/components/home/GlowHeading";

const benefits = [
  {
    icon: Brain,
    title: "Boosts Cognitive Skills",
    text: "Encourages problem solving and critical thinking.",
    card: "bg-teal-50 ring-teal-100",
    iconWrap: "bg-teal-500 text-white shadow-[0_10px_20px_-10px_rgba(13,148,136,0.7)]",
    titleColor: "text-teal-800",
    blob: "bg-teal-200/70",
  },
  {
    icon: Hand,
    title: "Enhances Motor Skills",
    text: "Builds hand-eye coordination and fine motor control.",
    card: "bg-coral-50 ring-coral-100",
    iconWrap: "bg-coral-500 text-white shadow-[0_10px_20px_-10px_rgba(242,112,74,0.7)]",
    titleColor: "text-coral-700",
    blob: "bg-coral-200/70",
  },
  {
    icon: Palette,
    title: "Encourages Creativity",
    text: "Sparks imagination and honest self-expression.",
    card: "bg-sun-50 ring-sun-100",
    iconWrap: "bg-sun-400 text-ink-800 shadow-[0_10px_20px_-10px_rgba(240,162,2,0.65)]",
    titleColor: "text-sun-600",
    blob: "bg-sun-200/80",
  },
  {
    icon: Award,
    title: "Builds Confidence",
    text: "Helps children try, finish, and feel proud of play.",
    card: "bg-mint-50 ring-mint-100",
    iconWrap: "bg-mint-500 text-white shadow-[0_10px_20px_-10px_rgba(27,179,126,0.65)]",
    titleColor: "text-mint-800",
    blob: "bg-mint-200/80",
  },
  {
    icon: Users,
    title: "Strengthens Social Skills",
    text: "Encourages sharing, teamwork, and communication.",
    card: "bg-sky-50 ring-sky-100",
    iconWrap: "bg-sky-500 text-white shadow-[0_10px_20px_-10px_rgba(43,116,199,0.6)]",
    titleColor: "text-sky-700",
    blob: "bg-sky-200/80",
  },
];

export function LearningBenefits() {
  return (
    <section id="benefits" className="relative overflow-hidden bg-white py-14">
      <div className="pointer-events-none absolute -left-16 top-10 h-40 w-40 rounded-full bg-teal-100/70 blur-3xl" />
      <div className="pointer-events-none absolute -right-10 bottom-6 h-44 w-44 rounded-full bg-coral-100/80 blur-3xl" />
      <div className="pointer-events-none absolute left-1/2 top-0 h-28 w-56 -translate-x-1/2 rounded-full bg-sun-100/80 blur-3xl" />
      <Container className="relative">
        <GlowHeading eyebrow="Play with purpose" title="Learning Benefits for Every Child" />
        <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
          {benefits.map((item) => (
            <article
              key={item.title}
              className={`group relative overflow-hidden rounded-[1.7rem] p-5 text-center ring-1 transition duration-500 ease-out hover:-translate-y-0.5 ${item.card}`}
            >
              <span className={`pointer-events-none absolute -right-6 -top-8 h-20 w-20 rounded-full ${item.blob}`} />
              <span className={`pointer-events-none absolute -bottom-8 -left-6 h-16 w-16 rounded-full ${item.blob}`} />
              <div className={`relative mx-auto grid h-14 w-14 place-items-center rounded-full ${item.iconWrap}`}>
                <item.icon className="h-7 w-7" strokeWidth={1.75} />
              </div>
              <h3 className={`relative mt-3 font-display text-base font-bold ${item.titleColor}`}>{item.title}</h3>
              <p className="relative mt-1 text-sm leading-relaxed text-ink-600">{item.text}</p>
            </article>
          ))}
        </div>
      </Container>
    </section>
  );
}
