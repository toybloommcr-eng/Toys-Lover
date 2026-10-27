#!/usr/bin/env node
/**
 * Apply WhatsApp import plan to Toy Bloom on the laptop.
 * - Copy primary (+extra) images into public/images/products/
 * - Unhide matched slugs
 * - Update name, categorySlug, images, priceTBC on existing stock entries
 * - Append new products to lib/data/whatsapp-stock.ts and wire into products.ts
 * - Update assigned-categories.ts
 * Prices left as priceTBC (user will set later).
 */
import fs from 'fs';
import path from 'path';

const ROOT = process.argv[2] || 'C:/Ai/toybloom';
const planPath = path.join(ROOT, 'whatsapp-photos/wa-import-plan.json');
const waImgDir = path.join(ROOT, 'public/images/products/whatsapp');
const prodImgDir = path.join(ROOT, 'public/images/products');
const plan = JSON.parse(fs.readFileSync(planPath, 'utf8'));
const products = plan.products;

function ensureDir(d){ fs.mkdirSync(d,{recursive:true}); }
ensureDir(prodImgDir);

function copyImage(srcName, destBase){
  const src = path.join(waImgDir, srcName);
  if (!fs.existsSync(src)) {
    // try extracted path under whatsapp-photos
    const alt = path.join(ROOT, 'whatsapp-photos/INCOMING/2026-10-25', srcName);
    if (fs.existsSync(alt)) {
      fs.copyFileSync(alt, path.join(prodImgDir, destBase));
      return `/images/products/${destBase}`;
    }
    console.warn('MISSING image', srcName);
    return null;
  }
  fs.copyFileSync(src, path.join(prodImgDir, destBase));
  return `/images/products/${destBase}`;
}

const imageMap = {}; // slug -> [paths]
for (const p of products) {
  const slug = p.match_existing_slug || p.slug;
  const primaryExt = path.extname(p.primary_image_file).toLowerCase() === '.jpeg' ? '.jpg' : path.extname(p.primary_image_file);
  const primaryName = `${slug}${primaryExt === '.jpg' || primaryExt === '.jpeg' ? '.jpg' : primaryExt}`;
  // normalize to .jpg name for site
  const destPrimary = `${slug}.jpg`;
  const urls = [];
  const u = copyImage(p.primary_image_file, destPrimary);
  if (u) urls.push(u);
  let i = 2;
  for (const extra of (p.extra_image_files || [])) {
    const dest = `${slug}-${i}.jpg`;
    const eu = copyImage(extra, dest);
    if (eu) urls.push(eu);
    i++;
  }
  imageMap[slug] = urls;
  // also map plan slug for new products
  imageMap[p.slug] = urls;
}

// --- hidden-products.ts: remove unhide slugs ---
const hiddenPath = path.join(ROOT, 'lib/data/hidden-products.ts');
let hidden = fs.readFileSync(hiddenPath, 'utf8');
const unhide = products.filter(p => p.action === 'unhide_and_update' && p.match_existing_slug).map(p => p.match_existing_slug);
for (const slug of unhide) {
  const re = new RegExp(`\\s*"${slug}",?\\r?\\n`, 'g');
  hidden = hidden.replace(re, '\n');
}
fs.writeFileSync(hiddenPath, hidden);
console.log('unhid', unhide.length, 'slugs');

// --- assigned-categories.ts ---
const assignedPath = path.join(ROOT, 'lib/data/assigned-categories.ts');
let assigned = fs.readFileSync(assignedPath, 'utf8');
for (const p of products) {
  const slug = p.match_existing_slug || p.slug;
  const cat = p.category_slug;
  const lineRe = new RegExp(`("${slug}"\\s*:\\s*")[^"]+(")`);
  if (lineRe.test(assigned)) {
    assigned = assigned.replace(lineRe, `$1${cat}$2`);
  } else {
    // insert before closing };
    assigned = assigned.replace(/\n\};\s*$/, `\n  "${slug}": "${cat}",\n};\n`);
  }
}
fs.writeFileSync(assignedPath, assigned);
console.log('updated assigned-categories');

// --- Update name/category/images/priceTBC in all stock *.ts ---
const dataDir = path.join(ROOT, 'lib/data');
const stockFiles = fs.readdirSync(dataDir).filter(f => f.endsWith('.ts'));

