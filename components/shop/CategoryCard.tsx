import type { Category } from "@/lib/types";
import { toTitleCase } from "@/lib/utils";
import { Button } from "@/components/ui/Button";
import { ToyPhoto } from "@/components/ui/ToyPhoto";

const accents = {
  coral: "from-coral-600/85",
  sky: "from-sky-600/85",
  mint: "from-mint-700/80",
  sun: "from-sun-500/80",
};

export function CategoryCard({
  category,
  productNames = [],
  count,
}: {
  category: Category;
  productNames?: string[];
  count?: number;
}) {
  const mentioned = productNames.slice(0, 5);

  return (
    <article className="media-hover group flex h-full flex-col overflow-hidden rounded-[1.75rem] bg-white shadow-card">
      <div className="relative aspect-square overflow-hidden bg-white">
        <ToyPhoto
          src={category.image}
          alt={category.name}
          sizes="(min-width: 1024px) 25vw, 50vw"
          fit="contain"
          className="h-full w-full"
        />
        <div className={`absolute inset-0 bg-gradient-to-t ${accents[category.accent]} via-transparent to-transparent`} />
        <h2 className="heading-glow-light absolute bottom-4 left-4 right-4 font-display text-2xl font-extrabold text-white">
          {toTitleCase(category.shortName)}
        </h2>
      </div>
      <div className="flex flex-1 flex-col p-5">
        <p className="mb-2 inline-flex w-fit rounded-full bg-[#7A4A2B] px-3 py-1 font-display text-xs font-black uppercase tracking-wide text-white">
          {typeof count === "number" ? `${count} products` : "Category"}
        </p>
        <p className="text-sm font-medium leading-relaxed text-ink-500">{category.description}</p>
        {mentioned.length ? (
          <ul className="mt-3 flex-1 space-y-1.5 border-t border-cream-200 pt-3">
            <li className="text-[10px] font-bold uppercase tracking-wide text-ink-400">Products in this category</li>
            {mentioned.map((name) => (
              <li key={name} className="truncate text-sm font-semibold text-ink-700">
                · {toTitleCase(name)}
              </li>
            ))}
          </ul>
        ) : (
          <div className="flex-1" />
        )}
        <Button href={`/shop/${category.slug}`} className="mt-5 w-full">
          Shop Category
        </Button>
      </div>
    </article>
  );
}
