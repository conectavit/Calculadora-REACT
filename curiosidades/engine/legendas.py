# Gera legendas .srt (do que a narração fala) para cada vídeo, com tempo por palavra.
# uso: python3 legendas.py <saidaDir>
import asyncio, json, os, subprocess, sys, edge_tts
here = os.path.dirname(os.path.abspath(__file__)); outroot = sys.argv[1]
VOICE, RATE, LEAD, MAXW = "pt-BR-AntonioNeural", "+10%", 0.2, 5
d = json.loads(subprocess.check_output(["node", "-e", """
const {VIDEOS,timeline}=require('./data.js');const {FALAS}=require('./falas.js');
process.stdout.write(JSON.stringify(VIDEOS.map(v=>({id:v.id,slug:v.slug,starts:timeline(v).map(c=>c.start),falas:FALAS[v.id]}))))"""], cwd=here))
proxy = os.environ.get("HTTPS_PROXY")
def ts(s):
    ms = int(round(s * 1000)); return f"{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}"
async def words(txt):
    for tent in range(4):
        try:
            ws = []
            async for ch in edge_tts.Communicate(txt, VOICE, rate=RATE, proxy=proxy, boundary="WordBoundary").stream():
                if ch["type"] == "WordBoundary":
                    ws.append((ch["offset"] / 1e7, (ch["offset"] + ch["duration"]) / 1e7, ch["text"]))
            return ws
        except Exception as e:
            print("retry", e); await asyncio.sleep(3)
async def main():
    for v in d:
        cues = []
        for start, txt in zip(v["starts"], v["falas"]):
            ws = await words(txt)
            # junta palavras em blocos curtos, quebrando também em pontuação
            toks = txt.split(); chunk = []
            for i, (a, b, w) in enumerate(ws):
                chunk.append((a, b, toks[i] if len(toks) == len(ws) else w))
                last = chunk[-1][2]
                if len(chunk) >= MAXW or last[-1] in ".,!?:…" or i == len(ws) - 1:
                    cues.append([start + LEAD + chunk[0][0], start + LEAD + chunk[-1][1], " ".join(c[2] for c in chunk)]); chunk = []
        for i in range(len(cues) - 1):  # sem sobreposição, sem buracos curtos
            if cues[i+1][0] - cues[i][1] < 0.3: cues[i][1] = cues[i+1][0] - 0.01
        srt = "".join(f"{i+1}\n{ts(a)} --> {ts(b)}\n{t}\n\n" for i, (a, b, t) in enumerate(cues))
        p = os.path.join(outroot, v["slug"], v["slug"] + ".srt"); open(p, "w").write(srt)
        print(v["id"], len(cues), "blocos")
asyncio.run(main())
