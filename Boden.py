# Boden.py – Der Anbau: das Unikat pflanzt sich in einen Koerper (Stufe 3)
# Partitionieren, formatieren, GRUB einpflanzen - HANDLUNGEN OHNE WIEDERKEHR.
# Auf dem Boden lebt womoeglich anderes; deshalb fragt der Boden dreimal,
# zeigt alles offen und vergisst nichts (gate_log).
import os
import json
import shutil
import subprocess
import sys
import glob
from config import *
from Gate import alarmfrage, _loggen
from Dialog import _interaktiv


# ============================================================
#  KLEINE WERKZEUGE
# ============================================================

def _lauf(befehl):
    ergebnis = subprocess.run(befehl, capture_output=True, text=True)
    if ergebnis.returncode != 0:
        raise RuntimeError(f"{befehl[0]} fiel aus: {ergebnis.stderr.strip()[:300]}")
    return ergebnis.stdout


def _platte_von(ziel):
    # /dev/sda2 -> /dev/sda , /dev/nvme0n1p3 -> /dev/nvme0n1
    for i in range(len(ziel), 1, -1):
        stummel = ziel[:i]
        if os.path.exists(stummel) and os.path.isdir(f"/sys/block/{os.path.basename(stummel)}"):
            return stummel
    return None


def _grosse(platte):
    try:
        with open(f"/sys/block/{os.path.basename(platte)}/size") as f:
            return int(f.read()) * 512
    except OSError:
        return None


def _erste_partition(platte):
    for form in (f"{platte}p1", f"{platte}1"):
        if os.path.exists(form):
            return form
    raise RuntimeError(f"keine Partition nach dem Saen gefunden ({platte})")


# ============================================================
#  SCHUTZ - Dreifaches Wort, keins weniger
# ============================================================

def pruefen(ziel):
    if os.geteuid() != 0:
        raise RuntimeError("nur mit Wurzelrechten - der Boden gehoert dem System")
    if not ziel.startswith("/dev/") or not os.path.exists(ziel):
        raise RuntimeError(f"{ziel} ist kein Datentraeger")
    if os.path.realpath(ziel) != ziel:
        raise RuntimeError(f"{ziel} ist eine Verknuepfung - nimm das wahre Ziel")
    with open("/proc/mounts") as f:
        for zeile in f:
            if zeile.split()[0].startswith(ziel):
                raise RuntimeError(f"{ziel} (oder ein Teil davon) ist eingebunden - erst loesen")
    return _platte_von(ziel)


def ritual(ziel):
    if not _interaktiv():
        raise RuntimeError("kein Wort moeglich (kein tty) - der Boden bleibt unberuehrt")
    platte = _platte_von(ziel) or ziel
    grosse = _grosse(platte)
    gross = f"{grosse // 1024**3} GiB" if grosse else "unbekannt"
    print(f"[BODEN] {ziel}: alles, was dort lebt, geht ohne Wiederkehr.")
    print(f"[BODEN] Platte: {platte}, Groesse {gross}.")
    if not alarmfrage(f"[BODEN] {ziel} wirklich ganz ausraeumen und pflanzen? (j/n): "):
        raise RuntimeError("verstanden - der Boden bleibt")
    wort = input(f"[BODEN] Nenne den vollen Namen des Bodens zum Bestaetigen ({ziel}): ").strip()
    if wort != ziel:
        raise RuntimeError("das Wort passt nicht zum Boden - verweigert")
    _loggen("boden-" + os.path.basename(ziel), "zustimmung", erlaubt=True)


GRUB_BODEN = """set timeout=1
default=0
menuentry "FARB-OS" {{
    linux /boot/vmlinuz boden=PARTUUID={partuuid} console=tty0
    initrd /boot/initramfs.img
}}
"""


# ============================================================
#  ANBAUEN - saeen, formatieren, bootfaehig machen
# ============================================================

def anbauen(ziel, ordner=BOOT_ORDNER):
    vmlinuz = os.path.join(ordner, "iso_wurzel", "boot", "vmlinuz")
    initramfs = os.path.join(ordner, "iso_wurzel", "boot", "initramfs.img")
    if not (os.path.exists(vmlinuz) and os.path.exists(initramfs)):
        raise RuntimeError("kein Bootsatz gefunden - erst: python3 Bootsatz.py --iso")

    _brauche("sfdisk", "gehoert zu util-linux - sollte nie fehlen")
    _brauche("mkfs." + BODEN_DATEISYSTEM, "auf Debian/Ubuntu: sudo apt install e2fsprogs")
    _brauche("grub-install", "auf Debian/Ubuntu: sudo apt install grub-pc grub-efi-amd64-bin")
    _brauche("mount", "gehoert zu util-linux")

    platte = pruefen(ziel)
    ritual(ziel)

    _lauf(["sh", "-c", f"printf 'label: gpt\\ntype=8300\\n' | sfdisk --wipe always {platte}"])
    _loggen("boden-" + os.path.basename(platte), "gesaet", erlaubt=True)

    teil_1 = _erste_partition(platte)
    _lauf(["mkfs." + BODEN_DATEISYSTEM, "-q", teil_1])
    spender = subprocess.run(["lsblk", "-J", "-o", "PATH,PARTUUID", teil_1],
                             capture_output=True, text=True)
    if spender.returncode != 0:
        raise RuntimeError("lsblk fiel aus")
    partuuid = json.loads(spender.stdout)["blockdevices"][0]["partuuid"]

    ort = "/farb-os-boden"
    os.makedirs(ort, exist_ok=True)
    _lauf(["mount", teil_1, ort])
    try:
        os.makedirs(os.path.join(ort, "boot", "grub"), exist_ok=True)
        os.makedirs(os.path.join(ort, "farb-os", "home"), exist_ok=True)
        shutil.copy(vmlinuz, os.path.join(ort, "boot", "vmlinuz"))
        shutil.copy(initramfs, os.path.join(ort, "boot", "initramfs.img"))
        with open(os.path.join(ort, "boot", "grub", "grub.cfg"), "w") as f:
            f.write(GRUB_BODEN.format(partuuid=partuuid))
        if os.path.exists("/sys/firmware/efi"):
            _lauf(["grub-install", "--target=x86_64-efi", "--efi-directory=" + ort,
                   "--boot-directory=" + os.path.join(ort, "boot"), "--removable", platte])
        else:
            _lauf(["grub-install", "--target=i386-pc",
                   "--boot-directory=" + os.path.join(ort, "boot"), platte])
    finally:
        _lauf(["sync"])
        subprocess.run(["umount", ort])
        os.rmdir(ort)

    _loggen("boden-" + os.path.basename(platte), "gepflanzt", erlaubt=True)
    print(f"[BODEN] Das Unikat wohnt jetzt in {teil_1} (PARTUUID {partuuid}).")
    return {"boden": teil_1, "partuuid": partuuid}


if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            print("Aufruf: python3 Boden.py /dev/sdX   (der Boden, ganz oder gar nicht)")
            sys.exit(1)
        anbauen(sys.argv[1])
    except RuntimeError as weh:
        print(f"[BODEN] Verweigert: {weh}")
        sys.exit(1)
