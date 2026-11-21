# HwScan.py – Der Abdruck der Maschine
# Jede Hardware drueckt dem Colorverse ihren Stempel auf.
# Je staerker sie von der Norm abweicht, desto individueller wird die Welt.
import hashlib
import json
import os
import platform
import shutil
import uuid
from config import *


# ============================================================
#  DIE NORM - eine abstrakte Standardmaschine
# ============================================================

NORM = {
    "plattform": "Linux",
    "architektur": "x86_64",
    "host": "standardhost",
    "prozessoren": 4,
    "speicher": 16000,
    "platte": 500000,
}


# ============================================================
#  SCAN
# ============================================================

def scan():
    u = platform.uname()
    try:
        seite = os.sysconf("SC_PAGE_SIZE")
        rahmen = os.sysconf("SC_PHYS_PAGES")
        speicher = seite * rahmen / (1024 * 1024)
    except (ValueError, OSError, AttributeError):
        speicher = -1.0

    try:
        platte = shutil.disk_usage(os.sep).total / (1024 * 1024)
    except OSError:
        platte = -1.0

    return {
        "plattform": u.system or "unbekannt",
        "kernel": u.release or "unbekannt",
        "architektur": u.machine or "unbekannt",
        "host": u.node or "unbekannt",
        "prozessoren": os.cpu_count() or -1,
        "speicher": round(speicher),
        "platte": round(platte),
        "mac": uuid.getnode(),
    }


# ============================================================
#  ABWEICHUNG & INDIVIDUALITAET
# ============================================================

def abweichung(daten=None):
    daten = daten or scan()
    abw = 0.0

    if daten["plattform"] != NORM["plattform"]:
        abw += 0.10
    if daten["architektur"] != NORM["architektur"]:
        abw += 0.15
    if daten["host"] != NORM["host"]:
        abw += 0.20

    for feld, gewicht in (("prozessoren", 0.25), ("speicher", 0.20), ("platte", 0.20)):
        norm_wert = NORM[feld]
        wert = daten[feld]
        if wert > 0:
            abw += gewicht * min(1.0, abs(wert - norm_wert) / max(1.0, norm_wert))
        else:
            abw += gewicht

    return min(1.0, abw)


def individualitaet():
    if not ENABLE_HWSCAN:
        return 0.0
    return abweichung()


# ============================================================
#  SIGNATUR & SAMEN
# ============================================================

def signatur(daten=None):
    daten = json.dumps(_kern(daten or scan()), sort_keys=True).encode()
    return hashlib.sha256(daten).hexdigest()


def stabile_signatur(daten=None):
    # Nur der ruhige Kern: Plattform und Architektur aendern sich
    # nicht mit Kernel-Updates oder MAC-Zufall.
    daten = daten or scan()
    kern = {k: daten[k] for k in ("plattform", "architektur")}
    return hashlib.sha256(json.dumps(kern, sort_keys=True).encode()).hexdigest()


def _kern(daten):
    return {k: daten[k] for k in ("plattform", "kernel", "architektur", "prozessoren", "speicher", "platte", "mac")}


def samen(engine):
    if not ENABLE_HWSCAN:
        return 0.0

    ind = individualitaet()

    feld = engine.harmonie_feld
    feld["stoerimpulse"] = min(1.0, feld["stoerimpulse"] * (0.5 + ind))
    feld["global_drift"] = min(1.0, feld["global_drift"] * (0.5 + ind))

    versatz = int(ind * 360.0)
    for z in engine.zellen:
        z.hue = (z.hue + versatz) % 360

    return ind


if __name__ == "__main__":
    d = scan()
    for k, v in d.items():
        print(f"{k:14}: {v}")
    print("Abweichung    :", round(abweichung(d), 3))
    print("Signatur      :", signatur(d))
