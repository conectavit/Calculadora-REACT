"""
Gera o clip "A Calculadora Feliz" (formato Shorts 1080x1920) com música
infantil original, voz cantando (sintetizada) e letra em estilo karaokê.
A música conta de 1 + 1 até 5 + 5 = 10.

Uso:  python3 clip/gerar_clip.py   ->  clip/calculadora_feliz_shorts.mp4
      python3 clip/gerar_clip.py --preview   (só áudio + alguns quadros PNG)

Requer: numpy, Pillow, ffmpeg,
        mbrola + voz brasileira br4  (apt-get install mbrola mbrola-br4)
"""
import math
import os
import subprocess
import sys
import tempfile
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_WAV = os.path.join(HERE, "musica_calculadora_feliz.wav")
OUT_MP4 = os.path.join(HERE, "calculadora_feliz_shorts.mp4")
MBROLA_VOZ = "/usr/share/mbrola/br4/br4"

SR = 44100
BPM = 120
BEAT = 60 / BPM
BAR = 4 * BEAT
W, H, FPS = 1080, 1920, 30

# ----------------------------------------------------------------- letra
NOTE = {n: i for i, n in enumerate("C C# D D# E F F# G G# A A# B".split())}


def freq(name):
    pitch, octave = name[:-1], int(name[-1])
    midi = 12 * (octave + 1) + NOTE[pitch]
    return 440 * 2 ** ((midi - 69) / 12)


# Fonemas (voz MBROLA br4) de cada sílaba; "*" marca a vogal sustentada.
FONEMAS = {
    "um": "*un", "dois": "d *o y s2", "três": "t r *e s2", "qua": "k w *a", "tro": "t r *u",
    "cin": "s *in", "co": "k *u", "seis": "s *e y s2", "oi": "*o y", "to": "t *u", "dez": "d *ee s2",
    "mais": "m *a y s2", "quan": "k w *an", "dá": "d *a",
    "va": "v *a", "mos": "m *u z", "a": "*a", "per": "p *e r", "tar": "t *a r2", "pra": "p r *a",
    "ver": "v *e r2", "vem": "v *en", "con": "k *on", "mi": "m *i", "go": "g *u",
    "ba": "b *a", "te": "t *i", "pal": "p *a w", "ma": "m *a", "bem": "b *en", "fe": "f *e",
    "liz": "l *i s2", "pu": "p *u", "la": "l *a", "mui": "m *u y", "mãos": "m *an w s2",
    "ci": "s *i", "can": "k *an", "na": "n *a", "cal": "k *a w", "cu": "k *u", "do": "d *o",
    "ra": "r *a", "plim": "p l *in", "pa": "p *a", "re": "r *ee", "ce": "s *i", "vo": "v *o",
    "cê": "s *e", "ta": "t *a", "sem": "s *en", "rar": "r *a r2", "nú": "n *u", "me": "m *e",
    "ros": "r *u s2", "gen": "j *en", "brin": "b r *in", "car": "k *a r2", "nos": "n *u s2",
    "ve": "v *e", "zes": "z *i s2", "di": "d *i", "vi": "v *i", "dir": "d *i r2",
    "má": "m *a", "ti": "t *i", "ca": "k *a", "faz": "f *a s2", "sor": "s *o", "rir": "rr *i r2",
}

NUMERO = {1: ["Um"], 2: ["Dois"], 3: ["Três"], 4: ["Qua", "tro"], 5: ["Cin", "co"],
          6: ["Seis"], 8: ["Oi", "to"], 10: ["Dez"]}
LINHA2 = {
    1: ["Va", "mos ", "a", "per", "tar ", "pra ", "ver!"],
    2: ["Vem ", "con", "tar ", "co", "mi", "go, ", "vem!"],
    3: ["Ba", "te ", "pal", "ma, ", "bem ", "fe", "liz!"],
    4: ["Pu", "la, ", "pu", "la, ", "mui", "to ", "bem!"],
    5: ["Mãos ", "pra ", "ci", "ma, ", "vem ", "can", "tar!"],
}

