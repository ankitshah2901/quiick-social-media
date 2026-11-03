"""Render a day's Quiick Medicine carousel + reel in the brand ad style.

Usage: python3 brand/generate.py posts/YYYY-MM-DD/content.json

Outputs next to content.json:
  carousel_1.png ... carousel_N.png  (1080x1080, Instagram/Facebook feed)
  reel.mp4                            (1080x1920, ~15-20 s, animated)

content.json fields (see CONTENT_PLAN.md for the rules on what may be said):
{
  "topic": "Cold and flu season essentials",
  "type": "education" | "product" | "myth" | "local",
  "badge": {"line1": "November 14", "line2": "World Diabetes Day"},      # optional ribbon, top right
  "headline": "Beat the", "highlight": "Sniffles!",                       # highlight = big blue italic word
  "subhead": "Be ready before cold season hits.",
  "intro": "One or two short sentences under the headline.",
  "hero_icon": "virus",                  # Tabler icon name shown when there is no photo
  "photo": "media/shelves.jpg",          # optional, path relative to the repo root
  "icons": [{"icon": "bed", "label": "Rest well"}, ...],                  # exactly 3
  "panel_title": "Find it at Quiick Medicine",
  "tiles": [{"icon": "thermometer", "label": "Thermometers", "photo": "media/x.jpg"}, ...],  # 3, photo optional
  "cta_tag": "Ask our pharmacist!",
  "points": [{"icon": "droplet", "title": "Stay hydrated", "body": "...", "tip": "optional short tip"}],  # 2-4
  "cta_title_1": "Not sure what", "cta_title_2": "you need?",
  "cta_body": "Our pharmacists are happy to help you choose.",
  "reel_hook": "3 things to have before cold season",                   # first frame of the reel
  "caption_instagram": "...", "caption_facebook": "..."
}
Icon names: any Tabler icon (https://tabler.io/icons), e.g. pill, first-aid-kit, thermometer, bandage,
droplet, leaf, sun, snowflake, virus, heart, heartbeat, run, walk, bed, wash, spray, medicine-syrup,
shield-check, truck-delivery, arrows-exchange, building-store, users, calendar, clock, stethoscope.
"""
import html, json, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
V = "file://" + os.path.join(HERE, "vendor") + "/"
LOGO = "file://" + os.path.join(HERE, "logo.png")
PHONE, EMAIL, WEB = "416-789-0100", "rx@quiickmedicine.ca", "quiickmedicine.ca"
ADDRESS = "3250 Dufferin St #6, North York, ON M6A 2T3"
HOURS = "Mon–Fri 8:30–6:30 · Sat 9–4"
TAGLINE = "Quiick Medicine – Your Health, Our Priority."
DISCLAIMER = "For general awareness only. Follow your healthcare professional's advice."

e = html.escape

def img(path):
    if not path:
        return None
    p = path if os.path.isabs(path) else os.path.join(REPO, path)
    return "file://" + p if os.path.exists(p) else None

