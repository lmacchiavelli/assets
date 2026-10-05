#!/usr/bin/env python3
"""Genera HTML di mockup (contenitori CSS + etichetta SVG) e l'immagine hero del listing."""
import os, re, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(ROOT, "templates"); H = os.path.join(ROOT, "build", "html")
STYLES = ["minimal", "botanico", "clinico"]
svgs = sorted(f for f in os.listdir(os.path.join(T, "minimal")) if f.endswith(".svg"))
FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Inter:wght@400;600;700&family=Playfair+Display:wght@500;700&family=Josefin+Sans:wght@400;600&display=swap">'

def load(name, st="minimal"):
    s = open(os.path.join(T, st, name)).read()
    s = s.split("<svg", 1)[1]; s = "<svg" + s
    # nascondi livelli guida come farebbe il designer
    for lid in ("AREA_SICURA", "ABBONDANZA", "CROCINI", "NOTE", "FUSTELLA"):
        s = re.sub(rf'<g id="{lid}"', f'<g id="{lid}" style="display:none"', s)
    s = re.sub(r'width="[\d.]+mm" height="[\d.]+mm"', 'width="100%" height="100%"', s, count=1)
    return s

CSS = """
body{margin:0;background:#e9e4da;font-family:-apple-system,Inter,Helvetica,Arial,sans-serif}
.scene{width:1200px;height:900px;position:relative;background:radial-gradient(ellipse at 50% 30%,#f7f3ec,#d9d2c4);display:flex;align-items:center;justify-content:center;overflow:hidden}
.shadow{position:absolute;bottom:120px;left:50%;transform:translateX(-50%);width:420px;height:60px;border-radius:50%;background:rgba(0,0,0,.25);filter:blur(22px)}
.jar{position:relative;width:360px;height:420px}
.jar .body{position:absolute;left:0;top:70px;width:360px;height:350px;border-radius:28px 28px 40px 40px/20px 20px 60px 60px;background:linear-gradient(90deg,#d8d2c6 0%,#fbf8f2 25%,#f3eee5 55%,#cfc8ba 100%);box-shadow:inset 0 -30px 40px rgba(0,0,0,.08)}
.jar .lid{position:absolute;left:-10px;top:20px;width:380px;height:80px;border-radius:14px/40px;background:linear-gradient(90deg,#8a7f70,#e6ddd0 30%,#d7cdbd 60%,#7a6f61);box-shadow:0 6px 10px rgba(0,0,0,.2)}
.jar .lid::before{content:"";position:absolute;left:0;top:0;right:0;height:22px;border-radius:50%;background:linear-gradient(90deg,#a89b8a,#fff8ee 40%,#b9ad9c)}
.label{position:absolute;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,.18)}
.label::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(0,0,0,.18),rgba(255,255,255,.18) 25%,rgba(255,255,255,0) 55%,rgba(0,0,0,.22));pointer-events:none}
.bottle{position:relative;width:260px;height:560px}
.bottle .body{position:absolute;left:0;top:120px;width:260px;height:440px;border-radius:30px 30px 36px 36px/24px 24px 40px 40px;background:linear-gradient(90deg,#b8aa96 0%,#f6f0e6 22%,#ece5d8 60%,#a69b89 100%)}
.bottle .neck{position:absolute;left:95px;top:40px;width:70px;height:90px;background:linear-gradient(90deg,#7c7264,#d8cfc0 40%,#6f665a)}
.bottle .cap{position:absolute;left:85px;top:0;width:90px;height:50px;border-radius:10px;background:linear-gradient(90deg,#2f2b26,#6a625a 40%,#2b2723)}
.bottle .pump{position:absolute;left:120px;top:-40px;width:20px;height:50px;background:#3a352f;border-radius:4px}
.tube{position:relative;width:200px;height:560px}
.tube .body{position:absolute;left:0;top:60px;width:200px;height:500px;border-radius:12px 12px 100px 100px/12px 12px 30px 30px;background:linear-gradient(90deg,#c5b9a6,#fbf7f0 25%,#f1ebe1 60%,#b3a795)}
.tube .cap{position:absolute;left:60px;top:0;width:80px;height:70px;border-radius:12px 12px 4px 4px;background:linear-gradient(90deg,#2f2b26,#746b61 40%,#2b2723)}
.candle{position:relative;width:300px;height:360px}
.candle .glass{position:absolute;left:0;top:0;width:300px;height:360px;border-radius:14px 14px 30px 30px/10px 10px 30px 30px;background:linear-gradient(90deg,rgba(90,80,70,.55),rgba(255,250,240,.35) 25%,rgba(255,250,240,.2) 60%,rgba(70,60,50,.6))}
.candle .wax{position:absolute;left:8px;top:40px;width:284px;height:312px;border-radius:10px 10px 26px 26px/8px 8px 26px 26px;background:linear-gradient(90deg,#e9e2d4,#fbf8f2 40%,#e3dccd)}
.pouch{position:relative;width:330px;height:480px}
.pouch .body{position:absolute;inset:0;border-radius:14px 14px 30px 30px/14px 14px 50px 50px;background:linear-gradient(90deg,#8a8378,#d9d3c8 20%,#cfc8bb 60%,#7f786d);box-shadow:inset 0 0 40px rgba(0,0,0,.15)}
.pouch .zip{position:absolute;left:14px;right:14px;top:38px;height:10px;background:rgba(0,0,0,.25);border-radius:3px}
.soap{position:relative;width:360px;height:240px}
.soap .bar{position:absolute;inset:0;border-radius:40px/30px;background:linear-gradient(90deg,#c8bfae,#f4eee2 30%,#ece4d6 65%,#b8af9d)}
.caption{position:absolute;left:0;right:0;bottom:28px;text-align:center;color:#6b665c;font-size:20px;letter-spacing:.02em}
"""

