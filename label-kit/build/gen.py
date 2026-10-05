#!/usr/bin/env python3
"""Genera i 12 template SVG (mm reali, livelli), i simboli vettoriali e le sorgenti HTML di guida/checklist."""
import os, math
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(ROOT, "templates"); S = os.path.join(ROOT, "simboli"); H = os.path.join(ROOT, "build", "html")
for d in (T, S, H): os.makedirs(d, exist_ok=True)

BLEED = 3.0; SAFE = 3.0
STYLES = {
 "minimal":  dict(bg="#f4efe6", ink="#1b1a17", accent="#1f6f5b", muted="#6b665c", serif="'Cormorant Garamond', Georgia, serif", sans="'Inter', Helvetica, Arial, sans-serif"),
 "botanico": dict(bg="#d9c7a7", ink="#2e2418", accent="#5a6b3b", muted="#6e5f4a", serif="'Playfair Display', Georgia, serif", sans="'Josefin Sans', Helvetica, Arial, sans-serif"),
 "clinico":  dict(bg="#ffffff", ink="#10213a", accent="#2a6fdb", muted="#5c6b80", serif="'Inter', Helvetica, Arial, sans-serif", sans="'Inter', Helvetica, Arial, sans-serif"),
}
# (file, titolo, tipo, w, h, uso) — w,h = misura etichetta finita in mm. tipo: rect | round | wrap | tube
TEMPLATES = [
 ("01-vasetto-50ml-coperchio", "Vasetto 50 ml — coperchio", "round", 60, 60, "Crema viso, balsamo, scrub"),
 ("02-vasetto-50ml-fascia", "Vasetto 50 ml — fascia laterale", "wrap", 160, 30, "Fascia avvolgente sotto il coperchio"),
 ("03-flacone-100ml-fronte", "Flacone 100 ml — fronte", "rect", 60, 90, "Siero, tonico, olio"),
 ("04-flacone-200ml-fronte", "Flacone 200 ml — fronte", "rect", 80, 110, "Detergente, latte corpo"),
 ("05-flacone-250ml-avvolgente", "Flacone 250 ml — avvolgente", "wrap", 180, 100, "Fronte + retro su un'unica etichetta"),
 ("06-tubetto-100ml", "Tubetto 100 ml — verticale", "tube", 50, 110, "Crema mani, gel, dentifricio"),
 ("07-candela-180g-avvolgente", "Candela 180 g — avvolgente", "wrap", 200, 70, "Vaso in vetro Ø 65 mm"),
 ("08-candela-fondo-sicurezza", "Candela — etichetta fondo sicurezza", "round", 50, 50, "Pittogrammi EN 15494 + CLP"),
 ("09-bustina-integratore", "Bustina / doypack integratore", "rect", 90, 130, "Fronte stand-up pouch"),
 ("10-barattolo-capsule-avvolgente", "Barattolo capsule — avvolgente", "wrap", 170, 80, "Barattolo 100–150 cc"),
 ("11-sapone-fascetta", "Sapone — fascetta", "wrap", 200, 50, "Saponetta 90 × 60 × 25 mm"),
 ("12-rettangolare-generica", "Etichetta rettangolare generica", "rect", 100, 60, "Qualsiasi contenitore"),
]

def mm(v): return f"{v:.2f}"

def frame(w, h):
    """Ritorna (W,H) totali con abbondanza e il contenuto dei livelli guida."""
    W, H_ = w + 2*BLEED, h + 2*BLEED
    return W, H_

