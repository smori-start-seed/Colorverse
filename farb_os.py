# farb_os.py – Einstiegspunkt des Farb-Betriebssystems
# Reihenfolge des Lebens: erinnern, evolvieren, sehen, hoeren, verwahren.
import time
from config import *
from engine import Engine
from saturings import build_world
from Gedaechtnis import speichern, laden
from HwScan import samen
from Emack import schlag
from Terminal import zeige
from Klang import erzeuge as klang_erzeugen
from Dialog import gespraech
from installation import wache


# ============================================================
#  HAUPTSCHLEIFE DES FARB-OS
# ============================================================

def main(steps=200, delay=0.0, snapshot_interval=SNAPSHOT_INTERVALL):
    geburt = wache()
    if geburt.get("fremd"):
        print("[FARB-OS]  Der Geburtsakt widerspricht dieser Maschine.")
        print("           Dieses Unikat wohnt nicht hier. Keine Erinnerung, keine Geburt.")
        return

    engine = Engine()
    build_world(engine)

    if laden(engine):
        print(f"[FARB-OS] Erinnerung geladen – Schritt {engine.step_count}")
    else:
        samen(engine)
        if "geburtsakt" in geburt:
            print(f"[FARB-OS]  Erinnerung unbekannt – die Welt sät neu, Individualität {geburt['individualitaet']:.3f}.")
        else:
            print(f"[FARB-OS] Neugeboren – Individualität {geburt['individualitaet']:.3f}.")

    for _ in range(steps):
        engine.step()
        schlag(engine)

        if engine.step_count % KONSOLE_INTERVALL == 0:
            zeige(engine)

        if ENABLE_KLANG and engine.step_count % KLANG_INTERVALL == 0:
            datei = klang_erzeugen(engine)
            if datei:
                print(f"[KLANG]  {datei}")

        if engine.step_count % DIALOG_INTERVALL == 0:
            worte = gespraech(engine)
            if worte["gewirkt"]:
                print("[DIALOG] Impuls des Interactors wirkt.")

        if engine.step_count % snapshot_interval == 0:
            speichern(engine)

        if delay > 0:
            time.sleep(delay)

    speichern(engine)
    print(f"[FARB-OS]  Colorverse verwahrt: {GEDAECHTNIS_DATEI}")


if __name__ == "__main__":
    main(steps=20, delay=0.0, snapshot_interval=10)
