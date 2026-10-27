import type { FaqItem } from "@/lib/types";

export const faqs: FaqItem[] = [
  {
    group: "Shipping",
    question: "Where do you ship from, and how long does delivery take?",
    answer:
      "Orders ship from our Manchester shop in the United Kingdom. Most UK addresses receive parcels in 1–3 working days. You will receive a tracking note by email.",
  },
  {
    group: "Shipping",
    question: "Do you offer free shipping?",
    answer:
      "Yes. Standard UK shipping is free on orders over £60. Below that, a flat UK rate applies. Expedited options can be selected at checkout.",
  },
  {
    group: "Shipping",
    question: "Can I change my address after placing an order?",
    answer:
      "If the parcel has not been handed to the courier, write to hello@toybloom.example with your order number. Once it is in transit, we can help redirect only where the courier allows it.",
  },
  {
    group: "Returns",
    question: "What is your return window?",
    answer:
      "You have 14 days after delivery to start a return for unused items in original packaging. Opened toys that have been played with cannot be resold for safety reasons, except in the case of a defect.",
  },
  {
    group: "Returns",
    question: "How do I return a damaged or incorrect item?",
    answer:
      "Photograph the issue, keep the packaging, and email us within 48 hours of delivery. We will arrange a replacement or refund without asking you to pay return postage for our mistake.",
  },
  {
    group: "Safety",
    question: "How do you check toys for safety?",
    answer:
      "We only list products that meet recognised standards such as EN 71 or ASTM F963 (as applicable). Product pages list materials, age guidance, and supervision notes.",
  },
  {
    group: "Safety",
    question: "Are your materials non-toxic?",
    answer:
      "We favour food-grade silicone, organic cotton, water-based paints, and FSC wood. Each product’s Safety & materials section names what you are buying.",
  },
  {
    group: "Age",
    question: "How should I use the age ranges?",
    answer:
      "Age marks are about small parts, strength, and typical development — not a child’s intelligence. If your child is between stages, choose the more conservative option for unsupervised play.",
  },
  {
    group: "Age",
    question: "Can I buy a STEM kit for a younger child if I supervise?",
    answer:
      "Often yes. Check the product page: some kits say “10+ with an adult.” Supervision does not make tiny parts safe for toddlers.",
  },
  {
    group: "Payments",
    question: "Which payment methods do you accept?",
    answer:
      "We accept secure deposits and payments through Stripe (cards) and PayPal. Tap Pay Now, enter your details on Toy Bloom, then finish on Stripe or PayPal’s official checkout. Prices are in pounds sterling.",
  },
  {
    group: "Orders",
    question: "Can I order for pickup in Manchester?",
    answer:
      "Yes — choose local pickup at checkout and we will confirm when your bag is ready at 14 King Street Arcade. Bring the confirmation email.",
  },
  {
    group: "Orders",
    question: "Do you wrap gifts?",
    answer:
      "We can add simple kraft wrap and a handwritten note. Mention it in the checkout comments.",
  },
];

export const faqGroups = Array.from(new Set(faqs.map((item) => item.group)));
