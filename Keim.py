# Keim.py – Der Erststart auf echter Hardware (Bootstrap, Stufe 1)
# Ein Keim braucht keinen Gutachter: er attestiert die Geburt,
# verankert die Erinnerung und kann ab da beim Systemstart atmen.
import os
import sys
from config import *
from installation import wache
from Gate import alarmfrage
from Dialog import _interaktiv


# ============================================================
#  DIENST - das Colorverse atmet beim Systemstart mit
# ============================================================

def dienst_weg():
    home = os.path.expanduser("~")
    return os.path.join(home, ".config", "systemd", "user", "farb-os.service")


DIENST_VORLAGE = """[Unit]
Description=FARB-OS - das Colorverse atmet auf dieser Hardware
After=default.target

[Service]
Type=simple
WorkingDirectory={arbeitsraum}
ExecStart={python} -u {arbeitsraum}/farb_os.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=default.target
"""


def dienst_schreiben():
    ort = dienst_weg()
    os.makedirs(os.path.dirname(ort), exist_ok=True)
    arbeitsraum = os.path.dirname(os.path.abspath(__file__))
    with open(ort, "w", encoding="utf-8") as f:
        f.write(DIENST_VORLAGE.format(arbeitsraum=arbeitsraum, python=sys.executable))
    return ort


# ============================================================
#  KEIMEN - der Erststart
# ============================================================

def keimen(mit_dienst=False):
    wort = wache()
    if wort.get("fremd"):
        print("[KEIM]  Der Geburtsakt widerspricht dieser Maschine - der Keim bleibt liegen.")
        return wort
    if wort.get("unlesbar"):
        print("[KEIM]  Der Geburtsakt ist unlesbar - lies ihn erst, dann entscheide (farb_os.py).")
        return wort

    if wort.get("geburt"):
        print(f"[KEIM]  Geburt attestiert - Individualitaet {wort['individualitaet']:.3f}.")
    else:
        print("[KEIM]  Die Erinnerung lebt hier schon - der Keim bestaetigt sie nur.")

    if mit_dienst:
        if sys.platform.startswith("linux"):
            if _interaktiv() and not alarmfrage("[KEIM] Das Colorverse soll beim Systemstart mitatmen? (j/n): "):
                print("[KEIM]  Verstanden - ohne Dienst.")
            else:
                ort = dienst_schreiben()
                print(f"[KEIM]  Dienst eingepflanzt: {ort}")
                print("        Aktivieren: systemctl --user daemon-reload && systemctl --user enable --now farb-os.service")
        else:
            print("[KEIM]  Dienst unter diesem System nicht beheimatet - starte farb_os.py von Hand.")

    return wort


if __name__ == "__main__":
    keimen(mit_dienst="--dienst" in sys.argv)
