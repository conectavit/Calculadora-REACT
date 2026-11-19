// node preview.js <videoId> <t1,t2,...> <outdir>
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [id, ts, out] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.resolve(__dirname, 'player.html') + '?v=' + id);
  await p.evaluate(() => document.fonts.ready);
  const info = await p.evaluate(() => window.__info);
  console.log(JSON.stringify(info));
  for (const t of ts.split(',')) {
    await p.evaluate(t => window.__render(t), +t);
    await p.screenshot({ path: `${out}/v${id}_t${t}.png` });
  }
  await b.close();
})();
