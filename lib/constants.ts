export const SITE_NAME = "Toy Bloom";

export const SITE_TAGLINE = "Play. Learn. Grow Together.";

export const SITE_DESCRIPTION =
  "Toy Bloom is a UK toy store for families — age-appropriate play, safe materials, and gifts that spark curiosity. Free UK shipping over £60.";

export const SITE_URL = (
  process.env.NEXT_PUBLIC_SITE_URL || "https://toybloom.co.uk"
).replace(/\/$/, "");

export const FREE_SHIPPING_GBP = 60;

export const CONTACT = {
  email: "hello@toybloom.example",
  phone: "+44 16 1396 0184",
  addressLine1: "14 King Street Arcade",
  city: "Manchester",
  region: "Greater Manchester",
  postcode: "M2 6AQ",
  country: "United Kingdom",
  hours: "Mon–Sat, 9:30 AM – 6:00 PM",
};

export const MAPS_EMBED_SRC = `https://maps.google.com/maps?q=${encodeURIComponent(
  `${CONTACT.addressLine1}, ${CONTACT.city} ${CONTACT.postcode}, ${CONTACT.country}`,
)}&z=16&output=embed`;

export const MAPS_LINK = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(
  `${CONTACT.addressLine1}, ${CONTACT.city} ${CONTACT.postcode}`,
)}`;

export const SOCIAL = {
  facebook: "https://facebook.com",
  instagram: "https://instagram.com",
  youtube: "https://youtube.com",
  whatsapp: "https://wa.me/441613960184",
  tiktok: "https://tiktok.com",
};

export { HERO_SLIDES } from "@/lib/media";

export const AGE_RANGES = [
  "0-2 years",
  "3-5 years",
  "6-8 years",
  "9-12 years",
  "13+ years",
] as const;

export const SORT_OPTIONS = [
  { id: "popularity", label: "Popularity" },
  { id: "newest", label: "Newest" },
  { id: "price-asc", label: "Price: Low to High" },
  { id: "price-desc", label: "Price: High to Low" },
] as const;
