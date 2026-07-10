# WCDW External Media & Partner Guide

The **external-facing** companion to the internal [WCDW Asset Dashboard](https://github.com/LauraRestum/wcdw-asset-dashboard): a single page that gives media, sponsors, and community partners everything they need to talk about **Envision** and the **Celebrating Independence: White Cane Day Walk** (Dallas Zoo · Saturday, Oct 17, 2026 · 5:00–7:00 PM) — and to grab any asset in one click.

Open [`index.html`](index.html) — it is the whole product, styled and laid out like the internal **Campaign Studio** (same navy hero, split bar, tabs, cards, and shared light/dark theme). The hero carries the quick facts (date, time, venue, registration URL, live countdown), and four tabs hold the rest:

| Tab | What it gives partners |
| --- | --- |
| **Talking points** | The primary message plus short/expanded/launch/final-push variants from the 2026 Messaging Guide with copy buttons; approved headline + body + CTA for eight audiences; and Envision boilerplate, including the Dallas Lighthouse for the Blind legacy line (keep intact) and naming rules. |
| **Language & brand** | Say-this/never-that rules: *people who are blind or have low vision* (never "impaired"/BVI), no retired names, no pity framing, one CTA per asset; the five pillars; click-to-copy palette (Navy `#002855` → Terracotta `#DC4405`) and Montserrat/sentence-case type rules. |
| **PSA scripts** | Ready-to-read :10 and :30 event + awareness spots. |
| **Asset library** | Searchable, filterable gallery with lightbox preview and one-click download — logo, brand video, 14 press-resolution event photos, 5 social graphics, 5 email banners. |

## Running it locally

The page works straight from disk (double-click `index.html` — it reads the pre-generated `guide/data.js`), or serve it:

```bash
python3 -m http.server 8000   # then open http://localhost:8000/
```

## How assets work

[`manifest.json`](manifest.json) is the single source of truth — a machine-readable index of every asset with path, category, description, and keyword tags (built for search tools and AI assistants too).

- **Photos** in `assets/photos/` are exported at **press/web resolution (2400px long edge, JPEG q85)** from the internal dashboard's originals, keeping this repo light. Need the full-resolution original? It lives in the internal repo under `event-photos/`.
- **Logos, social graphics, and email banners** are full production size.

### Adding or changing an asset

1. Drop the file under `assets/…` and add an entry to `manifest.json` (path, category, description, tags).
2. Rebuild thumbnails and the embedded data:

   ```bash
   pip install Pillow   # once
   python3 guide/build.py
   ```

3. Commit the results (including `guide/thumbnails/…` and `guide/data.js`).

To pull a new photo down from the internal repo at press resolution:

```python
from PIL import Image, ImageOps
im = ImageOps.exif_transpose(Image.open("path/to/original.jpg")).convert("RGB")
im.thumbnail((2400, 2400), Image.LANCZOS)
im.save("assets/photos/name.jpg", "JPEG", quality=85, optimize=True, progressive=True)
```

## Usage notes for everything in this repo

- Event photos contain **identifiable attendees** — use them in coverage or promotion of Envision and the White Cane Day Walk only, per Envision's photo-consent and privacy practices. Credit "Courtesy of Envision" where a credit is customary.
- Refer to the audience as **people who are blind or have low vision** — never "visually impaired" or "BVI".
- When an email banner goes in an email, **hyperlink the whole image to <https://whitecanedaywalk.com>**.
- Post the 3-slide Instagram save-the-date carousel **in slide order**.
