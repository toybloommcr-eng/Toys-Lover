import { cn } from "@/lib/utils";

export function Container({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <div className={cn("mx-auto w-full max-w-[72rem] px-3 sm:px-5 lg:px-6", className)}>
      {children}
    </div>
  );
}
