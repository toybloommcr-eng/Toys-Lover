import type { Metadata } from "next";
import { categories } from "@/lib/data/categories";
import { img } from "@/lib/media";
import { PageHero } from "@/components/ui/PageHero";
import { CategoryTiles } from "@/components/home/CategoryTiles";
import { SquishyLane } from "@/components/home/SquishyLane";

export const metadata: Metadata = {
  title: "Categories",
};

export default function ShopPage() {
  return (
    <>
      <PageHero
        image={img.pageShop}
        eyebrow="Aisles"
        title="Shop by category."
        description={`Browse all ${categories.length} categories. Squishies are listed first — every squeeze, dumpling and slow-rise toy is in that aisle.`}
      />
      <SquishyLane />
      <CategoryTiles title="All Categories" eyebrow={`${categories.length} aisles — squishies first`} />
    </>
  );
}
