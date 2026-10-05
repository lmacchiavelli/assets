#!/usr/bin/env python3
"""Genera editor/index.html: compila i campi una volta, 36 etichette si aggiornano, download SVG/PDF."""
import os, json, re, base64
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(ROOT, "templates"); OUT = os.path.join(ROOT, "editor"); os.makedirs(OUT, exist_ok=True)
STYLES = ["minimal", "botanico", "clinico"]
STYLE_COLORS = {"minimal": ("#f4efe6", "#1f6f5b", "#1b1a17"), "botanico": ("#d9c7a7", "#5a6b3b", "#2e2418"), "clinico": ("#ffffff", "#2a6fdb", "#10213a")}

tpls = []
for st in STYLES:
    for f in sorted(os.listdir(os.path.join(T, st))):
        s = open(os.path.join(T, st, f)).read()
        s = s[s.index("<svg"):]
        title = re.search(r"<title>(.*?)</title>", s).group(1).split(" · ")[0]
        w = float(re.search(r'width="([\d.]+)mm"', s).group(1)); h = float(re.search(r'height="([\d.]+)mm"', s).group(1))
        tpls.append(dict(id=f[:-4], style=st, title=title, w=w, h=h, svg=s))

# font come data-uri per il download SVG autonomo (opzionale, pesante): usiamo i font di sistema nel browser + @font-face da fonts/
fontcss = ""
for fam, path in [("Inter", "inter/Inter[opsz,wght].ttf"), ("Cormorant Garamond", "cormorantgaramond/CormorantGaramond[wght].ttf"), ("Playfair Display", "playfairdisplay/PlayfairDisplay[wght].ttf"), ("Josefin Sans", "josefinsans/JosefinSans[wght].ttf")]:
    fontcss += f"@font-face{{font-family:'{fam}';src:url('../fonts/{path}') format('truetype');font-weight:100 900}}\n"

