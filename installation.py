# installation.py – Die Geburt des Unikats
# Beim Erststart attestiert die Software den Abdruck der Maschine.
# Danach zählt die Geburt, nicht jeder Kernel-Update: Damit die
# Erinnerung sich nicht mit jedem Treiber verliert.
import json
import os
import time
from config import *
from HwScan import scan, signatur, stabile_signatur, abweichung
from Gedaechtnis import _verschluesseln, _entschluesseln


# ============================================================
#  GEBURTSAKT
# ============================================================

def geburtsakt_schreiben(erneuern=False):
    if os.path.exists(GEBURTSAKT_DATEI) and not erneuern:
        return False

    d = scan()
    akt = {
        "signatur": signatur(d),
        "stabil": stabile_signatur(d),
        "abdruck": d,
        "individualitaet": abweichung(d),
        "version": COLORVERSE_VERSION,
        "zeit": time.strftime("%Y-%m-%d %H:%M:%S"),
    }

    with open(GEBURTSAKT_DATEI, "wb") as f:
        f.write(_verschluesseln(json.dumps(akt).encode()))
    return True


def geburtsakt_lesen():
    if not os.path.exists(GEBURTSAKT_DATEI):
        return None

    with open(GEBURTSAKT_DATEI, "rb") as f:
        paket = f.read()

    try:
        return json.loads(_entschluesseln(paket).decode())
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None


# ============================================================
#  WACHE - vor jeder Erinnerung oder Geburt
# ============================================================

def wache():
    if not os.path.exists(GEBURTSAKT_DATEI):
        geburtsakt_schreiben()
        return {"geburt": True, "individualitaet": abweichung()}

    akt = geburtsakt_lesen()

    if akt is None:
        # Datei vorhanden, aber unlesbar: NIE still neu gebaren.
        return {"unlesbar": True}

    if akt.get("stabil") != stabile_signatur():
        return {"fremd": True, "geburtsakt": akt}

    return {"geburtsakt": akt, "individualitaet": akt.get("individualitaet", 0.0)}


if __name__ == "__main__":
    print(json.dumps(wache(), indent=2))
