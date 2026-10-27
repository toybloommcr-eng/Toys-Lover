/** @type {import('next').NextConfig} */
const nextConfig = {
  // Static HTML for GitHub Pages (custom domain toybloom.co.uk via GoDaddy DNS)
  output: "export",
  trailingSlash: true,
  compress: true,
  poweredByHeader: false,
  experimental: {
    optimizePackageImports: ["lucide-react", "framer-motion"],
  },
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