html = r'''<!doctype html>
<html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Label Kit Editor</title>
<style>
__FONTCSS__
:root{--bg:#faf8f4;--fg:#1b1a17;--muted:#6b665c;--accent:#1f6f5b;--line:#e6e1d7;--card:#fff}
*{box-sizing:border-box}body{margin:0;font:15px/1.5 Inter,-apple-system,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--fg)}
header{display:flex;align-items:center;gap:16px;padding:12px 20px;border-bottom:1px solid var(--line);background:var(--card);position:sticky;top:0;z-index:5}
header h1{font-size:18px;margin:0}header .sp{flex:1}header small{color:var(--muted)}
.wrap{display:grid;grid-template-columns:340px 1fr;min-height:calc(100vh - 54px)}
aside{border-right:1px solid var(--line);padding:18px;background:var(--card);overflow:auto;max-height:calc(100vh - 54px);position:sticky;top:54px}
label{display:block;font-size:12px;font-weight:600;color:var(--muted);margin:12px 0 4px;text-transform:uppercase;letter-spacing:.04em}
input,textarea,select{width:100%;padding:8px 10px;border:1px solid var(--line);border-radius:8px;font:inherit;background:#fff;color:var(--fg)}
textarea{min-height:70px;resize:vertical}
.row{display:flex;gap:8px}.row>*{flex:1}
.seg{display:flex;gap:6px;flex-wrap:wrap}.seg button{flex:1;padding:8px;border:1px solid var(--line);background:#fff;border-radius:8px;cursor:pointer;font:inherit}.seg button.on{background:var(--accent);color:#fff;border-color:var(--accent)}
.chk{display:flex;align-items:center;gap:8px;margin-top:10px;font-size:14px}.chk input{width:auto}
main{padding:18px 20px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px;display:flex;flex-direction:column;gap:8px}
.card .pv{height:200px;display:flex;align-items:center;justify-content:center;background:#efece6;border-radius:8px;overflow:hidden}
.card .pv svg{max-width:96%;max-height:96%;width:auto;height:auto;filter:drop-shadow(0 2px 4px rgba(0,0,0,.15))}
.card .t{font-size:13px;font-weight:600}.card .m{font-size:12px;color:var(--muted)}
.card .b{display:flex;gap:6px}.card .b button{flex:1;padding:7px;border:1px solid var(--line);background:#fff;border-radius:8px;cursor:pointer;font:inherit;font-size:13px}.card .b button:hover{border-color:var(--accent);color:var(--accent)}
.help{font-size:12px;color:var(--muted);margin-top:14px;border-top:1px solid var(--line);padding-top:10px}
@media(max-width:800px){.wrap{grid-template-columns:1fr}aside{position:static;max-height:none;border-right:0;border-bottom:1px solid var(--line)}}
@media print{body *{visibility:hidden}#printbox,#printbox *{visibility:visible}#printbox{position:fixed;left:0;top:0}}
</style></head><body>
<header><h1>Label Kit Editor</h1><small>Compila una volta: 36 etichette si aggiornano. Scarica SVG o PDF.</small><span class="sp"></span><button id="dlall" class="seg" style="padding:8px 14px;border:1px solid var(--accent);color:var(--accent);background:#fff;border-radius:8px;cursor:pointer;font:inherit">Scarica tutti gli SVG dello stile</button></header>
<div class="wrap">
<aside>
  <label>Stile</label><div class="seg" id="style"><button data-v="minimal" class="on">Minimal</button><button data-v="botanico">Botanico</button><button data-v="clinico">Clinico</button></div>
  <label>Nome brand</label><input id="brand" value="NOME BRAND" maxlength="28">
  <label>Nome prodotto</label><input id="product" value="Nome Prodotto" maxlength="26">
  <label>Claim / funzione</label><input id="claim" value="claim breve · funzione" maxlength="40">
  <label>Quantità</label><div class="row"><input id="qty" value="50 ml"><select id="emark"><option value="℮">con ℮</option><option value="">senza ℮</option></select></div>
  <label>Ingredienti / INCI</label><textarea id="inci">Aqua, Glycerin, Cocos Nucifera Oil, Butyrospermum Parkii Butter, Parfum, Tocopherol, Limonene</textarea>
  <label>Modo d'uso</label><input id="uso" value="Applicare su pelle pulita mattina e sera.">
  <label>Avvertenze</label><input id="avv" value="Evitare il contatto con gli occhi. Tenere fuori dalla portata dei bambini.">
  <label>Responsabile immissione sul mercato</label><input id="resp" value="Nome Srl, Via Esempio 1, 00000 Città (IT)">
  <label>Lotto / origine</label><input id="lotto" value="Lotto: vedi fondo · Made in Italy">
  <label>Colori</label><div class="row"><div><small>Sfondo</small><input type="color" id="bg"></div><div><small>Accento</small><input type="color" id="accent"></div><div><small>Testo</small><input type="color" id="ink"></div></div>
  <div class="chk"><input type="checkbox" id="guides" checked><label for="guides" style="margin:0;text-transform:none;font-weight:500;color:var(--fg)">Mostra guide (fustella, abbondanza, area sicura)</label></div>
  <div class="help">Le guide si nascondono automaticamente nei file scaricati. Il PDF usa la stampa del browser: imposta "margini: nessuno" e "sfondo: sì". Per la tipografia, l'SVG aperto in Illustrator resta la via più sicura (vedi guida).</div>
</aside>
<main><div class="grid" id="grid"></div></main>
</div>
<div id="printbox"></div>
<script>
const TPL = __TPL__;
const SC = __SC__;
const $ = s => document.querySelector(s);
const esc = s => s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
let style = 'minimal';
function setColorsFromStyle(){ const [bg,ac,ink] = SC[style]; $('#bg').value=bg; $('#accent').value=ac; $('#ink').value=ink; }
setColorsFromStyle();
function wrapLines(text, maxChars){ const out=[]; let line=''; for (const w of text.split(/\s+/)){ if((line+' '+w).trim().length>maxChars){ out.push(line.trim()); line=w; } else line=(line+' '+w); } if(line.trim()) out.push(line.trim()); return out; }
function render(t, forDownload){
  const [bg0,ac0,ink0] = SC[t.style];
  let s = t.svg;
  // colori
  const bg=$('#bg').value, ac=$('#accent').value, ink=$('#ink').value;
  if (bg!==bg0) s = s.split(bg0).join(bg);
  if (ac!==ac0) s = s.split(ac0).join(ac);
  if (ink!==ink0) s = s.split(ink0).join(ink);
  // testi
  const brand=esc($('#brand').value||' '), prod=esc($('#product').value||' '), claim=esc($('#claim').value||' ');
  const qty=esc(($('#qty').value||'').trim()+' '+$('#emark').value).trim();
  s = s.replace(/>NOME BRAND</g, '>'+brand+'<').replace(/>Nome Prodotto</g, '>'+prod+'<').replace(/>claim breve · funzione</g, '>'+claim+'<').replace(/>50 ml ℮</g, '>'+qty+'<');
  // blocco retro (solo avvolgenti): sostituisco le 5 righe con righe a capo automatico
  const lines = [...wrapLines('INGREDIENTI / INCI: '+$('#inci').value, 78), ...wrapLines("MODO D'USO: "+$('#uso').value, 78), ...wrapLines('AVVERTENZE: '+$('#avv').value, 78), ...wrapLines('Resp. immissione sul mercato: '+$('#resp').value, 78), $('#lotto').value];
  const m = s.match(/<text x="([\d.]+)" y="([\d.]+)" font-family="([^"]+)" font-size="1.8" fill="([^"]+)" xml:space="preserve">INGREDIENTI \/ INCI[^<]*<\/text>/);
  if (m){
    const x=m[1], y0=parseFloat(m[2]), ff=m[3], fill=m[4];
    s = s.replace(/<text x="[\d.]+" y="[\d.]+" font-family="[^"]+" font-size="1.8" fill="[^"]+" xml:space="preserve">(INGREDIENTI \/ INCI|MODO D'USO|AVVERTENZE|Responsabile immissione|Lotto:)[^<]*<\/text>\s*/g, '');
    const block = lines.map((ln,i)=>`<text x="${x}" y="${(y0+i*2.6).toFixed(2)}" font-family="${ff}" font-size="1.8" fill="${fill}" xml:space="preserve">${esc(ln)}</text>`).join('');
    s = s.replace('<g id="TESTI"', block.length ? '<g id="TESTI"' : '<g id="TESTI"').replace(/(<g id="TESTI"[^>]*>)/, '$1'+block);
    // sposta l'area "testi aggiuntivi" sotto il blocco
    const yb = y0 + lines.length*2.6 + 1;
    s = s.replace(/<rect x="([\d.]+)" y="[\d.]+" width="([\d.]+)" height="([\d.]+)" fill="none" stroke="#9e9e9e" stroke-width="0.1" stroke-dasharray="0.5 0.5"\/>/, (a,x1,w1,h1)=>`<rect x="${x1}" y="${yb.toFixed(2)}" width="${w1}" height="${Math.max(3, parseFloat(h1)-(lines.length-5)*2.6).toFixed(2)}" fill="none" stroke="#9e9e9e" stroke-width="0.1" stroke-dasharray="0.5 0.5"/>`);
    s = s.replace(/<text x="([\d.]+)" y="[\d.]+" font-family="([^"]+)" font-size="1.5" fill="#9e9e9e">area testi aggiuntivi/, (a,x1,ff1)=>`<text x="${x1}" y="${(yb+2.5).toFixed(2)}" font-family="${ff1}" font-size="1.5" fill="#9e9e9e">area testi aggiuntivi`);
  }
  // guide
  const hide = forDownload || !$('#guides').checked;
  if (hide) for (const id of ['AREA_SICURA','ABBONDANZA','NOTE']) s = s.replace(`<g id="${id}"`, `<g id="${id}" style="display:none"`);
  if (!forDownload) s = s.replace(/width="[\d.]+mm" height="[\d.]+mm"/, 'width="100%" height="100%"');
  return s;
}
function draw(){
  const g=$('#grid'); g.innerHTML='';
  TPL.filter(t=>t.style===style).forEach(t=>{
    const c=document.createElement('div'); c.className='card';
    c.innerHTML=`<div class="pv">${render(t,false)}</div><div class="t">${t.title}</div><div class="m">${(t.w-6).toFixed(0)} × ${(t.h-6).toFixed(0)} mm + 3 mm abbondanza · ${t.style}</div><div class="b"><button data-a="svg">SVG</button><button data-a="pdf">PDF</button></div>`;
    c.querySelector('[data-a=svg]').onclick=()=>dl(t); c.querySelector('[data-a=pdf]').onclick=()=>pdf(t);
    g.appendChild(c);
  });
}
function fileName(t){ return ($('#brand').value||'brand').toLowerCase().replace(/[^a-z0-9]+/g,'-')+'_'+t.id+'_'+t.style; }
function dl(t){ const s='<?xml version="1.0" encoding="UTF-8"?>\n'+render(t,true); const b=new Blob([s],{type:'image/svg+xml'}); const a=document.createElement('a'); a.href=URL.createObjectURL(b); a.download=fileName(t)+'.svg'; a.click(); }
function pdf(t){ const box=$('#printbox'); box.innerHTML=render(t,true); let st=document.getElementById('pp'); if(!st){st=document.createElement('style');st.id='pp';document.head.appendChild(st);} st.textContent=`@page{size:${t.w}mm ${t.h}mm;margin:0}`; setTimeout(()=>{window.print(); box.innerHTML='';},50); }
$('#dlall').onclick=()=>{ TPL.filter(t=>t.style===style).forEach((t,i)=>setTimeout(()=>dl(t), i*250)); };
document.querySelectorAll('#style button').forEach(b=>b.onclick=()=>{ document.querySelectorAll('#style button').forEach(x=>x.classList.remove('on')); b.classList.add('on'); style=b.dataset.v; setColorsFromStyle(); draw(); });
document.querySelectorAll('aside input, aside textarea, aside select').forEach(el=>el.addEventListener('input', draw));
draw();
</script></body></html>'''
html = html.replace("__FONTCSS__", fontcss).replace("__TPL__", json.dumps(tpls, ensure_ascii=False)).replace("__SC__", json.dumps(STYLE_COLORS))
open(os.path.join(OUT, "index.html"), "w").write(html)
print("editor:", len(html)//1024, "KB,", len(tpls), "template")
