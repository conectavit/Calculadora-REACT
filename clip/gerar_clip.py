"""
Gera o clip "A Calculadora Feliz" (formato Shorts 1080x1920) com música
infantil original sintetizada e letra em estilo karaokê.

Uso:  python3 clip/gerar_clip.py   ->  clip/calculadora_feliz_shorts.mp4
Requer: numpy, Pillow, ffmpeg
"""
import math
import os
import subprocess
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_WAV = os.path.join(HERE, "musica_calculadora_feliz.wav")
OUT_MP4 = os.path.join(HERE, "calculadora_feliz_shorts.mp4")

SR = 44100
BPM = 120
BEAT = 60 / BPM
BAR = 4 * BEAT
W, H, FPS = 1080, 1920, 30

# ----------------------------------------------------------------- música
NOTE = {n: i for i, n in enumerate("C C# D D# E F F# G G# A A# B".split())}


def freq(name):
    pitch, octave = name[:-1], int(name[-1])
    midi = 12 * (octave + 1) + NOTE[pitch]
    return 440 * 2 ** ((midi - 69) / 12)


# Cada linha: lista de (sílaba, nota, duração em tempos). 8 tempos = 2 compassos.
VERSO_MELODIA = [
    (["C4", "E4", "G4", "A4", "G4", "E4"], [1, 1, 2, 1, 1, 2]),
    (["F4", "F4", "A4", "G4", "G4", "E4", "D4"], [.5, .5, 1, .5, .5, 1, 4]),
    (["E4", "E4", "E4", "F4", "G4", "A4", "C5"], [.5, .5, .5, .5, 1, 1, 4]),
    (["C5", "A4", "A4", "G4", "E4", "D4", "D4", "C4"], [1, .5, .5, 1, 1, .5, .5, 3]),
]
REFRAO_MELODIA = [
    (["G4", "E4", "G4", "E4", "F4", "G4", "A4"], [1, 1, 1, 1, 1, 1, 2]),
    (["G4", "F4", "E4", "D4", "E4", "F4", "E4", "D4"], [1, .5, .5, 1, 1, 1, 1, 2]),
    (["C5", "B4", "A4", "A4", "G4", "A4", "B4", "C5"], [1, .5, .5, 1, 1, 1, 1, 2]),
    (["G4", "A4", "B4", "C5", "A4", "G4", "E4", "D4", "C4"], [.5, .5, .5, 1.5, .5, .5, 1, 1, 2]),
]

VERSO1 = [
    ["Um ", "mais ", "um, ", "quan", "to ", "dá?"],
    ["A", "per", "ta o ", "bo", "tão ", "pra ", "ver!"],
    ["Na ", "cal", "cu", "la", "do", "ra, ", "plim!"],
    ["Dois ", "a", "pa", "re", "ce ", "pra ", "vo", "cê!"],
]
VERSO2 = [
    ["Dois ", "mais ", "dois, ", "quan", "to ", "dá?"],
    ["Vem ", "con", "tar ", "co", "mi", "go, ", "vem!"],
    ["Na ", "cal", "cu", "la", "do", "ra, ", "plim!"],
    ["Qua", "tro a", "pa", "re", "ce, ", "o", "ba, ", "olé!"],
]
REFRAO = [
    ["Con", "ta, ", "con", "ta, ", "sem ", "pa", "rar,"],
    ["nú", "me", "ros ", "pra ", "gen", "te ", "brin", "car!"],
    ["Mais, ", "me", "nos, ", "ve", "zes, ", "di", "vi", "dir,"],
    ["a ", "ma", "te", "má", "ti", "ca ", "faz ", "sor", "rir!"],
]

# Estrutura: (nome, letra, melodia, acordes por compasso, cor de fundo)
SECOES = [
    ("intro", None, None, ["C", "G"]),
    ("verso1", VERSO1, VERSO_MELODIA, ["C", "Am", "F", "G", "C", "F", "F", "C"]),
    ("verso2", VERSO2, VERSO_MELODIA, ["C", "Am", "F", "G", "C", "F", "F", "C"]),
    ("refrao", REFRAO, REFRAO_MELODIA, ["C", "F", "C", "G", "Am", "G", "F", "G"]),
    ("outro", None, None, ["C", "C"]),
]

