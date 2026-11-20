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


# ============================================================
#  HAUPTSCHLEIFE DES FARB-OS
# ============================================================

def main(steps=200, delay=0.0, snapshot_interval=SNAPSHOT_INTERVALL):
    engine = Engine()
    build_world(engine)

    if samen_und_laden(engine):
        print(f"[FARB-OS] Erinnerung geladen – Schritt {engine.step_count}")
    else:
        print(f"[FARB-OS] Neugeboren – dieses Colorverse beginnt bei null.")

    for _ in range(steps):
        engine.step()
        schlag(engine)

        if engine.step_count % KONSOLE_INTERVALL == 0:
            zeige(engine)

        if ENABLE_KLANG and engine.step_count % KLANG_INTERVALL == 0:
            datei = klang_erzeugen(engine)
            if datei:
                print(f"[KLANG]  {datei}")

        if engine.step_count % snapshot_interval == 0:
            speichern(engine)

        if delay > 0:
            time.sleep(delay)

    speichern(engine)
    print(f"[FARB-OS]  Colorverse verwahrt: {GEDAECHTNIS_DATEI}")


def samen_und_laden(engine):
    if laden(engine):
        return True
    samen(engine)
    return False


if __name__ == "__main__":
    main(steps=20, delay=0.0, snapshot_interval=10)
