# Dialog.py – Das Gespraech mit dem Interactor
# Hinauf: Der Zustand des Colorverse - nur mit Zustimmung.
# Herab: Was der Interactor sagt - nur mit Zustimmung,
#        und es wirkt wie ein Impuls in das Evolutionsfeld.
import json
import os
import sys
from config import *
from Gate import darf, senden, empfangen, zustimmung_einholen, _loggen


# ============================================================
#  HINAUF - Zustand des Colorverse
# ============================================================

def _zustand(engine):
    uni = engine.universe
    return {
        "schritt": engine.step_count,
        "modus": uni.modus,
        "harmonie": round(uni.harmonie, 4),
        "drift": round(uni.drift, 4),
        "energie": round(uni.energy, 4),
        "stoerimpulse": round(engine.harmonie_feld["stoerimpulse"], 4),
    }


def hinauf(engine):
    if not darf(DIALOG_KANAL_HINAUF):
        if sys.stdin.isatty() if hasattr(sys.stdin, "isatty") else False:
            zustimmung_einholen(DIALOG_KANAL_HINAUF)
        if not darf(DIALOG_KANAL_HINAUF):
            return None

    zustand = _zustand(engine)
    paket = senden(DIALOG_KANAL_HINAUF, zustand)
    if paket is None:
        return None

    with open(DIALOG_AUSGANG_DATEI, "w", encoding="utf-8") as f:
        json.dump(paket, f, indent=2)
    return paket


# ============================================================
#  HERAB - Impuls des Interactors
# ============================================================

def _impuls_anwenden(engine, impuls):
    versatz = impuls.get("hue_versatz", 0.0)
    stoeren = impuls.get("stoerimpulse", None)

    if versatz:
        for z in engine.zellen:
            z.hue = (z.hue + versatz) % 360

    if stoeren is not None:
        engine.harmonie_feld["stoerimpulse"] = max(0.0, min(1.0, float(stoeren)))
        return True

    return bool(versatz)


def herab(engine):
    if not os.path.exists(DIALOG_EINGANG_DATEI):
        return None

    with open(DIALOG_EINGANG_DATEI, "r", encoding="utf-8") as f:
        roh = f.read()

    if not darf(DIALOG_KANAL_HERAB):
        if sys.stdin.isatty() if hasattr(sys.stdin, "isatty") else False:
            zustimmung_einholen(DIALOG_KANAL_HERAB)
        if not darf(DIALOG_KANAL_HERAB):
            return None

    try:
        impuls = json.loads(roh)
    except json.JSONDecodeError:
        os.remove(DIALOG_EINGANG_DATEI)
        return None

    paket = empfangen(DIALOG_KANAL_HERAB, impuls)
    if paket is None:
        return None

    gewirkt = _impuls_anwenden(engine, paket)
    os.remove(DIALOG_EINGANG_DATEI)
    return gewirkt


# ============================================================
#  GESPRAECH - beides in einem Atemzug
# ============================================================

def gespraech(engine):
    gewirkt = herab(engine)
    auskunft = hinauf(engine)
    return {"gewirkt": gewirkt, "auskunft": auskunft}
