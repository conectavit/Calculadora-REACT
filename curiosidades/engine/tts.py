# Gera a narração de cada cena com voz neural pt-BR e grava voz/durs.js
# uso: python3 tts.py [voz] [velocidade]
import asyncio, json, os, subprocess, sys, edge_tts
VOICE = sys.argv[1] if len(sys.argv) > 1 else "pt-BR-AntonioNeural"
RATE = sys.argv[2] if len(sys.argv) > 2 else "+10%"
here = os.path.dirname(os.path.abspath(__file__)); out = os.path.join(here, "voz"); os.makedirs(out, exist_ok=True)
falas = json.loads(subprocess.check_output(["node", "-e", "process.stdout.write(JSON.stringify(require('./falas.js').FALAS))"], cwd=here))
proxy = os.environ.get("HTTPS_PROXY")
async def one(vid, i, txt):
    f = f"{out}/v{vid}_{i:02d}.mp3"
    for tent in range(4):
        try:
            await edge_tts.Communicate(txt, VOICE, rate=RATE, proxy=proxy).save(f); break
        except Exception as e:
            print("retry", vid, i, e); await asyncio.sleep(2 + tent * 3)
    d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))
    return round(d, 3)
async def main():
    durs = {}
    for vid, lst in falas.items():
        durs[vid] = [await one(vid, i, t) for i, t in enumerate(lst)]
        print(vid, durs[vid], round(sum(durs[vid]), 1))
    open(f"{out}/durs.js", "w").write("var VOZ = " + json.dumps(durs) + ";\nif (typeof module !== 'undefined') module.exports = { VOZ };\n")
asyncio.run(main())
