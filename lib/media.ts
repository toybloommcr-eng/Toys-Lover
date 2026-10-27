/** Isolated studio stills and lifestyle photos. Crowded shop-floor shots are not used on the site. */

export const img = {
  heroPlay: "/images/hero-play.jpg",
  heroKids2: "/images/hero-kids-2.jpg",
  heroKids3: "/images/hero-kids-3.jpg",
  heroToys: "/images/hero-toys.jpg",
  logo: "/images/logo-mark.png",
  logoBloom: "/images/logo-bloom.jpg",
  wordmark: "/images/logo-wordmark.png",
  homeHero: "/images/home/home-hero-child.jpg",
  age012: "/images/home/age-0-12.png",
  age12: "/images/home/age-1-2.png",
  age34: "/images/home/age-3-4.png",
  age57: "/images/home/age-5-7.png",
  ageStem: "/images/home/age-stem.png",
  ageBooks: "/images/home/age-books.png",
  ageGifts: "/images/home/age-gifts.png",
  giftBirthday: "/images/home/gift-birthday.png",
  giftHoliday: "/images/home/gift-holiday.png",
  giftSchool: "/images/home/gift-school.png",
  giftRainy: "/images/home/gift-rainy.png",
  giftArt: "/images/home/gift-art.png",
  giftTravel: "/images/home/gift-travel.png",
  stem: "/images/cat-stem.jpg",
  figures: "/images/cat-figures.jpg",
  plush: "/images/cat-plush.jpg",
  blocks: "/images/cat-blocks.jpg",
  games: "/images/cat-games.jpg",
  arts: "/images/cat-arts.jpg",
  outdoor: "/images/cat-outdoor.jpg",
  baby: "/images/cat-baby.jpg",
  roleplay: "/images/cat-roleplay.jpg",
  gadgets: "/images/cat-gadgets.jpg",
  teamAmina: "/images/team-amina.jpg",
  teamHassan: "/images/team-hassan.jpg",
  teamSana: "/images/team-sana.jpg",
  pageDiscover: "/images/page-discover.jpg",
  pageSale: "/images/page-sale.jpg",
  pageContact: "/images/page-contact.jpg",
  pageShop: "/images/page-shop.jpg",
  pageBlog: "/images/page-blog.jpg",
  pageAbout: "/images/page-about.jpg",
  gardenPlay: "/images/banner-garden-play.jpg",
  squishyLane: "/images/banner-squishy-lane.jpg",
  age13: "/images/age-13-plus.jpg",
  heroVideo: "/videos/hero-play.mp4",
};

/** Real shop-floor photographs — priority product imagery. */
export const shop = {
  s01: "/images/shop/shop-01.jpg",
  s02: "/images/shop/shop-02.jpg",
  s03: "/images/shop/shop-03.jpg",
  s04: "/images/shop/shop-04.jpg",
  s05: "/images/shop/shop-05.jpg",
  s06: "/images/shop/shop-06.jpg",
  s07: "/images/shop/shop-07.jpg",
  s08: "/images/shop/shop-08.jpg",
  s09: "/images/shop/shop-09.jpg",
  s10: "/images/shop/shop-10.jpg",
  s11: "/images/shop/shop-11.jpg",
  s12: "/images/shop/shop-12.jpg",
  s13: "/images/shop/shop-13.jpg",
  s14: "/images/shop/shop-14.jpg",
  s15: "/images/shop/shop-15.jpg",
  s16: "/images/shop/shop-16.jpg",
  s17: "/images/shop/shop-17.jpg",
  s18: "/images/shop/shop-18.jpg",
  s19: "/images/shop/shop-19.jpg",
  s20: "/images/shop/shop-20.jpg",
  p01: "/images/shop/pic-01.jpg",
  p02: "/images/shop/pic-02.jpg",
  p03: "/images/shop/pic-03.jpg",
  p04: "/images/shop/pic-04.jpg",
  p05: "/images/shop/pic-05.jpg",
};

