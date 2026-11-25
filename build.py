#!/usr/bin/env python3
"""Builds the yoGee studios website. Edit the GAMES list or the text below, then run:  python3 build.py"""
import html, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECTS = os.path.dirname(ROOT)
STUDIO = "yoGee studios"
EMAIL = "yogeestudios@gmail.com"
YEAR = "2026"

GAMES = [
    dict(slug="fliplits", name="Fliplits", tag="Tap once. Light everything.", accent="#b45fd6",
         status="Out now", store="https://apps.apple.com/app/id6825532299",
         blurb="A cozy chain-reaction puzzle. Wake one sleepy tile and its light flips the next, and the next, until the whole board glows.",
         facts=["400 hand-tuned puzzles", "3 bonus modes", "A new Daily Puzzle every day"]),
    dict(slug="snap-bandits", name="Snap Bandits", tag="Snip them loose!", accent="#ff4d6d",
         status="Coming soon", store=None,
         blurb="A rubber-band physics puzzle. Snip the right band and a masked bandit flings into its getaway tube. Snip the wrong one and you're busted.",
         facts=["300 puzzles", "30 worlds", "Bandits with big personalities"]),
    dict(slug="hex-appeal", name="Hex Appeal", tag="Turn the tiles. Connect the light.", accent="#7a5cff",
         status="Coming soon", store=None, hidden=True,  # hidden while publisher talks are open
         blurb="A calm light-path puzzle. Rotate glowing glass tiles to send light from every core to every gem, then watch the board bloom.",
         facts=["200 relaxing puzzles", "7 hand-lit worlds", "No timers, no lives"]),
    dict(slug="twisted-system", name="Blade Runners: Twisted System", tag="Jump. Duck. Survive the spiral.", accent="#ff8a1f",
         status="Out now", store="https://apps.apple.com/app/id6808706055",
         blurb="A fast one-thumb obstacle race on a track that winds around a giant tower. Dodge spinning blades and outrun three rivals.",
         facts=["Endless and race modes", "20 skins to unlock", "Game Center leaderboards"]),
    dict(slug="iqube", name="iQube: Intelligent Blocks", tag="Outsmart the rolling grid.", accent="#18c9bb",
         status="Out now", store="https://apps.apple.com/app/id6815485986",
         blurb="A neon puzzle-action game. Mark, capture and blast a rolling wall of cubes before the stage crumbles under you.",
         facts=["9 worlds to conquer", "Endless mode", "Game Center leaderboards"]),
    dict(slug="itty-bitty-angler", name="Itty Bitty Angler", tag="Big fish. Tiny world.", accent="#f39a1e",
         status="In development", store=None, docs=False,
         blurb="A top-down fishing adventure. Steer your boat across hand-crafted waters, spot shadows under the surface, land your lure in front of them and fight each fish in a tug-of-war.",
         facts=["A journal of species to fill", "Gear to upgrade", "Legends hiding in every region"]),
]
GAMES = [g for g in GAMES if not g.get("hidden")]