# Melodias: (notas, durações em tempos); cada "vaga" pode ter 1 ou 2 sílabas
MEL_V = [
    (["C4", "E4", "G4", "A4", "G4", "E4"], [1, 1, 2, 1, 1, 2]),
    (["F4", "F4", "A4", "G4", "G4", "E4", "D4"], [.5, .5, 1, .5, .5, 1, 4]),
    (["E4", "E4", "E4", "F4", "G4", "A4", "C5"], [.5, .5, .5, .5, 1, 1, 4]),
    (["C5", "A4", "A4", "G4", "E4", "D4", "D4", "C4"], [1, .5, .5, 1, 1, .5, .5, 3]),
]
MEL_R = [
    (["G4", "E4", "G4", "E4", "F4", "G4", "A4"], [1, 1, 1, 1, 1, 1, 2]),
    (["G4", "F4", "E4", "D4", "E4", "F4", "E4", "D4"], [1, .5, .5, 1, 1, 1, 1, 2]),
    (["C5", "B4", "A4", "A4", "G4", "A4", "B4", "C5"], [1, .5, .5, 1, 1, 1, 1, 2]),
    (["G4", "A4", "B4", "C5", "A4", "G4", "E4", "D4", "C4"], [.5, .5, .5, 1.5, .5, .5, 1, 1, 2]),
]
REFRAO = [
    [["Con"], ["ta, "], ["con"], ["ta, "], ["sem "], ["pa"], ["rar,"]],
    [["nú"], ["me"], ["ros "], ["pra "], ["gen"], ["te "], ["brin"], ["car!"]],
    [["Mais, "], ["me"], ["nos, "], ["ve"], ["zes, "], ["di"], ["vi"], ["dir,"]],
    [["a "], ["ma"], ["te"], ["má"], ["ti"], ["ca "], ["faz "], ["sor"], ["rir!"]],
]
LINHA3 = [["Na "], ["cal"], ["cu"], ["la"], ["do"], ["ra, "], ["plim!"]]


def com_fim(sil, fim):
    s = list(sil)
    s[-1] = s[-1] + fim
    return s


def verso(n):
    num, res = NUMERO[n], NUMERO[2 * n]
    return [
        [com_fim(num, " "), ["mais "], com_fim([num[0].lower()] + num[1:], ", "), ["quan"], ["to "], ["dá?"]],
        [[s] for s in LINHA2[n]],
        LINHA3,
        [com_fim(res, " "), ["a"], ["pa"], ["re"], ["ce "], ["pra "], ["vo"], ["cê!"]],
    ]


VERSO_ACORDES = ["C", "Am", "F", "G", "C", "F", "F", "C"]
REFRAO_ACORDES = ["C", "F", "C", "G", "Am", "G", "F", "G"]
SECOES = [("intro", None, None, ["C", "G"])]
for n in range(1, 6):
    SECOES.append((f"verso{n}", verso(n), MEL_V, VERSO_ACORDES))
    if n in (2, 4):
        SECOES.append(("refrao", REFRAO, MEL_R, REFRAO_ACORDES))
SECOES.append(("outro", None, None, ["C", "G", "C", "C"]))

CHORDS = {
    "C": ["C3", "E3", "G3", "C4"], "F": ["F3", "A3", "C4", "F4"],
    "G": ["G3", "B3", "D4", "G4"], "Am": ["A3", "C4", "E4", "A4"],
}
ROOT = {"C": "C2", "F": "F2", "G": "G2", "Am": "A2"}

# Linha do tempo
silabas = []      # (t_inicio, t_fim, idx_linha, idx_silaba, nota)
linhas = []       # (t_inicio, t_fim, [sílabas], secao)
acordes = []      # (t_inicio, nome)
secoes_t = []     # (t_inicio, t_fim, nome)
t = 0.0
for nome, letra, mel, chs in SECOES:
    t0 = t
    for i, c in enumerate(chs):
        acordes.append((t0 + i * BAR, c))
    if letra:
        for li, (vagas, (notas, durs)) in enumerate(zip(letra, mel)):
            assert len(vagas) == len(notas) == len(durs) and sum(durs) == 8, (nome, li)
            lt = t0 + li * 2 * BAR
            sil = [s for v in vagas for s in v]
            linhas.append((lt, lt + 2 * BAR, sil, nome))
            tt, si = lt, 0
            for v, n, d in zip(vagas, notas, durs):
                for s in v:
                    dd = d / len(v)
                    silabas.append((tt, tt + dd * BEAT, len(linhas) - 1, si, n))
                    tt += dd * BEAT
                    si += 1
    t = t0 + len(chs) * BAR
    secoes_t.append((t0, t, nome))
