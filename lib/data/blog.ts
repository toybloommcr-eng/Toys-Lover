import type { BlogPost } from "@/lib/types";
import { productShot } from "@/lib/media";

export const blogCategories = [
  "Parenting Tips",
  "Learning Through Play",
  "Gift Guides",
  "Toy Safety & Reviews",
  "Activities & DIY Ideas",
] as const;

export const posts: BlogPost[] = [
  {
    slug: "gift-guide-ages-three-to-five",
    title: "The Calm Gift Guide for Ages 3–5",
    excerpt:
      "Presents that last past the wrapping paper — chosen for attention spans, small homes, and parents who are tired of noisy toys.",
    content: [
      "Choosing gifts for preschoolers is less about “more” and more about match: match the child’s stage, the family’s space, and how much noise everyone can live with.",
      "At Toy Bloom, we start with open-ended toys — blocks, dolls, pretend kitchens — because they stretch across weeks, not a single afternoon. A three-year-old who receives one well-made market stand will still be pricing felt mangoes at five.",
      "Look for pieces that invite language. When a child narrates a doctor visit to a teddy, they are rehearsing courage for the real clinic. When they stack cedar blocks, they are quietly doing physics.",
      "If you are buying for a home with limited storage, favor sets that fold, bag, or nest. Our Little Market Stand and Pebble Stack Rings were designed with apartment living in mind.",
      "Finally, wrap the gift with a short note about how to play — not instructions, just an invitation. Parents remember kindness. Kids remember being seen.",
    ],
    category: "Gift Guides",
    author: "Amina Raza",
    authorRole: "Founder, Toy Bloom",
    date: "2026-03-12",
    readTime: "6 min",
    image: productShot("snuggle-puppy-plush"),
    featured: true,
  },
  {
    slug: "learning-through-play-science",
    title: "Learning Through Play: Why Kitchen-Table Science Works",
    excerpt:
      "You do not need a lab coat. You need twenty minutes, a curious child, and experiments that will not stain the sofa.",
    content: [
      "Children remember the experiment that fizzed on a Saturday more clearly than any worksheet. That is not a slogan — it is how memory works when emotion and surprise show up together.",
      "Kitchen-table science works because it is close. The tools look like home. The questions (“why did it bubble?”) belong to the child, not the textbook.",
      "We built the Aurora Discovery Lab so parents across the UK can say yes without a chemistry degree. Every card shows the “why” in one sentence.",
      "Keep sessions short. Stop while they still want one more. That hunger is the real curriculum.",
    ],
    category: "Learning Through Play",
    author: "Dr. Sana Malik",
    authorRole: "Education advisor",
    date: "2026-02-28",
    readTime: "5 min",
    image: productShot("space-explorer-kit"),
  },
  {
    slug: "toy-safety-checklist",
    title: "A Parent’s Toy Safety Checklist (Without the Panic)",
    excerpt:
      "Labels, ages, and materials — a clear list you can actually use in a busy shop or while scrolling on your phone.",
    content: [
      "Safety shopping should feel like competence, not fear. Start with age marks, then look at how parts attach, then at materials you can name.",
      "For under-threes, skip anything that detaches into a mouthful. Embroidered faces beat plastic noses. One-piece silicone beats hollow bath toys that stay wet inside.",
      "We publish materials on every Toy Bloom product page because parents deserve the same clarity we would want for our own kids.",
      "If a toy arrives damaged, stop play and write to us. We would rather replace a product than guess.",
    ],
    category: "Toy Safety & Reviews",
    author: "Hassan Qureshi",
    authorRole: "Operations, Toy Bloom",
    date: "2026-02-10",
    readTime: "7 min",
    image: productShot("piano-fitness-gym"),
  },
  {
    slug: "rainy-day-diy-fort",
    title: "Rainy-Day Forts and Five Other Zero-Cost Play Ideas",
    excerpt:
      "When the weather stays in and the Wi-Fi looks tempting, these setups take a sheet, a lamp, and twenty minutes.",
    content: [
      "A dining table, a cotton sheet, and a warm lamp become a city. Give the kids a job: “You are in charge of the door.” Responsibility is a kind of play.",
      "Rotate three toys onto the living-room rug and put the rest away. Scarcity, oddly, increases invention.",
      "Tape a paper road on the floor. Suddenly every block and figure has somewhere to go.",
      "None of this replaces a well-chosen toy. It just reminds us that play is a practice, not a purchase.",
    ],
    category: "Activities & DIY Ideas",
    author: "Amina Raza",
    authorRole: "Founder, Toy Bloom",
    date: "2026-01-22",
    readTime: "4 min",
    image: productShot("dream-castle-playset"),
  },
  {
    slug: "screen-smart-weeknights",
    title: "Screen-Smart Weeknights for Tired Parents",
    excerpt:
      "You do not have to ban devices. You need a closing ritual that kids can predict — and toys that are ready when the screen goes dark.",
    content: [
      "Predictability beats perfection. A 20-minute wind-down that always includes the same basket of quiet toys will outperform a new rule announced in anger.",
      "Keep a “evening shelf” at child height: a puzzle, a soft book, a plush. If they have to ask you to fetch play, they will ask for the tablet instead.",
      "Older kids can handle a timer they can see. When it ends, the gadget lab or strategy duel is already on the table.",
    ],
    category: "Parenting Tips",
    author: "Mariam Aziz",
    authorRole: "Parent coach",
    date: "2026-01-08",
    readTime: "5 min",
    image: productShot("quick-push-console"),
  },
  {
    slug: "budget-eid-gifts",
    title: "Eid & Birthday Gifts Under £30 That Still Feel Special",
    excerpt:
      "A budget is not a compromise when the toy is well made and wrapped with a story.",
    content: [
      "Felt, wood, and cloth age more gracefully than flashing plastic. A £22 embroidery kit can become a wall piece. A £24 constellation puzzle becomes a shared evening.",
      "Buy one toy and one consumable — paints, extra felt fruit — so the gift keeps unfolding.",
      "If you shop at Toy Bloom, filter by price and age together. The best “small” gifts are the ones that match the child, not the discount tag.",
    ],
    category: "Gift Guides",
    author: "Hassan Qureshi",
    authorRole: "Operations, Toy Bloom",
    date: "2025-12-18",
    readTime: "4 min",
    image: productShot("beauty-princess-doll"),
  },
  {
    slug: "first-year-toys",
    title: "First-Year Toys: Less Clutter, More Signal",
    excerpt:
      "Babies need contrast, chew-safe textures, and you — not a mountain of rattles.",
    content: [
      "In the first year, the most expensive toy is still a rested parent. The second is a small set of sensory objects that can be washed.",
      "High-contrast cloth books, silicone pebbles, and one excellent plush cover most days. Rotate weekly so the living room does not become a warehouse.",
      "We designed Pebble Stack Rings without water-trapping holes because bath toys that stay wet are a quiet safety issue nobody photographs.",
    ],
    category: "Toy Safety & Reviews",
    author: "Dr. Sana Malik",
    authorRole: "Education advisor",
    date: "2025-11-30",
    readTime: "6 min",
    image: productShot("dino-world-musical-mat"),
  },
  {
    slug: "building-focus-with-puzzles",
    title: "How Puzzles Build Focus (and How to Not Force Them)",
    excerpt:
      "A puzzle is a conversation with frustration. The skill is staying in the conversation.",
    content: [
      "If a child walks away, leave the puzzle out. Completion is not the only win; returning is.",
      "Sort edges together, then step back. Your job is company, not solving.",
      "Glow puzzles like our constellation set add a second act: dim the lights and see what you built. Delight is a legitimate teaching tool.",
    ],
    category: "Learning Through Play",
    author: "Mariam Aziz",
    authorRole: "Parent coach",
    date: "2025-11-12",
    readTime: "5 min",
    image: productShot("eva-number-foam-puzzle"),
  },
];

export function getPost(slug: string) {
  return posts.find((post) => post.slug === slug);
}

export function getFeaturedPost() {
  return posts.find((post) => post.featured) ?? posts[0];
}

export function getRelatedPosts(post: BlogPost, limit = 3) {
  return posts
    .filter((item) => item.slug !== post.slug && item.category === post.category)
    .concat(posts.filter((item) => item.slug !== post.slug && item.category !== post.category))
    .slice(0, limit);
}
