import type { AgeRange, Category } from "@/lib/types";
import { categoryCovers } from "@/lib/data/category-covers";

export const categories: Category[] = [
  {
    slug: "squishies",
    name: "Squishies",
    shortName: "Squishies",
    description: "Jumbo, Small, Sugar, Wax, Butter, Crunchy, Vaseline, Dumpling and Christmas squishies.",
    longDescription:
      "Every squishy in the shop lives here: Jumbo, Small, Sugar, Wax, Butter, Crunchy, Vaseline, Dumpling and Christmas. One aisle family, priced mostly as boxes of 12.",
    image: categoryCovers.squishies,
    accent: "coral",
    ageLabel: "Ages 3+",
  },
  {
    slug: "jumbo-squishies",
    name: "Jumbo Squishies",
    shortName: "Jumbo",
    description: "Giant and jumbo-size squishies for big squeezes.",
    longDescription:
      "Oversized fruit, food, pickle, rocket and cheese squishies — the jumbo aisle of Squishies.",
    image: categoryCovers.squishies,
    accent: "coral",
    ageLabel: "Ages 3+",
    parentSlug: "squishies",
  },
  {
    slug: "small-squishies",
    name: "Small Squishies",
    shortName: "Small",
    description: "Pocket and desk squishies. £1.50 each — minimum order 12 pieces.",
    longDescription:
      "Everyday small squishies, fruit squeezes and sensory jars. Priced each at £1.50, with a minimum order of 12 pieces.",
    image: categoryCovers.squishies,
    accent: "coral",
    ageLabel: "Ages 3+",
    parentSlug: "squishies",
  },
  {
    slug: "sugar-squishies",
    name: "Sugar Squishies",
    shortName: "Sugar",
    description: "Candy, glitter, cube-squeeze and soft-cute sugar squishies. Minimum order 12 pieces.",
    longDescription:
      "Candy-shaped glitter squeezes, cube boxes, expression squares, block packs and Nice Cream-style sugar squishies. Minimum order 12 pieces.",
    image: categoryCovers.squishies,
    accent: "coral",
    ageLabel: "Ages 3+",
    parentSlug: "squishies",
  },
  {
    slug: "wax-squishies",
    name: "Wax Squishies",
    shortName: "Wax",
    description: "Crispy chocolate and wax-feel squishies in clear tubs.",
    longDescription:
      "Crisp Choco bars and crispy pastel balls in clear tubs — the wax aisle of Squishies.",
    image: categoryCovers.squishies,
    accent: "coral",
    ageLabel: "Ages 3+",
    parentSlug: "squishies",
  },
  {
    slug: "crunchy-squishies",
    name: "Crunchy Squishies",
    shortName: "Crunchy",
    description: "Crunchy and crispy sensory squishies.",
    longDescription:
      "Crunchy, crispy and crackle-feel squishies for that satisfying squeeze sound.",
    image: categoryCovers.squishies,
    accent: "coral",
    ageLabel: "Ages 3+",
    parentSlug: "squishies",
  },
  {
    slug: "vaseline-squishies",
    name: "Vaseline Squishies",
    shortName: "Vaseline",
    description: "Soft Vaseline-style butter and fruit squishies.",
    longDescription:
      "Vaseline butter sticks, fruit Vaseline jars and slow-rise cream squeezes.",
    image: categoryCovers.squishies,
    accent: "coral",
    ageLabel: "Ages 3+",
    parentSlug: "squishies",
  },
  {
    slug: "dumpling-squishies",
    name: "Dumpling Squishies",
    shortName: "Dumpling",
    description: "Dumpling, bun and Scrunchems mega dumpling sets.",
    longDescription:
      "Face dumplings, festive dumplings, 3D buns and mega rainbow dumpling packs.",
    image: categoryCovers.squishies,
    accent: "coral",
    ageLabel: "Ages 3+",
    parentSlug: "squishies",
  },
  {
    slug: "butter-squishies",
    name: "Butter Squishies",
    shortName: "Butter",
    description: "Butter bricks and sticks. Priced each — small £2.50, big £4.50. Minimum order 12.",
    longDescription:
      "Slow-rise butter bricks, rainbow butter and big butter sticks. Priced each (small £2.50 / big £4.50), minimum order 12 pieces.",
    image: categoryCovers["butter-squishies"],
    accent: "coral",
    ageLabel: "Ages 3+",
    parentSlug: "squishies",
  },
  {
    slug: "christmas-squishies",
    name: "Christmas Squishies",
    shortName: "Christmas",
    description: "Real Christmas squishies from the client Christmas folder. Prices on request until confirmed.",
    longDescription:
      "Merry & Bright water squishies, gingerbread and NeeDoh Christmas cubes from the client Christmas squishy stock. Display-box Taba character sets are not listed here. Advent calendars stay under Seasonal.",
    image: categoryCovers["christmas-squishies"],
    accent: "coral",
    ageLabel: "Ages 3+",
    parentSlug: "squishies",
  },
  {
    slug: "cars-vehicles",
    name: "Cars & Vehicles",
    shortName: "Cars & Vehicles",
    description: "Die-cast cars, trucks, aircraft and remote-control vehicles.",
    longDescription:
      "Metal model cars, fire trucks, stunt racers, aircraft and other vehicles with a clear photo and a UK price on every card.",
    image: categoryCovers["cars-vehicles"],
    accent: "sky",
    ageLabel: "Ages 3–12",
  },
  {
    slug: "dolls",
    name: "Dolls",
    shortName: "Dolls",
    description: "Fashion dolls, baby dolls, princess dolls and doll playsets.",
    longDescription:
      "Dolls you can dress, care for and take on a day out — fashion dolls, baby dolls, princess dolls, cry baby dolls and doll playsets, each with its own photo.",
    image: categoryCovers.dolls,
    accent: "coral",
    ageLabel: "Ages 3–8",
  },
  {
    slug: "plush-soft-toys",
    name: "Plush & Soft Toys",
    shortName: "Plush & Soft Toys",
    description: "Teddies, character plush and hug-size soft toys.",
    longDescription:
      "Soft toys and plush characters — teddies, Stitch, Bluey and other hug-size friends. Labubu has its own aisle. Plush keyrings stay with the keyrings.",
    image: categoryCovers["plush-soft-toys"],
    accent: "coral",
    ageLabel: "Ages 0–8",
  },
  {
    slug: "labubu",
    name: "Labubu",
    shortName: "Labubu",
    description: "Labubu plush, outfits, bags and surprise boxes.",
    longDescription:
      "The Labubu aisle: plush, outfits, bags, surprise boxes and big sizes. Squishy Labubu stays with the squishies.",
    image: categoryCovers.labubu,
    accent: "mint",
    ageLabel: "Ages 6+",
  },
  {
    slug: "action-figures",
    name: "K-Pop & Collectible Figures",
    shortName: "K-Pop & Figures",
    description: "K-Pop sets, Sonny Angels and collectible figures.",
    longDescription:
      "K-Pop dolls and figures, Sonny Angels, character figures and surprise figure packs. Keyrings stay in the keyring aisle.",
    image: categoryCovers["action-figures"],
    accent: "sun",
    ageLabel: "Ages 6+",
  },
  {
    slug: "fidget-spinners",
    name: "Fidget & Sensory",
    shortName: "Fidget & Sensory",
    description: "Spinners, slime, pop-its and stress toys.",
    longDescription:
      "Desk fidgets that are not squishies: spinners, slime, pop-its, push-pops and stress toys.",
    image: categoryCovers["fidget-spinners"],
    accent: "sky",
    ageLabel: "Ages 6+",
  },
  {
    slug: "light-up-toys",
    name: "Light-Up Toys",
    shortName: "Light-Up Toys",
    description: "LED toys, glow swords, lanterns and light-up wands.",
    longDescription:
      "Toys picked for the light: swords, wands, lanterns, glasses and other LED play. Christmas light sets sit in Seasonal.",
    image: categoryCovers["light-up-toys"],
    accent: "sun",
    ageLabel: "Ages 3–12",
  },
  {
    slug: "novelty-keyrings",
    name: "Keyrings & Bag Charms",
    shortName: "Keyrings & Charms",
    description: "Keyrings, bag charms and clip-on characters.",
    longDescription:
      "Bag charms and keyrings, from soft critters to metal clips. One listing per style so the charm is easy to see.",
    image: categoryCovers["novelty-keyrings"],
    accent: "coral",
    ageLabel: "Ages 6+",
  },
  {
    slug: "bubble-blowers",
    name: "Bubbles & Water Toys",
    shortName: "Bubbles & Water",
    description: "Bubble guns, bubble cameras and splash water toys.",
    longDescription:
      "Garden bubbles and water play: bubble guns, animal bubble cameras and splash balls.",
    image: categoryCovers["bubble-blowers"],
    accent: "sky",
    ageLabel: "Ages 3–8",
  },
  {
    slug: "outdoor-sports",
    name: "Outdoor & Sports",
    shortName: "Outdoor & Sports",
    description: "Balls, blasters, bikes and garden sports.",
    longDescription:
      "Outside play: balls, blasters, skateboards, bikes and other garden sports.",
    image: categoryCovers["outdoor-sports"],
    accent: "mint",
    ageLabel: "Ages 3–12",
  },
  {
    slug: "building-sets",
    name: "Building & Construction",
    shortName: "Building",
    description: "Blocks, tracks and construction sets.",
    longDescription:
      "Building sets, block packs and track play. Slow-rise food blocks stay with the squishies.",
    image: categoryCovers["building-sets"],
    accent: "sun",
    ageLabel: "Ages 3–12",
  },
  {
    slug: "arts-crafts",
    name: "Arts, Crafts & Stationery",
    shortName: "Arts & Stationery",
    description: "Pens, stickers, calendars and making kits.",
    longDescription:
      "Stationery and making: gel pens, stickers, calendars and craft sets.",
    image: categoryCovers["arts-crafts"],
    accent: "sun",
    ageLabel: "Ages 3–12",
  },
  {
    slug: "role-play",
    name: "Role Play & Pretend Play",
    shortName: "Role Play",
    description: "Kitchens, salons, castles and pretend-play sets.",
    longDescription:
      "Pretend play: kitchens, salons, castles, doctor kits and other dress-up sets.",
    image: categoryCovers["role-play"],
    accent: "coral",
    ageLabel: "Ages 3–8",
  },
  {
    slug: "board-games",
    name: "Games & Cards",
    shortName: "Games & Cards",
    description: "Playing cards, table games and puzzles.",
    longDescription:
      "Cards, table games and puzzles for a kitchen-table round.",
    image: categoryCovers["board-games"],
    accent: "mint",
    ageLabel: "Ages 4–12",
  },
  {
    slug: "baby-toddler",
    name: "Baby & Toddler",
    shortName: "Baby & Toddler",
    description: "First gyms, mats and push toys for the youngest players.",
    longDescription:
      "Early play: activity gyms, musical mats and first ride-ons sized for toddlers.",
    image: categoryCovers["baby-toddler"],
    accent: "sky",
    ageLabel: "Ages 0–2",
  },
  {
    slug: "bags-accessories",
    name: "Bags & Accessories",
    shortName: "Bags & Accessories",
    description: "Character bags, purses and small accessories.",
    longDescription:
      "Bags, purses, trolleys and character accessories, listed one style at a time.",
    image: categoryCovers["bags-accessories"],
    accent: "coral",
    ageLabel: "Ages 3–12",
  },
  {
    slug: "party-spotlight",
    name: "Party, Hats & Dress-Up",
    shortName: "Party & Hats",
    description: "Party hats, masks, flags and dress-up.",
    longDescription:
      "Hats, masks, flags and dress-up for parties. Halloween and Christmas pieces also appear under Seasonal.",
    image: categoryCovers["party-spotlight"],
    accent: "sun",
    ageLabel: "Ages 3–12",
  },
  {
    slug: "seasonal",
    name: "Seasonal (Halloween & Christmas)",
    shortName: "Seasonal",
    description: "Halloween and Christmas toys, lights and advent calendars.",
    longDescription:
      "Halloween and Christmas: masks, advent calendars, Santa toys and festive lights. Seasonal squishies stay in Squishies.",
    image: categoryCovers.seasonal,
    accent: "coral",
    ageLabel: "Ages 3+",
  },
  {
    slug: "home-gifts",
    name: "Home & Gifts",
    shortName: "Home & Gifts",
    description: "Blankets, fans, cups, bottles, frames and gift-home bits.",
    longDescription:
      "Home and gift lines: bedding, blankets, towels, cups, bottles, fans, cushion covers, umbrellas and frames.",
    image: categoryCovers["home-gifts"],
    accent: "mint",
    ageLabel: "All ages",
  },
];