CSS = """
@font-face { font-family: "Lilita One"; src: url("FONTDIR/LilitaOne-Regular.ttf") format("truetype"); font-display: swap; }
:root { --ink: #2a1840; --soft: #6b5a80; --bg: #fff8f1; --card: #ffffff; --line: #eadfd6; --brand: #ff4d6d; --brand2: #7a5cff; --sun: #ffc93c; }
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body { margin: 0; background: var(--bg); color: var(--ink); font: 17px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
img { max-width: 100%; display: block; }
a { color: var(--brand2); }
h1, h2, h3, .logo, .btn, .badge { font-family: "Lilita One", "Arial Rounded MT Bold", system-ui, sans-serif; font-weight: 400; }
.wrap { max-width: 1120px; margin: 0 auto; padding: 0 20px; }
header.nav { position: sticky; top: 0; z-index: 10; background: rgba(255, 248, 241, 0.92); backdrop-filter: blur(8px); border-bottom: 2px solid var(--line); }
header.nav .wrap { display: flex; align-items: center; justify-content: space-between; height: 64px; }
.logo { font-size: 28px; text-decoration: none; color: var(--ink); letter-spacing: 0.3px; }
.logo b { font-weight: 400; color: var(--brand); }
nav a { margin-left: 22px; text-decoration: none; color: var(--ink); font-weight: 600; font-size: 16px; }
nav a:hover { color: var(--brand); }
.hero { padding: 72px 0 40px; text-align: center; }
.hero h1 { font-size: clamp(40px, 7vw, 76px); line-height: 1.02; margin: 0 0 18px; }
.hero h1 span { color: var(--brand); }
.hero p { font-size: 20px; color: var(--soft); max-width: 640px; margin: 0 auto 28px; }
.btn { display: inline-block; padding: 13px 26px; border-radius: 999px; background: var(--ink); color: #fff; text-decoration: none; font-size: 18px; border: 0; box-shadow: 0 5px 0 rgba(42, 24, 64, 0.22); transition: transform 0.12s; }
.btn:hover { transform: translateY(-2px); }
.btn.alt { background: #fff; color: var(--ink); border: 2px solid var(--ink); box-shadow: 0 5px 0 rgba(42, 24, 64, 0.12); }
.icons { display: flex; justify-content: center; gap: 14px; margin: 38px 0 0; flex-wrap: wrap; }
.icons img { width: 84px; height: 84px; border-radius: 20px; box-shadow: 0 8px 18px rgba(42, 24, 64, 0.18); }
section { padding: 56px 0; }
section > .wrap > h2 { font-size: 40px; margin: 0 0 8px; }
.lead { color: var(--soft); margin: 0 0 30px; }
.game { background: var(--card); border: 2px solid var(--line); border-radius: 28px; overflow: hidden; margin-bottom: 34px; box-shadow: 0 10px 30px rgba(42, 24, 64, 0.07); }
.game .banner { aspect-ratio: 21 / 9; width: 100%; object-fit: cover; }
.game .body { display: grid; grid-template-columns: 1.15fr 1fr; gap: 28px; padding: 26px 28px 30px; align-items: start; }
.title { display: flex; gap: 16px; align-items: center; margin-bottom: 12px; }
.title img { width: 76px; height: 76px; border-radius: 18px; flex: none; box-shadow: 0 6px 14px rgba(42, 24, 64, 0.18); }
.title h3 { font-size: 30px; line-height: 1.1; margin: 0 0 6px; }
.badge { display: inline-block; font-size: 13px; letter-spacing: 0.6px; text-transform: uppercase; padding: 4px 12px; border-radius: 999px; color: #fff; background: var(--accent); }
.badge.soon { background: #fff; color: var(--accent); border: 2px solid var(--accent); }
.tag { font-size: 20px; color: var(--accent); margin: 0 0 8px; font-family: "Lilita One", system-ui, sans-serif; }
.game p { margin: 0 0 12px; color: var(--soft); }
.facts { list-style: none; padding: 0; margin: 0 0 18px; }
.facts li { padding-left: 26px; position: relative; margin: 4px 0; font-weight: 600; }
.facts li::before { content: ""; position: absolute; left: 0; top: 8px; width: 12px; height: 12px; border-radius: 50%; background: var(--accent); }
.links { display: flex; flex-wrap: wrap; gap: 10px 18px; align-items: center; }
.links small a { color: var(--soft); }
.shots { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
.shots img { border-radius: 16px; border: 2px solid var(--line); }
.about { background: #fff; border-top: 2px solid var(--line); border-bottom: 2px solid var(--line); }
.cols { display: grid; grid-template-columns: repeat(3, 1fr); gap: 22px; margin-top: 26px; }
.cols div { background: var(--bg); border-radius: 20px; padding: 22px; border: 2px solid var(--line); }
.cols h3 { margin: 0 0 6px; font-size: 22px; }
.cols p { margin: 0; color: var(--soft); }
.contact { text-align: center; }
.contact .mail { font-size: clamp(22px, 4vw, 34px); font-family: "Lilita One", system-ui, sans-serif; color: var(--brand); text-decoration: none; word-break: break-all; }
footer { padding: 30px 0 46px; color: var(--soft); font-size: 15px; text-align: center; }
footer a { color: var(--soft); margin: 0 8px; }
.doc { max-width: 760px; margin: 0 auto; padding: 46px 20px 70px; }
.doc h1 { font-size: 40px; margin: 0 0 10px; }
.doc h2 { font-size: 24px; margin: 34px 0 8px; }
.doc p, .doc li { color: #4a3a60; }
@media (max-width: 820px) {
  .game .body { grid-template-columns: 1fr; padding: 20px; }
  .cols { grid-template-columns: 1fr; }
  nav a { margin-left: 14px; font-size: 15px; }
  .logo { font-size: 23px; }
  section > .wrap > h2 { font-size: 32px; }
  .hero { padding: 48px 0 26px; }
}
"""

