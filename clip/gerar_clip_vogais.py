"""
Gera o clip "A E I O U - As Vogais" (formato Shorts 1080x1920) com música
infantil original, voz cantando (sintetizada) e letra em estilo karaokê.
Reaproveita os instrumentos e a voz de gerar_clip.py.

Uso:  python3 clip/gerar_clip_vogais.py   ->  clip/vogais_shorts.mp4
      python3 clip/gerar_clip_vogais.py --preview 5 30 ...   (áudio + quadros PNG)
Requer: numpy, Pillow, ffmpeg, mbrola + mbrola-br4
"""
import math
import os
import subprocess
import sys
import wave

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gerar_clip as g  # noqa: E402

OUT_WAV = os.path.join(HERE, "musica_vogais.wav")
OUT_MP4 = os.path.join(HERE, "vogais_shorts.mp4")
SR, BEAT, BAR, W, H, FPS = g.SR, g.BEAT, g.BAR, g.W, g.H, g.FPS
freq, fonte, texto_centro, estrela, nota_musical = g.freq, g.fonte, g.texto_centro, g.estrela, g.nota_musical
g.CONS_MS.update({"lh": 75, "nh": 70})

# ----------------------------------------------------------------- letra
FONEMAS = {
    "a": "*a", "e": "*e", "é": "*ee", "i": "*i", "o": "*o", "u": "*u",
    "de": "d *i", "be": "b *e", "lha": "lh *a", "es": "*e s2", "tre": "t r *e", "la": "l *a",
    "vo": "v *o", "va": "v *a",
    "faz": "f *a s2", "zum": "z *un", "vai": "v *a y", "ar": "*a r2",
    "bri": "b r *i", "lá": "l *a", "no": "n *u", "céu": "s *ee w",
    "tem": "t *en", "co": "k *o", "quei": "k *e y", "ro": "r *u", "sol": "s *oo w", "mar": "m *a r2",
    "pin": "p *in", "ti": "t *i", "nho": "nh *u", "sa": "s *a", "ir": "*i r2",
    "bo": "b *o", "pro": "p r *o", "var": "v *a r2",
    "gais": "g *a y s2", "pra": "p r *a", "can": "k *an", "tar": "t *a r2",
    "vem": "v *en", "mi": "m *i", "go": "g *u", "brin": "b r *in", "car": "k *a r2",
}

VOGAIS = [
    # vogal, palavra (sílabas), segunda linha
    ("A", ["A", "be", "lha,"], ["faz ", "zum", "zum ", "e ", "vai ", "vo", "ar!"]),
    ("E", ["Es", "tre", "la,"], ["bri", "lha, ", "bri", "lha ", "lá ", "no ", "céu!"]),
    ("I", ["I", "lha,"], ["tem ", "co", "quei", "ro, ", "sol ", "e ", "mar!"]),
    ("O", ["O", "vo,"], ["o ", "pin", "ti", "nho ", "vai ", "sa", "ir!"]),
    ("U", ["U", "va,"], ["u", "va ", "bo", "a ", "de ", "pro", "var!"]),
]
PALAVRA = {"A": "Abelha", "E": "Estrela", "I": "Ilha", "O": "Ovo", "U": "Uva"}


def estrofe(v, palavra, linha2):
    base_s = [f"{v}, ", f"{v.lower()}, ", f"{v.lower()}, ", "é ", "de "]
    base_d = [1, 1, 1, .5, .5]
    base_n = ["G4", "G4", "G4", "E4", "F4"]
    pal = [palavra[0].lower()] + palavra[1:]
    pal[-1] = pal[-1] + " "
    if len(palavra) == 3:
        pd, pn = [1, 1, 2], ["G4", "A4", "G4"]
    else:
        pd, pn = [2, 2], ["A4", "G4"]
    l1 = (base_s + pal, base_n + pn, base_d + pd)
    l2 = (linha2, ["A4", "G4", "F4", "E4", "D4", "E4", "C4"], [1, .5, .5, 1, 1, 1, 3])
    return [l1, l2]


