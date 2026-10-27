"use client";

import Image, { type ImageProps } from "next/image";
import { useEffect, useState } from "react";
import { img } from "@/lib/media";

type Props = Omit<ImageProps, "src" | "alt"> & {
  src?: string | null;
  alt: string;
  fallback?: string;
};

export function SafeImage({ src, alt, fallback = img.heroToys, onError, ...rest }: Props) {
  const initial = src || fallback;
  const [current, setCurrent] = useState(initial);

  useEffect(() => {
    setCurrent(src || fallback);
  }, [src, fallback]);

  return (
    <Image
      {...rest}
      src={current}
      alt={alt}
      onError={(event) => {
        if (current !== fallback) setCurrent(fallback);
        onError?.(event);
      }}
    />
  );
}
