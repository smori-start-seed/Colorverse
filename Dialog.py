# Dialog.py – Das Gespraech mit dem Interactor
# Hinauf: Der Zustand des Colorverse - nur mit Zustimmung.
# Herab: Was der Interactor sagt - nur mit Zustimmung,
#        und erst durch das innere Gericht (Schattenlauf),
#        bevor es in die Welt wirkt. Widerspricht die Welt,
#        fragt die Wache - ausser im Skriptbetrieb, da gilt ihr Nein.
import json
import os
import sys
from config import *
from Gate import darf, senden, empfangen, zustimmung_einholen, _loggen, alarmfrage


# ============================================================
#  KLEINE WOERTER
# ============================================================

def _interaktiv():
    try:
        return sys.stdin.isatty()
    except Exception:
        return False


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
    schritt = engine.step_count
    if not darf(DIALOG_KANAL_HINAUF, schritt):
        if _interaktiv():
            zustimmung_einholen(DIALOG_KANAL_HINAUF, schritt=schritt, zweck="Lesen des Zustands")
        if not darf(DIALOG_KANAL_HINAUF, schritt):
            return None

    zustand = _zustand(engine)
    paket = senden(DIALOG_KANAL_HINAUF, zustand, schritt=schritt)
    if paket is None:
        return None

    with open(DIALOG_AUSGANG_DATEI, "w", encoding="utf-8") as f:
        json.dump(paket, f, indent=2)
    return paket


# ============================================================
#  IMPULS & SCHATTEN (das innere Gericht)
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


def _einmal_patch(impuls):
    # Ein Impuls ist eine Beruehrung, kein Dauerzustand:
    # im Schattenlauf wirkt er genau einmal, dann lebt die Welt weiter.
    erste = [True]

    def patch(welt):
        if erste[0]:
            erste[0] = False
            _impuls_anwenden(welt, impuls)
    return patch


# ============================================================
#  HERAB - Impuls des Interactors
# ============================================================

def herab(engine):
    if not os.path.exists(DIALOG_EINGANG_DATEI):
        return None

    with open(DIALOG_EINGANG_DATEI, "r", encoding="utf-8") as f:
        roh = f.read()

    if not darf(DIALOG_KANAL_HERAB, engine.step_count):
        if _interaktiv():
            zustimmung_einholen(DIALOG_KANAL_HERAB, schritt=engine.step_count, zweck="Impulse in das Evolutionsfeld")
        if not darf(DIALOG_KANAL_HERAB, engine.step_count):
            return None

    try:
        impuls = json.loads(roh)
    except json.JSONDecodeError:
        os.remove(DIALOG_EINGANG_DATEI)
        return None

    paket = empfangen(DIALOG_KANAL_HERAB, impuls, schritt=engine.step_count)
    if paket is None:
        return None

    ergebnis = None
    ueberschrieben = False

    if DIALOG_SCHATTEN:
        from Schatten import simuliere
        ergebnis = simuliere(engine, patch=_einmal_patch(paket))

        if not ergebnis["annahme"]:
            ueber = False
            if _interaktiv():
                frage = (f"[WACHE] Der Impuls widerspricht dem Sinn "
                         f"(Harmonie {ergebnis['harmonie_delta']:+.3f}, "
                         f"Drift {ergebnis['drift_delta']:+.3f}). "
                         "Trotzdem wirken? (j/n): ")
                ueber = alarmfrage(frage)

            if not ueber:
                _loggen(DIALOG_KANAL_HERAB, "abgelehnt", erlaubt=False)
                os.remove(DIALOG_EINGANG_DATEI)
                return {"gewirkt": False, "urteil": ergebnis, "ueberschrieben": False}

            ueberschrieben = True
            _loggen(DIALOG_KANAL_HERAB, "ueberschreibung", erlaubt=True)

    gewirkt = _impuls_anwenden(engine, paket)
    os.remove(DIALOG_EINGANG_DATEI)
    return {"gewirkt": gewirkt, "urteil": ergebnis, "ueberschrieben": ueberschrieben}


# ============================================================
#  GESPRAECH - beides in einem Atemzug
# ============================================================

def gespraech(engine):
    return {
        "impuls": herab(engine),
        "auskunft": hinauf(engine),
    }