def guide_layer(tipo, w, h):
    W, H_ = frame(w, h)
    g = []
    g.append(f'<g id="ABBONDANZA" data-name="ABBONDANZA (3 mm) - non stampare">')
    if tipo == "round":
        r = w/2
        g.append(f'<circle cx="{mm(W/2)}" cy="{mm(H_/2)}" r="{mm(r+BLEED)}" fill="none" stroke="#ff00ff" stroke-width="0.15" stroke-dasharray="1 1"/>')
    else:
        g.append(f'<rect x="0" y="0" width="{mm(W)}" height="{mm(H_)}" fill="none" stroke="#ff00ff" stroke-width="0.15" stroke-dasharray="1 1"/>')
    g.append('</g>')
    g.append(f'<g id="FUSTELLA" data-name="FUSTELLA - linea di taglio">')
    if tipo == "round":
        g.append(f'<circle cx="{mm(W/2)}" cy="{mm(H_/2)}" r="{mm(w/2)}" fill="none" stroke="#00a0e9" stroke-width="0.2"/>')
    else:
        g.append(f'<rect x="{mm(BLEED)}" y="{mm(BLEED)}" width="{mm(w)}" height="{mm(h)}" rx="2" fill="none" stroke="#00a0e9" stroke-width="0.2"/>')
    g.append('</g>')
    g.append(f'<g id="AREA_SICURA" data-name="AREA SICURA (3 mm dal taglio) - tieni dentro i testi">')
    if tipo == "round":
        g.append(f'<circle cx="{mm(W/2)}" cy="{mm(H_/2)}" r="{mm(w/2-SAFE)}" fill="none" stroke="#00c853" stroke-width="0.15" stroke-dasharray="2 1"/>')
    else:
        g.append(f'<rect x="{mm(BLEED+SAFE)}" y="{mm(BLEED+SAFE)}" width="{mm(w-2*SAFE)}" height="{mm(h-2*SAFE)}" fill="none" stroke="#00c853" stroke-width="0.15" stroke-dasharray="2 1"/>')
    if tipo == "wrap":
        # zona sovrapposizione 5 mm a destra
        g.append(f'<rect x="{mm(BLEED+w-5)}" y="{mm(BLEED)}" width="5" height="{mm(h)}" fill="#ff9800" fill-opacity="0.15" stroke="none"/>')
        g.append(f'<text x="{mm(BLEED+w-2.5)}" y="{mm(BLEED+h/2)}" font-family="Helvetica, Arial" font-size="2" fill="#ff9800" text-anchor="middle" transform="rotate(-90 {mm(BLEED+w-2.5)} {mm(BLEED+h/2)})">SOVRAPPOSIZIONE 5 mm</text>')
        # divisione fronte/retro
        g.append(f'<line x1="{mm(BLEED+w/2)}" y1="{mm(BLEED)}" x2="{mm(BLEED+w/2)}" y2="{mm(BLEED+h)}" stroke="#9e9e9e" stroke-width="0.1" stroke-dasharray="0.5 0.5"/>')
        g.append(f'<text x="{mm(BLEED+w/4)}" y="{mm(BLEED+2.5)}" font-family="Helvetica, Arial" font-size="1.8" fill="#9e9e9e" text-anchor="middle">FRONTE</text>')
        g.append(f'<text x="{mm(BLEED+3*w/4)}" y="{mm(BLEED+2.5)}" font-family="Helvetica, Arial" font-size="1.8" fill="#9e9e9e" text-anchor="middle">RETRO</text>')
    if tipo == "tube":
        g.append(f'<rect x="{mm(BLEED)}" y="{mm(BLEED+h-8)}" width="{mm(w)}" height="8" fill="#ff9800" fill-opacity="0.15" stroke="none"/>')
        g.append(f'<text x="{mm(BLEED+w/2)}" y="{mm(BLEED+h-3.5)}" font-family="Helvetica, Arial" font-size="1.8" fill="#ff9800" text-anchor="middle">ZONA SALDATURA - niente testi</text>')
    g.append('</g>')
    return "\n".join(g)

def crop_marks(W, H_):
    L = 3; o = 1  # lunghezza, offset
    m = []
    for (x, y, dx, dy) in [(BLEED, BLEED, -1, -1), (W-BLEED, BLEED, 1, -1), (BLEED, H_-BLEED, -1, 1), (W-BLEED, H_-BLEED, 1, 1)]:
        m.append(f'<line x1="{mm(x+dx*o)}" y1="{mm(y)}" x2="{mm(x+dx*(o+L))}" y2="{mm(y)}" stroke="#000" stroke-width="0.1"/>')
        m.append(f'<line x1="{mm(x)}" y1="{mm(y+dy*o)}" x2="{mm(x)}" y2="{mm(y+dy*(o+L))}" stroke="#000" stroke-width="0.1"/>')
    return f'<g id="CROCINI" data-name="CROCINI DI TAGLIO">{"".join(m)}</g>'