CSS = f"""
@font-face{{font-family:M;font-weight:500;src:url({V}montserrat-latin-500-normal.woff2)}}
@font-face{{font-family:M;font-weight:700;src:url({V}montserrat-latin-700-normal.woff2)}}
@font-face{{font-family:M;font-weight:800;src:url({V}montserrat-latin-800-normal.woff2)}}
@font-face{{font-family:M;font-weight:900;src:url({V}montserrat-latin-900-normal.woff2)}}
@font-face{{font-family:M;font-weight:800;font-style:italic;src:url({V}montserrat-latin-800-italic.woff2)}}
@font-face{{font-family:M;font-weight:900;font-style:italic;src:url({V}montserrat-latin-900-italic.woff2)}}
@font-face{{font-family:K;src:url({V}kaushan-script-latin-400-normal.woff2)}}
@font-face{{font-family:tabler-icons;src:url({V}tabler-icons.woff2)}}
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--navy:#0a3a75;--blue:#0b5fb0;--sky:#e3f0fc;--yellow:#ffd83d;--red:#e21f26;--green:#2e9b3e}}
body{{width:var(--w);height:var(--h);font-family:M,sans-serif;color:var(--navy);overflow:hidden;position:relative;
  background:linear-gradient(160deg,#ffffff 0%,#f2f8ff 45%,#d9eafb 100%)}}
.ti{{font-family:tabler-icons;font-style:normal;line-height:1}}
.blob{{position:absolute;border-radius:50%;background:radial-gradient(circle,#cfe4fa 0%,rgba(207,228,250,0) 70%)}}
.logo{{position:absolute;left:52px;top:44px;width:var(--logo)}}
.badge{{position:absolute;right:40px;top:44px;background:var(--navy);color:#fff;padding:22px 34px 24px;
  transform:rotate(-3deg);border-radius:14px 40px 14px 40px;text-align:center;box-shadow:0 10px 24px rgba(10,58,117,.25)}}
.badge b{{display:block;color:var(--yellow);font-weight:900;font-size:30px}}
.badge span{{display:block;font-weight:800;font-size:34px;line-height:1.1;max-width:330px}}
.hl{{font-weight:900;line-height:1.02;letter-spacing:-1px}}
.hl em{{font-style:italic;color:var(--blue);position:relative;display:inline-block}}
.hl em:after{{content:"";position:absolute;left:4%;right:2%;bottom:-6px;height:12px;border-radius:12px;background:var(--yellow);transform:rotate(-1.5deg);z-index:-1}}
.sub{{font-weight:800;font-style:italic}}
.intro{{font-weight:500;line-height:1.35;color:#173a63}}
.photo{{position:absolute;object-fit:cover}}
.hero{{position:absolute;border-radius:50%;background:radial-gradient(circle at 35% 30%,#ffffff 0%,#d6e8fb 55%,#b7d5f5 100%);
  display:flex;align-items:center;justify-content:center;box-shadow:inset 0 0 0 10px rgba(255,255,255,.6)}}
.hero .ti{{color:var(--blue)}}
.float{{position:absolute;width:86px;height:86px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;
  box-shadow:0 8px 20px rgba(10,58,117,.15);color:var(--navy);font-size:46px}}
.icons{{position:absolute;display:flex}}
.icons div{{flex:1;text-align:center;padding:0 10px;border-right:3px solid rgba(10,58,117,.25)}}
.icons div:last-child{{border-right:none}}
.icons i{{display:inline-flex;width:82px;height:82px;border-radius:50%;background:var(--navy);color:#fff;font-size:46px;align-items:center;justify-content:center;
  box-shadow:0 0 0 5px #fff,0 0 0 8px var(--navy)}}
.icons p{{font-weight:700;font-size:21px;margin-top:12px;line-height:1.15}}
.panel{{position:absolute;background:rgba(255,255,255,.85);border:3px solid #c9def5;border-radius:26px;display:flex;padding:46px 14px 14px}}
.panel h4{{position:absolute;left:50%;top:-26px;transform:translateX(-50%);background:var(--navy);color:#fff;font-weight:800;font-size:26px;
  padding:10px 30px;border-radius:30px;white-space:nowrap}}
.tile{{flex:1;text-align:center;border-right:2px solid #c9def5;padding:0 8px}}
.tile:last-child{{border-right:none}}
.tile .pic{{height:64px;display:flex;align-items:center;justify-content:center}}
.tile .pic img{{max-height:64px;max-width:150px;object-fit:contain;border-radius:10px}}
.tile .pic i{{font-size:54px;color:var(--blue)}}
.tile p{{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-weight:700;font-size:19px;line-height:1.15;margin-top:6px;background:var(--sky);border-radius:12px;padding:6px 8px}}
.tag{{position:absolute;background:var(--yellow);transform:rotate(-6deg);padding:18px 30px;border-radius:8px 30px 8px 30px;
  font-family:K;color:var(--navy);text-align:center;line-height:1.05;box-shadow:0 10px 22px rgba(0,0,0,.15)}}
.band{{position:absolute;left:0;right:0;background:var(--navy);color:#fff;display:flex;align-items:center;justify-content:center;gap:26px;font-weight:700}}
.band span{{display:flex;align-items:center;gap:10px}}
.band .sep{{width:3px;height:34px;background:rgba(255,255,255,.6)}}
.foot{{position:absolute;left:0;right:0;display:flex;align-items:center;justify-content:center;gap:24px;background:#fff}}
.foot .t{{font-weight:800;font-style:italic;color:var(--navy)}}
.foot .d{{font-size:15px;font-style:italic;color:#4a5b70;max-width:300px;line-height:1.25;border-left:2px solid var(--navy);padding-left:16px}}
.num{{display:inline-flex;align-items:center;justify-content:center;border-radius:50%;background:var(--navy);color:#fff;font-weight:900}}
.tip{{background:#fff;border-left:10px solid var(--yellow);border-radius:0 18px 18px 0;padding:22px 28px;font-weight:700;color:var(--navy);
  box-shadow:0 8px 20px rgba(10,58,117,.1)}}
.page{{position:absolute;right:52px;top:58px;font-weight:800;font-size:24px;color:var(--blue);background:#fff;border:3px solid #c9def5;border-radius:30px;padding:8px 20px}}
"""

