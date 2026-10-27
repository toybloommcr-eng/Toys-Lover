"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Heart, MapPin, Menu, Search, ShoppingCart, Sparkles, X } from "lucide-react";
import { useCart } from "@/lib/context/CartContext";
import { useWishlist } from "@/lib/context/WishlistContext";
import { FREE_SHIPPING_GBP } from "@/lib/constants";
import { cn } from "@/lib/utils";
import { Logo } from "@/components/layout/Logo";

const links = [
  { href: "/shop/squishies", label: "Squishies" },
  { href: "/shop", label: "Shop All" },
  { href: "/#all-categories", label: "Toys" },
  { href: "/shop/seasonal", label: "Seasonal" },
  { href: "/about", label: "About Us" },
];

export function Navbar() {
  const pathname = usePathname();
  const { itemCount } = useCart();
  const { count: wishCount } = useWishlist();
  const [open, setOpen] = useState(false);

  useEffect(() => {
    setOpen(false);
  }, [pathname]);

  useEffect(() => {
    document.body.style.overflow = open ? "hidden" : "";
    return () => {
      document.body.style.overflow = "";
    };
  }, [open]);

  return (
    <header className="sticky top-0 z-50 border-b border-cream-200/80 bg-white/95 backdrop-blur-md">
      <div className="bg-coral-500 px-4 py-1 text-[11px] font-semibold text-white sm:py-1.5 sm:text-xs">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-2">
          <p>Free UK shipping over £{FREE_SHIPPING_GBP}</p>
          <p className="hidden items-center gap-1 sm:inline-flex">
            <MapPin className="h-3.5 w-3.5" aria-hidden />
            United Kingdom
          </p>
        </div>
      </div>

      <div className="mx-auto flex max-w-7xl items-center gap-2 px-4 py-2 sm:gap-3 sm:px-6 sm:py-2.5 lg:px-8">
        <Logo compact />

        <nav aria-label="Primary" className="hidden flex-1 items-center justify-center gap-1 lg:flex">
          {links.map((link) => {
            const active =
              pathname === link.href || (link.href !== "/shop" && pathname.startsWith(link.href));
            return (
              <Link
                key={`${link.href}-${link.label}`}
                href={link.href}
                prefetch={false}
                data-active={active ? "true" : "false"}
                className={cn(
                  "nav-link-glow rounded-full px-4 py-2.5 font-display text-lg font-extrabold tracking-tight hover:bg-cream-50 xl:px-5 xl:text-xl",
                  link.href === "/shop/squishies" && "bg-gradient-to-r from-[#FFE4F0] to-[#FFF0E8] ring-1 ring-[#E85D8C]/35",
                  active && "bg-cream-100",
                  active && link.href === "/shop/squishies" && "bg-[#E85D8C] text-white ring-[#E85D8C]",
                )}
              >
                <span className={cn("heading-glow-coral", active && link.href === "/shop/squishies" && "text-white")}>{link.label}</span>
              </Link>
            );
          })}
        </nav>

        <div className="ml-auto flex shrink-0 items-center gap-1 text-ink-700 sm:gap-1.5">
          <Link
            href="/pay"
            className={cn(
              "header-pay-now group relative hidden items-center gap-1.5 overflow-hidden rounded-full sm:inline-flex",
              "bg-gradient-to-r from-sun-300 via-sun-400 to-coral-400 px-3 py-2",
              "font-display text-[11px] font-black uppercase tracking-wide text-ink-900 sm:text-xs",
              "shadow-soft ring-1 ring-white/80 transition hover:-translate-y-0.5",
              pathname.startsWith("/pay") && "ring-coral-400",
            )}
          >
            <Sparkles className="h-3.5 w-3.5 text-coral-600" aria-hidden />
            <span className="relative z-10">Pay Now</span>
          </Link>

          <Link
            href="/shop"
            className="grid h-11 w-11 place-items-center rounded-full hover:bg-cream-100"
            aria-label="Search toys"
          >
            <Search className="h-5 w-5" />
          </Link>
          <Link
            href="/wishlist"
            className="relative grid h-11 w-11 place-items-center rounded-full hover:bg-cream-100"
            aria-label="Wishlist"
          >
            <Heart className="h-5 w-5" />
            {wishCount > 0 ? (
              <span className="absolute right-1 top-1 grid h-4 min-w-4 place-items-center rounded-full bg-coral-500 px-1 text-[10px] font-bold text-white">
                {wishCount}
              </span>
            ) : null}
          </Link>
          <Link
            href="/cart"
            className="relative grid h-11 w-11 place-items-center rounded-full hover:bg-cream-100"
            aria-label={`Cart${itemCount ? `, ${itemCount} items` : ""}`}
          >
            <ShoppingCart className="h-5 w-5" />
            {itemCount > 0 ? (
              <span className="absolute right-1 top-1 grid h-4 min-w-4 place-items-center rounded-full bg-coral-500 px-1 text-[10px] font-bold text-white">
                {itemCount}
              </span>
            ) : null}
          </Link>
          <button
            type="button"
            className="grid h-11 w-11 place-items-center rounded-full hover:bg-cream-100 lg:hidden"
            aria-expanded={open}
            aria-controls="mobile-nav"
            aria-label={open ? "Close menu" : "Open menu"}
            onClick={() => setOpen((value) => !value)}
          >
            {open ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </button>
        </div>
      </div>

      {open ? (
        <div className="lg:hidden">
          <button
            type="button"
            className="fixed inset-0 z-40 bg-ink-900/40"
            aria-label="Close menu"
            onClick={() => setOpen(false)}
          />
          <nav
            id="mobile-nav"
            aria-label="Mobile"
            className="absolute inset-x-0 top-full z-50 max-h-[min(70vh,32rem)] overflow-y-auto border-b border-cream-200 bg-white px-4 py-4 shadow-card"
          >
            <div className="grid gap-1">
              {links.map((link) => (
                <Link
                  key={`${link.href}-${link.label}-m`}
                  href={link.href}
                  prefetch={false}
                  className="nav-link-glow rounded-2xl px-4 py-3.5 font-display text-xl font-extrabold tracking-tight hover:bg-cream-100"
                >
                  <span className={cn("heading-glow-coral", pathname.startsWith("/shop/squishies") && link.href === "/shop/squishies" && open && "text-ink-800")}>{link.label}</span>
                </Link>
              ))}
              <div className="mt-2 grid grid-cols-2 gap-2">
                <Link
                  href="/cart"
                  prefetch={false}
                  className="inline-flex items-center justify-center gap-2 rounded-2xl border border-cream-200 bg-cream-50 px-4 py-3.5 font-display text-sm font-bold text-ink-800"
                >
                  <ShoppingCart className="h-4 w-4" />
                  Cart{itemCount > 0 ? ` (${itemCount})` : ""}
                </Link>
                <Link
                  href="/wishlist"
                  prefetch={false}
                  className="inline-flex items-center justify-center gap-2 rounded-2xl border border-cream-200 bg-cream-50 px-4 py-3.5 font-display text-sm font-bold text-ink-800"
                >
                  <Heart className="h-4 w-4" />
                  Wishlist
                </Link>
              </div>
              <Link
                href="/pay"
                prefetch={false}
                className="mt-1 inline-flex items-center justify-center gap-2 rounded-2xl bg-gradient-to-r from-sun-300 to-coral-400 px-4 py-3.5 font-display text-base font-black uppercase tracking-wide text-ink-900 shadow-soft"
              >
                <Sparkles className="h-4 w-4" />
                Pay Now
              </Link>
            </div>
          </nav>
        </div>
      ) : null}
    </header>
  );
}
