# Live on toybloom.co.uk (GitHub + GoDaddy DNS only)

No Vercel. No Cloudflare. No GoDaddy paid hosting required.

## How it works
1. GitHub Actions builds the static site from this repo (`out/`).
2. GitHub Pages hosts the files.
3. GoDaddy DNS points `toybloom.co.uk` at GitHub Pages.

## GoDaddy DNS (Domain → DNS)
Delete parking A records (e.g. `3.33.130.190`, `15.197.148.33`).

Add:

| Type | Name | Value | TTL |
|------|------|--------|-----|
| A | @ | 185.199.108.153 | 600 |
| A | @ | 185.199.109.153 | 600 |
| A | @ | 185.199.110.153 | 600 |
| A | @ | 185.199.111.153 | 600 |
| CNAME | www | studyextremeconsultltd-hub.github.io | 600 |

Keep GoDaddy nameservers (`*.domaincontrol.com`).

## GitHub
- Repo: https://github.com/studyextremeconsultltd-hub/Toys-Lover
- Settings → Pages → Source: **GitHub Actions**
- Custom domain: `toybloom.co.uk` (Enforce HTTPS after DNS works)

## After each update
Push to `main` — Actions rebuilds and publishes automatically.
