"""Render a day's carousel slides and reel for Quiick Medicine.

Usage: python3 brand/generate.py posts/YYYY-MM-DD/content.json

content.json:
{
  "cover_line1": "How to read your",
  "cover_line2": "medication label",
  "cover_sub": "Swipe through for a quick guide.",
  "points": [{"title": "1. Dosage", "body": "..."}, ...],   # 2-4 points
  "cta_line1": "Not sure about",
  "cta_line2": "anything on your label?",
  "cta_body": ["Ask your pharmacist. We're happy to help.",
               "Call 416-789-0100 or visit us in North York."],
  "caption_post": "...", "caption_reel": "..."
}
Writes carousel_N.png (1080x1080) and reel.mp4 (1080x1920) next to content.json.
"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 1080
NAVY = (10, 61, 107); BLUE = (0, 100, 154); WHITE = (255, 255, 255)
YELLOW = (253, 224, 71); GREY = (70, 80, 95); PALE = (200, 220, 240)
PHONE, EMAIL, WEB = "416-789-0100", "rx@quiickmedicine.ca", "quiickmedicine.ca"
ADDRESS = "3250 Dufferin St #6, North York, ON M6A 2T3"

INTER = "/usr/share/fonts/opentype/inter/"
DEJAVU = "/usr/share/fonts/truetype/dejavu/"
def _font(inter, dejavu, size):
    for p in (INTER + inter, DEJAVU + dejavu):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()
bold = lambda s: _font("Inter-Bold.otf", "DejaVuSans-Bold.ttf", s)
med = lambda s: _font("Inter-Medium.otf", "DejaVuSans.ttf", s)
reg = lambda s: _font("Inter-Regular.otf", "DejaVuSans.ttf", s)

_logo = Image.open(os.path.join(HERE, "logo.png")).convert("RGB")
def logo(width):
    return _logo.resize((width, int(_logo.height * width / _logo.width)), Image.LANCZOS)

def wrap(d, text, fnt, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines

def fit(d, text, start, maxw, face=bold):
    size = start
    while size > 40 and d.textlength(text, font=face(size)) > maxw:
        size -= 4
    return face(size)

def footer(d, dark=False):
    d.rectangle([0, H - 150, W, H], fill=(6, 40, 72) if dark else NAVY)
    d.text((60, H - 118), f"{PHONE}   |   {EMAIL}", font=med(30), fill=WHITE)
    d.text((60, H - 72), f"{ADDRESS}   |   {WEB}", font=reg(26), fill=PALE)

def render(c, out):
    slides = []
    im = Image.new("RGB", (W, H), WHITE); d = ImageDraw.Draw(im)
    im.paste(logo(460), (60, 60))
    d.text((60, 400), c["cover_line1"], font=fit(d, c["cover_line1"], 78, W - 120), fill=NAVY)
    d.text((60, 490), c["cover_line2"], font=fit(d, c["cover_line2"], 78, W - 120), fill=BLUE)
    d.rectangle([60, 610, 260, 620], fill=YELLOW)
    d.text((60, 650), c.get("cover_sub", "Swipe through for a quick guide."), font=reg(36), fill=GREY)
    footer(d); slides.append(im)

    for p in c["points"]:
        im = Image.new("RGB", (W, H), WHITE); d = ImageDraw.Draw(im)
        im.paste(logo(300), (60, 60))
        d.text((60, 360), p["title"], font=fit(d, p["title"], 88, W - 120), fill=NAVY)
        d.rectangle([60, 480, 260, 490], fill=YELLOW)
        y = 530
        for line in wrap(d, p["body"], reg(44), W - 120)[:5]:
            d.text((60, y), line, font=reg(44), fill=GREY); y += 62
        footer(d); slides.append(im)

    im = Image.new("RGB", (W, H), NAVY); d = ImageDraw.Draw(im)
    im.paste(logo(300), (60, 60))
    d.text((60, 360), c["cta_line1"], font=fit(d, c["cta_line1"], 80, W - 120), fill=WHITE)
    d.text((60, 450), c["cta_line2"], font=fit(d, c["cta_line2"], 80, W - 120), fill=YELLOW)
    y = 590
    for line in c.get("cta_body", [f"Ask your pharmacist. Call {PHONE}."]):
        d.text((60, y), line, font=fit(d, line, 40, W - 120, reg), fill=WHITE); y += 70
    footer(d, dark=True); slides.append(im)

    for f in os.listdir(out):
        if f.startswith("carousel_") and f.endswith(".png"):
            os.remove(os.path.join(out, f))
    names = []
    for i, s in enumerate(slides, 1):
        n = f"carousel_{i}.png"; s.save(os.path.join(out, n), optimize=True); names.append(n)

    lst = os.path.join(out, "_frames.txt")
    with open(lst, "w") as fh:
        for n in names:
            fh.write(f"file '{n}'\nduration 3\n")
        fh.write(f"file '{names[-1]}'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                    "-vf", "scale=1080:1080,pad=1080:1920:0:420:white,format=yuv420p",
                    "-r", "30", "-c:v", "libx264", "-preset", "fast", "-crf", "22",
                    "-movflags", "+faststart", os.path.join(out, "reel.mp4")], check=True)
    os.remove(lst)
    return names + ["reel.mp4"]

if __name__ == "__main__":
    path = sys.argv[1]
    with open(path) as fh:
        content = json.load(fh)
    print("\n".join(render(content, os.path.dirname(os.path.abspath(path)))))