CHORDS = {
    "C": ["C3", "E3", "G3", "C4"], "F": ["F3", "A3", "C4", "F4"],
    "G": ["G3", "B3", "D4", "G4"], "Am": ["A3", "C4", "E4", "A4"],
}
ROOT = {"C": "C2", "F": "F2", "G": "G2", "Am": "A2"}

# Linha do tempo: sílabas (para karaokê) e acordes
silabas = []      # (t_inicio, t_fim, idx_linha_global, idx_silaba, nota)
linhas = []       # (t_inicio, t_fim, [sílabas], secao)
acordes = []      # (t_inicio, nome)
secoes_t = []     # (t_inicio, t_fim, nome)
t = 0.0
for nome, letra, mel, chs in SECOES:
    t0 = t
    for i, c in enumerate(chs):
        acordes.append((t0 + i * BAR, c))
    if letra:
        for li, (sil, (notas, durs)) in enumerate(zip(letra, mel)):
            assert len(sil) == len(notas) == len(durs) and sum(durs) == 8, (nome, li)
            lt = t0 + li * 2 * BAR
            linhas.append((lt, lt + 2 * BAR, sil, nome))
            tt = lt
            for si, (n, d) in enumerate(zip(notas, durs)):
                silabas.append((tt, tt + d * BEAT, len(linhas) - 1, si, n))
                tt += d * BEAT
    t = t0 + len(chs) * BAR
    secoes_t.append((t0, t, nome))
DUR = t + 1.0


def env(n, a, r_len):
    e = np.ones(n)
    na = min(int(a * SR), n)
    e[:na] = np.linspace(0, 1, na)
    nr = min(int(r_len * SR), n)
    e[n - nr:] *= np.linspace(1, 0, nr)
    return e


def toy_piano(f, dur):
    n = int((dur + 0.4) * SR)
    tt = np.arange(n) / SR
    s = (np.sin(2 * np.pi * f * tt) + 0.35 * np.sin(2 * np.pi * 2 * f * tt)
         + 0.12 * np.sin(2 * np.pi * 3.01 * f * tt) + 0.08 * np.sin(2 * np.pi * 4.2 * f * tt) * np.exp(-tt * 12))
    vib = 1 + 0.004 * np.sin(2 * np.pi * 5.5 * tt)
    s2 = 0.5 * np.sin(2 * np.pi * f * vib * tt)  # flauta suave sustentada
    decay = np.exp(-tt * 3.2)
    sustain = np.clip(1 - tt / (dur + 0.35), 0, 1)
    return (s * decay * 0.6 + s2 * sustain * 0.5) * env(n, 0.005, 0.12)


def karplus(f, dur, bright=0.5):
    n = int(dur * SR)
    p = max(2, int(SR / f))
    rng = np.random.default_rng(int(f * 100))
    buf = rng.uniform(-1, 1, p)
    out = np.empty(n)
    for i in range(n):
        out[i] = buf[i % p]
        buf[i % p] = 0.996 * (bright * buf[i % p] + (1 - bright) * 0.5 * (buf[i % p] + buf[(i + 1) % p]))
    return out * env(n, 0.002, 0.05)


def bass(f, dur):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * 2 * f * tt)
    return s * np.exp(-tt * 2.5) * env(n, 0.005, 0.05)


def kick():
    n = int(0.35 * SR)
    tt = np.arange(n) / SR
    fr = 50 + 110 * np.exp(-tt * 30)
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-tt * 9)


def clap():
    n = int(0.25 * SR)
    tt = np.arange(n) / SR
    rng = np.random.default_rng(1)
    noise = rng.uniform(-1, 1, n)
    noise = np.convolve(noise, [1, -0.9], "same")
    return noise * np.exp(-tt * 22) * 0.6


def shaker():
    n = int(0.08 * SR)
    tt = np.arange(n) / SR
    rng = np.random.default_rng(2)
    noise = np.diff(rng.uniform(-1, 1, n + 1))
    return noise * np.exp(-tt * 60) * 0.25


def sparkle():
    out = np.zeros(int(1.2 * SR))
    for k, nm in enumerate(["C6", "E6", "G6", "C7"]):
        s = toy_piano(freq(nm), 0.3) * 0.5
        st = int(k * 0.07 * SR)
        out[st:st + len(s)] += s[:len(out) - st]
    return out


