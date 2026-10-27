import { cn } from "@/lib/utils";

export function Section({
  children,
  className,
  id,
  tone = "plain",
}: {
  children: React.ReactNode;
  className?: string;
  id?: string;
  tone?: "plain" | "cream" | "white" | "ink";
}) {
  const tones = {
    plain: "",
    cream: "bg-cream-100",
    white: "bg-white",
    ink: "bg-ink-900 text-cream-100",
  };

  return (
    <section id={id} className={cn("py-6 sm:py-8", tones[tone], className)}>
      {children}
    </section>
  );
}
