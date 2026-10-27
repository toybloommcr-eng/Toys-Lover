import Image from "next/image";
import { Container } from "@/components/ui/Container";
import { toTitleCase } from "@/lib/utils";

export function PageHero({
  image,
  eyebrow,
  title,
  description,
}: {
  image: string;
  eyebrow: string;
  title: string;
  description?: string;
}) {
  return (
    <div className="bg-cream-100">
      <Container className="grid items-center gap-6 py-10 lg:grid-cols-[1.2fr_0.8fr] lg:py-12">
        <div>
          <p className="font-display text-xs font-bold uppercase tracking-[0.18em] text-teal-700">
            {toTitleCase(eyebrow)}
          </p>
          <h1 className="heading-glow mt-2 font-display text-4xl font-extrabold leading-tight text-ink-900 sm:text-5xl lg:text-6xl">
            <span className="heading-glow-coral">{toTitleCase(title)}</span>
          </h1>
          {description ? <p className="mt-3 max-w-xl text-base text-ink-600">{description}</p> : null}
        </div>
        <div className="relative overflow-hidden rounded-[1.8rem] bg-white shadow-soft ring-1 ring-cream-200">
          <div className="relative aspect-square">
            <Image
              src={image}
              alt={title}
              fill
              sizes="(min-width: 1024px) 36vw, 80vw"
              quality={90}
              className="object-contain object-center bg-white p-3"
              priority
            />
          </div>
        </div>
      </Container>
    </div>
  );
}