function updateObjectBlock(src, slug, updates) {
  // Find slug: "slug" block starting at { containing that slug
  const slugIdx = src.indexOf(`slug: "${slug}"`);
  if (slugIdx < 0) return { src, found: false };
  // walk back to opening {
  let start = slugIdx;
  while (start > 0 && src[start] !== '{') start--;
  // walk forward with brace depth
  let depth = 0, end = start;
  for (; end < src.length; end++) {
    if (src[end] === '{') depth++;
    else if (src[end] === '}') {
      depth--;
      if (depth === 0) { end++; break; }
    }
  }
  let block = src.slice(start, end);
  if (updates.name) {
    block = block.replace(/name:\s*"[^"]*"/, `name: ${JSON.stringify(updates.name)}`);
  }
  if (updates.categorySlug) {
    if (/categorySlug:\s*"/.test(block)) {
      block = block.replace(/categorySlug:\s*"[^"]*"/, `categorySlug: "${updates.categorySlug}"`);
    } else {
      block = block.replace(/slug:\s*"[^"]*",/, (m) => `${m}\n    categorySlug: "${updates.categorySlug}",`);
    }
  }
  if (updates.images && updates.images.length) {
    const imgLit = `[${updates.images.map(u => JSON.stringify(u)).join(', ')}]`;
    if (/images:\s*\[/.test(block)) {
      block = block.replace(/images:\s*\[[^\]]*\]/s, `images: ${imgLit}`);
    } else {
      block = block.replace(/slug:\s*"[^"]*",/, (m) => `${m}\n    images: ${imgLit},`);
    }
  }
  if (updates.priceTBC) {
    if (/priceTBC\s*:/.test(block)) {
      block = block.replace(/priceTBC\s*:\s*(true|false)/, 'priceTBC: true');
    } else {
      block = block.replace(/price:\s*[0-9.]+,?/, (m) => `${m}\n    priceTBC: true,`);
    }
  }
  if (updates.shortDescription) {
    if (/shortDescription:\s*"/.test(block)) {
      block = block.replace(/shortDescription:\s*"(?:\\.|[^"\\])*"/, `shortDescription: ${JSON.stringify(updates.shortDescription)}`);
    }
  }
  return { src: src.slice(0, start) + block + src.slice(end), found: true };
}

let updatedExisting = 0;
let missingExisting = [];
for (const p of products.filter(x => x.action === 'unhide_and_update')) {
  const slug = p.match_existing_slug;
  const imgs = imageMap[slug] || [];
  let foundAny = false;
  for (const f of stockFiles) {
    const fp = path.join(dataDir, f);
    let src = fs.readFileSync(fp, 'utf8');
    if (!src.includes(`slug: "${slug}"`)) continue;
    const r = updateObjectBlock(src, slug, {
      name: p.title_en,
      categorySlug: p.category_slug,
      images: imgs,
      priceTBC: true,
      shortDescription: p.title_en,
    });
    if (r.found) {
      fs.writeFileSync(fp, r.src);
      foundAny = true;
      updatedExisting++;
      console.log('updated', slug, 'in', f);
      break;
    }
  }
  if (!foundAny) missingExisting.push(slug);
}
console.log('updatedExisting', updatedExisting, 'missing', missingExisting);

// --- New products → whatsapp-stock.ts ---
const news = products.filter(p => p.action === 'new_product');
function esc(s){ return JSON.stringify(s); }
const newEntries = news.map(p => {
  const imgs = imageMap[p.slug] || [];
  const imgLit = imgs.length ? `[${imgs.map(esc).join(', ')}]` : `["/images/products/${p.slug}.jpg"]`;
  return `  {
    slug: ${esc(p.slug)},
    name: ${esc(p.title_en)},
    price: 0,
    priceTBC: true,
    ageRange: "3-5 years",
    brand: "Toy Bloom Wholesale",
    theme: "WhatsApp new stock",
    categorySlug: ${esc(p.category_slug)},
    images: ${imgLit},
    shortDescription: ${esc(p.title_en)},
    description: ${esc(p.title_en + '. Wholesale price on request — ask for a quote.')},
    features: [${p.item_no ? esc('Item no: '+p.item_no)+', ' : ''}${esc('Price on request')}, ${esc('Added from WhatsApp photos 25 Oct 2026')}],
    safety: "Use under adult supervision. Not for children who mouth small parts.",
    materials: "As supplied by manufacturer.",
    isNew: true,
    stock: 50,
  }`;
}).join(',\n');

const waStock = `import type { Product } from "@/lib/types";

/** Products added from WhatsApp Unknown zip 2026-10-25. Prices left TBC. */
export const whatsappStock: Product[] = [
${newEntries}
];
`;
fs.writeFileSync(path.join(dataDir, 'whatsapp-stock.ts'), waStock);
console.log('wrote whatsapp-stock.ts with', news.length, 'products');

// Wire into products.ts
const productsPath = path.join(dataDir, 'products.ts');
let productsTs = fs.readFileSync(productsPath, 'utf8');
if (!productsTs.includes('whatsapp-stock')) {
  productsTs = productsTs.replace(
    /import \{ telegramStock \} from "@\/lib\/data\/telegram-stock";/,
    `import { telegramStock } from "@/lib/data/telegram-stock";\nimport { whatsappStock } from "@/lib/data/whatsapp-stock";`
  );
  // Find catalog array concat / spread — look for telegramStock usage
  if (productsTs.includes('...telegramStock')) {
    productsTs = productsTs.replace('...telegramStock', '...telegramStock,\n  ...whatsappStock');
  } else if (productsTs.includes('telegramStock,')) {
    productsTs = productsTs.replace('telegramStock,', 'telegramStock,\n  ...whatsappStock,');
  } else {
    // append before rank/filter
    productsTs = productsTs.replace(
      /const catalog: Product\[\] = \[/,
      'const catalog: Product[] = [\n  ...whatsappStock,'
    );
  }
  fs.writeFileSync(productsPath, productsTs);
  console.log('wired whatsappStock into products.ts');
} else {
  console.log('products.ts already imports whatsapp-stock');
}

console.log(JSON.stringify({
  unhide: unhide.length,
  newProducts: news.length,
  missingExisting,
  imageMapped: Object.keys(imageMap).length,
}, null, 2));
