# Gate.py – Datenaustausch nur mit Zustimmung des Interactors
# Ohne Eintrag im Ledger fuehrt kein Weg nach draussen und kein Weg hierher.
import json
import os
import time
from config import *
from Gedaechtnis import hardware_signatur


# ============================================================
#  LEDGER (Vereinbarungen)
# ============================================================

def _ledger_lesen():
    if not os.path.exists(GATE_LEDGER_DATEI):
        return {}
    with open(GATE_LEDGER_DATEI, "r", encoding="utf-8") as f:
        return json.load(f)


def _ledger_schreiben(ledger):
    with open(GATE_LEDGER_DATEI, "w", encoding="utf-8") as f:
        json.dump(ledger, f, indent=2)


def _loggen(kanal, ereignis, erlaubt=False):
    eintrag = {
        "zeit": time.strftime("%Y-%m-%d %H:%M:%S"),
        "kanal": kanal,
        "ereignis": ereignis,
        "erlaubt": erlaubt,
        "hardware": hardware_signatur()[:16],
    }
    with open(GATE_LOG_DATEI, "a", encoding="utf-8") as f:
        f.write(json.dumps(eintrag) + "\n")


# ============================================================
#  ZUSTIMMUNG
# ============================================================

def zustimmen(kanal):
    ledger = _ledger_lesen()
    ledger[kanal] = {
        "erlaubt": True,
        "seit": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    _ledger_schreiben(ledger)
    _loggen(kanal, "zustimmung", erlaubt=True)


def widerrufen(kanal):
    ledger = _ledger_lesen()
    ledger.pop(kanal, None)
    _ledger_schreiben(ledger)
    _loggen(kanal, "widerruf", erlaubt=False)


def darf(kanal):
    return bool(_ledger_lesen().get(kanal, {}).get("erlaubt", False))


def zustimmung_einholen(kanal):
    try:
        antwort = input(f"[GATE] Austausch ueber '{kanal}' erlauben? (j/n): ").strip().lower()
    except EOFError:
        antwort = "n"
    if antwort == "j":
        zustimmen(kanal)
        return True
    widerrufen(kanal)
    return False


# ============================================================
#  AUSTAUSCH (der einzige Weg rein und raus)
# ============================================================

def senden(kanal, daten):
    erlaubt = darf(kanal)
    _loggen(kanal, "senden", erlaubt=erlaubt)
    if not erlaubt:
        return None
    return daten


def empfangen(kanal, daten):
    erlaubt = darf(kanal)
    _loggen(kanal, "empfangen", erlaubt=erlaubt)
    if not erlaubt:
        return None
    return daten