DUR = t + 1.0


def chave(s):
    return s.strip(" ,!?").lower()


# ----------------------------------------------------------------- voz
CONS_MS = {"p": 70, "t": 70, "k": 75, "b": 60, "d": 55, "g": 60, "f": 90, "v": 65, "s": 95,
           "z": 70, "j": 85, "m": 70, "n": 65, "l": 60, "r": 35, "rr": 90, "w": 45, "y": 45,
           "s2": 90, "r2": 50}


def gerar_voz(silabas=None, linhas=None, fonemas=None):
    """Monta um arquivo .pho (fonema, duração, curva de altura) e sintetiza com MBROLA."""
    silabas = silabas if silabas is not None else globals()["silabas"]
    linhas = linhas if linhas is not None else globals()["linhas"]
    fonemas = fonemas or FONEMAS
    itens = []
    for (t0, t1, li, si, n) in silabas:
        fon = fonemas[chave(linhas[li][2][si])].split()
        k = [i for i, p in enumerate(fon) if p.startswith("*")][0]
        onset = [(p, CONS_MS[p] / 1000) for p in fon[:k]]
        coda = [(p, CONS_MS[p] / 1000) for p in fon[k + 1:]]
        itens.append(dict(t0=t0, t1=t1, f=freq(n), onset=onset, vogal=fon[k][1:], coda=coda,
                          fim_linha=si == len(linhas[li][2]) - 1))
    segs = []  # (fonema, inicio, fim, f0)
    for i, it in enumerate(itens):
        on_dur = sum(d for _, d in it["onset"])
        ts = it["t0"] - on_dur
        for p, d in it["onset"]:
            segs.append((p, ts, ts + d, it["f"]))
            ts += d
        prox = itens[i + 1] if i + 1 < len(itens) else None
        roubo = sum(d for _, d in prox["onset"]) if prox and abs(prox["t0"] - it["t1"]) < 1e-6 else 0
        respiro = 0.14 if it["fim_linha"] else 0.0
        cod_dur = sum(d for _, d in it["coda"])
        v_fim = max(it["t0"] + 0.05, it["t1"] - roubo - respiro - cod_dur)
        segs.append((it["vogal"], it["t0"], v_fim, it["f"]))
        ts = v_fim
        for p, d in it["coda"]:
            segs.append((p, ts, ts + d, it["f"]))
            ts += d
    linhas_pho = []
    cursor = 0.0
    for (p, a, b, f) in segs:
        if a - cursor > 0.005:
            linhas_pho.append(f"_ {int(round((a - cursor) * 1000))}")
        a = max(a, cursor)
        dur = b - a
        if dur <= 0.01:
            continue
        ms = int(round(dur * 1000))
        pts = []
        npt = max(2, int(dur / 0.04))
        for j in range(npt + 1):
            x = j / npt
            tl = x * dur
            sc = 2 ** (-0.8 / 12 * math.exp(-tl / 0.05))           # pequena "escorregada" na nota
            vib = 1 + 0.012 * math.sin(2 * math.pi * 5.6 * tl) * min(1, max(0, (tl - 0.25) / 0.3))
            pts.append(f"{x * 100:.0f} {f * sc * vib:.1f}")
        linhas_pho.append(f"{p} {ms} " + " ".join(pts))
        cursor = a + ms / 1000
    linhas_pho.append("_ 500")
    with tempfile.TemporaryDirectory() as td:
        pho, w16, w44 = (os.path.join(td, x) for x in ("voz.pho", "voz16.wav", "voz44.wav"))
        open(pho, "w").write("_ 1\n" + "\n".join(linhas_pho) + "\n")
        subprocess.run(["mbrola", "-e", MBROLA_VOZ, pho, w16], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", w16, "-ar", str(SR), "-ac", "1", w44], check=True)
        with wave.open(w44) as w:
            v = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float64) / 32768
    return v


