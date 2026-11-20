# farb_os.py – Einstiegspunkt des Farb-Betriebssystems
# Reihenfolge des Lebens: erinnern, evolvieren, verwahren.
import time
from config import *
from engine import Engine
from saturings import build_world
from Gedaechtnis import speichern, laden


# ============================================================
#  HAUPTSCHLEIFE DES FARB-OS
# ============================================================

def main(steps=200, delay=0.0, snapshot_interval=SNAPSHOT_INTERVALL):
    engine = Engine()
    build_world(engine)

    if laden(engine):
        print(f"[FARB-OS] Erinnerung geladen – Schritt {engine.step_count}")
    else:
        print("[FARB-OS] Neugeboren – dieses Colorverse beginnt bei null.")

    for _ in range(steps):
        engine.step()

        if engine.step_count % snapshot_interval == 0:
            speichern(engine)

        if delay > 0:
            time.sleep(delay)

    speichern(engine)
    print(f"[FARB-OS]  Colorverse verwahrt: {GEDAECHTNIS_DATEI}")


if __name__ == "__main__":
    main(steps=20, delay=0.0, snapshot_interval=10)
