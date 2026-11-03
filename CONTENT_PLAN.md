# Quiick Medicine daily social content plan

Posts publish AUTOMATICALLY to Facebook and Instagram (Metricool brand 7849582). No human reviews them,
so every post must be safe to go live as-is.

## Hard rules (never break)
- Allowed: general pharmacy and wellness education, and OVER-THE-COUNTER (non-prescription) product
  CATEGORY spotlights: pain relief, cold and flu, allergy, digestive health, skin care, first aid,
  vitamins and natural health products, diabetes supplies (meters, strips, lancets), heat and cold
  therapy, thermometers, hand sanitizer, and similar front-of-store items.
- Talk about categories, not brands. No brand names, no specific product claims, no comparisons.
- Never: prescription drug names, GLP-1 / semaglutide / Ozempic / weight-loss drugs, hormone therapy,
  compounded-medication promotion, prices, discounts, "buy now" for medications, before/after or
  body-image content.
- No health claims ("cures", "treats", "prevents", "guaranteed"). Use "relief", "support", "help you choose".
- No dosing advice beyond "read and follow the label" and "ask your pharmacist".
- Every caption ends with: "For general awareness only. Follow your healthcare professional's advice."
- Canadian spelling. Friendly, plain language.
- Do not mention free delivery or prices unless the owner confirms them here.

## Fixed details
- Address: 3250 Dufferin St #6, North York, ON M6A 2T3
- Phone 416-789-0100 | rx@quiickmedicine.ca | quiickmedicine.ca | @quiickmedicine
- Hours: Mon–Fri 8:30 AM–6:30 PM, Sat 9 AM–4 PM, Sun closed
- Delivery: prescription delivery across Ontario
- Tagline: "Quiick Medicine – Your Health, Our Priority"

## Weekly mix (by weekday, America/Toronto)
- Mon: education (checklist or how-to, built to be SAVED)
- Tue: OTC product category spotlight
- Wed: myth vs fact (built to be SHARED)
- Thu: education tied to a health awareness day/month or the season
- Fri: OTC product category spotlight
- Sat: local / service post (prescription transfers, Ontario delivery, North York location, meet the pharmacy)
- Sun: quick tip or seasonal wellness

## What the Instagram algorithm rewards (use it every day)
- DM shares, watch time/completion, and saves are the strongest signals. End the reel with
  "Send this to someone who needs it" (built into the template) and make carousels worth saving.
- The reel hook (first frame) must be a specific promise or question, under 8 words.
- Keyword-rich captions beat hashtags. First line = hook; second line includes 1–2 search phrases such as
  "North York pharmacy", "pharmacy near Yorkdale", "Toronto pharmacy", "prescription transfer Toronto",
  "cold and flu relief Toronto". Then 3–5 hashtags max.
- Original content only; never repost other accounts' visuals or audio.

## Captions and links
- Instagram caption: hook, value, keywords, a save/share prompt, "🔗 Link in bio: quiickmedicine.ca",
  address/phone lines, disclaimer, 3–5 hashtags incl. #QuiickMedicine #NorthYork #PharmacyToronto.
- Facebook caption: same message but with a clickable tracked link instead of "link in bio":
  https://quiickmedicine.ca/?utm_source=facebook&utm_medium=social&utm_campaign=<YYYY-MM-DD>-<topic-slug>
- Recommended Instagram bio link (owner sets once):
  https://quiickmedicine.ca/?utm_source=instagram&utm_medium=social&utm_campaign=bio

## Daily schedule (America/Toronto)
- 12:00 PM carousel: separate Facebook POST and Instagram POST (different captions, see above)
- 7:00 PM reel: separate Facebook REEL and Instagram REEL

## Content length limits (so the template fits)
- headline ≤ 16 characters, highlight ≤ 14, subhead ≤ 34, intro ≤ 110
- icon labels ≤ 18, tile labels ≤ 14, panel_title ≤ 30, cta_tag ≤ 22
- point title ≤ 26, point body ≤ 110, tip ≤ 45, reel_hook ≤ 48, badge line2 ≤ 22

## Topic ideas (check posts/ to avoid repeats within 30 days)
- Questions to ask your pharmacist; reading a medication label; keeping a medication list
- Myth vs fact: antibiotics and colds, expired meds, "natural means safe", etc.
- Storing medications; safe disposal of old medications (bring them to the pharmacy)
- Prescription transfers; Ontario-wide delivery; our North York location; what a compounding pharmacy is
- OTC spotlights: cold and flu kit, allergy season, first aid kit, winter skin care, digestive health,
  pain relief options, vitamin D in Canadian winters (category only), heat and cold therapy, diabetes supplies
- Health awareness days and months (Canadian calendar), seasonal wellness, travel health checklist

## Media
- Product photos from quiickmedicine.ca live in media/products/ (refreshed weekly by a GitHub Action).
  ALWAYS pick them with: python3 scripts/pick_photos.py <theme> <count>
  Themes: cold-flu, pain, allergy, digestion, sleep, vitamin-d, immune, vitamins, skin, sun, eyes,
  diabetes, first-aid, travel, heart, joints. The picker only returns safe OTC products.
- Use product photos for "photo" (cover hero), the three tile "photo"s, and optionally a point "photo".
  Tile and point labels must describe the CATEGORY that matches the photo (e.g. "Sinus relief"),
  never the brand, and never a claim about that specific product.
- Education/myth/local posts may use icons only, or product photos only when they genuinely fit.
- Real pharmacy photos/clips the owner provides go in media/ (not media/products/); use them as
  "bg_photo" for the reel background.
- brand/generate.py renders everything; brand/example_content.json is a complete example.
