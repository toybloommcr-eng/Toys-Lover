import Link from "next/link";
import { CONTACT, SITE_NAME, SITE_TAGLINE } from "@/lib/constants";
import { Container } from "@/components/ui/Container";
import { SocialIcons } from "@/components/ui/SocialIcons";
import { Logo } from "@/components/layout/Logo";
import { NestDoodle } from "@/components/brand/Doodles";

export function Footer() {
  return (
    <footer className="bg-teal-800 text-teal-50">
      <Container className="grid gap-10 py-12 sm:grid-cols-2 lg:grid-cols-[1.35fr_1fr_1fr_1fr_1.1fr]">
        <div className="flex flex-col items-start">
          <div className="footer-logo-stage">
            <Logo inverted />
          </div>
          <p className="footer-brand-name mt-3 font-display text-2xl font-extrabold text-white sm:text-3xl">
            {SITE_NAME}
          </p>
          <p className="mt-1 text-sm font-semibold text-sun-300">{SITE_TAGLINE}</p>
          <p className="mt-3 max-w-xs text-sm leading-relaxed text-teal-100">
            We believe in the power of play to inspire young minds and create bright futures.
          </p>
          <SocialIcons className="mt-5" size="sm" />
        </div>
        <div>
          <p className="font-display text-sm font-bold text-white">Shop</p>
          <ul className="mt-3 space-y-2 text-sm text-teal-100">
            <li><Link href="/shop/squishies" className="hover:text-white">Squishies</Link></li>
            <li><Link href="/shop/butter-squishies" className="hover:text-white">Butter Squishies</Link></li>
            <li><Link href="/shop" className="hover:text-white">Shop All</Link></li>
            <li><Link href="/shop#all-categories" className="hover:text-white">All Categories</Link></li>
            <li><Link href="/shop/seasonal" className="hover:text-white">Seasonal</Link></li>
            <li><Link href="/shop/plush-soft-toys" className="hover:text-white">Plush & Soft Toys</Link></li>
            <li><Link href="/shop/cars-vehicles" className="hover:text-white">Cars & Vehicles</Link></li>
            <li><Link href="/shop/board-games" className="hover:text-white">Games & Cards</Link></li>
            <li><Link href="/pay" className="hover:text-white">Pay Now</Link></li>
          </ul>
        </div>
        <div>
          <p className="font-display text-sm font-bold text-white">Customer Care</p>
          <ul className="mt-3 space-y-2 text-sm text-teal-100">
            <li><Link href="/contact" className="hover:text-white">Contact Us</Link></li>
            <li><Link href="/shipping" className="hover:text-white">Shipping Info</Link></li>
            <li><Link href="/faq" className="hover:text-white">Returns & Exchanges</Link></li>
            <li><Link href="/faq" className="hover:text-white">FAQ</Link></li>
          </ul>
        </div>
        <div>
          <p className="font-display text-sm font-bold text-white">About Us</p>
          <ul className="mt-3 space-y-2 text-sm text-teal-100">
            <li><Link href="/about" className="hover:text-white">Our Story</Link></li>
            <li><Link href="/blog" className="hover:text-white">Blog</Link></li>
            <li><Link href="/privacy" className="hover:text-white">Safety & Quality</Link></li>
            <li><Link href="/terms" className="hover:text-white">Terms of Service</Link></li>
          </ul>
        </div>
        <div className="relative overflow-hidden rounded-3xl bg-white/10 p-5">
          <NestDoodle className="absolute -right-4 -top-2 h-28 w-36 opacity-90" />
          <p className="relative font-display text-lg font-bold leading-snug text-white">
            Nurturing Play.
            <br />
            Inspiring Growth.
          </p>
          <p className="relative mt-3 text-xs text-teal-100">
            {CONTACT.city} · {CONTACT.postcode}
          </p>
        </div>
      </Container>
      <div className="border-t border-white/10 py-4">
        <Container className="flex flex-col items-center justify-between gap-2 text-xs text-teal-100 sm:flex-row">
          <p>© {new Date().getFullYear()} {SITE_NAME}. Prices in £.</p>
          <p className="flex gap-4">
            <Link href="/terms" className="hover:text-white">Terms of Service</Link>
            <Link href="/privacy" className="hover:text-white">Privacy Policy</Link>
          </p>
        </Container>
      </div>
    </footer>
  );
}
