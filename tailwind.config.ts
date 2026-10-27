import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        coral: {
          50: "#FFF4F0",
          100: "#FFE4DB",
          200: "#FFC7B5",
          300: "#FFA185",
          400: "#FF7A55",
          500: "#F2704A",
          600: "#E85A38",
          700: "#C94A2C",
          800: "#8F2C18",
          900: "#742816",
        },
        teal: {
          50: "#F0FDFA",
          100: "#CCFBF1",
          200: "#99F6E4",
          300: "#5EEAD4",
          400: "#2DD4BF",
          500: "#14B8A6",
          600: "#0D9488",
          700: "#0F766E",
          800: "#115E59",
          900: "#134E4A",
        },
        sky: {
          50: "#F0F7FF",
          100: "#DCEBFF",
          200: "#B8D6FF",
          300: "#85B8FF",
          400: "#4A90E2",
          500: "#2B74C7",
          600: "#1D5BA3",
          700: "#184882",
          800: "#173C6B",
          900: "#16335A",
        },
        mint: {
          50: "#EEFBF6",
          100: "#D5F5E8",
          200: "#AEEBD3",
          300: "#76DBB6",
          400: "#3ECF9A",
          500: "#1BB37E",
          600: "#109066",
          700: "#0F7354",
          800: "#115C45",
          900: "#104C3A",
        },
        sun: {
          50: "#FFFBEB",
          100: "#FFF3C4",
          200: "#FFE588",
          300: "#FFD34A",
          400: "#FFC107",
          500: "#F0A202",
          600: "#D17C02",
        },
        cream: {
          50: "#FFF8F0",
          100: "#FDEFE3",
          200: "#F7E4D0",
          300: "#EDE3D4",
        },
        ink: {
          50: "#F6F4F1",
          100: "#E8E4DE",
          200: "#D2CBC0",
          300: "#AFA599",
          400: "#7D7368",
          500: "#5C534A",
          600: "#433C36",
          700: "#2F2A26",
          800: "#211E1B",
          900: "#161412",
        },
      },
      fontFamily: {
        display: ["var(--font-display)", "system-ui", "sans-serif"],
        body: ["var(--font-body)", "system-ui", "sans-serif"],
      },
      boxShadow: {
        card: "0 12px 32px -16px rgba(47, 42, 38, 0.18)",
        soft: "0 8px 22px -10px rgba(47, 42, 38, 0.12)",
        lift: "0 18px 40px -16px rgba(242, 112, 74, 0.35)",
      },
      borderRadius: {
        "4xl": "2rem",
      },
    },
  },
  plugins: [],
};

export default config;
