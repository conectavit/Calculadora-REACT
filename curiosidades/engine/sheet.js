// node sheet.js <outdir> [ids]  -> contact sheet com cada cena em ~2.6s
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [out, ids = '1,2,3,4,5,6,7,8,9,10'] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  for (const id of ids.split(',')) {
    await p.goto('file://' + path.resolve(__dirname, 'player.html') + '?v=' + id);
    await p.evaluate(() => document.fonts.ready);
    const info = await p.evaluate(() => window.__info);
    let i = 0;
    for (const s of info.scenes) {
      await p.evaluate(t => window.__render(t), s.start + Math.min(s.dur - 0.5, 3.2));
      await p.screenshot({ path: `${out}/s${id}_${i++}.png` });
    }
    console.log(id, info.total.toFixed(1) + 's');
  }
  await b.close();
})();