export function getCategory(slug: string) {
  return categories.find((category) => category.slug === slug);
}

export const CATEGORY_AGE_GROUPS = [
  { id: "0-2", label: "Ages 0–2", slugs: ["baby-toddler"] },
  {
    id: "3-5",
    label: "Ages 3–5",
    slugs: ["dolls", "plush-soft-toys", "role-play", "bubble-blowers"],
  },
  {
    id: "6-8",
    label: "Ages 6–8",
    slugs: ["squishies", "building-sets", "board-games", "seasonal", "party-spotlight", "light-up-toys", "labubu"],
  },
  {
    id: "9-12",
    label: "Ages 9–12",
    slugs: ["outdoor-sports", "bags-accessories", "novelty-keyrings", "home-gifts", "arts-crafts", "action-figures"],
  },
  { id: "13+", label: "Ages 13+", slugs: ["cars-vehicles", "fidget-spinners"] },
] as const;

export const AGE_GROUP_RANGES: Record<(typeof CATEGORY_AGE_GROUPS)[number]["id"], AgeRange> = {
  "0-2": "0-2 years",
  "3-5": "3-5 years",
  "6-8": "6-8 years",
  "9-12": "9-12 years",
  "13+": "13+ years",
};

export function getCategoriesByAge() {
  return CATEGORY_AGE_GROUPS.map((group) => ({
    ...group,
    items: group.slugs
      .map((slug) => categories.find((category) => category.slug === slug))
      .filter((category): category is Category => Boolean(category)),
  }));
}