def scene(kind, svg, caption, labelbox):
    inner = {
     "jar": f'<div class="jar"><div class="lid"></div><div class="body"></div><div class="label" style="{labelbox}">{svg}</div></div>',
     "bottle": f'<div class="bottle"><div class="pump"></div><div class="cap"></div><div class="neck"></div><div class="body"></div><div class="label" style="{labelbox}">{svg}</div></div>',
     "tube": f'<div class="tube"><div class="cap"></div><div class="body"></div><div class="label" style="{labelbox}">{svg}</div></div>',
     "candle": f'<div class="candle"><div class="wax"></div><div class="label" style="{labelbox}">{svg}</div><div class="glass"></div></div>',
     "pouch": f'<div class="pouch"><div class="body"></div><div class="zip"></div><div class="label" style="{labelbox}">{svg}</div></div>',
     "soap": f'<div class="soap"><div class="bar"></div><div class="label" style="{labelbox}">{svg}</div></div>',
    }[kind]
    return f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>{CSS}</style></head><body><div class="scene"><div class="shadow"></div>{inner}<div class="caption">{html.escape(caption)}</div></div></body></html>'

# (template file, tipo contenitore, posizione etichetta)
SCENES = [
 ("01-vasetto-50ml-coperchio.svg", "jar", "left:30px;top:-10px;width:300px;height:100px;border-radius:50%/50%;transform:scaleY(.42);transform-origin:top", "Vasetto 50 ml · coperchio"),
 ("02-vasetto-50ml-fascia.svg", "jar", "left:0;top:160px;width:360px;height:68px", "Vasetto 50 ml · fascia"),
 ("03-flacone-100ml-fronte.svg", "bottle", "left:40px;top:220px;width:180px;height:270px", "Flacone 100 ml"),
 ("05-flacone-250ml-avvolgente.svg", "bottle", "left:0;top:200px;width:260px;height:290px", "Flacone 250 ml · avvolgente"),
 ("06-tubetto-100ml.svg", "tube", "left:10px;top:120px;width:180px;height:396px", "Tubetto 100 ml"),
 ("07-candela-180g-avvolgente.svg", "candle", "left:8px;top:120px;width:284px;height:200px", "Candela 180 g"),
 ("09-bustina-integratore.svg", "pouch", "left:40px;top:80px;width:250px;height:360px", "Bustina integratore"),
 ("10-barattolo-capsule-avvolgente.svg", "jar", "left:0;top:110px;width:360px;height:300px", "Barattolo capsule"),
 ("11-sapone-fascetta.svg", "soap", "left:0;top:70px;width:360px;height:90px", "Sapone · fascetta"),
]
STYLE_FOR = {"01":"minimal","02":"botanico","03":"clinico","05":"minimal","06":"clinico","07":"botanico","09":"clinico","10":"minimal","11":"botanico"}
for f, kind, box, cap in SCENES:
    st = STYLE_FOR[f[:2]]
    open(os.path.join(H, "mockup-" + f.replace(".svg", ".html")), "w").write(scene(kind, load(f, st), cap + " · stile " + st, box))

