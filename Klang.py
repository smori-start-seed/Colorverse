# Klang.py – Das Colorverse wird hoerbar
# Der Farbsatz der MetaSphere wird zu einem Akkord:
# der Hue gibt den Grundton, die Harmonie die Konsonanz,
# der Drift den Triton, die Stoerimpulse das Rauschen.
import math
import struct
import wave
from config import *

SR = 22050


# ============================================================
#  AKKORD
# ============================================================

def _akkord(engine):
    hue = engine.metasphere.hue_avg
    uni = engine.universe

    grund = KLANG_MIN_FREQ + (hue % 360.0) / 360.0 * (KLANG_MAX_FREQ - KLANG_MIN_FREQ)

    stimmen = [
        (grund, 0.30),
        (grund * 1.5, 0.20 * uni.harmonie),
        (grund * 1.26, 0.15 * (1.0 - uni.harmonie)),
        (grund * 1.414, 0.15 * uni.drift),
    ]
    return stimmen


# ============================================================
#  ERZEUGEN
# ============================================================

def erzeuge(engine, dauer=None, datei=None):
    if not ENABLE_KLANG:
        return None

    dauer = dauer if dauer is not None else KLANG_DAUER
    datei = datei if datei is not None else KLANG_DATEI
    if datei and not datei.endswith(".wav"):
        datei += ".wav"

    stimmen = _akkord(engine)
    n = int(SR * dauer)
    samples = [0.0] * n

    for freq, st in stimmen:
        w = 2.0 * math.pi * freq / SR
        for i in range(n):
            samples[i] += st * math.sin(w * i)

    stoer = engine.harmonie_feld["stoerimpulse"]
    for i in range(n):
        samples[i] += (stoer * 0.05) * (math.sin(2.0 * math.pi * 7.0 * i / SR) * math.sin(2.0 * math.pi * 0.25 * i / SR))

    maximum = max(1e-6, max(abs(s) for s in samples))
    lautstaerke = 0.6 * min(1.0, engine.universe.energy + 0.3)
    faktor = lautstaerke / maximum

    with wave.open(datei, "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SR)
        f.writeframes(b"".join(
            struct.pack("<h", int(max(-1.0, min(1.0, s * faktor)) * 32767))
            for s in samples
        ))

    return datei