def content_layers(tipo, w, h, titolo, st):
    c = STYLES[st]
    W, H_ = frame(w, h)
    cx, cy = W/2, H_/2
    small = h < 40 or w < 55
    g = []
    g.append('<g id="GRAFICA" data-name="GRAFICA - sfondo, pattern, illustrazioni">')
    if tipo == "round":
        g.append(f'<circle cx="{mm(cx)}" cy="{mm(cy)}" r="{mm(w/2+BLEED)}" fill="{c["bg"]}"/>')
    else:
        g.append(f'<rect x="0" y="0" width="{mm(W)}" height="{mm(H_)}" fill="{c["bg"]}"/>')
    if st == "minimal":
        if tipo == "round":
            g.append(f'<circle cx="{mm(cx)}" cy="{mm(cy)}" r="{mm(w/2-SAFE-1)}" fill="none" stroke="{c["accent"]}" stroke-width="0.4"/>')
        else:
            g.append(f'<rect x="{mm(BLEED+SAFE)}" y="{mm(BLEED+SAFE)}" width="{mm(w-2*SAFE)}" height="{mm(h-2*SAFE)}" fill="none" stroke="{c["accent"]}" stroke-width="0.4" rx="1"/>')
    elif st == "botanico":
        # rametto stilizzato in alto e in basso + texture puntinata
        leaf = lambda x, y, sc, rot: f'<g transform="translate({mm(x)},{mm(y)}) scale({sc}) rotate({rot})" fill="{c["accent"]}" fill-opacity="0.85"><path d="M0 0 C-3 -4 -3 -9 0 -12 C3 -9 3 -4 0 0Z"/><path d="M0 0 L0 -12" stroke="{c["bg"]}" stroke-width="0.4"/><path d="M-6 -3 C-4 -7 -2 -8 0 -8 C-1 -5 -3 -3 -6 -3Z"/><path d="M6 -3 C4 -7 2 -8 0 -8 C1 -5 3 -3 6 -3Z"/></g>'
        fx0 = cx if tipo != "wrap" else BLEED + w/4
        top = BLEED + SAFE + (4 if h > 40 else 1.5)
        if h > 40: g.append(leaf(fx0, top + 5, 0.45, 0))
        g.append(f'<rect x="{mm(BLEED)}" y="{mm(BLEED+h-SAFE-0.8)}" width="{mm(w)}" height="0.8" fill="{c["accent"]}" fill-opacity="0.9"/>')
        g.append(f'<rect x="{mm(BLEED)}" y="{mm(BLEED)}" width="{mm(w)}" height="0.8" fill="{c["accent"]}" fill-opacity="0.9"/>')
    elif st == "clinico":
        band_h = min(10, h*0.22)
        if tipo == "round":
            g.append(f'<path d="M{mm(cx-w/2-BLEED)} {mm(cy)} A{mm(w/2+BLEED)} {mm(w/2+BLEED)} 0 0 0 {mm(cx+w/2+BLEED)} {mm(cy)} Z" fill="{c["accent"]}" fill-opacity="0.08"/>')
            g.append(f'<rect x="{mm(cx-w/2)}" y="{mm(cy-0.3)}" width="{mm(w)}" height="0.6" fill="{c["accent"]}"/>')
        else:
            g.append(f'<rect x="0" y="0" width="{mm(W)}" height="{mm(BLEED+band_h)}" fill="{c["accent"]}"/>')
            g.append(f'<rect x="0" y="{mm(BLEED+band_h)}" width="{mm(W)}" height="0.5" fill="{c["ink"]}" fill-opacity="0.15"/>')
            for i in range(1, 6):
                yy = BLEED + band_h + (h - band_h) * i / 6
                g.append(f'<rect x="{mm(BLEED+SAFE)}" y="{mm(yy)}" width="{mm(w-2*SAFE)}" height="0.15" fill="{c["accent"]}" fill-opacity="0.12"/>')
    g.append('</g>')
    g.append('<g id="TESTI" data-name="TESTI - nome, claim, INCI, avvertenze">')
    fx = cx if tipo != "wrap" else BLEED + w/4
    fs_brand = 2.4 if small else 3.2
    fs_name = 4.5 if small else 7
    fs_sub = 2 if small else 2.6
    brand_col = "#ffffff" if (st == "clinico" and tipo != "round") else c["accent"]
    brand_y = (BLEED + min(10, h*0.22)/2 + fs_brand/2.8) if (st == "clinico" and tipo != "round") else cy - (h*0.18)
    g.append(f'<text x="{mm(fx)}" y="{mm(brand_y)}" text-anchor="middle" font-family="{c["sans"]}" font-weight="600" font-size="{fs_brand}" letter-spacing="0.6" fill="{brand_col}">NOME BRAND</text>')
    g.append(f'<text x="{mm(fx)}" y="{mm(cy + 1.5)}" text-anchor="middle" font-family="{c["serif"]}" font-weight="{"700" if st=="clinico" else "500"}" font-size="{fs_name}" fill="{c["ink"]}">Nome Prodotto</text>')
    g.append(f'<text x="{mm(fx)}" y="{mm(cy + (h*0.16))}" text-anchor="middle" font-family="{c["sans"]}" font-size="{fs_sub}" fill="{c["muted"]}">claim breve · funzione</text>')
    g.append(f'<text x="{mm(fx)}" y="{mm(BLEED + h - SAFE - 1.5)}" text-anchor="middle" font-family="{c["sans"]}" font-size="{fs_sub}" fill="{c["ink"]}">50 ml ℮</text>')
    if tipo == "wrap":
        bx = BLEED + w/2 + SAFE + 2; by = BLEED + SAFE + (12 if st=="clinico" else 5); bw = w/2 - 5 - 2*SAFE - 2
        lines = ["INGREDIENTI / INCI: Aqua, Glycerin, ... (min. 1,2 mm x-height consigliata)",
                 "MODO D'USO: ...", "AVVERTENZE: ...",
                 "Responsabile immissione sul mercato: Nome, Indirizzo, Città (IT)",
                 "Lotto: vedi fondo · Made in Italy"]
        y = by
        for ln in lines:
            g.append(f'<text x="{mm(bx)}" y="{mm(y)}" font-family="{c["sans"]}" font-size="1.8" fill="{c["ink"]}" xml:space="preserve">{ln}</text>')
            y += 3.2
        g.append(f'<rect x="{mm(bx)}" y="{mm(y)}" width="{mm(bw)}" height="{mm(max(4, BLEED+h-SAFE-y-10))}" fill="none" stroke="#9e9e9e" stroke-width="0.1" stroke-dasharray="0.5 0.5"/>')
        g.append(f'<text x="{mm(bx+1)}" y="{mm(y+2.5)}" font-family="{c["sans"]}" font-size="1.5" fill="#9e9e9e">area testi aggiuntivi / codice a barre</text>')
    g.append('</g>')
    # simboli: usa i file in /simboli; qui solo segnaposto
    g.append('<g id="SIMBOLI" data-name="SIMBOLI OBBLIGATORI - incolla da cartella simboli">')
    sx = (BLEED + w - SAFE - 14) if tipo != "round" else (cx - 6)
    sy = BLEED + h - SAFE - 6 if tipo != "round" else cy + w/2 - SAFE - 8
    if tipo == "wrap": sx = BLEED + w - 5 - SAFE - 14
    for i, lab in enumerate(["PAO", "℮", "♻"]):
        g.append(f'<rect x="{mm(sx + i*4.6)}" y="{mm(sy)}" width="4" height="4" rx="0.5" fill="none" stroke="#9e9e9e" stroke-width="0.1" stroke-dasharray="0.4 0.4"/>')
        g.append(f'<text x="{mm(sx + i*4.6 + 2)}" y="{mm(sy+2.8)}" text-anchor="middle" font-family="Helvetica, Arial" font-size="1.6" fill="#9e9e9e">{lab}</text>')
    g.append('</g>')
    return "\n".join(g)