const NEW_AISLES = [
  "bubble-blowers",
  "christmas-surprise",
  "ear-buddy-plush",
  "party-flags",
  "party-spotlight",
  "kids-hats",
  "novelty-keyrings",
  "light-up-toys",
  "articulated-keyrings",
  "handheld-fans",
  "bottle-plush",
  "christmas-glow",
  "glitter-squeeze",
  "glow-wands",
  "play-balls",
  "halloween-squishies",
  "fidget-spinners",
  "monster-buddy-bags",
  "hatch-dragons",
  "fashion-play-sets",
  "monster-buddy-keyrings",
  "light-up-hats",
  "metal-keyrings",
  "mini-shoulder-bags",
  "pocket-critter-keyrings",
  "push-pop-games",
  "star-buddy-cups",
  "star-buddy-plush",
  "crunchy-squishies",
  "dumpling-squishies",
  "vaseline-squishies",
  "sugar-squishies",
  "wax-squishies",
  "small-squishies",
  "jumbo-squishies",
  "funky-frights",
  "festive-dumplings",
  "halloween-hats",
  "light-up-glasses",
  "light-up-gloves",
  "cheese-squishies",
  "glow-swords",
  "fruit-squishies",
  "food-squishies",
  "sensory-jars",
  "bath-bomb-gifts",
  "others",
] as const;

export const categoryStudio: Record<string, string> = {
  "educational-stem": img.stem,
  "action-figures": img.figures,
  "plush-soft-toys": img.plush,
  "building-sets": img.blocks,
  "board-games": img.games,
  "arts-crafts": img.arts,
  "outdoor-sports": img.outdoor,
  "baby-toddler": img.baby,
  "role-play": img.roleplay,
  squishies: "/images/categories/squishies.jpg",
  "games-gadgets": img.gadgets,
  ...Object.fromEntries(NEW_AISLES.map((slug) => [slug, `/images/categories/${slug}.jpg`])),
};

/** One isolated product per aisle tile — never a crowded shelf. */
export const categoryImage: Record<string, string> = {
  "educational-stem": "/images/categories/educational-stem.jpg",
  "action-figures": "/images/categories/action-figures.jpg",
  "plush-soft-toys": "/images/categories/plush-soft-toys.jpg",
  "building-sets": "/images/categories/building-sets.jpg",
  "board-games": "/images/categories/board-games.jpg",
  "arts-crafts": "/images/categories/squishies.jpg",
  "outdoor-sports": "/images/categories/outdoor-sports.jpg",
  "baby-toddler": "/images/categories/baby-toddler.jpg",
  "role-play": "/images/categories/role-play.jpg",
  squishies: "/images/categories/squishies.jpg",
  "games-gadgets": "/images/categories/games-gadgets.jpg",
  ...Object.fromEntries(NEW_AISLES.map((slug) => [slug, `/images/categories/${slug}.jpg`])),
};

export function productShot(slug: string) {
  return `/images/products/${slug}.jpg`;
}

/** Explicit product photos win. Otherwise fall back to /images/products/<slug>.jpg. */
export function productGallery(slug: string, _categorySlug?: string, images?: string[]) {
  const listed = images?.filter((src) => src.startsWith("/images/products/"));
  if (listed && listed.length > 0) return listed;
  return [productShot(slug)];
}

