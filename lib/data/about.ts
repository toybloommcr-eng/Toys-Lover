import type { TeamMember } from "@/lib/types";
import { img, productShot } from "@/lib/media";

export const gallery = [
  { src: productShot("snuggle-puppy-plush"), alt: "Snuggle puppy plush" },
  { src: productShot("realistic-baby-care-doll"), alt: "Baby care doll" },
  { src: productShot("rc-monster-truck"), alt: "Remote-control monster truck" },
  { src: productShot("rocket-48-bubble-machine"), alt: "Electric bubble rocket" },
  { src: productShot("dream-castle-playset"), alt: "Dream castle playset" },
  { src: productShot("jumbo-peach-squishy"), alt: "Jumbo peach squishy" },
];

export const timeline = [
  {
    year: "2018",
    title: "A living-room shelf",
    image: img.heroPlay,
  },
  {
    year: "2020",
    title: "First Manchester shop",
    image: img.baby,
  },
  {
    year: "2023",
    title: "STEM & pretend play",
    image: img.stem,
  },
  {
    year: "2026",
    title: "Play, still honest",
    image: img.roleplay,
  },
];

export const values = [
  {
    title: "Safety",
    image: img.plush,
  },
  {
    title: "Quality",
    image: img.blocks,
  },
  {
    title: "Learning",
    image: img.stem,
  },
];

export const team: TeamMember[] = [
  {
    name: "Amina Raza",
    role: "Founder",
    bio: "",
    image: img.teamAmina,
  },
  {
    name: "Hassan Qureshi",
    role: "Operations",
    bio: "",
    image: img.teamHassan,
  },
  {
    name: "Dr. Sana Malik",
    role: "Learning advisor",
    bio: "",
    image: img.teamSana,
  },
];