def svg_template(file, titolo, tipo, w, h, uso, st="minimal"):
    W, H_ = frame(w, h)
    os.makedirs(os.path.join(T, st), exist_ok=True)
    body = f'''<?xml version="1.0" encoding="UTF-8"?>
<!-- Label Kit — stile {st.upper()} — {titolo} — misura finita {w} × {h} mm, abbondanza {BLEED} mm per lato, area sicura {SAFE} mm.
     Livelli (gruppi di primo livello): GRAFICA, TESTI, SIMBOLI, AREA_SICURA, FUSTELLA, ABBONDANZA, CROCINI, NOTE.
     Prima di esportare: nascondi AREA_SICURA, ABBONDANZA, NOTE; FUSTELLA su colore spot "CutContour" o nascosta (chiedi alla tipografia). -->
<svg xmlns="http://www.w3.org/2000/svg" width="{mm(W)}mm" height="{mm(H_)}mm" viewBox="0 0 {mm(W)} {mm(H_)}">
<title>{titolo} · {st}</title>
{content_layers(tipo, w, h, titolo, st)}
{guide_layer(tipo, w, h)}
{crop_marks(W, H_)}
<g id="NOTE" data-name="NOTE PER IL DESIGNER - non stampare">
<text x="{mm(BLEED)}" y="{mm(H_ + 0)}" font-family="Helvetica, Arial" font-size="1.6" fill="#9e9e9e" transform="translate(0,-0.6)">{titolo} · {w}×{h} mm · {uso} · magenta = abbondanza · ciano = taglio · verde = area sicura</text>
</g>
</svg>
'''
    with open(os.path.join(T, st, file + ".svg"), "w") as f: f.write(body)

