#!/usr/bin/env python3
"""
Ultra-fast OCR tracklist extractor
Image -> clean TXT
No playback. No ML bloat. No nonsense.
"""

import sys
import cv2
import easyocr
from pathlib import Path

def clean_line(line):
    junk = ["track", "disc", "|", "•"]
    l = line.strip()
    for j in junk:
        l = l.replace(j, "")
    return l.strip(" -._")

def extract_tracks(image_path):
    reader = easyocr.Reader(['en'], gpu=False)

    img = cv2.imread(str(image_path))
    if img is None:
        raise ValueError("Could not load image")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 31, 2
    )

    results = reader.readtext(gray, detail=0)

    tracks = []
    for r in results:
        t = clean_line(r)
        if len(t) > 3 and not t.isdigit():
            tracks.append(t)

    return tracks

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ocr_tracks.py image.jpg")
        sys.exit(1)

    img_path = Path(sys.argv[1])
    tracks = extract_tracks(img_path)

    out = img_path.with_suffix(".txt")
    with open(out, "w", encoding="utf-8") as f:
        for t in tracks:
            f.write(t + "\n")

    print(f"✅ Extracted {len(tracks)} lines -> {out}")
