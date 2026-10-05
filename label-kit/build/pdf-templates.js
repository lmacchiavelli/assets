// Esporta ogni template SVG in PDF vettoriale alla misura esatta in mm (con abbondanza).
const { chromium } = require('playwright'); const path = require('path'), fs = require('fs');
const ROOT = path.resolve(__dirname, '..'); const T = path.join(ROOT, 'templates'), OUT = path.join(ROOT, 'templates-pdf');
const FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Inter:wght@400;600;700&family=Playfair+Display:wght@500;700&family=Josefin+Sans:wght@400;600&display=swap">';
(async () => {
  const b = await chromium.launch(); const p = await b.newPage(); let n = 0;
  for (const st of fs.readdirSync(T)) {
    fs.mkdirSync(path.join(OUT, st), { recursive: true });
    for (const f of fs.readdirSync(path.join(T, st)).filter(f => f.endswith ? false : f.endsWith('.svg'))) {
      let svg = fs.readFileSync(path.join(T, st, f), 'utf8'); svg = svg.slice(svg.indexOf('<svg'));
      const w = /width="([\d.]+)mm"/.exec(svg)[1], h = /height="([\d.]+)mm"/.exec(svg)[1];
      await p.setContent(`<!doctype html><html><head><meta charset="utf-8">${FONTS}<style>@page{size:${w}mm ${h}mm;margin:0}html,body{margin:0}svg{display:block;width:${w}mm;height:${h}mm}</style></head><body>${svg}</body></html>`, { waitUntil: 'networkidle' });
      await p.pdf({ path: path.join(OUT, st, f.replace('.svg', '.pdf')), width: `${w}mm`, height: `${h}mm`, printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } }); n++;
    }
  }
  await b.close(); console.log('pdf templates:', n);
})();