import shutil
for old in [f for f in os.listdir(T) if f.endswith(".svg")]: os.remove(os.path.join(T, old))
for st in STYLES:
    for t in TEMPLATES: svg_template(*t, st=st)

# ---------- SIMBOLI ----------
def write_sym(name, w, h, inner, desc):
    with open(os.path.join(S, name + ".svg"), "w") as f:
        f.write(f'''<?xml version="1.0" encoding="UTF-8"?>
<!-- {desc} -->
<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}"><title>{desc}</title>
{inner}
</svg>
''')

# PAO: vasetto aperto con coperchio sollevato e "12M"
pao = '''<g fill="none" stroke="#000" stroke-width="0.45" stroke-linejoin="round" stroke-linecap="round">
<path d="M2.2 4.2 H8.8 V10.6 a0.8 0.8 0 0 1 -0.8 0.8 H3 a0.8 0.8 0 0 1 -0.8 -0.8 Z"/>
<path d="M2.6 2.3 a0.6 0.6 0 0 1 0.6 -0.6 h4.6 a0.6 0.6 0 0 1 0.6 0.6 v0.9 H2.6 Z" transform="rotate(-18 5.5 2.6) translate(0.2,-0.3)"/>
</g>
<text x="5.5" y="8.6" text-anchor="middle" font-family="Helvetica, Arial" font-weight="700" font-size="3.2" fill="#000">12M</text>'''
write_sym("pao-12m", 11, 12, pao, "PAO — Period After Opening (Reg. CE 1223/2009, All. VII). Cambia 12M con i mesi reali: 6M, 12M, 24M, 36M")

clessidra = '''<g fill="none" stroke="#000" stroke-width="0.5" stroke-linejoin="round">
<path d="M2 1 H9 M2 11 H9 M2.8 1 V3 C2.8 5 5.5 5 5.5 6 C5.5 7 2.8 7 2.8 9 V11 M8.2 1 V3 C8.2 5 5.5 5 5.5 6 C5.5 7 8.2 7 8.2 9 V11"/>
<path d="M3.6 10 C3.6 8.3 5.5 8 5.5 7.2 C5.5 8 7.4 8.3 7.4 10 Z" fill="#000" stroke="none"/>
</g>'''
write_sym("clessidra-durata-minima", 11, 12, clessidra, "Clessidra — data di durata minima (obbligatoria se durata ≤ 30 mesi), accompagnata da mese/anno")

emark = '''<text x="5.5" y="9.4" text-anchor="middle" font-family="Helvetica, Arial" font-weight="400" font-size="11" fill="#000">℮</text>'''
write_sym("e-mark", 11, 12, emark, "Marchio ℮ — quantità nominale stimata (Dir. 76/211/CEE). Altezza minima 3 mm, dopo il valore: 50 ml ℮")

mobius = '''<g fill="#000" transform="translate(5.5,6)">
<path id="a" d="M0 -5.2 l2.6 4.5 h-1.4 l0.7 1.2 h-3.8 l0.7 -1.2 h-1.4 Z" transform="rotate(0)"/>
<use href="#a" transform="rotate(120)"/><use href="#a" transform="rotate(240)"/>
</g>'''
write_sym("mobius-riciclabile", 11, 12, mobius, "Anello di Möbius — materiale riciclabile. Da affiancare al codice materiale (es. PP 5, GL 70, PAP 21)")

