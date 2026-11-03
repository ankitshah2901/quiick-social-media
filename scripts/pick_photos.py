"""Pick safe over-the-counter product photos for a post theme.

Usage: python3 scripts/pick_photos.py <theme> [count]
Prints JSON: [{"photo": "media/products/x.jpg", "name": ..., "categories": [...]}, ...]

Only products in THEMES categories are returned, and any product that is also in an EXCLUDED
category is never returned. Captions and slide text still talk about the CATEGORY, not the brand.
"""
import html, json, os, random, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, "media", "products", "index.json")

THEMES = {
    "cold-flu": ["Cough and Cold", "Cough and Congestion", "Dry Cough", "Mucus and Phlegm", "Nasal Spray", "Sinus", "Fever and Pain"],
    "pain": ["Fever and Pain", "Headache", "Muscle and Back Pain", "Joint and Arthritis Pain", "Topical Pain Relief", "Pain", "For Pain"],
    "allergy": ["Allergy", "Allergy Relief", "Sinus", "Nasal Spray"],
    "digestion": ["Antacid and Heartburn", "Anti-Diarrhea and Gas", "Digestion", "Digestive Aid & Probiotics", "Fiber and Laxatives",
                  "Gastrointestinal Health", "For Digestion", "Probiotics", "Constipation & Gut Health"],
    "sleep": ["For Sleep", "Melatonin", "Sleep & Relaxation", "Stress Support"],
    "vitamin-d": ["Vitamins D3", "Vitamin D"],
    "immune": ["Immune Supporter", "Immune Support", "Vitamins C", "Vitamin C"],
    "vitamins": ["Multivitamins", "Vitamins and Minerals", "Magnesium", "Iron", "Calcium", "Vitamin B12", "Fish oils"],
    "skin": ["Face and Body Care", "Moisturiser", "Lip Balm", "Beauty & Personal Care"],
    "sun": ["Sunscreen"],
    "eyes": ["Dry Eye", "Eye Health", "Contact Lens Solutions"],
    "diabetes": ["Diabetes Care", "At-Home Diagnostic Test Kits & Monitoring Devices"],
    "first-aid": ["Wound care and Dressing", "Home Health"],
    "travel": ["Motion Sickness and Nausea", "Motion Sickness, Vomiting and Nausea", "Hydration & Electrolytes", "Electrolytes"],
    "heart": ["For Heart Health", "Cardiovascular Support", "Fish oils"],
    "joints": ["Joint and Arthritis Pain", "Healthy Joints", "Bone Support"],
}
EXCLUDED = {
    "Condoms", "Lubricants", "Yeast Infection and Vaginal Infection", "Pregnancy Tests / Pregnancy Control", "Ovulation Test",
    "Fertility Tests", "Women's Health & Family Planning", "Female Reproductive Health", "Estrogen Support", "Menopause",
    "Hemorrhoids Pain & Itch", "Nicotine Gum", "Nicotine Pouches", "Smoking Cessation", "Weight Management",
    "Weight Management & Wellness", "Prostate Support", "Thyroid Support", "Targeted Therapy", "Infection", "Corneal edema",
    "Infant Headache", "Kids & Baby", "Blood Sugar", "Berberine", "Histamine Intolerance", "Adrenal Support",
}
NAME_EXCLUDED = re.compile(r"child|kid|infant|baby|pediatric|junior|suppositor|vaginal|condom|nicotine|diet|weight|slim|keto", re.I)

def load():
    with open(INDEX) as fh:
        items = json.load(fh)
    for p in items:
        p["categories"] = [html.unescape(c) for c in p.get("categories", [])]
        p["name"] = html.unescape(p.get("name", ""))
    return items

def pick(theme, count=3, seed=None):
    cats = set(THEMES[theme])
    pool = [p for p in load() if p.get("files") and cats & set(p["categories"]) and not EXCLUDED & set(p["categories"]) and not NAME_EXCLUDED.search(p["name"])]
    random.Random(seed).shuffle(pool)
    return [{"photo": f"media/products/{p['files'][0]}", "name": p["name"], "categories": p["categories"]} for p in pool[:count]]

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in THEMES:
        print("themes:", ", ".join(THEMES)); sys.exit(1)
    print(json.dumps(pick(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 3), indent=1, ensure_ascii=False))
