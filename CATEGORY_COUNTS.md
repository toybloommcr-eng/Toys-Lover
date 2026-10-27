# Category counts

Generated after the 25 Oct 2026 catalogue audit. Hidden products are omitted from the visible column.

| Category | Slug | Visible | Hidden | All |
| --- | --- | ---: | ---: | ---: |
| Squishies | `squishies` | 52 | 150 | 202 |
| K-Pop & Collectible Figures | `action-figures` | 52 | 9 | 61 |
| Plush & Soft Toys | `plush-soft-toys` | 38 | 9 | 47 |
| Light-Up Toys | `light-up-toys` | 38 | 18 | 56 |
| Seasonal (Halloween & Christmas) | `seasonal` | 32 | 1 | 33 |
| Home & Gifts | `home-gifts` | 30 | 6 | 36 |
| Keyrings & Bag Charms | `novelty-keyrings` | 27 | 17 | 44 |
| Labubu | `labubu` | 25 | 2 | 27 |
| Outdoor & Sports | `outdoor-sports` | 19 | 6 | 25 |
| Cars & Vehicles | `cars-vehicles` | 16 | 18 | 34 |
| Bags & Accessories | `bags-accessories` | 16 | 20 | 36 |
| Role Play & Pretend Play | `role-play` | 16 | 17 | 33 |
| Dolls | `dolls` | 14 | 7 | 21 |
| Party, Hats & Dress-Up | `party-spotlight` | 12 | 13 | 25 |
| Bubbles & Water Toys | `bubble-blowers` | 11 | 9 | 20 |
| Building & Construction | `building-sets` | 7 | 5 | 12 |
| Games & Cards | `board-games` | 7 | 5 | 12 |
| Arts, Crafts & Stationery | `arts-crafts` | 7 | 1 | 8 |
| Fidget & Sensory | `fidget-spinners` | 7 | 14 | 21 |
| Baby & Toddler | `baby-toddler` | 1 | 2 | 3 |
| **Total** | | **427** | **329** | **756** |

Dolls and Plush & Soft Toys are separate aisles. Plush keyrings stay in Keyrings & Bag Charms.
Labubu keeps its own aisle; Labubu squishies stay in Squishies.
Seasonal holds Christmas lights, advent calendars and Halloween dress-up. Seasonal squishies stay in Squishies.

## Verify locally

```bash
npm install
npm run dev
```

Open http://localhost:3000 and check `/shop`, `/shop/seasonal`, `/shop/party-spotlight`, `/shop/dolls`, `/sale`. Hidden SKUs must not appear. `npm run build` should still succeed.