def page(title, body, depth=0, desc=""):
    up = "../" * depth
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc or 'yoGee studios makes bright, tactile puzzle and arcade games for iPhone.')}">
<link rel="stylesheet" href="{up}style.css">
</head>
<body>
<header class="nav"><div class="wrap">
  <a class="logo" href="{up}index.html">yo<b>Gee</b> studios</a>
  <nav><a href="{up}index.html#games">Games</a><a href="{up}index.html#about">About</a><a href="{up}support.html">Support</a></nav>
</div></header>
{body}
<footer><div class="wrap">
  &copy; {YEAR} {STUDIO}. All rights reserved.<br>
  <a href="{up}support.html">Support</a><a href="{up}privacy/index.html">Privacy</a><a href="mailto:{EMAIL}">Contact</a>
</div></footer>
</body>
</html>
"""

def game_card(g):
    s = g["slug"]
    soon = g["status"] != "Out now"
    badge = f'<span class="badge{" soon" if soon else ""}">{g["status"]}</span>'
    btn = (f'<a class="btn" href="{g["store"]}">Get it on the App Store</a>' if g["store"]
           else None)
    facts = "".join(f"<li>{html.escape(f)}</li>" for f in g["facts"])
    n = g.get("shots", 3)
    shots = "".join(f'<img src="img/{s}-shot{i}.jpg" alt="{html.escape(g["name"])} screenshot {i}" loading="lazy">' for i in range(1, n + 1))
    docs = (f'<small><a href="support.html#{s}">Support</a> &middot; <a href="privacy/{s}.html">Privacy</a></small>' if g.get("docs", True) else "")
    label = "Coming to the App Store" if g["status"] == "Coming soon" else "In the works"
    return f"""
<article class="game" id="{s}" style="--accent: {g['accent']}">
  <img class="banner" src="img/{s}-header.jpg" alt="{html.escape(g['name'])} key art" loading="lazy">
  <div class="body">
    <div>
      <div class="title"><img src="img/{s}-icon.jpg" alt="{html.escape(g['name'])} app icon"><div><h3>{html.escape(g['name'])}</h3>{badge}</div></div>
      <p class="tag">{html.escape(g['tag'])}</p>
      <p>{html.escape(g['blurb'])}</p>
      <ul class="facts">{facts}</ul>
      <div class="links">{btn or f'<span class="btn alt" aria-disabled="true">{label}</span>'}{docs}</div>
    </div>
    <div class="shots" style="grid-template-columns: repeat({n}, 1fr)">{shots}</div>
  </div>
</article>"""

def index():
    icons = "".join(f'<a href="#{g["slug"]}"><img src="img/{g["slug"]}-icon.jpg" alt="{html.escape(g["name"])}"></a>' for g in GAMES)
    cards = "".join(game_card(g) for g in GAMES)
    body = f"""
<main>
<section class="hero"><div class="wrap">
  <h1>Small games.<br><span>Big personality.</span></h1>
  <p>{STUDIO} is an independent studio making bright, tactile puzzle and arcade games for iPhone.</p>
  <a class="btn" href="#games">See the games</a>
  <div class="icons">{icons}</div>
