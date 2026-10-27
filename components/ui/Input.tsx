import { cn } from "@/lib/utils";

type InputProps = React.InputHTMLAttributes<HTMLInputElement> & {
  label: string;
  hint?: string;
};

export function Input({ label, hint, id, className, ...props }: InputProps) {
  const fieldId = id ?? label.toLowerCase().replace(/\s+/g, "-");

  return (
    <label className="block space-y-1.5" htmlFor={fieldId}>
      <span className="text-sm font-display font-semibold text-ink-800">{label}</span>
      <input
        id={fieldId}
        className={cn(
          "w-full rounded-2xl border border-ink-200 bg-white px-4 py-3 text-ink-800 shadow-sm transition placeholder:text-ink-300 focus:border-coral-400 focus:outline-none focus:ring-4 focus:ring-coral-100",
          className,
        )}
        {...props}
      />
      {hint ? <span className="text-xs text-ink-400">{hint}</span> : null}
    </label>
  );
}

export function Textarea({
  label,
  id,
  className,
  ...props
}: React.TextareaHTMLAttributes<HTMLTextAreaElement> & { label: string }) {
  const fieldId = id ?? label.toLowerCase().replace(/\s+/g, "-");

  return (
    <label className="block space-y-1.5" htmlFor={fieldId}>
      <span className="text-sm font-display font-semibold text-ink-800">{label}</span>
      <textarea
        id={fieldId}
        className={cn(
          "min-h-[140px] w-full rounded-2xl border border-ink-200 bg-white px-4 py-3 text-ink-800 shadow-sm transition placeholder:text-ink-300 focus:border-coral-400 focus:outline-none focus:ring-4 focus:ring-coral-100",
          className,
        )}
        {...props}
      />
    </label>
  );
}

export function Select({
  label,
  id,
  children,
  className,
  ...props
}: React.SelectHTMLAttributes<HTMLSelectElement> & { label: string }) {
  const fieldId = id ?? label.toLowerCase().replace(/\s+/g, "-");

  return (
    <label className="block space-y-1.5" htmlFor={fieldId}>
      <span className="text-sm font-display font-semibold text-ink-800">{label}</span>
      <select
        id={fieldId}
        className={cn(
          "w-full rounded-xl border border-ink-200 bg-white px-3 py-2.5 text-sm text-ink-800 shadow-sm transition focus:border-coral-400 focus:outline-none focus:ring-2 focus:ring-coral-100",
          className,
        )}
        {...props}
      >
        {children}
      </select>
    </label>
  );
}