REFRAO = [
    (["A, ", "E, ", "I, ", "O, ", "U!"], ["E4", "G4", "A4", "G4", "C5"], [1, 1, 1, 1, 4]),
    (["Vo", "gais ", "pra ", "can", "tar!"], ["A4", "G4", "F4", "E4", "D4"], [1, 1, 1, 1, 4]),
    (["A, ", "E, ", "I, ", "O, ", "U!"], ["E4", "G4", "A4", "B4", "C5"], [1, 1, 1, 1, 4]),
    (["Vem ", "co", "mi", "go, ", "vem ", "brin", "car!"], ["C5", "A4", "A4", "G4", "E4", "D4", "C4"],
     [1, .5, .5, 1, 1, 1, 3]),
]


SECOES = [("intro", None, ["C", "G"]), ("refrao", REFRAO, ["C", "C", "F", "G", "Am", "C", "F", "G"])]
for v, pal, l2 in VOGAIS:
    SECOES.append((f"vogal_{v}", estrofe(v, pal, l2), ["C", "G", "F", "C"]))
SECOES.append(("refrao", REFRAO, ["C", "C", "F", "G", "Am", "C", "F", "G"]))
SECOES.append(("outro", None, ["C", "G", "C", "C"]))

silabas, linhas, acordes, secoes_t = [], [], [], []
t = 0.0
for nome, letra, chs in SECOES:
    t0 = t
    for i, c in enumerate(chs):
        acordes.append((t0 + i * BAR, c))
    if letra:
        for li, (sil, notas, durs) in enumerate(letra):
            assert len(sil) == len(notas) == len(durs) and sum(durs) == 8, (nome, li, sil)
            lt = t0 + li * 2 * BAR
            linhas.append((lt, lt + 2 * BAR, sil, nome))
            tt = lt
            for si, (n, d) in enumerate(zip(notas, durs)):
                silabas.append((tt, tt + d * BEAT, len(linhas) - 1, si, n))
                tt += d * BEAT
    t = t0 + len(chs) * BAR
    secoes_t.append((t0, t, nome))
DUR = t + 1.0

for (_, _, s, _) in linhas:
    for x in s:
        assert g.chave(x) in FONEMAS, f"sem fonemas: {x!r}"