# ----------------------------------------------------------------- instrumentos
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
    s2 = 0.5 * np.sin(2 * np.pi * f * vib * tt)
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
    noise = np.random.default_rng(1).uniform(-1, 1, n)
    noise = np.convolve(noise, [1, -0.9], "same")
    return noise * np.exp(-tt * 22) * 0.6


def shaker():
    n = int(0.08 * SR)
    tt = np.arange(n) / SR
    noise = np.diff(np.random.default_rng(2).uniform(-1, 1, n + 1))
    return noise * np.exp(-tt * 60) * 0.25


def sparkle():
    out = np.zeros(int(1.2 * SR))
    for k, nm in enumerate(["C6", "E6", "G6", "C7"]):
        s = toy_piano(freq(nm), 0.3) * 0.5
        st = int(k * 0.07 * SR)
        out[st:st + len(s)] += s[:len(out) - st]
    return out


def reverb(x):
    out = x.copy()
    for d_ms, g in [(31, .32), (47, .27), (73, .22), (109, .17), (151, .12), (211, .08), (293, .05)]:
        d = int(d_ms / 1000 * SR)
        out[d:] += x[:-d] * g
    return out


def gerar_audio():
    total = int((DUR + 2) * SR)
    lead = np.zeros(total)
    ritmo = np.zeros(total)

    def add(buf, sig, t0, g=1.0):
        i = int(t0 * SR)
        j = min(len(buf), i + len(sig))
        buf[i:j] += g * sig[:j - i]

    for (t0, t1, _, _, n) in silabas:
        add(lead, toy_piano(freq(n), t1 - t0), t0, 0.28)
    for (t0, t1, li, si, n) in silabas:
        if "plim" in linhas[li][2][si]:
            add(lead, sparkle(), t0 + 0.5, 0.35)
    for nm, b, d in [("G4", 0, 1), ("E4", 1, 1), ("C5", 2, 2), ("G4", 4, 1), ("A4", 5, 1), ("B4", 6, 1), ("C5", 7, 1)]:
        add(lead, toy_piano(freq(nm), d * BEAT), b * BEAT, 0.45)
    out_t = secoes_t[-1][0]
    for nm, b, d in [("C5", 0, 1), ("G4", 1, 1), ("E4", 2, 1), ("C5", 3, 2), ("E5", 8, 1), ("D5", 9, 1),
                     ("B4", 10, 1), ("C5", 11, 5)]:
        add(lead, toy_piano(freq(nm), d * BEAT), out_t + b * BEAT, 0.45)
    add(lead, sparkle(), out_t + 11 * BEAT, 0.4)

    cache = {}
    for idx, (t0, c) in enumerate(acordes):
        ultimo = idx == len(acordes) - 1
        add(ritmo, bass(freq(ROOT[c]), BEAT * (4 if ultimo else 1.9)), t0, 0.55)
        if not ultimo:
            add(ritmo, bass(freq(ROOT[c]) * 1.5, BEAT * 1.9), t0 + 2 * BEAT, 0.4)
        for b in ([0] if ultimo else [0, 1, 1.5, 2.5, 3]):
            for k, nm in enumerate(CHORDS[c]):
                key = (nm, ultimo)
                if key not in cache:
                    cache[key] = karplus(freq(nm), 2.5 if ultimo else 0.9)
                add(ritmo, cache[key], t0 + b * BEAT + k * 0.012, 0.13)
        if not ultimo:
            for b in range(4):
                add(ritmo, kick() if b in (0, 2) else clap(), t0 + b * BEAT, 0.7 if b in (0, 2) else 0.45)
            for b in range(8):
                add(ritmo, shaker(), t0 + b * BEAT / 2, 1.0 if b % 2 else 0.6)

    voz = gerar_voz()
    voz = voz / (np.max(np.abs(voz)) + 1e-9)
    vbuf = np.zeros(total)
    vbuf[:min(total, len(voz))] = voz[:total]
    vbuf = reverb(vbuf)
    vbuf /= np.max(np.abs(vbuf))

    instr = lead + ritmo * 0.8
    d = int(0.375 * SR)
    instr[d:] += lead[:-d] * 0.2
    instr /= np.max(np.abs(instr))
    mix = 0.62 * instr + 0.75 * vbuf
    mix = mix[:int(DUR * SR)]
    mix *= env(len(mix), 0.01, 0.8)
    mix = np.tanh(mix / (np.max(np.abs(mix)) * 0.8)) * 0.9
    st = np.stack([mix, np.roll(mix, int(0.004 * SR)) * 0.97], 1)
    with wave.open(OUT_WAV, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((st * 32767).astype("<i2").tobytes())


# ----------------------------------------------------------------- vídeo
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
_fontes = {}


def fonte(tam):
    tam = int(tam)
    if tam not in _fontes:
        _fontes[tam] = ImageFont.truetype(BOLD, tam)
    return _fontes[tam]


F_TITLE, F_LYR, F_NEXT, F_BTN, F_DISP, F_BIG = (fonte(s) for s in (84, 64, 42, 70, 96, 150))

LAYOUT = [["x", "/", "c", "0"], ["7", "8", "9", "-"], ["4", "5", "6", "+"], ["1", "2", "3", "="]]
CORES_VERSO = [((255, 236, 179), (255, 196, 214)), ((200, 245, 210), (180, 215, 255)),
               ((255, 220, 190), (210, 200, 255)), ((190, 240, 240), (255, 220, 180)),
               ((255, 205, 205), (255, 245, 170))]
PALETAS = {"intro": ((255, 214, 230), (190, 225, 255)), "refrao": ((225, 205, 255), (255, 205, 225)),
           "outro": ((255, 214, 230), (190, 225, 255))}
for i, c in enumerate(CORES_VERSO):
    PALETAS[f"verso{i + 1}"] = c

# Eventos da calculadora: (tempo, botão, texto no visor, efeito, resultado alcançado)
eventos = []
for (t0, t1, li, si, n) in silabas:
    lt0, lt1, sil, sec = linhas[li]
    linha_sec = [l for l in linhas if l[0] >= [s for s in secoes_t if s[0] <= lt0 < s[1]][0][0]
                 and l[3] == sec].index(linhas[li])
    if sec.startswith("verso"):
        k = int(sec[5:])
        nl = len(NUMERO[k])
        if linha_sec == 0 and si == 0:
            eventos.append((t0, str(k), str(k), None, None))
        elif linha_sec == 0 and si == nl:
            eventos.append((t0, "+", f"{k}+", None, None))
        elif linha_sec == 0 and si == nl + 1:
            eventos.append((t0, str(k), f"{k}+{k}", None, None))
        elif linha_sec == 2 and si == 6:
            eventos.append((t0, "=", str(2 * k), "boom", 2 * k))
    elif sec == "refrao":
        if linha_sec == 0 and si in (0, 2, 4, 6):
            eventos.append((t0, str(si // 2 + 1), "1234"[: si // 2 + 1], None, None))
        elif linha_sec == 1 and si in (0, 2, 4, 6):
            d = "5678"[si // 2]
            eventos.append((t0, d, d, None, None))
        elif linha_sec == 2:
            m = {0: "+", 1: "-", 3: "x", 5: "/"}
            if si in m:
                eventos.append((t0, m[si], m[si], None, None))
        elif linha_sec == 3 and si == 8:
            eventos.append((t0, "=", ":)", "boom", None))
eventos.append((secoes_t[-1][0] + 11 * BEAT, "c", "10", "boom", 10))
eventos.sort(key=lambda e: e[0])


def estado_calc(t):
    disp, botao, tb, boom, alcan = "0", None, -9, -9, 0
    for (te, b, d, fx, r) in eventos:
        if te <= t:
            disp, botao, tb = d, b, te
            if fx:
                boom = te
            if r:
                alcan = max(alcan, r)
    return disp, botao, t - tb, t - boom, alcan


def grad(c1, c2):
    y = np.linspace(0, 1, H)[:, None, None]
    a = np.array(c1)[None, None, :] * (1 - y) + np.array(c2)[None, None, :] * y
    return np.broadcast_to(a, (H, W, 3)).astype(np.uint8)


GRADS = {k: grad(*v) for k, v in PALETAS.items()}


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
    texto_centro(d, W / 2, 80 + tb, "A Calculadora", F_TITLE, (255, 255, 255), 8, (255, 110, 160))
    texto_centro(d, W / 2, 175 + tb, "Feliz!", F_TITLE, (255, 230, 90), 8, (255, 110, 160))

    disp, botao, dtb, dboom, alcan = estado_calc(t)

    # trilha de 1 a 10
    r0, sp = 34, 96
    sx = W / 2 - 4.5 * sp
    for k in range(1, 11):
        px, py = sx + (k - 1) * sp, 320
        on = k <= alcan
        rr = r0 + (8 * math.exp(-max(0, dboom) * 4) if on and k == alcan else 0)
        d.ellipse([px - rr, py - rr, px + rr, py + rr], fill=(255, 200, 60) if on else (255, 255, 255, 150),
                  outline=(255, 110, 160) if on else (200, 200, 220), width=5)
        ft = fonte(30 if k == 10 else 36)
        texto_centro(d, px, py - ft.size * 0.62, str(k), ft, (255, 255, 255) if on else (170, 170, 200))

    bounce = 18 * pulso
    tilt = 4 * math.sin(t * math.pi / BEAT)
    cw, ch = 640, 860
    cx = W / 2 + tilt * 3
    x0, y0 = cx - cw / 2, 410 + bounce
    for lx in (x0 + 170, x0 + cw - 210):
        d.rounded_rectangle([lx, y0 + ch - 20, lx + 40, y0 + ch + 60 - bounce], 18, fill=(90, 90, 120))
        d.ellipse([lx - 30, y0 + ch + 40 - bounce, lx + 70, y0 + ch + 90 - bounce], fill=(255, 110, 160))
    braco = 40 * math.sin(t * math.pi / BEAT)
    for lado in (-1, 1):
        bx = x0 + 10 if lado < 0 else x0 + cw - 10
        hx = bx + lado * 100
        hy = y0 + 330 + lado * braco
        d.line([(bx, y0 + 420), (hx, hy)], fill=(90, 90, 120), width=26)
        d.ellipse([hx - 40, hy - 40, hx + 40, hy + 40], fill=(255, 255, 255), outline=(90, 90, 120), width=8)
    d.rounded_rectangle([x0 + 12, y0 + 16, x0 + cw + 12, y0 + ch + 16], 60, fill=(0, 0, 0, 40))
    d.rounded_rectangle([x0, y0, x0 + cw, y0 + ch], 60, fill=(255, 255, 255), outline=(205, 205, 205), width=14)

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
    # boca abre e fecha com a voz
    cantando = any(s[0] <= t < s[1] - 0.06 for s in silabas)
    abert = 0
    if cantando:
        s = [s for s in silabas if s[0] <= t < s[1]][0]
        abert = 20 + 22 * math.exp(-(t - s[0]) * 5)
    if cantando:
        d.ellipse([cx - 45, y0 + 112, cx + 45, y0 + 125 + abert], fill=(220, 70, 110))
        d.ellipse([cx - 22, y0 + 112 + abert * 0.6, cx + 22, y0 + 122 + abert], fill=(255, 140, 160))
    else:
        boca = 40 if feliz else 26 + 10 * pulso
        d.chord([cx - 60, y0 + 108 - boca / 3, cx + 60, y0 + 120 + boca], 0, 180, fill=(220, 70, 110))

    vx0, vy0, vx1, vy1 = x0 + 50, y0 + 190, x0 + cw - 50, y0 + 320
    d.rounded_rectangle([vx0, vy0, vx1, vy1], 20, fill=(170, 170, 255))
    fd = F_DISP if dboom >= 0.5 else fonte(96 + 40 * (1 - dboom / 0.5))
    tw = d.textlength(disp, font=fd)
    d.text((vx1 - 30 - tw, (vy0 + vy1) / 2 - fd.size * 0.6), disp, font=fd, fill=(255, 255, 255))
    bx0, by0 = x0 + 50, y0 + 350
    bw, bh, gap = (cw - 100 - 3 * 18) / 4, 105, 18
    for r, row in enumerate(LAYOUT):
        for c, lab in enumerate(row):
            px, py = bx0 + c * (bw + gap), by0 + r * (bh + gap)
            ativo = lab == botao and dtb < 0.35
            off = 8 if ativo else 0
            d.rounded_rectangle([px, py + 8, px + bw, py + bh + 8], 22, fill=(220, 150, 20) if ativo else (0, 120, 180))
            d.rounded_rectangle([px, py + off, px + bw, py + bh + off], 22, fill=(255, 200, 60) if ativo else (0, 170, 240))
            lw = d.textlength(lab, font=F_BTN)
            d.text((px + bw / 2 - lw / 2, py + off + 10), lab, font=F_BTN, fill=(255, 255, 255))

    if 0 <= dboom < 1.4:
        k = dboom / 1.4
        for i in range(14):
            ang = i * 2 * math.pi / 14
            rr = 150 + 520 * k
            estrela(d, cx + rr * math.cos(ang), y0 + 255 + rr * math.sin(ang) * 0.9,
                    40 * (1 - k) + 8, (255, 220, 80, int(255 * (1 - k))), ang + t * 3)
        texto_centro(d, W / 2, 1130 - 60 * k, "PLIM!", F_BIG, (255, 255, 255, int(255 * (1 - k))), 10,
                     (255, 110, 160, int(255 * (1 - k))))

    # karaokê
    ky = 1480
    d.rounded_rectangle([50, ky - 40, W - 50, ky + 310], 50, fill=(255, 255, 255, 200))
    atual = None
    for i, (a, b, sil, sec) in enumerate(linhas):
        if a - 0.25 <= t < b - 0.25:
            atual = i
    nome = secoes_t[secao_em(t)][2]
    if atual is None:
        if nome == "intro":
            conta = int(t / BEAT) % 4 + 1 if t > BAR else None
            texto_centro(d, W / 2, ky + 20, "Vamos contar até 10?", F_LYR, (255, 110, 160))
            if conta:
                texto_centro(d, W / 2, ky + 120, " ".join(str(i) for i in range(1, conta + 1)), F_BIG, (0, 170, 240))
        else:
            texto_centro(d, W / 2, ky + 30, "Chegamos ao 10!", F_LYR, (255, 110, 160))
            texto_centro(d, W / 2, ky + 140, "Tchau, tchau! Até a próxima conta! :)", F_NEXT, (0, 150, 220))
        return img
    a, b, sil, sec = linhas[atual]
    if sec.startswith("verso"):
        k = int(sec[5:])
        rotulo = f"{k} + {k}" + (f" = {2 * k}" if alcan >= 2 * k else "")
    else:
        rotulo = "Refrão"
    texto_centro(d, W / 2, ky - 10, rotulo, F_NEXT, (180, 140, 220))
    texto = "".join(sil)
    fl = F_LYR
    total = d.textlength(texto, font=fl)
    if total > W - 160:
        fl = fonte(64 * (W - 160) / total)
        total = d.textlength(texto, font=fl)
    x = W / 2 - total / 2
    sil_t = [s for s in silabas if s[2] == atual]
    for si, s in enumerate(sil):
        st0 = sil_t[si][0]
        cantada = t >= st0
        agora = st0 <= t < sil_t[si][1]
        dy = -14 * math.exp(-(t - st0) * 8) if agora else 0
        d.text((x, ky + 60 + dy), s, font=fl, fill=(255, 110, 160) if cantada else (120, 120, 150),
               stroke_width=3 if cantada else 0, stroke_fill=(255, 255, 255))
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
        if i % 600 == 0:
            print(f"quadro {i}/{n}", flush=True)
    proc.stdin.close()
    proc.wait()


if __name__ == "__main__":
    gerar_audio()
    print(f"áudio pronto: {DUR:.1f}s")
    if "--preview" in sys.argv:
        for tt in sys.argv[2:] or ["5", "13", "60", "118"]:
            desenhar(float(tt)).save(os.path.join(HERE, f"preview_{tt}.png"))
    else:
        gerar_video()
        print("vídeo pronto:", OUT_MP4)
