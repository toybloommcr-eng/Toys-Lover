import type { MetadataRoute } from "next";
import { SITE_URL } from "@/lib/constants";
import { products } from "@/lib/data/products";
import { categories } from "@/lib/data/categories";
import { posts } from "@/lib/data/blog";

export default function sitemap(): MetadataRoute.Sitemap {
  const staticRoutes: MetadataRoute.Sitemap = [
    "",
    "/shop/",
    "/sale/",
    "/discover/",
    "/brands/",
    "/blog/",
    "/about/",
    "/contact/",
    "/faq/",
    "/shipping/",
    "/privacy/",
    "/terms/",
    "/pay/",
  ].map((path) => ({
    url: `${SITE_URL}${path || "/"}`,
    lastModified: new Date(),
    changeFrequency: path === "" ? "daily" : "weekly",
    priority: path === "" ? 1 : path === "/shop/" ? 0.9 : 0.7,
  }));

  const productRoutes = products.map((product) => ({
    url: `${SITE_URL}/product/${product.slug}/`,
    lastModified: new Date(),
    changeFrequency: "weekly" as const,
    priority: 0.8,
  }));

  const categoryRoutes = categories.map((category) => ({
    url: `${SITE_URL}/shop/${category.slug}/`,
    lastModified: new Date(),
    changeFrequency: "weekly" as const,
    priority: 0.75,
  }));

  const blogRoutes = posts.map((post) => ({
    url: `${SITE_URL}/blog/${post.slug}/`,
    lastModified: new Date(post.date),
    changeFrequency: "monthly" as const,
    priority: 0.65,
  }));

  return [...staticRoutes, ...productRoutes, ...categoryRoutes, ...blogRoutes];
}
