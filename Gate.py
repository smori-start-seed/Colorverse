# Gate.py – Datenaustausch nur mit Zustimmung des Interactors
# Ohne Eintrag im Ledger fuehrt kein Weg nach draussen und kein Weg hierher.
# Eine Zustimmung lebt in Schritten des Colorverse - und verblasst damit
# in der eigenen Zeit des Systems, nicht in einer Wanduhr.
import json
import os
import select
import sys
import time
from config import *
from Gedaechtnis import hardware_signatur


def _ledger_lesen():
    if not os.path.exists(GATE_LEDGER_DATEI):
        return {}
    try:
        with open(GATE_LEDGER_DATEI, "r", encoding="utf-8") as f:
            return json.load(f)
    except (ValueError, OSError):
        # Ein unlesbares Ledger verweigert alles - nie die Welt sterben lassen.
        return {}


def _ledger_schreiben(ledger):
    with open(GATE_LEDGER_TEMPO, "w", encoding="utf-8") as f:
        json.dump(ledger, f, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(GATE_LEDGER_TEMPO, GATE_LEDGER_DATEI)


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
#  ZUSTIMMUNG (zweck-gebunden, mit Ablauf in Schritten)
# ============================================================

def zustimmen(kanal, zweck=None, schritt=None, dauer=ZUSTIMMUNG_DAUER):
    ledger = _ledger_lesen()
    eintrag = {
        "erlaubt": True,
        "seit": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    if zweck:
        eintrag["zweck"] = zweck
    if schritt is not None and dauer is not None:
        eintrag["ablauf"] = schritt + dauer
    ledger[kanal] = eintrag
    _ledger_schreiben(ledger)
    _loggen(kanal, "zustimmung", erlaubt=True)


def widerrufen(kanal):
    ledger = _ledger_lesen()
    ledger.pop(kanal, None)
    _ledger_schreiben(ledger)
    _loggen(kanal, "widerruf", erlaubt=False)


def darf(kanal, schritt=None):
    eintrag = _ledger_lesen().get(kanal)
    if not eintrag or not eintrag.get("erlaubt", False):
        return False

    ablauf = eintrag.get("ablauf")
    if ablauf is not None and schritt is not None and schritt > ablauf:
        widerrufen(kanal)
        return False

    return True


def _wort_holen(frage):
    # Eine Frage der Welt wartet eine Wartezeit lang auf das Wort des
    # Interactors - und schweigen ist Ablehnung. Die Welt steht nie
    # still, weil niemand am Wort haelt..
    sys.stdout.write(frage)
    sys.stdout.flush()
    try:
        bereit, _, _ = select.select([sys.stdin], [], [], GATE_FRAGE_SEKUNDEN)
    except (OSError, ValueError):
        return ""
    if not bereit:
        return ""
    try:
        return sys.stdin.readline().strip().lower()
    except (EOFError, OSError):
        return ""


def zustimmung_einholen(kanal, schritt=None, zweck=None):
    frage = f"[GATE] Austausch ueber '{kanal}'"
    if zweck:
        frage += f" (Zweck: {zweck})"
    frage += " erlauben? (j/n/i): "

    antwort = _wort_holen(frage)

    if antwort == "j":
        zustimmen(kanal, zweck=zweck, schritt=schritt)
        return True
    if antwort == "i":
        zustimmen(kanal, zweck=zweck, schritt=None, dauer=None)
        return True
    widerrufen(kanal)
    return False


def alarmfrage(frage):
    # Eine Lebensentscheidung der Wache - kein Ledger-Eintrag,
    # kein Austausch: nur das Wort des Interactors.
    antwort = _wort_holen(frage)
    return antwort == "j"


# ============================================================
#  AUSTAUSCH (der einzige Weg rein und raus)
# ============================================================

def senden(kanal, daten, schritt=None):
    erlaubt = darf(kanal, schritt)
    _loggen(kanal, "senden", erlaubt=erlaubt)
    if not erlaubt:
        return None
    return daten


def empfangen(kanal, daten, schritt=None):
    erlaubt = darf(kanal, schritt)
    _loggen(kanal, "empfangen", erlaubt=erlaubt)
    if not erlaubt:
        return None
    return daten