def band(top, h=78, fs=27):
    return (f'<div class="band" style="top:{top}px;height:{h}px;font-size:{fs}px">'
            f'<span><i class="ti">&#xeb09;</i>{PHONE}</span><div class="sep"></div>'
            f'<span><i class="ti">&#xeae5;</i>{EMAIL}</span><div class="sep"></div>'
            f'<span><i class="ti">&#xeb54;</i>{WEB}</span></div>')

def foot(top, h=72):
    return (f'<div class="foot" style="top:{top}px;height:{h}px"><span class="t" style="font-size:28px">{TAGLINE}</span>'
            f'<span class="d">{DISCLAIMER}</span></div>')

def icon(name):
    return f'<i class="ti ti-{e(name)}"></i>'

def page(body, w, h, logo_w=420):
    return (f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="{V}tabler-icons.min.css">'
            f'<style>{CSS}</style></head><body style="--w:{w}px;--h:{h}px;--logo:{logo_w}px">{body}</body></html>')

def hero_visual(c, x, y, size):
    ph = img(c.get("photo"))
    if ph:
        return (f'<img class="photo" src="{ph}" style="left:{x}px;top:{y}px;width:{size}px;height:{size}px;border-radius:50% 50% 40% 50%;'
                f'border:10px solid #fff;box-shadow:0 18px 40px rgba(10,58,117,.25)">')
    s = size
    out = [f'<div class="hero" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px">'
           f'<i class="ti ti-{e(c.get("hero_icon","pill"))}" style="font-size:{int(s*0.5)}px"></i></div>']
    extra = [i["icon"] for i in c.get("tiles", [])][:3]
    spots = [(x - 30, y + s * 0.62), (x + s * 0.78, y - 10), (x + s * 0.84, y + s * 0.72)]
    for name, (fx, fy) in zip(extra, spots):
        out.append(f'<div class="float" style="left:{int(fx)}px;top:{int(fy)}px">{icon(name)}</div>')
    return "".join(out)

def cover(c, total):
    b = c.get("badge")
    badge = (f'<div class="badge"><b>{e(b["line1"])}</b><span>{e(b["line2"])}</span></div>' if b else "")
    icons = "".join(f'<div>{icon(i["icon"])}<p>{e(i["label"])}</p></div>' for i in c["icons"][:3])
    tiles = "".join(
        f'<div class="tile"><div class="pic">'
        + (f'<img src="{img(t.get("photo"))}">' if img(t.get("photo")) else icon(t["icon"]))
        + f'</div><p>{e(t["label"])}</p></div>' for t in c["tiles"][:3])
    hl = f'{e(c["headline"])}<br><em>{e(c["highlight"])}</em>'
    body = f"""
<div class="blob" style="width:700px;height:700px;right:-200px;top:120px"></div>
<img class="logo" src="{LOGO}">
{badge}
<div style="position:absolute;left:52px;top:236px;width:590px;display:flex;flex-direction:column;gap:14px">
<div class="hl" style="font-size:74px">{hl}</div>
<div class="sub" style="font-size:34px;margin-top:10px">{e(c["subhead"])}</div>
<div class="intro" style="font-size:25px">{e(c["intro"])}</div></div>
{hero_visual(c, 640, 260 if b else 200, 390)}
<div class="icons" style="left:40px;top:640px;width:600px">{icons}</div>
<div class="panel" style="left:40px;top:818px;width:690px;height:158px"><h4>{e(c["panel_title"])}</h4>{tiles}</div>
<div class="tag" style="right:34px;top:790px;width:300px;font-size:44px">{e(c["cta_tag"])}</div>
{band(984, 60, 25)}<div class="foot" style="top:1044px;height:36px"><span class="t" style="font-size:18px">{TAGLINE}</span><span class="d" style="font-size:12px;max-width:none;white-space:nowrap;padding-left:12px">{DISCLAIMER}</span></div>
"""
    return page(body, 1080, 1080, 400)