export function isTelegramPhoto(src?: string | null) {
  return Boolean(src && /\/images\/products\/telegram\//.test(src));
}

export function isStudioPhoto(src?: string | null) {
  return Boolean(src && (/\/images\/products\//.test(src) || isTelegramPhoto(src)));
}

/** Isolated catalog stills that must stay fully inside the tile. */
export function isFramedPhoto(src?: string | null) {
  return Boolean(src && (/\/images\/(products|categories)\//.test(src) || isTelegramPhoto(src)));
}

export function isShopPhoto(src?: string | null) {
  return Boolean(src && /\/images\/shop\//.test(src));
}

const RELATED_PHOTOS: Record<string, string[]> = {
  "educational-stem": [
    productShot("eva-number-foam-puzzle"),
    productShot("explorer-binoculars"),
    productShot("space-explorer-kit"),
  ],
  "action-figures": [
    productShot("hipper-collectible-pack"),
    productShot("big-into-energy-surprise"),
    productShot("hatch-dragon-egg-01"),
  ],
  "plush-soft-toys": [
    productShot("snuggle-puppy-plush"),
    productShot("unicorn-snuggle-plush"),
    productShot("wrap-around-plush-monkey"),
  ],
  "building-sets": [
    productShot("dino-expedition-build"),
    productShot("mech-pioneer-build"),
    productShot("eva-number-foam-puzzle"),
  ],
  "bubble-blowers": [
    productShot("animal-bubble-camera-set"),
    productShot("funtasy-bubble-gun"),
    productShot("rocket-48-bubble-machine"),
  ],
  "board-games": [
    productShot("soccer-star-table-game"),
    productShot("tabletop-football-pitch"),
    productShot("stage-quest-card-game"),
  ],
  "arts-crafts": [
    productShot("diy-bead-jewelry-set"),
    productShot("space-explorer-kit"),
    productShot("eva-number-foam-puzzle"),
  ],
  "outdoor-sports": [
    productShot("sports-ball-pack"),
    productShot("soft-dart-modular-blaster"),
    productShot("character-play-balls"),
  ],
  "baby-toddler": [
    productShot("piano-fitness-gym"),
    productShot("dino-world-musical-mat"),
    productShot("wrap-around-plush-monkey"),
  ],
  "role-play": [
    productShot("dream-castle-playset"),
    productShot("doctor-clinic-set"),
    productShot("unicorn-vanity-kit"),
  ],
  "games-gadgets": [
    productShot("rc-monster-truck"),
    productShot("twin-track-rc-set"),
    productShot("speed-phantom-rc"),
  ],
  others: [
    productShot("racers-camera-car"),
    productShot("colorful-gear-sport-car"),
    productShot("crystal-mood-lamp"),
  ],
  "christmas-surprise": [productShot("christmas-surprise-figure-bag")],
  "ear-buddy-plush": [productShot("ear-buddy-plush-pair"), productShot("glowing-ear-buddy-plush")],
  "party-flags": [productShot("union-jack-flag"), productShot("st-george-england-flag")],
  "party-spotlight": [
    productShot("rainbow-cloud-flop-hat"),
    productShot("neon-star-wand"),
    productShot("sequin-cowboy-hat"),
  ],
  "kids-hats": [
    productShot("candy-sports-bucket-hats"),
    productShot("cool-sports-bucket-hats"),
    productShot("red-sports-bucket-hats"),
  ],
  "novelty-keyrings": [
    productShot("mini-sneaker-keyrings"),
    productShot("speed-crew-keyrings"),
    productShot("alien-crew-keyrings"),
  ],
  "light-up-toys": [
    productShot("lace-heart-wands"),
    productShot("lollipop-light-wands"),
    productShot("fibre-unicorn-wands"),
  ],
  "articulated-keyrings": [
    productShot("rainbow-sphynx-keyring-set"),
    productShot("sunset-sphynx-keyring"),
    productShot("teal-jointed-lizard"),
  ],
  "handheld-fans": [
    productShot("chrome-spray-fan"),
    productShot("navy-pocket-fan"),
    productShot("mint-table-fan"),
  ],
  "bottle-plush": [productShot("sports-bottle-plush-set")],
  "christmas-glow": [
    productShot("santa-snow-train"),
    productShot("mini-lit-christmas-trees"),
    productShot("christmas-booth-lanterns"),
  ],
  "glitter-squeeze": [
    productShot("crystal-unicorn-squeeze"),
    productShot("jumbo-squishy-surprise-bag"),
    productShot("ra-579-31-unicorn-squishy"),
  ],
  "glow-wands": [
    productShot("trio-glow-spinner-wands"),
    productShot("spinner-character-wands"),
    productShot("bow-kitty-plush-wand"),
  ],
  "play-balls": [productShot("character-play-balls")],
  "halloween-squishies": [
    productShot("halloween-butter-squishy"),
    productShot("halloween-tray-squishy-01"),
    productShot("halloween-tray-squishy-02"),
  ],
  "fidget-spinners": [
    productShot("hero-fidget-spinner-range"),
    productShot("ra-103-2key-spinner"),
    productShot("dumpling-pop-spinner"),
  ],
  "monster-buddy-bags": [
    productShot("monster-buddy-big-bag-01"),
    productShot("fluffy-monster-bag-charm"),
    productShot("monster-buddy-small-bag-01"),
  ],
  "hatch-dragons": [productShot("hatch-dragon-egg-01"), productShot("hatch-dragon-egg-02")],
  "fashion-play-sets": [productShot("fashion-play-set-01"), productShot("fashion-play-set-02")],
  "monster-buddy-keyrings": [productShot("monster-buddy-keyring-01"), productShot("monster-buddy-keyring-05")],
  "light-up-hats": [productShot("light-up-party-hat-01"), productShot("light-up-party-hat-05"), productShot("glow-party-hat")],
  "metal-keyrings": [productShot("metal-charm-keyring-01"), productShot("metal-charm-keyring-03")],
  "mini-shoulder-bags": [productShot("mini-shoulder-bag")],
  "pocket-critter-keyrings": [productShot("pocket-critter-keyring-01"), productShot("pocket-critter-keyring-02")],
  "push-pop-games": [productShot("push-pop-game-01"), productShot("push-pop-game-03")],
  "star-buddy-cups": [productShot("star-buddy-cup-01"), productShot("star-buddy-cup-03")],
  "star-buddy-plush": [productShot("star-buddy-plush-01"), productShot("star-buddy-plush-04")],
  "crunchy-squishies": [productShot("crunchy-squishy-01"), productShot("crunchy-squishy-03"), productShot("crunchy-squishy-06")],
  "funky-frights": [productShot("funky-fright-01"), productShot("funky-fright-02"), productShot("funky-fright-03")],
  "festive-dumplings": [productShot("festive-dumpling-01"), productShot("festive-dumpling-03"), productShot("mini-festive-dumpling")],
  "halloween-hats": [productShot("halloween-party-hat")],
  "light-up-glasses": [productShot("light-up-shutter-glasses")],
  "light-up-gloves": [productShot("light-up-party-gloves")],
  "cheese-squishies": [productShot("mini-cheese-squishy-03"), productShot("jumbo-cheese-squishy-01"), productShot("jumbo-cheese-squishy-02")],
  "glow-swords": [productShot("pixel-glow-sword-01"), productShot("pixel-glow-sword-02"), productShot("pixel-glow-sword-03")],
};

function shiftIndex(slug: string) {
  return slug.split("").reduce((total, char) => total + char.charCodeAt(0), 0);
}

export function productPhotos(categorySlug: string, slug: string): string[] {
  const pool = RELATED_PHOTOS[categorySlug] ?? [productShot("snuggle-puppy-plush")];
  const start = shiftIndex(slug) % pool.length;
  return Array.from(new Set(pool.map((_, index) => pool[(start + index) % pool.length]))).slice(0, 3);
}

export function fallbackPhoto(src?: string | null) {
  return src || img.heroToys;
}

export const HERO_SLIDES = [
  {
    src: productShot("rainbow-butter-squishy"),
    alt: "Rainbow butter squishy",
    title: "Squishies are the main event.",
    text: "Fruit, butter, and jelly fidgets — each with its own photo.",
  },
  {
    src: productShot("gummy-bear-squeeze-box"),
    alt: "Gummy bear squeeze box",
    title: "Slow-rise till-point hits.",
    text: "Counter-ready squeezes you can see before you order.",
  },
  {
    src: productShot("grape-cluster-squishy"),
    alt: "Grape cluster squishy",
    title: "Butter bricks and fruit fidgets.",
    text: "Viral squeezes, listed one by one at UK high-street prices.",
  },
];
