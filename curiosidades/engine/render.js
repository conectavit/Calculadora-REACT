// node render.js <id> <saidaDir>  -> mp4 + capa + imagens das cenas
const { chromium } = require('playwright');
const { spawn, execFileSync } = require('child_process');
const path = require('path'), fs = require('fs');
const FPS = 30;
(async () => {
  const [id, outRoot] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  const url = 'file://' + path.resolve(__dirname, 'player.html') + '?v=' + id;
  await p.goto(url); await p.evaluate(() => document.fonts.ready);
  const info = await p.evaluate(() => window.__info);
  const dir = path.join(outRoot, info.slug); fs.mkdirSync(path.join(dir, 'imagens'), { recursive: true });
  const tmp = fs.mkdtempSync('/tmp/claude-0/r');
  fs.writeFileSync(tmp + '/info.json', JSON.stringify(info));
  execFileSync('python3', [path.join(__dirname, 'music.py'), tmp + '/info.json', tmp + '/audio.wav']);
  // imagens das cenas
  for (const [i, s] of info.scenes.entries()) {
    await p.evaluate(t => window.__render(t), s.start + Math.min(s.dur - 0.45, 3.6));
    await p.screenshot({ path: `${dir}/imagens/cena-${String(i + 1).padStart(2, '0')}.png` });
  }
  // vídeo
  const frames = Math.ceil(info.total * FPS);
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-i', tmp + '/audio.wav', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p',
    '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', `${dir}/${info.slug}.mp4`], { stdio: ['pipe', 'inherit', 'inherit'] });
  const t0 = Date.now();
  for (let f = 0; f < frames; f++) {
    await p.evaluate(t => window.__render(t), f / FPS);
    const buf = await p.screenshot({ type: 'jpeg', quality: 92 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (f % 300 === 0) console.log(`[${id}] ${f}/${frames} ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r));
  // capa
  await p.goto(url + '&mode=cover'); await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: `${dir}/capa.png` });
  await b.close();
  console.log(`[${id}] pronto em ${((Date.now() - t0) / 1000).toFixed(0)}s`);
})();