# ----------------------------------------------------------------- áudio
def gerar_audio():
    total = int((DUR + 2) * SR)
    lead, ritmo = np.zeros(total), np.zeros(total)

    def add(buf, sig, t0, gain=1.0):
        i = int(t0 * SR)
        j = min(len(buf), i + len(sig))
        buf[i:j] += gain * sig[:j - i]

    for (t0, t1, li, si, n) in silabas:
        add(lead, g.toy_piano(freq(n), t1 - t0), t0, 0.28)
        if linhas[li][3].startswith("vogal") and si == 0:
            add(lead, g.sparkle(), t0, 0.25)
    for nm, b, d in [("C5", 0, 1), ("D5", 1, 1), ("E5", 2, 1), ("G5", 3, 1), ("A5", 4, 1), ("G5", 5, 1), ("E5", 6, 2)]:
        add(lead, g.toy_piano(freq(nm), d * BEAT), b * BEAT, 0.4)
    out_t = secoes_t[-1][0]
    for nm, b, d in [("E5", 0, 1), ("G5", 1, 1), ("A5", 2, 1), ("G5", 3, 2), ("E5", 8, 1), ("D5", 9, 1),
                     ("E5", 10, 1), ("C5", 11, 5)]:
        add(lead, g.toy_piano(freq(nm), d * BEAT), out_t + b * BEAT, 0.4)
    add(lead, g.sparkle(), out_t + 11 * BEAT, 0.4)

    cache = {}
    for idx, (t0, c) in enumerate(acordes):
        ultimo = idx == len(acordes) - 1
        add(ritmo, g.bass(freq(g.ROOT[c]), BEAT * (4 if ultimo else 1.9)), t0, 0.55)
        if not ultimo:
            add(ritmo, g.bass(freq(g.ROOT[c]) * 1.5, BEAT * 0.9), t0 + 2 * BEAT, 0.4)
            add(ritmo, g.bass(freq(g.ROOT[c]) * 2, BEAT * 0.9), t0 + 3 * BEAT, 0.3)
        for b in ([0] if ultimo else [0, .5, 1.5, 2, 3, 3.5]):
            for k, nm in enumerate(g.CHORDS[c]):
                key = (nm, ultimo)
                if key not in cache:
                    cache[key] = g.karplus(freq(nm), 2.5 if ultimo else 0.9)
                add(ritmo, cache[key], t0 + b * BEAT + k * 0.012, 0.12)
        if not ultimo:
            for b in range(4):
                add(ritmo, g.kick() if b in (0, 2) else g.clap(), t0 + b * BEAT, 0.7 if b in (0, 2) else 0.45)
            for b in range(8):
                add(ritmo, g.shaker(), t0 + b * BEAT / 2, 1.0 if b % 2 else 0.6)

    voz = g.gerar_voz(silabas, linhas, FONEMAS)
    voz = voz / (np.max(np.abs(voz)) + 1e-9)
    vbuf = np.zeros(total)
    vbuf[:min(total, len(voz))] = voz[:total]
    vbuf = g.reverb(vbuf)
    vbuf /= np.max(np.abs(vbuf))
    instr = lead + ritmo * 0.8
    d = int(0.375 * SR)
    instr[d:] += lead[:-d] * 0.2
    instr /= np.max(np.abs(instr))
    mix = (0.62 * instr + 0.75 * vbuf)[:int(DUR * SR)]
    mix *= g.env(len(mix), 0.01, 0.8)
    mix = np.tanh(mix / (np.max(np.abs(mix)) * 0.8)) * 0.9
    st = np.stack([mix, np.roll(mix, int(0.004 * SR)) * 0.97], 1)
    with wave.open(OUT_WAV, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((st * 32767).astype("<i2").tobytes())


# ----------------------------------------------------------------- vídeo
COR_VOGAL = {"A": (255, 90, 120), "E": (255, 170, 40), "I": (60, 190, 110), "O": (40, 160, 240), "U": (150, 90, 230)}
PALETAS = {
    "intro": ((255, 225, 240), (200, 230, 255)), "refrao": ((230, 210, 255), (255, 215, 230)),
    "outro": ((255, 225, 240), (200, 230, 255)),
    "vogal_A": ((255, 240, 190), (255, 205, 215)), "vogal_E": ((205, 220, 255), (240, 215, 255)),
    "vogal_I": ((200, 245, 255), (255, 240, 200)), "vogal_O": ((215, 250, 215), (255, 245, 205)),
    "vogal_U": ((240, 220, 255), (210, 250, 230)),
}
GRADS = {k: g.grad(*v) for k, v in PALETAS.items()}


def secao_em(t):
    for i, (a, b, n) in enumerate(secoes_t):
        if a <= t < b:
            return i
    return len(secoes_t) - 1


def fundo(t):
    i = secao_em(t)
    a = secoes_t[i][0]
    base = GRADS[secoes_t[i][2]]
    if t - a < 0.6 and i > 0:
        k = (t - a) / 0.6
        base = GRADS[secoes_t[i - 1][2]] * (1 - k) + base * k
    return Image.fromarray(np.asarray(base, dtype=np.uint8))


rng = np.random.default_rng(11)
PARTICULAS = [dict(x=rng.uniform(0, W), y=rng.uniform(0, H), v=rng.uniform(40, 110), s=rng.uniform(26, 56),
                   tipo=rng.choice(["nota", "estrela", "letra"]), ch="AEIOU"[int(rng.integers(0, 5))],
                   fase=rng.uniform(0, 6.28),
                   cor=tuple(int(c) for c in rng.choice([[255, 255, 255], [255, 170, 200], [120, 200, 255], [255, 220, 120]])))
              for _ in range(22)]


def silaba_atual(t):
    for s in silabas:
        if s[0] <= t < s[1]:
            return s
    return None


def boca_aberta(t, idx_linhas=None):
    s = silaba_atual(t)
    if not s or t > s[1] - 0.06 or (idx_linhas is not None and s[2] not in idx_linhas):
        return 0
    return 20 + 24 * math.exp(-(t - s[0]) * 5)


def letra_personagem(d, cx, cy, ch, tam, cor, abert, t, escala=1.0):
    """Letra gigante com olhos e boca."""
    f = fonte(tam * escala)
    w = d.textlength(ch, font=f)
    d.text((cx - w / 2 + 10, cy - f.size * 0.62 + 12), ch, font=f, fill=(0, 0, 0, 45))
    d.text((cx - w / 2, cy - f.size * 0.62), ch, font=f, fill=cor, stroke_width=int(10 * escala),
           stroke_fill=(255, 255, 255))
    s = tam * escala / 520
    ey = cy - 70 * s
    piscar = ((t + cx / 300) % 3.3) < 0.12
    for ex in (cx - 62 * s, cx + 62 * s):
        if piscar:
            d.line([(ex - 34 * s, ey), (ex + 34 * s, ey)], fill=(50, 50, 80), width=max(3, int(10 * s)))
        else:
            d.ellipse([ex - 44 * s, ey - 48 * s, ex + 44 * s, ey + 48 * s], fill=(255, 255, 255),
                      outline=(50, 50, 80), width=max(2, int(6 * s)))
            px = ex + 10 * s * math.sin(t * 2)
            d.ellipse([px - 20 * s, ey - 14 * s, px + 20 * s, ey + 26 * s], fill=(50, 50, 80))
            d.ellipse([px - 6 * s, ey - 6 * s, px + 6 * s, ey + 6 * s], fill=(255, 255, 255))
    my = cy + 30 * s
    if abert:
        d.ellipse([cx - 40 * s, my, cx + 40 * s, my + (12 + abert * 1.3) * s], fill=(200, 50, 90),
                  outline=(255, 255, 255), width=max(2, int(5 * s)))
    else:
        d.chord([cx - 50 * s, my - 25 * s, cx + 50 * s, my + 40 * s], 0, 180, fill=(200, 50, 90),
                outline=(255, 255, 255), width=max(2, int(5 * s)))
    d.ellipse([cx - 115 * s, ey + 40 * s, cx - 75 * s, ey + 62 * s], fill=(255, 150, 180, 170))
    d.ellipse([cx + 75 * s, ey + 40 * s, cx + 115 * s, ey + 62 * s], fill=(255, 150, 180, 170))


# --- ícones das palavras
def icone_abelha(d, cx, cy, t, s=1.0):
    cx += 30 * math.sin(t * 2.2)
    cy += 25 * math.sin(t * 4.4)
    flap = abs(math.sin(t * 25))
    for dx in (-40, 30):
        d.ellipse([cx + dx * s - 10 * s, cy - (110 + 30 * flap) * s, cx + (dx + 70) * s, cy - 20 * s],
                  fill=(200, 235, 255, 200), outline=(120, 170, 220), width=4)
    d.ellipse([cx - 120 * s, cy - 75 * s, cx + 120 * s, cy + 75 * s], fill=(255, 210, 40), outline=(60, 40, 20), width=6)
    for dx in (-40, 20, 75):
        d.rectangle([cx + dx * s - 14 * s, cy - 70 * s, cx + dx * s + 14 * s, cy + 70 * s], fill=(60, 40, 20))
    d.ellipse([cx - 120 * s, cy - 75 * s, cx + 120 * s, cy + 75 * s], outline=(60, 40, 20), width=6)
    d.ellipse([cx - 200 * s, cy - 70 * s, cx - 80 * s, cy + 50 * s], fill=(255, 210, 40), outline=(60, 40, 20), width=6)
    d.ellipse([cx - 165 * s, cy - 35 * s, cx - 135 * s, cy - 5 * s], fill=(40, 30, 20))
    d.arc([cx - 175 * s, cy - 10 * s, cx - 125 * s, cy + 25 * s], 20, 160, fill=(40, 30, 20), width=5)
    d.polygon([(cx + 118 * s, cy - 12 * s), (cx + 160 * s, cy), (cx + 118 * s, cy + 12 * s)], fill=(60, 40, 20))
    d.line([(cx - 160 * s, cy - 65 * s), (cx - 185 * s, cy - 115 * s)], fill=(60, 40, 20), width=5)
    d.ellipse([cx - 195 * s, cy - 125 * s, cx - 175 * s, cy - 105 * s], fill=(60, 40, 20))


def icone_estrela(d, cx, cy, t, s=1.0):
    r = 180 * s * (1 + 0.06 * math.sin(t * 6))
    for k in range(8):
        a = k * math.pi / 4 + t
        rr = 230 * s + 20 * math.sin(t * 5 + k)
        estrela(d, cx + rr * math.cos(a), cy + rr * math.sin(a), 18 * s, (255, 255, 200, 220), t * 2)
    estrela(d, cx + 8, cy + 10, r, (0, 0, 0, 40), 0.1 * math.sin(t * 2))
    estrela(d, cx, cy, r, (255, 205, 40), 0.1 * math.sin(t * 2))
    estrela(d, cx, cy, r * 0.8, (255, 225, 90), 0.1 * math.sin(t * 2))
    for ex in (cx - 40 * s, cx + 40 * s):
        d.ellipse([ex - 14 * s, cy - 30 * s, ex + 14 * s, cy + 2 * s], fill=(60, 40, 20))
    d.arc([cx - 35 * s, cy - 5 * s, cx + 35 * s, cy + 45 * s], 20, 160, fill=(60, 40, 20), width=6)


def icone_ilha(d, cx, cy, t, s=1.0):
    for k in range(3):
        y = cy + (110 + k * 30) * s
        d.arc([cx - 260 * s, y - 40 * s + 8 * math.sin(t * 3 + k), cx + 260 * s, y + 40 * s], 0, 180,
              fill=(80, 170, 240), width=10)
    d.ellipse([cx - 260 * s, cy + 40 * s, cx + 260 * s, cy + 200 * s], fill=(80, 170, 240))
    d.chord([cx - 200 * s, cy - 20 * s, cx + 200 * s, cy + 180 * s], 180, 360, fill=(250, 220, 150))
    sway = 12 * math.sin(t * 2)
    pts = [(cx - 20 * s + (sway * k / 6) + 14 * math.sin(k / 2) * s, cy + 70 * s - k * 45 * s) for k in range(7)]
    d.line(pts, fill=(150, 100, 50), width=int(30 * s), joint="curve")
    tx, ty = pts[-1]
    for a in (-160, -120, -60, -20, 200):
        ang = math.radians(a + sway)
        ex, ey = tx + 140 * s * math.cos(ang), ty + 140 * s * math.sin(ang) * 0.6 + 40 * s
        mx, my = (tx + ex) / 2, (ty + ey) / 2 - 40 * s
        d.polygon([(tx, ty), (mx - 25 * s, my), (ex, ey), (mx + 25 * s, my + 30 * s)], fill=(60, 180, 80))
    for dx in (-18, 14):
        d.ellipse([tx + dx * s - 16 * s, ty + 4 * s, tx + dx * s + 16 * s, ty + 36 * s], fill=(120, 80, 40))
    d.ellipse([cx + 130 * s, cy - 260 * s, cx + 230 * s, cy - 160 * s], fill=(255, 220, 60))


def icone_ovo(d, cx, cy, t, s=1.0, abre=0.0):
    if abre > 0:
        py = cy - 40 * s - 120 * s * min(1, abre)
        d.ellipse([cx - 80 * s, py - 70 * s, cx + 80 * s, py + 80 * s], fill=(255, 225, 60), outline=(220, 170, 20), width=5)
        for ex in (cx - 28 * s, cx + 28 * s):
            d.ellipse([ex - 10 * s, py - 20 * s, ex + 10 * s, py + 2 * s], fill=(40, 30, 20))
        d.polygon([(cx - 16 * s, py + 12 * s), (cx + 16 * s, py + 12 * s), (cx, py + 32 * s)], fill=(255, 140, 40))
    wob = 0.08 * math.sin(t * 12) if abre == 0 else 0
    pts_low = []
    for k in range(41):
        a = math.pi * k / 40
        x = cx + 140 * s * math.cos(a)
        y = cy + 40 * s + 160 * s * math.sin(a)
        pts_low.append((x + wob * (y - cy), y))
    if abre > 0:
        zig = [(cx + 140 * s - k * 28 * s, cy + 30 * s + (25 if k % 2 else -10) * s) for k in range(11)]
        d.polygon(pts_low + zig[::-1], fill=(255, 252, 240), outline=(210, 190, 160))
        top_y = cy - 120 * s - 160 * s * min(1, abre)
        d.chord([cx - 130 * s, top_y - 60 * s, cx + 130 * s, top_y + 140 * s], 180, 360, fill=(255, 252, 240),
                outline=(210, 190, 160), width=4)
    else:
        top = []
        for k in range(41):
            a = math.pi + math.pi * k / 40
            x = cx + 140 * s * math.cos(a)
            y = cy + 40 * s + 230 * s * math.sin(a)
            top.append((x + wob * (y - cy), y))
        d.polygon(top + pts_low, fill=(255, 252, 240), outline=(210, 190, 160))
        d.line([(cx - 60 * s, cy), (cx - 20 * s, cy - 30 * s), (cx + 10 * s, cy + 5 * s), (cx + 50 * s, cy - 25 * s)],
               fill=(190, 160, 120), width=4)


def icone_uva(d, cx, cy, t, s=1.0):
    sw = 6 * math.sin(t * 3)
    d.line([(cx + sw, cy - 200 * s), (cx, cy - 140 * s)], fill=(120, 80, 40), width=int(14 * s))
    d.polygon([(cx, cy - 170 * s), (cx + 110 * s, cy - 230 * s), (cx + 90 * s, cy - 150 * s)], fill=(80, 180, 80))
    rows = [5, 4, 3, 2, 1]
    r = 36 * s
    for i, n in enumerate(rows):
        for j in range(n):
            x = cx + (j - (n - 1) / 2) * 2 * r * 0.95
            y = cy - 120 * s + i * 1.7 * r + r
            d.ellipse([x - r, y - r, x + r, y + r], fill=(140, 70, 190), outline=(100, 40, 150), width=3)
            d.ellipse([x - r * 0.5, y - r * 0.6, x - r * 0.1, y - r * 0.2], fill=(210, 170, 240))


ICONES = {"A": icone_abelha, "E": icone_estrela, "I": icone_ilha, "O": icone_ovo, "U": icone_uva}


def desenhar(t):
    img = fundo(t)
    d = ImageDraw.Draw(img, "RGBA")
    pulso = math.exp(-((t / BEAT) % 1) * 6)
    for p in PARTICULAS:
        y = (p["y"] - p["v"] * t) % (H + 100) - 50
        x = p["x"] + 30 * math.sin(t * 1.3 + p["fase"])
        c = p["cor"] + (150,)
        if p["tipo"] == "nota":
            nota_musical(d, x, y, p["s"], c)
        elif p["tipo"] == "estrela":
            estrela(d, x, y, p["s"] * 0.5, c, t + p["fase"])
        else:
            d.text((x, y), p["ch"], font=fonte(p["s"] * 1.2), fill=c)

    tb = 6 * math.sin(t * 2 * math.pi / (BEAT * 2))
    titulo = "A  E  I  O  U"
    f = fonte(110)
    x = W / 2 - d.textlength(titulo, font=f) / 2
    for ch in titulo:
        if ch != " ":
            d.text((x, 60 + tb), ch, font=f, fill=COR_VOGAL[ch], stroke_width=8, stroke_fill=(255, 255, 255))
        x += d.textlength(ch, font=f)
    texto_centro(d, W / 2, 190 + tb, "As Vogais", fonte(60), (255, 255, 255), 6, (255, 110, 160))

    i_sec = secao_em(t)
    sec = secoes_t[i_sec][2]
    s0 = secoes_t[i_sec][0]
    # vogais já aprendidas
    aprendidas = {v for v in "AEIOU" for (a, b, n) in secoes_t if n == f"vogal_{v}" and t >= a}
    sp = 120
    for k, v in enumerate("AEIOU"):
        px = W / 2 + (k - 2) * sp
        on = v in aprendidas
        d.ellipse([px - 42, 300, px + 42, 384], fill=COR_VOGAL[v] if on else (255, 255, 255, 140),
                  outline=(255, 255, 255), width=5)
        texto_centro(d, px, 312, v, fonte(50), (255, 255, 255) if on else (190, 190, 210))

    abert = boca_aberta(t)
    if sec.startswith("vogal"):
        v = sec[-1]
        ent = min(1, (t - s0) / 0.4)
        esc = 0.3 + 0.7 * (1 - (1 - ent) ** 3) + 0.06 * pulso
        letra_personagem(d, 330, 720 + 14 * pulso, v, 520, COR_VOGAL[v], abert, t, esc)
        if v == "O":
            l2 = [l for l in linhas if l[3] == sec][1]
            abre = max(0, (t - (l2[0] + 1 * BEAT)) / 1.0)
            icone_ovo(d, 760, 760, t, 1.0, abre)
        else:
            ICONES[v](d, 760, 740, t, 1.0 if v != "I" else 0.95)
        # palavra com a vogal destacada
        pal = PALAVRA[v]
        f = fonte(96)
        x = W / 2 - d.textlength(pal, font=f) / 2
        for k, ch in enumerate(pal):
            cor = COR_VOGAL[v] if k == 0 else (90, 90, 130)
            d.text((x, 1110), ch, font=f, fill=cor, stroke_width=6 if k == 0 else 4, stroke_fill=(255, 255, 255))
            x += d.textlength(ch, font=f)
    elif sec == "refrao" or sec == "intro" or sec == "outro":
        s_at = silaba_atual(t)
        cantada = None
        if s_at and linhas[s_at[2]][3] == "refrao" and linhas[s_at[2]][2][0].startswith("A,"):
            cantada = s_at[3]
        for k, v in enumerate("AEIOU"):
            px = 140 + k * 200
            if sec == "intro":
                ap = (t - k * BEAT) / 0.35
                if ap <= 0:
                    continue
                esc = min(1, ap) * 0.42
            else:
                esc = 0.4
            pulo = 0
            if cantada == k:
                esc *= 1.35
                pulo = -60 * math.exp(-(t - s_at[0]) * 4)
            dance = 25 * math.sin(t * math.pi / BEAT + k * 1.2)
            ab = abert if (cantada == k or (cantada is None and abert)) else 0
            letra_personagem(d, px, 760 + dance + pulo, v, 520, COR_VOGAL[v], ab, t, esc)
        if sec == "outro":
            texto_centro(d, W / 2, 1060, "Muito bem!", fonte(110), (255, 255, 255), 10, (255, 110, 160))

    # karaokê
    ky = 1440
    d.rounded_rectangle([50, ky - 40, W - 50, ky + 330], 50, fill=(255, 255, 255, 205))
    atual = None
    for i, (a, b, sil, s_) in enumerate(linhas):
        if a - 0.25 <= t < b - 0.25:
            atual = i
    if atual is None:
        if sec == "intro":
            texto_centro(d, W / 2, ky + 40, "Vamos cantar as vogais?", fonte(64), (255, 110, 160))
            texto_centro(d, W / 2, ky + 160, "Canta junto comigo!", fonte(44), (0, 150, 220))
        else:
            texto_centro(d, W / 2, ky + 40, "Agora você sabe as vogais!", fonte(58), (255, 110, 160))
            texto_centro(d, W / 2, ky + 160, "Tchau, tchau! :)", fonte(50), (0, 150, 220))
        return img
    a, b, sil, s_ = linhas[atual]
    rotulo = "Refrão" if s_ == "refrao" else f"Vogal {s_[-1]}"
    texto_centro(d, W / 2, ky - 10, rotulo, fonte(42), (180, 140, 220))
    texto = "".join(sil)
    fl = fonte(72)
    total = d.textlength(texto, font=fl)
    if total > W - 160:
        fl = fonte(72 * (W - 160) / total)
        total = d.textlength(texto, font=fl)
    x = W / 2 - total / 2
    sil_t = [s for s in silabas if s[2] == atual]
    for si, s in enumerate(sil):
        st0 = sil_t[si][0]
        cantada = t >= st0
        agora = st0 <= t < sil_t[si][1]
        dy = -14 * math.exp(-(t - st0) * 8) if agora else 0
        cor = (255, 110, 160) if cantada else (120, 120, 150)
        eh_vogal = (s_ == "refrao" and sil[0].startswith("A,")) or (s_ != "refrao" and sil[1].startswith(sil[0][0].lower()) and si < 3)
        if eh_vogal and s.strip(" ,!").upper() in COR_VOGAL and cantada:
            cor = COR_VOGAL[s.strip(" ,!").upper()]
        d.text((x, ky + 60 + dy), s, font=fl, fill=cor, stroke_width=3 if cantada else 0, stroke_fill=(255, 255, 255))
        x += d.textlength(s, font=fl)
    if atual + 1 < len(linhas):
        texto_centro(d, W / 2, ky + 200, "".join(linhas[atual + 1][2]), fonte(44), (150, 150, 175))
    return img


def gerar_video():
    n = int(DUR * FPS)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", OUT_WAV,
           "-c:v", "libx264", "-preset", "medium", "-crf", "22", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", OUT_MP4]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        proc.stdin.write(desenhar(i / FPS).tobytes())
        if i % 600 == 0:
            print(f"quadro {i}/{n}", flush=True)
    proc.stdin.close()
    proc.wait()


if __name__ == "__main__":
    gerar_audio()
    print(f"áudio pronto: {DUR:.1f}s")
    if "--preview" in sys.argv:
        for tt in sys.argv[2:] or ["3", "12", "26", "60"]:
            desenhar(float(tt)).save(os.path.join(HERE, f"preview_vogais_{tt}.png"))
    else:
        gerar_video()
        print("vídeo pronto:", OUT_MP4)