# HERO: griglia dei 12 template
cards = ""
for f in svgs:
    name = f[3:-4].replace("-", " ")
    cards += f'<div class="card"><div class="thumb">{load(f)}</div><div class="n">{html.escape(name)}</div></div>'
hero = f'''<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>
body{{margin:0;font-family:-apple-system,Inter,Helvetica,Arial,sans-serif}}
.hero{{width:2000px;height:1500px;background:#f4efe6;padding:70px 80px;box-sizing:border-box;position:relative}}
h1{{font-size:58px;margin:0 0 8px;max-width:1380px;letter-spacing:-.02em;color:#1b1a17}}
p{{font-size:28px;color:#6b665c;margin:0 0 40px}}
.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:28px}}
.card{{background:#fff;border-radius:18px;padding:18px;box-shadow:0 8px 24px rgba(0,0,0,.08)}}
.thumb{{height:200px;display:flex;align-items:center;justify-content:center}}.thumb svg{{max-width:100%;max-height:100%;width:auto;height:auto;filter:drop-shadow(0 2px 4px rgba(0,0,0,.15))}}
.n{{font-size:20px;color:#1b1a17;margin-top:10px;text-transform:capitalize}}
.badge{{position:absolute;right:80px;top:88px;background:#1f6f5b;color:#fff;font-size:26px;font-weight:700;padding:14px 26px;border-radius:999px}}
</style></head><body><div class="hero"><div class="badge">36 template · 3 stili · SVG + PDF</div>
<h1>Label Kit — Etichette cosmetiche pronte stampa</h1><p>12 formati × 3 stili. Abbondanze, fustella, area sicura e simboli obbligatori già impostati. Cambi testi e colori, esporti, stampi.</p>
<div class="grid">{cards}</div></div></body></html>'''
open(os.path.join(H, "hero.html"), "w").write(hero)

# PRIMA / DOPO
bad = '''<svg viewBox="0 0 66 96" width="100%" height="100%"><rect width="66" height="96" fill="#fff"/><text x="33" y="30" text-anchor="middle" font-family="Comic Sans MS, Chalkboard, cursive" font-size="7" fill="#e91e63">Crema Viso</text><text x="33" y="42" text-anchor="middle" font-family="Arial" font-size="4" fill="#4caf50">100% NATURALE!!!</text><text x="33" y="60" text-anchor="middle" font-family="Arial" font-size="3" fill="#2196f3">aloe • argan • karitè</text><text x="33" y="85" text-anchor="middle" font-family="Arial" font-size="2.2" fill="#000">ingredienti: acqua, olio...</text><rect x="4" y="68" width="58" height="8" fill="#ffeb3b"/><text x="33" y="73.5" text-anchor="middle" font-family="Arial" font-size="3" fill="#000">OFFERTA</text></svg>'''
good = load("03-flacone-100ml-fronte.svg")
ba = f'''<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>{CSS}
.scene{{width:2000px;height:1500px;background:#f4efe6}}
.col{{position:absolute;top:0;bottom:0;width:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:40px}}
.t{{font-size:54px;font-weight:800;color:#1b1a17}}.t small{{display:block;font-size:26px;font-weight:400;color:#6b665c}}
.bottle{{transform:scale(1.5);transform-origin:top center;margin:40px 0 0}}
.col{{justify-content:flex-start;padding-top:140px}}
</style></head><body><div class="scene">
<div class="col" style="left:0"><div class="t">Prima<small>fatta su Canva, rimandata dalla tipografia</small></div><div class="bottle"><div class="pump"></div><div class="cap"></div><div class="neck"></div><div class="body"></div><div class="label" style="left:40px;top:220px;width:180px;height:270px">{bad}</div></div></div>
<div class="col" style="left:50%"><div class="t">Dopo<small>con Label Kit, accettata al primo invio</small></div><div class="bottle"><div class="pump"></div><div class="cap"></div><div class="neck"></div><div class="body"></div><div class="label" style="left:40px;top:220px;width:180px;height:270px">{good}</div></div></div>
</div></body></html>'''
open(os.path.join(H, "prima-dopo.html"), "w").write(ba)