</div></section>

<section id="games"><div class="wrap">
  <h2>Our games</h2>
  <p class="lead">Three out now, two on the way.</p>
  {cards}
</div></section>

<section class="about" id="about"><div class="wrap">
  <h2>About {STUDIO}</h2>
  <p class="lead">We make games that are easy to pick up and satisfying to master.</p>
  <div class="cols">
    <div><h3>Feel comes first</h3><p>Every tap, snip and chain reaction is tuned until it feels right, with sound and haptics to match.</p></div>
    <div><h3>Fair by design</h3><p>No pay walls and no pressure. Our puzzles are checked so every level can be solved.</p></div>
    <div><h3>Made for iPhone</h3><p>Smooth animation, one-hand play and offline support, so a game fits wherever you are.</p></div>
  </div>
</div></section>

<section class="contact" id="contact"><div class="wrap">
  <h2>Say hello</h2>
  <p class="lead">Players, press and publishers are all welcome.</p>
  <a class="mail" href="mailto:{EMAIL}">{EMAIL}</a>
</div></section>
</main>"""
    return page(f"{STUDIO} | Puzzle and arcade games for iPhone", body)

def md_to_html(md):
    out, in_list = [], False
    def inline(t):
        t = html.escape(t)
        t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
        t = re.sub(r"(?<![\w/])_(.+?)_(?![\w/])", r"<em>\1</em>", t)
        t = re.sub(r"(https?://[^\s<)]+)", r'<a href="\1">\1</a>', t)
        return t
    para = []
    def flush():
        nonlocal para
        if para: out.append("<p>" + inline(" ".join(para)) + "</p>"); para = []
    for line in md.splitlines():
        s = line.strip()
        if not s:
            flush()
            if in_list: out.append("</ul>"); in_list = False
            continue
        m = re.match(r"^(#{1,3})\s+(.*)$", s)
        if m:
            flush()
            if in_list: out.append("</ul>"); in_list = False
            lvl = min(len(m.group(1)), 2)
            out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>"); continue
        if s.startswith(("- ", "* ")):
            flush()
            if not in_list: out.append("<ul>"); in_list = True
            out.append("<li>" + inline(s[2:]) + "</li>"); continue
        para.append(s)
    flush()
    if in_list: out.append("</ul>")
    return "\n".join(out)

def main_of(path):
    """The inner content of an existing standalone HTML page (its <main>, or its <body>)."""
    t = open(path, encoding="utf-8").read()
    m = re.search(r"<main[^>]*>(.*?)</main>", t, re.S) or re.search(r"<body[^>]*>(.*?)</body>", t, re.S)
    inner = m.group(1) if m else t
    return re.sub(r"<(script|style)[^>]*>.*?</\1>", "", inner, flags=re.S)

SNAP_PRIVACY = f"""# Snap Bandits Privacy Policy

_Last updated: November 12, 2026_

Snap Bandits ("the app") is a puzzle game made by {STUDIO}. This policy explains what information the app handles and why.

## Information the app stores

Your game progress (levels, stars, coins and settings) is saved **only on your device**. We do not run servers that receive this information, and we do not ask you to create an account.

## Advertising

The app may show ads provided by **Unity Ads** (Unity Technologies). To deliver and measure ads, Unity Ads may collect information such as a device identifier, device and network information, approximate location derived from your IP address, and how you interact with ads. Unity's use of this information is described in the Unity Privacy Policy: https://unity.com/legal/game-player-and-app-user-privacy-policy

The app does not request permission to track you across other companies' apps and websites.

## Analytics

The app uses **Unity Analytics** (Unity Technologies) and **GameAnalytics** to understand how the game is played, for example which levels are started and finished, session length, and crashes. These services may collect a device identifier, device and network information, and approximate location derived from your IP address. This information is not used to identify you or to track you across other companies' apps. Unity's privacy policy is linked above; GameAnalytics' privacy policy: https://gameanalytics.com/privacy

