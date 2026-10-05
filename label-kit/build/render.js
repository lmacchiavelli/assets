const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
const ROOT = path.resolve(__dirname, '..'); const H = path.join(__dirname, 'html');
const OUT_M = path.join(ROOT, 'mockup'), OUT_L = path.join(ROOT, 'listing'); fs.mkdirSync(OUT_M, {recursive:true}); fs.mkdirSync(OUT_L, {recursive:true});
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  const pdf = async (name, out) => { await p.goto('file://' + path.join(H, name), {waitUntil:'networkidle'}); await p.pdf({ path: out, format: 'A4', printBackground: true, margin: {top:'18mm',bottom:'18mm',left:'16mm',right:'16mm'} }); };
  await pdf('guida.html', path.join(ROOT, 'guida-esportazione-tipografia.pdf'));
  await pdf('checklist.html', path.join(ROOT, 'checklist-conformita-etichetta.pdf'));
  const shot = async (name, out, w, h) => { await p.setViewportSize({width:w, height:h}); await p.goto('file://' + path.join(H, name), {waitUntil:'networkidle'}); await p.screenshot({ path: out, clip:{x:0,y:0,width:w,height:h} }); };
  for (const f of fs.readdirSync(H).filter(f => f.startsWith('mockup-'))) await shot(f, path.join(OUT_M, f.replace('.html', '.png')), 1200, 900);
  await shot('hero.html', path.join(OUT_L, '01-hero.png'), 2000, 1500);
  await shot('livelli.html', path.join(OUT_L, '02-livelli.png'), 2000, 1500);
  await shot('stili.html', path.join(OUT_L, '04-tre-stili.png'), 2000, 1500);
  await pdf('guida-en.html', path.join(ROOT, 'print-export-guide-EN.pdf'));
  await pdf('checklist-en.html', path.join(ROOT, 'label-compliance-checklist-EN.pdf'));
  await shot('prima-dopo.html', path.join(OUT_L, '03-prima-dopo.png'), 2000, 1500);
  await b.close(); console.log('render ok');
})();