mano_libro = '''<g fill="none" stroke="#000" stroke-width="0.45" stroke-linejoin="round" stroke-linecap="round">
<path d="M1.5 7.5 L5.5 6 L9.5 7.5 V10.5 L5.5 9 L1.5 10.5 Z M5.5 6 V9"/>
<path d="M3.2 6.2 V3.4 a0.6 0.6 0 0 1 1.2 0 V5 M4.4 3 a0.6 0.6 0 0 1 1.2 0 V5 M5.6 2.6 a0.6 0.6 0 0 1 1.2 0 V5 M6.8 3.2 a0.6 0.6 0 0 1 1.2 0 V5.6"/>
</g>'''
write_sym("mano-libro-vedi-foglietto", 11, 12, mano_libro, "Mano su libro — 'vedi informazioni allegate' (All. VII 1223/2009), quando INCI/avvertenze non entrano in etichetta")

def pict_candela(name, inner, desc):
    write_sym(name, 12, 12, f'<circle cx="6" cy="6" r="5.5" fill="none" stroke="#000" stroke-width="0.5"/>{inner}', desc)
pict_candela("candela-non-lasciare-incustodita", '''<path d="M4.2 8.5 h3.6 M5 8.5 V5.2 h2 V8.5 M6 2.6 c-0.9 1.1 -1.1 1.9 0 2.6 c1.1 -0.7 0.9 -1.5 0 -2.6Z" fill="none" stroke="#000" stroke-width="0.45" stroke-linejoin="round"/><line x1="2.5" y1="9.5" x2="9.5" y2="2.5" stroke="#000" stroke-width="0.6"/>''', "EN 15494 — Non lasciare mai una candela accesa incustodita")
pict_candela("candela-lontano-da-bambini", '''<circle cx="6" cy="4.2" r="1.1" fill="none" stroke="#000" stroke-width="0.45"/><path d="M4.3 9.5 V6.8 a1.7 1.7 0 0 1 3.4 0 V9.5" fill="none" stroke="#000" stroke-width="0.45"/><line x1="2.5" y1="9.5" x2="9.5" y2="2.5" stroke="#000" stroke-width="0.6"/>''', "EN 15494 — Tenere lontano dalla portata di bambini e animali")
pict_candela("candela-lontano-da-materiali-infiammabili", '''<path d="M3 9 V5.5 h2.4 V9 M7.3 4.2 c-0.9 1.1 -1.1 1.9 0 2.6 c1.1 -0.7 0.9 -1.5 0 -2.6Z M3.3 5.5 c0.3 -1 1.8 -1.2 2.1 0" fill="none" stroke="#000" stroke-width="0.45" stroke-linejoin="round"/><line x1="2.5" y1="9.5" x2="9.5" y2="2.5" stroke="#000" stroke-width="0.6"/>''', "EN 15494 — Tenere lontano da materiali infiammabili")

# Codice materiale (etichettatura ambientale IT, D.Lgs. 116/2020)
mat = '''<rect x="0.3" y="0.3" width="21.4" height="11.4" rx="1" fill="none" stroke="#000" stroke-width="0.35"/>
<g transform="translate(5.5,6) scale(0.8)"><path id="b" d="M0 -5.2 l2.6 4.5 h-1.4 l0.7 1.2 h-3.8 l0.7 -1.2 h-1.4 Z" fill="#000"/><use href="#b" transform="rotate(120)"/><use href="#b" transform="rotate(240)"/></g>
<text x="15.5" y="5.2" text-anchor="middle" font-family="Helvetica, Arial" font-weight="700" font-size="3.4" fill="#000">PP 5</text>
<text x="15.5" y="9.2" text-anchor="middle" font-family="Helvetica, Arial" font-size="2" fill="#000">PLASTICA</text>'''
write_sym("codice-materiale-pp5", 22, 12, mat, "Codice materiale imballaggio (D.Lgs. 116/2020 / Dec. 97/129/CE). Esempi: PP 5, PET 1, HDPE 2, GL 70 vetro, PAP 21 carta, ALU 41")

racc = '''<text x="0" y="3" font-family="Helvetica, Arial" font-size="2.2" fill="#000">Raccolta differenziata.</text>
<text x="0" y="6" font-family="Helvetica, Arial" font-size="2.2" fill="#000">Verifica le disposizioni del tuo Comune.</text>'''
write_sym("raccolta-differenziata-testo", 50, 8, racc, "Frase di raccolta (etichettatura ambientale Italia)")

print("templates:", sum(len(os.listdir(os.path.join(T,d))) for d in STYLES), "simboli:", len(os.listdir(S)))
