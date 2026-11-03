from PIL import Image, ImageDraw, ImageFont
W = H = 1080
NAVY = (10, 61, 107); BLUE = (0, 100, 154); LIGHT = (230, 241, 251)
WHITE = (255, 255, 255); YELLOW = (253, 224, 71); GREY = (70, 80, 95)
F = "/usr/share/fonts/opentype/inter/"
def font(name, size): return ImageFont.truetype(F + name, size)
bold = lambda s: font("Inter-Bold.otf", s)
med = lambda s: font("Inter-Medium.otf", s)
reg = lambda s: font("Inter-Regular.otf", s)
logo = Image.open("logo_crop.png").convert("RGB")
logo_w = 460
logo = logo.resize((logo_w, int(logo.height * logo_w / logo.width)), Image.LANCZOS)

def wrap(draw, text, fnt, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def footer(d, dark=False):
    col = WHITE if dark else NAVY
    sub = (200, 220, 240) if dark else GREY
    d.rectangle([0, H - 150, W, H], fill=NAVY if not dark else (6, 40, 72))
    d.text((60, H - 118), "416-789-0100   |   rx@quiickmedicine.ca", font=med(30), fill=WHITE)
    d.text((60, H - 72), "3250 Dufferin St #6, North York, ON M6A 2T3   |   quiickmedicine.ca", font=reg(26), fill=(200, 220, 240))

def base(bg=WHITE):
    im = Image.new("RGB", (W, H), bg); d = ImageDraw.Draw(im)
    im.paste(logo, (60, 60), logo if False else None)
    return im, d

slides = []
# 1 cover
im = Image.new("RGB", (W, H), WHITE); d = ImageDraw.Draw(im)
im.paste(logo, (60, 60))
d.text((60, 400), "How to read your", font=bold(78), fill=NAVY)
d.text((60, 490), "medication label", font=bold(78), fill=BLUE)
d.rectangle([60, 610, 260, 620], fill=YELLOW)
d.text((60, 650), "Swipe through for a quick guide.", font=reg(36), fill=GREY)
footer(d); slides.append(im)

# 2-4 content
content = [
    ("1. Dosage", "Find how much to take in each dose. It's usually written as a number of tablets, capsules, or millilitres."),
    ("2. Timing", "Check how often to take it, and whether it's taken with food or at a set time of day."),
    ("3. Expiry and storage", "Check the expiry date before you use it. Store it in a cool, dry place, away from children."),
]
for title, body in content:
    im = Image.new("RGB", (W, H), WHITE); d = ImageDraw.Draw(im)
    im.paste(logo.resize((300, int(logo.height*300/logo.width))), (60, 60))
    d.text((60, 360), title, font=bold(88), fill=NAVY)
    d.rectangle([60, 480, 260, 490], fill=YELLOW)
    y = 530
    for line in wrap(d, body, reg(44), W - 120):
        d.text((60, y), line, font=reg(44), fill=GREY); y += 62
    footer(d); slides.append(im)

# 5 ask pharmacist (dark)
im = Image.new("RGB", (W, H), NAVY); d = ImageDraw.Draw(im)
im.paste(logo.resize((300, int(logo.height*300/logo.width))), (60, 60))
d.text((60, 360), "Not sure about", font=bold(80), fill=WHITE)
d.text((60, 450), "anything on your label?", font=bold(80), fill=YELLOW)
d.text((60, 590), "Ask your pharmacist. We're happy to help.", font=reg(40), fill=WHITE)
d.text((60, 660), "Call 416-789-0100 or visit us in North York.", font=reg(40), fill=WHITE)
footer(d, dark=True); slides.append(im)

for i, s in enumerate(slides, 1):
    s.save(f"carousel_{i}.png", optimize=True)
print("saved", len(slides))
