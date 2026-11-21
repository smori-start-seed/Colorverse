# Terminal.py – Das Colorverse wird sichtbar (ANSI-Farben)
# Jeder Block ist eine Gruppe von Zellen: Hue, Saettigung und
# Helligkeit mischen sich zu einem Farbeindruck.
import math
from config import *


# ============================================================
#  FARBE
# ============================================================

def _rgb(hue, saturation, brightness):
    h = (hue % 360.0) / 60.0
    i = int(h) % 6
    f = h - int(h)

    c = brightness * saturation
    x = c * (1.0 - abs(f - 1.0))
    m = brightness - c

    sektoren = [
        (c, x, 0.0), (x, c, 0.0), (0.0, c, x),
        (0.0, x, c), (x, 0.0, c), (c, 0.0, x),
    ]
    r, g, b = sektoren[i]
    return int((r + m) * 255), int((g + m) * 255), int((b + m) * 255)


def _block(r, g, b):
    return f"\033[48;2;{r};{g};{b}m  \033[0m"


# ============================================================
#  ZEIGEN
# ============================================================

def zeige(engine, titel="FARB-OS"):
    if not ENABLE_KONSOLE:
        return

    n = len(engine.zellen)
    if n == 0:
        return

    anzahl = TERMINAL_BREITE * TERMINAL_HOEHE
    schritt = max(1, n // anzahl)

    zeilen = []
    for zr in range(TERMINAL_HOEHE):
        reihe = []
        for sp in range(TERMINAL_BREITE):
            basis = (zr * TERMINAL_BREITE + sp) * n // anzahl
            gruppe = engine.zellen[basis:basis + schritt]
            if not gruppe:
                break

            sin_sum = 0.0
            cos_sum = 0.0
            for z in gruppe:
                bogen = z.hue * 3.141592653589793 / 180.0
                sin_sum += math.sin(bogen)
                cos_sum += math.cos(bogen)
            hue = (math.atan2(sin_sum / len(gruppe), cos_sum / len(gruppe)) * 180.0 / 3.141592653589793) % 360.0

            sat = sum(z.saturation for z in gruppe) / len(gruppe)
            bri = sum(z.brightness for z in gruppe) / len(gruppe)
            reihe.append(_block(*_rgb(hue, sat, bri)))
        zeilen.append("".join(reihe))

    uni = engine.universe
    kopf = (f"{titel}  schritt={engine.step_count}  modus={uni.modus}  "
            f"harm={uni.harmonie:.2f}  drift={uni.drift:.2f}")
    print(kopf)
    print("\n".join(zeilen))
