// node engine/roteiros.js  -> gera ROTEIROS.md
const { VIDEOS, timeline } = require("./data.js");
const { FALAS } = require("./falas.js");
const clean = s => (s || "").replace(/\*/g, "");
let md = `# 10 vídeos de curiosidade: roteiros e textos de postagem

Formato: vertical 1080×1920, 30 fps, de 37 a 54 s, **com narração** (voz neural pt-BR "Antonio"), trilha original e efeitos sonoros.
Prontos para Reels, TikTok e Shorts. Cada pasta em \`saida/\` tem o **.mp4**, a **capa.jpg** (thumbnail) e as **imagens/** de cada cena (servem também para carrossel).

## Ordem sugerida de postagem
Comece pelos ganchos mais fortes: **#01 Ilha das Cobras** (tema brasileiro), **#08 Formiga zumbi** e **#05 Cleópatra**.
Depois alterne bichos (#02, #03, #04, #10) com ciência e história (#06, #07, #09).

`;
for (const v of VIDEOS) {
  const sc = timeline(v), tot = sc.reduce((a, c) => a + c.dur, 0);
  md += `---\n\n## #${String(v.id).padStart(2, "0")}: ${v.titulo}\n\n`;
  md += `**Arquivo:** \`saida/${v.slug}/${v.slug}.mp4\` · **Duração:** ${tot.toFixed(0)} s\n\n`;
  md += `| # | Tempo | Na tela | Narração |\n|---|---|---|---|\n`;
  sc.forEach((c, i) => {
    let txt = c.big ? `**${c.big}** ${clean(c.text)}` : clean(c.text);
    if (c.items) txt += " · " + c.items.map(it => `${it.e} ${it.y || it.big} ${it.l}`).join(" · ");
    if (c.sub) txt += ` _(${clean(c.sub)})_`;
    md += `| ${i + 1} | ${c.start.toFixed(1)}–${(c.start + c.dur).toFixed(1)} s | ${txt.replace(/\|/g, "/")} | ${FALAS[v.id][i]} |\n`;
  });
  md += `\n**Legenda:** ${v.legenda}\n\n**Hashtags:** ${v.hashtags}\n\n**Fontes:**\n${v.fontes.map(f => "- " + f).join("\n")}\n\n`;
}
md += `---\n\n## Como editar ou gerar de novo\n\n- Textos na tela: \`engine/data.js\` · Narração: \`engine/falas.js\` · Ilustrações: \`engine/art.js\`\n- Depois de mudar a narração: \`python3 engine/tts.py\` (opcional: \`python3 engine/tts.py pt-BR-FranciscaNeural +10%\` para voz feminina)\n- Renderizar: \`node engine/render.js <id> saida\` (ex.: \`node engine/render.js 3 saida\`)\n\nPrecisa de Node com Playwright (Chromium), Python 3 com numpy e edge-tts, e ffmpeg. A voz usa o serviço de voz neural da Microsoft (speech.platform.bing.com).\n`;
require("fs").writeFileSync(require("path").join(__dirname, "..", "ROTEIROS.md"), md);
console.log("ROTEIROS.md ok");
