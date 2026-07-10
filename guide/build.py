#!/usr/bin/env python3
"""Build step for the WCDW External Media & Partner Guide.

Does three things, all idempotent:

  1. Generates web-sized thumbnails (max 640px long edge, JPEG q80) for every
     raster asset under ``assets/`` into ``guide/thumbnails/`` mirroring the
     source paths.
  2. Enriches ``manifest.json`` with ``type``, ``filename``, ``thumbnail`` and
     backfilled ``dimensions`` for each asset. ``manifest.json`` stays the
     single source of truth.
  3. Emits ``guide/data.js`` (``window.WCDW_GUIDE = {...}``) so the guide
     renders both on a web server / GitHub Pages *and* when ``index.html`` is
     opened directly from disk (file://).

Requires Pillow (``pip install Pillow``). Run from anywhere:

    python3 guide/build.py
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSET_DIR = os.path.join(ROOT, "assets")
THUMB_DIR = os.path.join(ROOT, "guide", "thumbnails")
MAX_EDGE = 640
QUALITY = 80
RASTER = {".jpg", ".jpeg", ".png"}


def kind(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in RASTER:
        return "image"
    if ext in (".mp4", ".mov", ".webm"):
        return "video"
    if ext in (".html", ".htm"):
        return "html"
    return "other"


def build_thumbnails():
    from PIL import Image, ImageOps

    thumbs = {}
    for dirpath, _, files in os.walk(ASSET_DIR):
        for f in files:
            if os.path.splitext(f)[1].lower() not in RASTER:
                continue
            src = os.path.join(dirpath, f)
            rel = os.path.relpath(src, ROOT)
            out_rel = os.path.splitext(rel)[0] + ".jpg"
            out = os.path.join(THUMB_DIR, out_rel)
            os.makedirs(os.path.dirname(out), exist_ok=True)
            im = ImageOps.exif_transpose(Image.open(src))
            w, h = im.size
            if im.mode in ("RGBA", "P", "LA"):
                bg = Image.new("RGB", im.size, (255, 255, 255))
                rgba = im.convert("RGBA")
                bg.paste(rgba, mask=rgba.split()[-1])
                im = bg
            else:
                im = im.convert("RGB")
            im.thumbnail((MAX_EDGE, MAX_EDGE), Image.LANCZOS)
            im.save(out, "JPEG", quality=QUALITY, optimize=True)
            thumbs[rel] = {
                "w": w,
                "h": h,
                "thumb": os.path.join("guide/thumbnails", out_rel),
            }
    return thumbs


def enrich(manifest, thumbs):
    order = [
        "path", "filename", "category", "type", "dimensions",
        "duration_seconds", "thumbnail", "description", "tags",
    ]
    clean = []
    for a in manifest["assets"]:
        p = a["path"]
        a["type"] = kind(p)
        a["filename"] = os.path.basename(p)
        if p in thumbs:
            a["thumbnail"] = thumbs[p]["thumb"]
            a["dimensions"] = f'{thumbs[p]["w"]}x{thumbs[p]["h"]}'
        clean.append({k: a[k] for k in order if k in a})
    manifest["assets"] = clean
    return manifest


def main():
    thumbs = build_thumbnails()
    with open(os.path.join(ROOT, "manifest.json")) as fp:
        manifest = json.load(fp)
    manifest = enrich(manifest, thumbs)

    with open(os.path.join(ROOT, "manifest.json"), "w") as fp:
        json.dump(manifest, fp, indent=2, ensure_ascii=False)
        fp.write("\n")

    with open(os.path.join(ROOT, "guide", "data.js"), "w") as fp:
        fp.write("/* GENERATED FILE - do not edit by hand.\n")
        fp.write("   Source of truth is /manifest.json; regenerate with guide/build.py. */\n")
        fp.write("window.WCDW_GUIDE = ")
        json.dump(manifest, fp, indent=2, ensure_ascii=False)
        fp.write(";\n")

    n = len(manifest["assets"])
    print(f"Built guide: {n} assets, {len(thumbs)} thumbnails.")


if __name__ == "__main__":
    main()
