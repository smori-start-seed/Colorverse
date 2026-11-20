# Schatten.py – Interne Simulation vor und nach Umsetzung
# Jede geplante Aenderung laeuft erst in einer Schattenwelt:
# einmal ohne den Patch (vor vorher), einmal mit ihm (nachher).
# Das Colorverse entscheidet aus dem Sinn (Harmonie & Drift).
import contextlib
import io
from config import *
from engine import Engine
from saturings import build_world


# ============================================================
#  GRUNDWELT & ZUSTAND
# ============================================================

def _grundwelt():
    welt = Engine()
    with contextlib.redirect_stdout(io.StringIO()):
        build_world(welt)
    return welt


def _zustand_kopieren(engine):
    hexa = engine.zellen[0].hex
    return {
        "zellen": [
            {
                "hue": z.hue,
                "saturation": z.saturation,
                "brightness": z.brightness,
                "energy": z.energy,
                "drift": z.drift,
                "harmonie": z.harmonie,
                "in_cluster": z.in_cluster,
                "evolutionskeim": z.evolutionskeim,
            }
            for z in engine.zellen
        ],
        "feld": dict(engine.harmonie_feld),
        "hex": {
            "A": dict(hexa.A),
            "B": dict(hexa.B),
            "C": dict(hexa.C),
        },
    }


def _zustand_einspielen(welt, zustand):
    if len(welt.zellen) != len(zustand["zellen"]):
        return False

    for z, snap in zip(welt.zellen, zustand["zellen"]):
        z.hue = snap["hue"]
        z.saturation = snap["saturation"]
        z.brightness = snap["brightness"]
        z.energy = snap["energy"]
        z.drift = snap["drift"]
        z.harmonie = snap["harmonie"]
        z.in_cluster = snap["in_cluster"]
        z.evolutionskeim = snap["evolutionskeim"]

    welt.harmonie_feld.update(zustand["feld"])

    hexa = welt.zellen[0].hex
    hexa.A.update(zustand["hex"]["A"])
    hexa.B.update(zustand["hex"]["B"])
    hexa.C.update(zustand["hex"]["C"])
    return True


# ============================================================
#  SCHATTLAUF
# ============================================================

def _laufen(welt, schritte, patch):
    harmonie = []
    drift = []

    with contextlib.redirect_stdout(io.StringIO()):
        for _ in range(schritte):
            if patch:
                patch(welt)
            welt.step()
            harmonie.append(welt.harmonie_feld["global_harmonie"])
            drift.append(welt.harmonie_feld["global_drift"])

    return {
        "harmonie": sum(harmonie) / len(harmonie) if harmonie else 0.0,
        "drift": sum(drift) / len(drift) if drift else 0.0,
        "modus": welt.universe.modus,
    }


def entscheide(vorher, nachher):
    dh = nachher["harmonie"] - vorher["harmonie"]
    dd = nachher["drift"] - vorher["drift"]
    annahme = (dh >= -SCHATTEN_TOLERANZ) and (dd <= SCHATTEN_TOLERANZ)
    return {
        "annahme": annahme,
        "harmonie_delta": dh,
        "drift_delta": dd,
    }


# ============================================================
#  OEFFENTLICHE SIMULATION (vorher vs. nachher)
# ============================================================

def simuliere(engine, patch=None, schritte=None):
    schritte = schritte if schritte is not None else SCHATTEN_SCHRITTE
    zustand = _zustand_kopieren(engine)

    vorher_welt = _grundwelt()
    _zustand_einspielen(vorher_welt, zustand)
    vorher = _laufen(vorher_welt, schritte, None)

    nachher_welt = _grundwelt()
    _zustand_einspielen(nachher_welt, zustand)
    nachher = _laufen(nachher_welt, schritte, patch)

    ergebnis = entscheide(vorher, nachher)
    return {
        "vorher": vorher,
        "nachher": nachher,
        "harmonie_delta": ergebnis["harmonie_delta"],
        "drift_delta": ergebnis["drift_delta"],
        "annahme": ergebnis["annahme"],
    }


if __name__ == "__main__":
    engine = Engine()
    build_world(engine)

    for _ in range(3):
        engine.step()

    beispiel_patch = lambda w: [setattr(z, "alpha", 0.10) for z in w.zellen]

    ergebnis = simuliere(engine, patch=beispiel_patch)
    print("[SCHATT] vorher:", ergebnis["vorher"])
    print("[SCHATT] nachher:", ergebnis["nachher"])
    print(f"[SCHATT] dh={ergebnis['harmonie_delta']:+.4f} dd={ergebnis['drift_delta']:+.4f}")
    print("[SCHATT] entscheidung:", "ANNEHMEN" if ergebnis["annahme"] else "ABLEHNEN")