def point(c, p, n, total):
    tip = f'<div class="tip" style="position:absolute;left:52px;top:760px;width:976px;font-size:30px"><i class="ti">&#xea5e;</i> {e(p["tip"])}</div>' if p.get("tip") else ""
    body = f"""
<div class="blob" style="width:760px;height:760px;right:-260px;top:80px"></div>
<img class="logo" src="{LOGO}" style="width:300px">
<div class="page">{n} / {total}</div>
<div style="position:absolute;right:70px;top:230px;width:330px;height:330px" class="hero"><i class="ti ti-{e(p.get("icon","check"))}" style="font-size:170px"></i></div>
<div class="num" style="position:absolute;left:52px;top:250px;width:110px;height:110px;font-size:60px">{n - 1}</div>
<div class="hl" style="position:absolute;left:52px;top:390px;width:600px;font-size:68px">{e(p["title"])}</div>
<div style="position:absolute;left:52px;top:540px;width:180px;height:12px;border-radius:12px;background:var(--yellow)"></div>
<div class="intro" style="position:absolute;left:52px;top:580px;width:640px;font-size:34px">{e(p["body"])}</div>
{tip}
{band(930, 80, 27)}<div class="foot" style="top:1010px;height:70px"><span class="t" style="font-size:24px">{TAGLINE}</span><span class="d" style="font-size:13px;max-width:none;white-space:nowrap;padding-left:12px">{DISCLAIMER}</span></div>
"""
    return page(body, 1080, 1080)

def closing(c, total):
    rows = [("&#xeb09;", f"Call {PHONE}"), ("&#xeae5;", EMAIL), ("&#xeae8;", ADDRESS), ("&#xea70;", HOURS), ("&#xeb54;", WEB)]
    rws = "".join(f'<div style="display:flex;align-items:center;gap:20px;margin-bottom:22px"><span style="display:inline-flex;width:62px;height:62px;border-radius:50%;'
                  f'background:var(--yellow);color:var(--navy);align-items:center;justify-content:center;font-size:34px" class="ti">{i}</span>{e(t)}</div>' for i, t in rows)
    body = f"""
<div style="position:absolute;inset:0;background:linear-gradient(150deg,#0b4b93 0%,#0a3a75 60%,#072a56 100%)"></div>
<div style="position:absolute;left:40px;top:36px;background:#fff;border-radius:22px;padding:14px 22px"><img src="{LOGO}" style="width:320px;display:block"></div>
<div class="page">{total} / {total}</div>
<div class="hl" style="position:absolute;left:52px;top:250px;width:980px;font-size:74px;color:#fff">{e(c["cta_title_1"])}<br><span style="color:var(--yellow)">{e(c["cta_title_2"])}</span></div>
<div style="position:absolute;left:52px;top:440px;width:960px;font-size:32px;font-weight:700;color:#dbeafe">{e(c["cta_body"])}</div>
<div style="position:absolute;left:52px;top:540px;font-size:30px;font-weight:700;color:#fff">{rws}</div>
<div class="tag" style="right:44px;top:250px;width:260px;font-size:40px;transform:rotate(6deg)">{e(c["cta_tag"])}</div>
<div style="position:absolute;left:0;right:0;bottom:0;height:56px;background:#fff;display:flex;align-items:center;justify-content:center;gap:20px">
<span class="foot" style="position:static;background:none"><span class="t" style="font-size:22px">{TAGLINE}</span><span class="d" style="font-size:13px;max-width:380px">{DISCLAIMER}</span></span></div>
"""
    return page(body, 1080, 1080)

