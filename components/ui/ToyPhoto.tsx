import Image from "next/image";
import { cn } from "@/lib/utils";
import { isFramedPhoto, isShopPhoto, isStudioPhoto } from "@/lib/media";

export function ToyPhoto({
  src,
  alt,
  sizes,
  quality = 82,
  priority,
  className,
  fit,
}: {
  src?: string | null;
  alt: string;
  sizes: string;
  quality?: number;
  priority?: boolean;
  className?: string;
  fit?: "contain" | "cover";
}) {
  const framed = isFramedPhoto(src);
  const studio = isStudioPhoto(src);
  const shopFloor = isShopPhoto(src);
  const mode = fit ?? (framed || studio ? "contain" : "cover");
  const image = src || "/images/hero-play.jpg";

  return (
    <div
      className={cn(
        "media-hover-frame relative overflow-hidden",
        "bg-white",
        className,
      )}
    >
      <Image
        src={image}
        alt={alt}
        fill
        sizes={sizes}
        quality={quality}
        priority={priority}
        decoding={priority ? "sync" : "async"}
        className={
          mode === "contain"
            ? "h-full w-full object-contain object-center bg-white p-0.5 sm:p-1.5"
            : "object-cover object-center"
        }
      />
    </div>
  );
}