# LIVELLI: screenshot "cosa c'è dentro"
lay = f'''<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>
body{{margin:0;font-family:-apple-system,Inter,Helvetica,Arial,sans-serif}}
.s{{width:2000px;height:1500px;background:#2b2b2b;position:relative;color:#eee}}
.canvas{{position:absolute;left:80px;top:120px;width:1240px;height:1260px;background:#3c3c3c;display:flex;align-items:center;justify-content:center}}
.canvas svg{{width:1100px;height:auto;background:#fff}}
.panel{{position:absolute;right:80px;top:120px;width:520px;background:#1e1e1e;border:1px solid #444;border-radius:8px;font-size:26px}}
.panel .h{{padding:16px 20px;border-bottom:1px solid #444;color:#aaa;font-size:22px}}
.row{{display:flex;align-items:center;gap:14px;padding:14px 20px;border-bottom:1px solid #333}}
.eye{{width:26px;height:26px;border-radius:50%;background:#7ac;}}
.sw{{width:18px;height:18px;border-radius:3px}}
h1{{position:absolute;left:80px;top:40px;margin:0;font-size:44px;font-weight:700}}
</style></head><body><div class="s"><h1>Livelli già organizzati, come in uno studio di packaging</h1>
<div class="canvas">{load("05-flacone-250ml-avvolgente.svg").replace('style="display:none"','')}</div>
<div class="panel"><div class="h">Livelli</div>
<div class="row"><div class="eye"></div><div class="sw" style="background:#9e9e9e"></div>NOTE PER IL DESIGNER</div>
<div class="row"><div class="eye"></div><div class="sw" style="background:#000"></div>CROCINI DI TAGLIO</div>
<div class="row"><div class="eye"></div><div class="sw" style="background:#ff00ff"></div>ABBONDANZA (3 mm)</div>
<div class="row"><div class="eye"></div><div class="sw" style="background:#00a0e9"></div>FUSTELLA</div>
<div class="row"><div class="eye"></div><div class="sw" style="background:#00c853"></div>AREA SICURA (3 mm)</div>
<div class="row"><div class="eye"></div><div class="sw" style="background:#ff9800"></div>SIMBOLI OBBLIGATORI</div>
<div class="row"><div class="eye"></div><div class="sw" style="background:#fff"></div>TESTI</div>
<div class="row"><div class="eye"></div><div class="sw" style="background:#1f6f5b"></div>GRAFICA</div>
</div></div></body></html>'''
open(os.path.join(H, "livelli.html"), "w").write(lay)
print("html:", sorted(os.listdir(H)))

# TRE STILI: stesso formato, tre look
tre = ""
for st, lab in [("minimal","Minimal"),("botanico","Botanico"),("clinico","Clinico")]:
    tre += f'<div class="card"><div class="thumb" style="height:520px">{load("05-flacone-250ml-avvolgente.svg", st)}</div><div class="n" style="font-size:30px;text-align:center">{lab}</div></div>'
stili = f'''<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>
body{{margin:0;font-family:Inter,-apple-system,Helvetica,Arial,sans-serif}}
.hero{{width:2000px;height:1500px;background:#f4efe6;padding:70px 80px;box-sizing:border-box}}
h1{{font-size:58px;margin:0 0 8px;letter-spacing:-.02em;color:#1b1a17}}p{{font-size:28px;color:#6b665c;margin:0 0 40px}}
.grid{{display:grid;grid-template-columns:1fr;gap:26px}}
.card{{background:#fff;border-radius:18px;padding:18px 24px;box-shadow:0 8px 24px rgba(0,0,0,.08);display:grid;grid-template-columns:1fr 220px;align-items:center}}
.thumb svg{{max-width:100%;max-height:100%;width:auto;height:auto;filter:drop-shadow(0 2px 4px rgba(0,0,0,.15))}}.thumb{{display:flex;align-items:center;justify-content:center;height:330px!important}}
</style></head><body><div class="hero"><h1>Tre stili, ogni formato</h1><p>Minimal · Botanico (kraft) · Clinico (farmacia). Scegli il look del tuo brand e parti da lì.</p><div class="grid">{tre}</div></div></body></html>'''
open(os.path.join(H, "stili.html"), "w").write(stili)