def gerar_audio():
    mix = np.zeros(int((DUR + 2) * SR))
    lead = np.zeros_like(mix)
    ritmo = np.zeros_like(mix)

    def add(buf, sig, t0, g=1.0):
        i = int(t0 * SR)
        j = min(len(buf), i + len(sig))
        buf[i:j] += g * sig[:j - i]

    for (t0, t1, _, _, n) in silabas:
        add(lead, toy_piano(freq(n), t1 - t0), t0, 0.55)
    # "plim!" e o resultado ganham um brilho
    for (t0, t1, li, si, n) in silabas:
        if "plim" in linhas[li][2][si]:
            add(lead, sparkle(), t0 + 0.5, 0.35)
    # intro e outro: melodia "plim plim"
    intro_mel = [("G4", 0, 1), ("E4", 1, 1), ("C5", 2, 2), ("G4", 4, 1), ("A4", 5, 1), ("B4", 6, 1), ("C5", 7, 1)]
    for nm, b, d in intro_mel:
        add(lead, toy_piano(freq(nm), d * BEAT), b * BEAT, 0.45)
    out_t = secoes_t[-1][0]
    for nm, b, d in [("C5", 0, 1), ("G4", 1, 1), ("E4", 2, 1), ("C5", 3, 5)]:
        add(lead, toy_piano(freq(nm), d * BEAT), out_t + b * BEAT, 0.45)
    add(lead, sparkle(), out_t + 3 * BEAT, 0.4)

    cache = {}
    for idx, (t0, c) in enumerate(acordes):
        ultimo = idx == len(acordes) - 1
        add(ritmo, bass(freq(ROOT[c]), BEAT * (4 if ultimo else 1.9)), t0, 0.55)
        if not ultimo:
            add(ritmo, bass(freq(ROOT[c]) * 1.5, BEAT * 1.9), t0 + 2 * BEAT, 0.4)
        # ukulele: batida em 1, 2, 2.5, 3.5, 4
        batidas = [0] if ultimo else [0, 1, 1.5, 2.5, 3]
        for b in batidas:
            for k, nm in enumerate(CHORDS[c]):
                key = (nm, 0.6)
                if key not in cache:
                    cache[key] = karplus(freq(nm), 0.9 if not ultimo else 2.5)
                add(ritmo, cache[key], t0 + b * BEAT + k * 0.012, 0.13)
        if not ultimo:
            for b in range(4):
                if b in (0, 2):
                    add(ritmo, kick(), t0 + b * BEAT, 0.7)
                else:
                    add(ritmo, clap(), t0 + b * BEAT, 0.45)
            for b in range(8):
                add(ritmo, shaker(), t0 + b * BEAT / 2, 1.0 if b % 2 else 0.6)

    mix = lead + ritmo * 0.8
    # pequeno eco no lead
    d = int(0.375 * SR)
    eco = np.zeros_like(lead)
    eco[d:] = lead[:-d] * 0.22
    mix += eco
    mix = mix[:int(DUR * SR)]
    mix *= env(len(mix), 0.01, 0.8)
    mix = np.tanh(mix / (np.max(np.abs(mix)) * 0.75)) * 0.9
    st = np.stack([mix, np.roll(mix, int(0.004 * SR)) * 0.97], 1)
    with wave.open(OUT_WAV, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((st * 32767).astype("<i2").tobytes())


# ----------------------------------------------------------------- vídeo
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_TITLE = ImageFont.truetype(BOLD, 84)
F_SUB = ImageFont.truetype(BOLD, 44)
F_LYR = ImageFont.truetype(BOLD, 64)
F_NEXT = ImageFont.truetype(BOLD, 42)
F_BTN = ImageFont.truetype(BOLD, 70)
F_DISP = ImageFont.truetype(BOLD, 96)
F_BIG = ImageFont.truetype(BOLD, 150)

LAYOUT = [["x", "/", "c", "0"], ["7", "8", "9", "-"], ["4", "5", "6", "+"], ["1", "2", "3", "="]]
PALETAS = {
    "intro": ((255, 214, 230), (190, 225, 255)),
    "verso1": ((255, 236, 179), (255, 196, 214)),
    "verso2": ((200, 245, 210), (180, 215, 255)),
    "refrao": ((225, 205, 255), (255, 205, 225)),
    "outro": ((255, 214, 230), (190, 225, 255)),
}

# Eventos da calculadora: (tempo, botão, texto no visor, efeito)
eventos = []
for (t0, t1, li, si, n) in silabas:
    lt0, lt1, sil, sec = linhas[li]
    linha_sec = [l for l in linhas if l[3] == sec].index(linhas[li])
    if sec in ("verso1", "verso2"):
        num = "1" if sec == "verso1" else "2"
        res = "2" if sec == "verso1" else "4"
        if linha_sec == 0 and si == 0:
            eventos.append((t0, num, num, None))
        elif linha_sec == 0 and si == 1:
            eventos.append((t0, "+", num + "+", None))
        elif linha_sec == 0 and si == 2:
            eventos.append((t0, num, f"{num}+{num}", None))
        elif linha_sec == 2 and si == 6:
            eventos.append((t0, "=", res, "boom"))
    elif sec == "refrao":
        if linha_sec == 0 and si in (0, 2, 4, 6):
            d = str((si // 2) + 1)
            eventos.append((t0, d, "1234"[: (si // 2) + 1], None))
        elif linha_sec == 1 and si in (0, 2, 4, 6):
            d = "5678"[si // 2]
            eventos.append((t0, d, d, None))
        elif linha_sec == 2:
            m = {0: "+", 1: "-", 3: "x", 5: "/"}
            if si in m:
                eventos.append((t0, m[si], m[si], None))
        elif linha_sec == 3 and si == 8:
            eventos.append((t0, "=", ":)", "boom"))
eventos.append((secoes_t[-1][0] + 3 * BEAT, "c", "0", "boom"))
eventos.sort()


def estado_calc(t):
    disp, botao, tb, boom = "0", None, -9, -9
    for (te, b, d, fx) in eventos:
        if te <= t:
            disp, botao, tb = d, b, te
            if fx:
                boom = te
    return disp, botao, t - tb, t - boom


def grad(c1, c2):
    y = np.linspace(0, 1, H)[:, None, None]
    a = np.array(c1)[None, None, :] * (1 - y) + np.array(c2)[None, None, :] * y
    return np.broadcast_to(a, (H, W, 3)).astype(np.uint8)


GRADS = {k: grad(*v) for k, v in PALETAS.items()}


def secao_em(t):
    for (a, b, n) in secoes_t:
        if a <= t < b:
            return n, a, b
    return "outro", secoes_t[-1][0], secoes_t[-1][1]


def fundo(t):
    nome, a, b = secao_em(t)
    base = GRADS[nome].astype(np.float32)
    if t - a < 0.6 and a > 0:
        prev = [s for s in secoes_t if s[1] == a][0][2]
        k = (t - a) / 0.6
        base = GRADS[prev] * (1 - k) + base * k
    return Image.fromarray(base.astype(np.uint8))


rng = np.random.default_rng(7)
PARTICULAS = [dict(x=rng.uniform(0, W), y=rng.uniform(0, H), v=rng.uniform(40, 110),
                   s=rng.uniform(26, 56), tipo=rng.choice(["nota", "estrela", "num"]),
                   ch=str(rng.integers(0, 10)), fase=rng.uniform(0, 6.28),
                   cor=tuple(int(c) for c in rng.choice([[255, 255, 255], [255, 170, 200], [120, 200, 255], [255, 220, 120]])))
              for _ in range(22)]


def estrela(d, cx, cy, r, cor, rot=0.0):
    pts = []
    for k in range(10):
        ang = rot + k * math.pi / 5 - math.pi / 2
        rr = r if k % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=cor)


def nota_musical(d, x, y, s, cor):
    d.ellipse([x, y + s * 0.7, x + s * 0.55, y + s * 1.05], fill=cor)
    d.rectangle([x + s * 0.45, y, x + s * 0.55, y + s * 0.9], fill=cor)
    d.polygon([(x + s * 0.55, y), (x + s * 0.95, y + s * 0.25), (x + s * 0.55, y + s * 0.35)], fill=cor)


def texto_centro(d, cx, y, txt, font, fill, stroke=0, stroke_fill=None):
    w = d.textlength(txt, font=font)
    d.text((cx - w / 2, y), txt, font=font, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)


def desenhar(t):
    img = fundo(t)
    d = ImageDraw.Draw(img, "RGBA")
    batida = (t / BEAT) % 1
    pulso = math.exp(-batida * 6)

    for p in PARTICULAS:
        y = (p["y"] - p["v"] * t) % (H + 100) - 50
        x = p["x"] + 30 * math.sin(t * 1.3 + p["fase"])
        c = p["cor"] + (150,)
        if p["tipo"] == "nota":
            nota_musical(d, x, y, p["s"], c)
        elif p["tipo"] == "estrela":
            estrela(d, x, y, p["s"] * 0.5, c, t + p["fase"])
        else:
            d.text((x, y), p["ch"], font=ImageFont.truetype(BOLD, int(p["s"] * 1.2)), fill=c)

    # título
    tb = 6 * math.sin(t * 2 * math.pi / (BEAT * 2))
    texto_centro(d, W / 2, 110 + tb, "A Calculadora", F_TITLE, (255, 255, 255), 8, (255, 110, 160))
    texto_centro(d, W / 2, 205 + tb, "Feliz!", F_TITLE, (255, 230, 90), 8, (255, 110, 160))

    # calculadora personagem
    disp, botao, dtb, dboom = estado_calc(t)
    bounce = 18 * pulso
    tilt = 4 * math.sin(t * math.pi / BEAT)
    cw, ch = 640, 860
    cx, cy = W / 2 + tilt * 3, 360 + bounce
    x0, y0 = cx - cw / 2, cy
    # pernas e braços
    for lx in (x0 + 170, x0 + cw - 210):
        d.rounded_rectangle([lx, y0 + ch - 20, lx + 40, y0 + ch + 70 - bounce], 18, fill=(90, 90, 120))
        d.ellipse([lx - 30, y0 + ch + 50 - bounce, lx + 70, y0 + ch + 100 - bounce], fill=(255, 110, 160))
    braco = 40 * math.sin(t * math.pi / BEAT)
    d.line([(x0 + 10, y0 + 420), (x0 - 90, y0 + 330 - braco)], fill=(90, 90, 120), width=26)
    d.ellipse([x0 - 130, y0 + 290 - braco, x0 - 50, y0 + 370 - braco], fill=(255, 255, 255), outline=(90, 90, 120), width=8)
    d.line([(x0 + cw - 10, y0 + 420), (x0 + cw + 90, y0 + 330 + braco)], fill=(90, 90, 120), width=26)
    d.ellipse([x0 + cw + 50, y0 + 290 + braco, x0 + cw + 130, y0 + 370 + braco], fill=(255, 255, 255), outline=(90, 90, 120), width=8)
    # corpo (cores do app)
    d.rounded_rectangle([x0 + 12, y0 + 16, x0 + cw + 12, y0 + ch + 16], 60, fill=(0, 0, 0, 40))
    d.rounded_rectangle([x0, y0, x0 + cw, y0 + ch], 60, fill=(255, 255, 255), outline=(205, 205, 205), width=14)
    # rosto
    piscar = (t % 3.7) < 0.12
    feliz = dboom < 1.2
    for ex in (cx - 120, cx + 120):
        if piscar:
            d.line([(ex - 32, y0 + 95), (ex + 32, y0 + 95)], fill=(50, 50, 80), width=10)
        elif feliz:
            d.arc([ex - 36, y0 + 70, ex + 36, y0 + 130], 200, 340, fill=(50, 50, 80), width=12)
        else:
            d.ellipse([ex - 30, y0 + 62, ex + 30, y0 + 128], fill=(50, 50, 80))
            d.ellipse([ex - 12, y0 + 72, ex + 6, y0 + 92], fill=(255, 255, 255))
    d.ellipse([cx - 210, y0 + 120, cx - 160, y0 + 150], fill=(255, 160, 190, 170))
    d.ellipse([cx + 160, y0 + 120, cx + 210, y0 + 150], fill=(255, 160, 190, 170))
    boca = 40 if feliz else 26 + 10 * pulso
    d.chord([cx - 60, y0 + 108 - boca / 3, cx + 60, y0 + 120 + boca], 0, 180, fill=(220, 70, 110))
    # visor
    vx0, vy0, vx1, vy1 = x0 + 50, y0 + 190, x0 + cw - 50, y0 + 320
    d.rounded_rectangle([vx0, vy0, vx1, vy1], 20, fill=(170, 170, 255))
    fd = F_DISP
    tw = d.textlength(disp, font=fd)
    if dboom < 0.5:
        fd = ImageFont.truetype(BOLD, int(96 + 40 * (1 - dboom / 0.5)))
        tw = d.textlength(disp, font=fd)
    d.text((vx1 - 30 - tw, (vy0 + vy1) / 2 - fd.size * 0.6), disp, font=fd, fill=(255, 255, 255))
    # botões
    bx0, by0 = x0 + 50, y0 + 350
    bw, bh, gap = (cw - 100 - 3 * 18) / 4, 105, 18
    for r, row in enumerate(LAYOUT):
        for c, lab in enumerate(row):
            px, py = bx0 + c * (bw + gap), by0 + r * (bh + gap)
            ativo = lab == botao and dtb < 0.35
            cor = (255, 200, 60) if ativo else (0, 170, 240)
            off = 8 if ativo else 0
            d.rounded_rectangle([px, py + 8, px + bw, py + bh + 8], 22, fill=(0, 120, 180) if not ativo else (220, 150, 20))
            d.rounded_rectangle([px, py + off, px + bw, py + bh + off], 22, fill=cor)
            lw = d.textlength(lab, font=F_BTN)
            d.text((px + bw / 2 - lw / 2, py + off + 10), lab, font=F_BTN, fill=(255, 255, 255))

    # explosão de estrelas no resultado
    if 0 <= dboom < 1.4:
        k = dboom / 1.4
        for i in range(14):
            ang = i * 2 * math.pi / 14
            rr = 150 + 520 * k
            estrela(d, cx + rr * math.cos(ang), y0 + 255 + rr * math.sin(ang) * 0.9,
                    40 * (1 - k) + 8, (255, 220, 80, int(255 * (1 - k))), ang + t * 3)
        texto_centro(d, W / 2, 1080 - 60 * k, "PLIM!", F_BIG, (255, 255, 255, int(255 * (1 - k))), 10,
                     (255, 110, 160, int(255 * (1 - k))))

    # karaokê
    ky = 1440
    d.rounded_rectangle([50, ky - 40, W - 50, ky + 320], 50, fill=(255, 255, 255, 200))
    atual = None
    for i, (a, b, sil, sec) in enumerate(linhas):
        if a - 0.25 <= t < b - 0.25:
            atual = i
    nome, _, _ = secao_em(t)
    if atual is None:
        if nome == "intro":
            conta = int(t / BEAT) % 4 + 1 if t > BAR else None
            texto_centro(d, W / 2, ky + 20, "Vamos cantar e contar?", F_LYR, (255, 110, 160))
            if conta:
                texto_centro(d, W / 2, ky + 130, " ".join(str(i) for i in range(1, conta + 1)), F_BIG, (0, 170, 240))
        else:
            texto_centro(d, W / 2, ky + 40, "Tchau, tchau!", F_LYR, (255, 110, 160))
            texto_centro(d, W / 2, ky + 150, "Até a próxima conta! :)", F_NEXT, (0, 150, 220))
        return img
    a, b, sil, sec = linhas[atual]
    rotulo = {"verso1": "1 + 1", "verso2": "2 + 2", "refrao": "Refrão"}[sec]
    texto_centro(d, W / 2, ky - 10, rotulo, F_NEXT, (180, 140, 220))
    texto = "".join(sil)
    total = d.textlength(texto, font=F_LYR)
    escala = min(1.0, (W - 160) / total)
    fl = F_LYR if escala >= 1 else ImageFont.truetype(BOLD, int(64 * escala))
    total = d.textlength(texto, font=fl)
    x = W / 2 - total / 2
    sil_t = [s for s in silabas if s[2] == atual]
    for si, s in enumerate(sil):
        st0 = sil_t[si][0]
        cantada = t >= st0
        agora = st0 <= t < sil_t[si][1]
        dy = -14 * math.exp(-(t - st0) * 8) if agora else 0
        cor = (255, 110, 160) if cantada else (120, 120, 150)
        d.text((x, ky + 60 + dy), s, font=fl, fill=cor, stroke_width=3 if cantada else 0,
               stroke_fill=(255, 255, 255))
        x += d.textlength(s, font=fl)
    if atual + 1 < len(linhas):
        texto_centro(d, W / 2, ky + 190, "".join(linhas[atual + 1][2]), F_NEXT, (150, 150, 175))
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
        if i % 300 == 0:
            print(f"quadro {i}/{n}", flush=True)
    proc.stdin.close()
    proc.wait()


if __name__ == "__main__":
    import sys
    gerar_audio()
    print(f"áudio pronto: {DUR:.1f}s")
    if "--preview" in sys.argv:
        for tt in [1, 5, 9.6, 12.5, 37, 44, 50, 55]:
            desenhar(tt).save(os.path.join(HERE, f"preview_{tt}.png"))
    else:
        gerar_video()
        print("vídeo pronto:", OUT_MP4)
