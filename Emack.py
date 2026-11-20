# Emack.py – Der EMACK-Puls im Colorverse
# Agent B atmet mit dem Universum: Der Saturn ist A, der Puls ist B.
# Beide teilen dieselbe Sprache: af, pf, rf.
import importlib
import os
import sys
from config import *

basis = os.path.dirname(os.path.abspath(__file__))
URASIL_PFAD = [p for p in (os.path.abspath(os.path.join(basis, pfad)) for pfad in EMACK_URASIL_PFAD) if os.path.isdir(p)]

b_af = 0.5
b_pf = 0.5
b_rf = 0.5

_wahl = None


# ============================================================
#  ORGAN-WAHL (aus dem Geburtsakt)
# ============================================================

def _organ():
    global _wahl
    if _wahl is None:
        try:
            from installation import geburtsakt_lesen
            akt = geburtsakt_lesen()
            _wahl = bool(akt.get("emack", False)) if akt else False
        except Exception:
            _wahl = False
    return _wahl


# ============================================================
#  PULSGEBER LADEN
# ============================================================

def _puls():
    try:
        for pfad in URASIL_PFAD:
            if pfad not in sys.path:
                sys.path.insert(0, pfad)
            alter_ordner = os.getcwd()
            os.chdir(pfad)
            try:
                return importlib.import_module("emack_pulse")
            finally:
                os.chdir(alter_ordner)
        return None
    except Exception:
        return None


# ============================================================
#  SCHLAG - ein Puls von A nach B und zurueck
# ============================================================

def schlag(engine):
    global b_af, b_pf, b_rf

    if not ENABLE_EMACK or not _organ():
        return None

    modul = _puls()
    if modul is None:
        return None

    af = engine.universe.harmonie
    pf = 1.0 - engine.universe.drift
    rf = max(0.0, min(1.0, 1.0 - engine.harmonie_feld["stoerimpulse"]))

    stimmung = modul.mood(af, pf, rf, EMACK_MUTATION, 0.0)
    echo = modul.echo(af, pf, rf, EMACK_MUTATION, 0.0, stimmung)
    b_af, b_pf, b_rf = modul.agent_b_react(stimmung, echo, b_af, b_pf, b_rf)

    hexa = engine.zellen[0].hex
    if hexa:
        staerke = EMACK_SYNC_STAERKE
        hexa.B["af"] += (b_af - hexa.B["af"]) * staerke
        hexa.B["pf"] += (b_pf - hexa.B["pf"]) * staerke
        hexa.C["af"] += (b_pf - hexa.C["af"]) * staerke * 0.5
        hexa.C["pf"] += (b_rf - hexa.C["pf"]) * staerke * 0.5

    return {
        "stimmung": stimmung,
        "echo": echo,
        "b": (b_af, b_pf, b_rf),
    }
