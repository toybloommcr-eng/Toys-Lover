import Link from "next/link";
import Image from "next/image";
import { SITE_NAME } from "@/lib/constants";
import { img } from "@/lib/media";
import { cn } from "@/lib/utils";

export function Logo({
  compact = false,
  inverted = false,
  className,
}: {
  compact?: boolean;
  inverted?: boolean;
  className?: string;
}) {
  return (
    <Link
      href="/"
      aria-label={SITE_NAME}
      className={cn(
        "logo-glow group relative shrink-0",
        inverted && "logo-glow-inverted",
        className,
      )}
    >
      <Image
        src={img.logoBloom}
        alt={`${SITE_NAME} — Trendy Toys for Happy Kids`}
        width={160}
        height={160}
        quality={70}
        sizes={compact ? "64px" : inverted ? "112px" : "96px"}
        className={cn(
          "block object-cover object-center",
          compact && "h-12 w-12 sm:h-14 sm:w-14",
          !compact && !inverted && "h-20 w-20 sm:h-24 sm:w-24",
          inverted && "h-24 w-24 sm:h-28 sm:w-28",
        )}
      />
    </Link>
  );
}
