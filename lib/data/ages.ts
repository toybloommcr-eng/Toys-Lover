import type { AgeRange } from "@/lib/types";
import { productShot } from "@/lib/media";

export const AGE_GUIDES: {
  slug: string;
  range: AgeRange;
  label: string;
  title: string;
  usage: string;
  toys: string[];
  image: string;
  glow: string;
}[] = [
  {
    slug: "0-2",
    range: "0-2 years",
    label: "0–2 yrs",
    title: "First discoveries",
    usage:
      "Soft, chew-safe toys for grasping, rattling, and tummy time — short sessions that soothe and spark the senses.",
    toys: ["Piano gyms", "Musical mats", "Wrap-around plush"],
    image: productShot("piano-fitness-gym"),
    glow: "from-sky-500 to-mint-400 shadow-[0_0_22px_rgba(43,116,199,0.4)]",
  },
  {
    slug: "3-5",
    range: "3-5 years",
    label: "3–5 yrs",
    title: "Pretend & build",
    usage:
      "Dolls, castles, kitchens, and bubble rockets for make-believe days that grow language and sharing.",
    toys: ["Dream castles", "Bubble rockets", "Care dolls"],
    image: productShot("dream-castle-playset"),
    glow: "from-coral-500 to-sun-400 shadow-[0_0_22px_rgba(242,92,56,0.45)]",
  },
  {
    slug: "6-8",
    range: "6-8 years",
    label: "6–8 yrs",
    title: "Missions & science",
    usage:
      "Transformers, table football, and dinosaur builds that stretch focus — weekend missions they can lead.",
    toys: ["Transformers", "Table football", "Dinosaur builds"],
    image: productShot("dino-expedition-build"),
    glow: "from-sun-400 to-coral-500 shadow-[0_0_22px_rgba(255,193,7,0.5)]",
  },
  {
    slug: "9-12",
    range: "9-12 years",
    label: "9–12 yrs",
    title: "Think, code, create",
    usage:
      "8+ RC trucks, foam blasters, and maker kits for kids who want a challenge — still play, just faster.",
    toys: ["8+ RC trucks", "Soft-dart blasters", "Maker kits"],
    image: productShot("explorer-binoculars"),
    glow: "from-mint-500 to-sky-500 shadow-[0_0_22px_rgba(27,179,126,0.4)]",
  },
  {
    slug: "13-plus",
    range: "13+ years",
    label: "13+ yrs",
    title: "Tween & teen play",
    usage:
      "Street racers, mood lamps, and desk gadgets for older kids who have left the toddler aisle.",
    toys: ["Street racers", "Mood lamps", "Desk collectibles"],
    image: productShot("street-graffiti-rc"),
    glow: "from-sky-700 to-coral-500 shadow-[0_0_22px_rgba(23,60,107,0.45)]",
  },
];

export function getAgeGuide(slug: string) {
  return AGE_GUIDES.find((guide) => guide.slug === slug);
}