## In-app purchases

Purchases are processed by Apple through the App Store. We never see or store your payment details. Apple shares with the app only what is needed to confirm and restore your purchases.

## Children

The app is suitable for a general audience and is not directed at children under 13. We do not knowingly collect personal information from children.

## Changes

If this policy changes, the updated version will be posted at this address with a new date.

## Contact

Questions about this policy: {EMAIL}
"""

def write(rel, text):
    p = os.path.join(ROOT, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(text)

def build():
    write("CNAME", "yogeestudios.com\n")
    write("style.css", CSS.replace("FONTDIR", "fonts"))
    write("index.html", index())

    # ---- privacy pages (existing policies are reused as written)
    pol = {}
    pol["fliplits"] = md_to_html(open(os.path.join(PROJECTS, "Fliplits/Docs/PrivacyPolicy.md"), encoding="utf-8").read().replace("[your support email]", EMAIL))
    if any(g["slug"] == "hex-appeal" for g in GAMES): pol["hex-appeal"] = main_of(os.path.join(PROJECTS, "3D Cyber Casual Game/Docs/AppStore/site/privacy.html"))
    pol["snap-bandits"] = md_to_html(SNAP_PRIVACY)
    pol["twisted-system"] = main_of(os.path.join(PROJECTS, "Twisted System/AppStore/privacy-policy.html"))
    pol["iqube"] = md_to_html(open(os.path.join(PROJECTS, "iQube intelligent blocks/Marketing/App Store/Privacy_Policy.md"), encoding="utf-8").read())
    for g in [g for g in GAMES if g.get("docs", True)]:
        pol[g["slug"]] = re.sub(r"Yo[Gg]ee Studios?|YOGEE STUDIOS?", STUDIO, pol[g["slug"]])
        write(f"privacy/{g['slug']}.html", page(f"{g['name']} Privacy Policy | {STUDIO}", f'<main class="doc">{pol[g["slug"]]}</main>', depth=1))
    links = "".join(f'<li><a href="{g["slug"]}.html">{html.escape(g["name"])}</a></li>' for g in GAMES if g.get("docs", True))
    write("privacy/index.html", page(f"Privacy | {STUDIO}", f'<main class="doc"><h1>Privacy policies</h1><p>Each game has its own policy.</p><ul>{links}</ul></main>', depth=1))

    # ---- support
    sections = []
    for g in [g for g in GAMES if g.get("docs", True)]:
        extra = ""
        if g["slug"] == "snap-bandits":
            extra = "<p><strong>How do I play?</strong> Swipe across a rubber band to snip it. Get every bandit into the tube that matches its color. Fewer snips earn more stars.</p><p><strong>Restore purchases:</strong> open the Shop and tap Restore purchases at the bottom.</p>"
        elif g["slug"] == "hex-appeal":
            extra = "<p><strong>How do I play?</strong> Tap a hex tile to turn it. Connect the light from each glowing core to every gem on the board. Fewer turns earn more stars.</p>"
        elif g["slug"] == "fliplits":
            extra = "<p><strong>How do I play?</strong> Tap a tile to wake it. Its light flips the next tile it points at. Light every tile with the sparks you have.</p>"
        sections.append(f'<h2 id="{g["slug"]}">{html.escape(g["name"])}</h2>{extra}<p>Found a bug or need help with a purchase? Email <a href="mailto:{EMAIL}?subject={html.escape(g["name"])}%20support">{EMAIL}</a> with your iPhone model and iOS version. <a href="privacy/{g["slug"]}.html">Privacy policy</a>.</p>')
    body = f'<main class="doc"><h1>Support</h1><p>Need help with one of our games? Email <a href="mailto:{EMAIL}">{EMAIL}</a>. We usually reply within two business days.</p>{"".join(sections)}</main>'
    write("support.html", page(f"Support | {STUDIO}", body))
    print("built", len(GAMES), "games")

if __name__ == "__main__":
    build()
