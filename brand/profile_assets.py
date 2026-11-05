"""Render profile assets: profile picture, Facebook cover, story highlight covers, in-store QR sign."""
import os, sys, io, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generate as g
import qrcode

OUT = os.path.join(g.HERE, "profile")
MARK = "file://" + os.path.join(g.HERE, "logo_mark.png")
os.makedirs(OUT, exist_ok=True)

def qr(url):
    img = qrcode.make(url, border=1, box_size=12)
    buf = io.BytesIO(); img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

pages = {}
pages["profile_picture"] = (g.page(f'''<div style="position:absolute;inset:0;background:#fff"></div>
<img src="{MARK}" style="position:absolute;left:190px;top:200px;width:700px">''', 1080, 1080), 1080, 1080)

svc = [("arrows-exchange", "Easy Rx transfers"), ("flask", "Compounding lab"), ("truck-delivery", "Delivery across Ontario"),
       ("vaccine", "Flu and COVID shots"), ("pills", "Free blister packs")]
icons = "".join(f'<div>{g.icon(i)}<p>{g.e(t)}</p></div>' for i, t in svc)
pages["facebook_cover"] = (g.page(f'''
<div class="blob" style="width:900px;height:900px;right:-200px;top:-300px"></div>
<div class="hl" style="position:absolute;left:0;right:0;top:70px;text-align:center;font-size:76px">Your <em>North York</em> pharmacy</div>
<div class="sub" style="position:absolute;left:0;right:0;top:200px;text-align:center;font-size:38px">Compounding · Prescriptions · Everyday health</div>
<div class="icons" style="left:270px;top:290px;width:1100px">{icons}</div>
<div class="band" style="top:540px;height:84px;font-size:30px"><span><i class="ti">&#xeae8;</i>3250 Dufferin St #6, North York</span><div class="sep"></div>
<span><i class="ti">&#xeb09;</i>{g.PHONE}</span><div class="sep"></div><span><i class="ti">&#xeb54;</i>{g.WEB}</span></div>
''', 1640, 624), 1640, 624)

for slug, ic, label in [("transfers", "arrows-exchange", "Transfers"), ("compounding", "flask", "Compounding"),
                        ("delivery", "truck-delivery", "Delivery"), ("flu-shots", "vaccine", "Flu shots"),
                        ("reviews", "star", "Reviews"), ("tips", "bulb", "Tips"), ("contact", "map-pin", "Visit us")]:
    pages[f"highlight_{slug}"] = (g.page(f'''
<div style="position:absolute;inset:0;background:linear-gradient(170deg,#0b5fb0 0%,#0a3a75 60%,#072a56 100%)"></div>
<div style="position:absolute;left:240px;top:660px;width:600px;height:600px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;
 box-shadow:0 0 0 18px var(--yellow)"><i class="ti ti-{ic}" style="font-size:330px;color:var(--navy)"></i></div>
<div class="hl" style="position:absolute;left:0;right:0;top:1340px;text-align:center;font-size:84px;color:#fff">{label}</div>''', 1080, 1920), 1080, 1920)

ig = qr("https://www.instagram.com/quiickmedicine/")
rv = qr("https://search.google.com/local/writereview?placeid=ChIJ0-wV_wMzK4gR2LeRyuFwL9o")
def qrbox(src, title, sub, icon):
    return (f'<div style="flex:1;background:#fff;border-radius:36px;border:4px solid #c9def5;padding:40px;text-align:center">'
            f'<div style="font-size:46px;font-weight:900;color:var(--navy)"><i class="ti">{icon}</i> {title}</div>'
            f'<img src="{src}" style="width:440px;height:440px;margin:28px auto;display:block;image-rendering:pixelated">'
            f'<div style="font-size:30px;font-weight:700;color:#173a63">{sub}</div></div>')
pages["counter_sign"] = (g.page(f'''
<img src="{g.LOGO}" style="position:absolute;left:300px;top:70px;width:675px">
<div class="hl" style="position:absolute;left:0;right:0;top:420px;text-align:center;font-size:96px">Daily pharmacy <em>tips!</em></div>
<div class="sub" style="position:absolute;left:0;right:0;top:570px;text-align:center;font-size:44px">Scan to follow us, or tell us how we did</div>
<div style="position:absolute;left:80px;right:80px;top:680px;display:flex;gap:50px">
{qrbox(ig, "Follow us", "@quiickmedicine on Instagram", "&#xeb09;".replace("&#xeb09;", "&#xec20;"))}
{qrbox(rv, "Review us", "Leave a quick Google review", "&#xeb2e;")}</div>
<div class="band" style="top:1500px;height:90px;font-size:32px"><span>{g.PHONE}</span><div class="sep"></div><span>{g.WEB}</span></div>
<div class="foot" style="top:1590px;height:60px"><span class="t" style="font-size:28px">{g.TAGLINE}</span></div>
''', 1275, 1650), 1275, 1650)

g.shoot(pages, OUT)
from PIL import Image
Image.open(os.path.join(OUT, "counter_sign.png")).convert("RGB").save(os.path.join(OUT, "counter_sign.pdf"), resolution=150)
print("\n".join(sorted(os.listdir(OUT))))