def reel_frame(c, kind, p=None, n=0):
    ph = img(c.get("photo"))
    bg = (f'<img src="{ph}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">'
          f'<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(7,42,86,.35),rgba(7,42,86,.85))"></div>') if ph else \
         '<div style="position:absolute;inset:0;background:linear-gradient(170deg,#0b5fb0 0%,#0a3a75 55%,#072a56 100%)"></div>'
    logo = f'<div style="position:absolute;left:60px;top:90px;background:#fff;border-radius:24px;padding:16px 24px"><img src="{LOGO}" style="width:360px;display:block"></div>'
    end = (f'<div style="position:absolute;left:60px;right:60px;top:1470px;height:170px;border-radius:28px;background:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;'
           f'font-weight:800;font-size:34px;color:var(--navy)"><div>{PHONE} · {WEB}</div><div style="font-size:20px;font-weight:500;font-style:italic;margin-top:8px">{DISCLAIMER}</div></div>')
    if kind == "hook":
        mid = (f'<div class="hl" style="position:absolute;left:60px;right:60px;top:560px;font-size:104px;color:#fff">{e(c["reel_hook"])}</div>'
               f'<div class="hero" style="left:340px;top:930px;width:400px;height:400px"><i class="ti ti-{e(c.get("hero_icon","pill"))}" style="font-size:200px"></i></div>'
               f'<div style="position:absolute;left:60px;top:1360px;font-family:K;font-size:60px;color:var(--yellow)">Watch till the end</div>')
    elif kind == "point":
        mid = (f'<div class="num" style="position:absolute;left:60px;top:470px;width:150px;height:150px;font-size:84px;background:var(--yellow);color:var(--navy)">{n}</div>'
               f'<i class="ti ti-{e(p.get("icon","check"))}" style="position:absolute;right:70px;top:440px;font-size:220px;color:rgba(255,255,255,.9)"></i>'
               f'<div class="hl" style="position:absolute;left:60px;right:60px;top:720px;font-size:96px;color:#fff">{e(p["title"])}</div>'
               f'<div style="position:absolute;left:60px;right:60px;top:1000px;font-size:46px;font-weight:700;line-height:1.3;color:#e6f0fb">{e(p["body"])}</div>')
    else:
        mid = (f'<div class="hl" style="position:absolute;left:60px;right:60px;top:520px;font-size:96px;color:#fff">{e(c["cta_title_1"])}<br>'
               f'<span style="color:var(--yellow)">{e(c["cta_title_2"])}</span></div>'
               f'<div style="position:absolute;left:60px;right:60px;top:880px;font-size:46px;font-weight:700;line-height:1.3;color:#e6f0fb">{e(c["cta_body"])}</div>'
               f'<div class="tag" style="left:70px;top:1110px;width:900px;font-size:58px;padding:24px 36px">Send this to someone who needs it!</div>'
               f'<div style="position:absolute;left:60px;top:1330px;font-size:40px;font-weight:800;color:#fff"><i class="ti">&#xeae8;</i> 3250 Dufferin St #6, North York</div>')
    return page(bg + logo + mid + end, 1080, 1920)

def shoot(pages, out_dir):
    from playwright.sync_api import sync_playwright
    tmp = tempfile.mkdtemp()
    files = []
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for name, (htmltext, w, h) in pages.items():
            hp = os.path.join(tmp, name + ".html")
            with open(hp, "w") as fh:
                fh.write(htmltext)
            pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
            pg.goto("file://" + hp)
            pg.wait_for_timeout(400)
            target = os.path.join(out_dir, name + ".png")
            pg.screenshot(path=target)
            pg.close()
            files.append(target)
        b.close()
    shutil.rmtree(tmp)
    return files

def make_reel(frames, out, secs=3.6, fade=0.5):
    fps = 30
    inputs, filters = [], []
    for i, f in enumerate(frames):
        inputs += ["-i", f]
        # slow push-in so every frame moves
        filters.append(f"[{i}:v]scale=1188:2112,zoompan=z='min(zoom+0.0005,1.05)':d={int(secs*fps)}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps={fps},setsar=1[v{i}]")
    chain, last, offset = [], "v0", 0.0
    for i in range(1, len(frames)):
        offset += secs - fade
        chain.append(f"[{last}][v{i}]xfade=transition=slideleft:duration={fade}:offset={offset:.2f}[x{i}]")
        last = f"x{i}"
    fc = ";".join(filters + chain) + f";[{last}]format=yuv420p[out]"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", fc, "-map", "[out]",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "21", "-r", str(fps), "-movflags", "+faststart", out], check=True)

def render(c, out):
    total = len(c["points"]) + 2
    pages = {"carousel_1": (cover(c, total), 1080, 1080)}
    for i, p in enumerate(c["points"], 2):
        pages[f"carousel_{i}"] = (point(c, p, i, total), 1080, 1080)
    pages[f"carousel_{total}"] = (closing(c, total), 1080, 1080)
    pages["_reel_0"] = (reel_frame(c, "hook"), 1080, 1920)
    for i, p in enumerate(c["points"], 1):
        pages[f"_reel_{i}"] = (reel_frame(c, "point", p, i), 1080, 1920)
    pages["_reel_end"] = (reel_frame(c, "end"), 1080, 1920)
    for f in os.listdir(out):
        if f.startswith(("carousel_", "_reel_")) and f.endswith(".png"):
            os.remove(os.path.join(out, f))
    shoot(pages, out)
    frames = [os.path.join(out, f"_reel_{k}.png") for k in ["0"] + [str(i) for i in range(1, len(c["points"]) + 1)] + ["end"]]
    make_reel(frames, os.path.join(out, "reel.mp4"))
    keep = sorted(f for f in os.listdir(out) if f.startswith("carousel_"))
    for f in frames:
        os.remove(f)
    return keep + ["reel.mp4"]

if __name__ == "__main__":
    path = sys.argv[1]
    with open(path) as fh:
        content = json.load(fh)
    print("\n".join(render(content, os.path.dirname(os.path.abspath(path)))))
