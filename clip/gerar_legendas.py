"""
Gera as legendas (.srt) da letra cantada dos dois clips, no tempo exato de cada frase.

Uso:  python3 clip/gerar_legendas.py
      -> clip/calculadora_feliz_shorts.srt e clip/vogais_shorts.srt
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gerar_clip  # noqa: E402
import gerar_clip_vogais  # noqa: E402


def ts(seg):
    ms = int(round(seg * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def legendas(mod, extras, destino):
    inis = [max(0, [s[0] for s in mod.silabas if s[2] == i][0] - 0.15) for i in range(len(mod.linhas))]
    blocos = []
    for i, (a, b, sil, sec) in enumerate(mod.linhas):
        fim = min(b, inis[i + 1] - 0.05) if i + 1 < len(inis) else b
        blocos.append((inis[i], fim, "".join(sil).strip()))
    blocos += extras
    blocos.sort()
    with open(destino, "w", encoding="utf-8") as f:
        for n, (a, b, txt) in enumerate(blocos, 1):
            f.write(f"{n}\n{ts(a)} --> {ts(b)}\n{txt}\n\n")
    print(destino, len(blocos), "legendas")


if __name__ == "__main__":
    c, v = gerar_clip, gerar_clip_vogais
    legendas(c, [(0.3, c.secoes_t[0][1] - 0.2, "♪ Vamos contar até 10? ♪"),
                 (c.secoes_t[-1][0], c.DUR - 0.2, "♪ Chegamos ao 10! Tchau, tchau! ♪")],
             os.path.join(HERE, "calculadora_feliz_shorts.srt"))
    legendas(v, [(0.3, v.secoes_t[0][1] - 0.2, "♪ Vamos cantar as vogais? ♪"),
                 (v.secoes_t[-1][0], v.DUR - 0.2, "♪ Agora você sabe as vogais! Tchau, tchau! ♪")],
             os.path.join(HERE, "vogais_shorts.srt"))
