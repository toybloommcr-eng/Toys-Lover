export type AgeRange = "0-2 years" | "3-5 years" | "6-8 years" | "9-12 years" | "13+ years";

export interface Category {
  slug: string;
  name: string;
  shortName: string;
  description: string;
  longDescription: string;
  image: string;
  accent: "coral" | "sky" | "mint" | "sun";
  ageLabel: string;
  /** Parent aisle slug when this is a subcategory. */
  parentSlug?: string;
}

export interface Product {
  slug: string;
  name: string;
  price: number;
  compareAtPrice?: number;
  ageRange: AgeRange;
  brand: string;
  theme: string;
  categorySlug: string;
  images: string[];
  shortDescription: string;
  description: string;
  features: string[];
  safety: string;
  materials: string;
  isNew?: boolean;
  isBestSeller?: boolean;
  /** Pieces / units included in the retail box, or the wholesale minimum. */
  piecesPerBox?: number;
  /** Wholesale unit for the minimum, such as pcs or packs. */
  moqUnit?: string;
  /** Exact minimum-order line, for example "Min order: 12 pcs (1 box)". */
  moqLabel?: string;
  /** Wholesale line with no confirmed unit price. Do not render £0.00. */
  priceTBC?: boolean;
  stock: number;
}

export interface BlogPost {
  slug: string;
  title: string;
  excerpt: string;
  content: string[];
  category: string;
  author: string;
  authorRole: string;
  date: string;
  readTime: string;
  image: string;
  featured?: boolean;
}

export interface FaqItem {
  question: string;
  answer: string;
  group: "Shipping" | "Returns" | "Safety" | "Orders" | "Age" | "Payments";
}

export interface CartItem {
  slug: string;
  quantity: number;
}

export interface TeamMember {
  name: string;
  role: string;
  bio: string;
  image: string;
}
