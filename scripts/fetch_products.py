"""Download product photos from quiickmedicine.ca into media/products/ (runs on GitHub Actions).

Writes media/products/index.json: [{name, slug, permalink, categories, tags, files}]
"""
import io, json, os, re, sys, time, urllib.parse, urllib.request
from PIL import Image

SITE = "https://quiickmedicine.ca"
OUT = os.path.join(os.path.dirname(__file__), "..", "media", "products")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/130.0 Safari/537.36")
os.makedirs(OUT, exist_ok=True)

def get(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=40) as r:
        data = r.read()
    return data if binary else data.decode("utf-8", "replace")

def save_image(src, base):
    try:
        im = Image.open(io.BytesIO(get(src, binary=True)))
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, (255, 255, 255)); bg.paste(im, mask=im.split()[3])
        bg.thumbnail((1200, 1200))
        name = base + ".jpg"
        bg.save(os.path.join(OUT, name), quality=88)
        return name
    except Exception as e:
        print("image failed", src, e)
        return None

products = []
# 1) WooCommerce Store API (public, no auth)
try:
    page = 1
    while True:
        data = json.loads(get(f"{SITE}/wp-json/wc/store/v1/products?per_page=100&page={page}"))
        if not data:
            break
        for p in data:
            products.append({
                "name": re.sub("<[^>]+>", "", p.get("name", "")),
                "slug": p.get("slug"),
                "permalink": p.get("permalink"),
                "categories": [c.get("name") for c in p.get("categories", [])],
                "tags": [t.get("name") for t in p.get("tags", [])],
                "images": [i.get("src") for i in p.get("images", [])][:2],
            })
        page += 1
        time.sleep(1)
    print("store api products:", len(products))
except Exception as e:
    print("store api failed:", e)

# 2) Fallback: product sitemap + og:image
if not products:
    urls = []
    for sm in ("/product-sitemap.xml", "/wp-sitemap-posts-product-1.xml", "/sitemap_index.xml"):
        try:
            xml = get(SITE + sm)
            urls += re.findall(r"<loc>([^<]*/product/[^<]*)</loc>", xml)
        except Exception as e:
            print("sitemap failed", sm, e)
    for u in sorted(set(urls))[:300]:
        try:
            h = get(u)
            og = re.search(r'property="og:image"\s+content="([^"]+)"', h)
            t = re.search(r'property="og:title"\s+content="([^"]+)"', h)
            cats = re.findall(r'rel="tag">([^<]+)</a>', h)
            products.append({"name": t.group(1) if t else u, "slug": u.rstrip("/").split("/")[-1], "permalink": u,
                             "categories": cats, "tags": [], "images": [og.group(1)] if og else []})
            time.sleep(0.5)
        except Exception as e:
            print("page failed", u, e)
    print("sitemap products:", len(products))

index = []
for p in products:
    files = []
    for n, src in enumerate(p.pop("images")):
        if src:
            f = save_image(src, f"{p['slug']}-{n + 1}")
            if f:
                files.append(f)
    p["files"] = files
    index.append(p)
with open(os.path.join(OUT, "index.json"), "w") as fh:
    json.dump(index, fh, indent=1, ensure_ascii=False)
print("saved", sum(len(p["files"]) for p in index), "images for", len(index), "products")
if not index:
    sys.exit(1)
