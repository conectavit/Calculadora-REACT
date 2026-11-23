# Gera trilha original + efeitos sincronizados. uso: python3 music.py <info.json> <out.wav>
import sys, json, wave, numpy as np
SR = 44100
info = json.load(open(sys.argv[1])); out = sys.argv[2]
vid = info["id"]; total = info["total"] + 0.6
rng = np.random.default_rng(vid * 7)
N = int(total * SR); t = np.arange(N) / SR
L = np.zeros(N); R = np.zeros(N)

# estilo por vídeo: (bpm, tônica midi, progressão em graus da escala menor, brilho)
STY = {1:(96,45,[0,5,3,6]),2:(84,50,[0,3,5,4]),3:(90,47,[0,6,5,4]),4:(100,43,[0,5,6,4]),5:(88,48,[0,3,6,5]),
       6:(94,46,[0,5,3,4]),7:(104,52,[0,4,5,3]),8:(92,44,[0,1,0,6]),9:(80,49,[0,5,3,6]),10:(110,50,[0,3,4,5])}
bpm, root, prog = STY[vid]
minor = [0,2,3,5,7,8,10]
beat = 60 / bpm; bar = beat * 4
mf = lambda m: 440 * 2 ** ((m - 69) / 12)

def add(sig, start, gain=1.0, pan=0.0):
    i = int(start * SR)
    if i >= N: return
    sig = sig[:N - i]
    L[i:i+len(sig)] += sig * gain * (1 - max(pan, 0))
    R[i:i+len(sig)] += sig * gain * (1 + min(pan, 0))

def tone(f, dur, harm=6, decay=None, att=0.01):
    n = int(dur * SR); tt = np.arange(n) / SR
    s = sum(np.sin(2*np.pi*f*k*tt + k) / k**1.3 for k in range(1, harm+1))
    env = np.minimum(1, tt / att)
    env *= np.exp(-tt * decay) if decay else np.minimum(1, (dur - tt) / 0.3)
    return s * env

def chord(deg):
    return [root + 12 + minor[(deg + k) % 7] + 12 * ((deg + k) // 7) for k in (0, 2, 4)]

nb = int(total / bar) + 1
for b in range(nb):
    deg = prog[(b // 2) % 4]; c = chord(deg); s0 = b * bar
    for m in c:  # pad
        for det in (-0.12, 0.12):
            add(tone(mf(m) * 2**(det/12), bar + 0.4, harm=5, att=0.6), s0, 0.035, pan=det*4)
    for k in range(8):  # baixo em colcheias
        add(tone(mf(root - 12 + minor[deg % 7]), beat/2, harm=3, decay=7), s0 + k*beat/2, 0.16 if k % 2 == 0 else 0.09)
    arp = [c[0]+12, c[1]+12, c[2]+12, c[1]+12]
    for k in range(16):  # arpejo
        if rng.random() < 0.82:
            add(tone(mf(arp[k % 4]), 0.35, harm=4, decay=11), s0 + k*beat/4, 0.045, pan=0.5*np.sin(k))
    for k in range(4):  # bateria leve
        kt = np.arange(int(0.25*SR))/SR
        if k in (0, 2):
            add(np.sin(2*np.pi*(50 + 90*np.exp(-kt*30))*kt) * np.exp(-kt*14), s0 + k*beat, 0.5)
        else:
            sn = rng.standard_normal(len(kt)); sn = np.diff(sn, prepend=0) * np.exp(-kt*22)
            add(sn, s0 + k*beat, 0.07)
        h = np.diff(rng.standard_normal(int(0.06*SR)), prepend=0) * np.exp(-np.arange(int(0.06*SR))/SR*70)
        add(h, s0 + k*beat + beat/2, 0.05, pan=0.3)

# fade da música no início/fim + leve "duck" geral (deixa espaço p/ narração)
env = np.minimum(1, t / 1.5) * np.minimum(1, (total - t) / 1.8)
L *= env * 0.8; R *= env * 0.8

# efeitos sonoros
def whoosh(d=0.55):
    n = int(d*SR); tt = np.arange(n)/SR
    no = rng.standard_normal(n)
    k = np.ones(18)/18; no = np.convolve(no, k, 'same')  # passa-baixa
    no = np.diff(no, prepend=0) * 6
    return no * np.sin(np.pi * tt / d) ** 2
def pop():
    n = int(0.18*SR); tt = np.arange(n)/SR
    return np.sin(2*np.pi*(500 + 900*tt/0.18)*tt) * np.exp(-tt*28)
def ding():
    return tone(1318, 1.2, harm=3, decay=3.5) + 0.5*tone(1976, 1.2, harm=2, decay=4)

for i, s in enumerate(info["scenes"]):
    if i > 0: add(whoosh(), s["start"] - 0.3, 0.55)
    if s["t"] in ("stat", "hook", "like"): add(pop(), s["start"] + 0.3, 0.35)
    if s["t"] == "cta": add(ding(), s["start"] + 1.2, 0.25)
    if s["t"] == "timeline":
        n = s["n"]; step = (s["dur"] - 1.6) / n
        for k in range(n): add(pop(), s["start"] + 0.5 + k*step, 0.3)
    if s["t"] == "compare":
        for k in range(2): add(pop(), s["start"] + 0.5 + k*1.2, 0.3)

mx = max(np.abs(L).max(), np.abs(R).max())
L = np.tanh(L / mx * 1.1) * 0.89; R = np.tanh(R / mx * 1.1) * 0.89
data = (np.stack([L, R], 1) * 32767).astype(np.int16)
with wave.open(out, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(data.tobytes())
print("ok", out, round(total, 1))
