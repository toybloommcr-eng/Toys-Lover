import { cn } from "@/lib/utils";

export function Badge({
  children,
  tone = "coral",
  className,
}: {
  children: React.ReactNode;
  tone?: "coral" | "sky" | "mint" | "sun" | "ink";
  className?: string;
}) {
  const tones = {
    coral: "bg-coral-100 text-coral-700",
    sky: "bg-sky-100 text-sky-700",
    mint: "bg-mint-100 text-mint-800",
    sun: "bg-sun-100 text-sun-600",
    ink: "bg-ink-100 text-ink-700",
  };

  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-2.5 py-1 text-xs font-display font-bold uppercase tracking-wider",
        tones[tone],
        className,
      )}
    >
      {children}
    </span>
  );
}
