import { Container } from "@/components/ui/Container";
import { toTitleCase } from "@/lib/utils";

export function PageHeader({
  eyebrow,
  title,
  description,
}: {
  eyebrow?: string;
  title: string;
  description?: string;
}) {
  return (
    <div className="border-b border-ink-100 bg-gradient-to-br from-coral-50 via-cream-100 to-sky-50">
      <Container className="py-10 sm:py-12">
        {eyebrow ? (
          <p className="mb-3 text-xs font-display font-bold uppercase tracking-[0.2em] text-coral-600">
            {toTitleCase(eyebrow)}
          </p>
        ) : null}
        <h1 className="max-w-3xl font-display text-4xl font-extrabold tracking-tight sm:text-5xl lg:text-6xl">
          <span className="heading-glow-coral">{toTitleCase(title)}</span>
        </h1>
        {description ? (
          <p className="mt-4 max-w-2xl text-lg leading-relaxed text-ink-500">{description}</p>
        ) : null}
      </Container>
    </div>
  );
}
