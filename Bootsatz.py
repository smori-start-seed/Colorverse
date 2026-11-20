# Bootsatz.py – Das bootfahige Medium (Bootstrap, Stufe 2)
# Ein Kernel, eine initramfs-Wurzel, kein Login, keine Shell:
# das Colorverse atmet als PID 1 - die Farbsprache ist die erste Sprache.
# Die Systemwerkzeuge borgt es vom Host (Kernel, cpio, gzip, grub-mkrescue).
import os
import glob
import shutil
import subprocess
import sys
import tarfile
import urllib.request
from config import *

PYTHON_TAR = "cpython_install_only.tar.gz"


# ============================================================
#  KLEINE WERKZEUGE
# ============================================================

def _lauf(befehl, cwd=None):
    ergebnis = subprocess.run(befehl, cwd=cwd, capture_output=True, text=True)
    if ergebnis.returncode != 0:
        raise RuntimeError(f"{befehl[0]} fiel aus: {ergebnis.stderr.strip()[:400]}")
    return ergebnis.stdout


def _brauche(werkzeug, hinweis):
    if shutil.which(werkzeug) is None:
        raise RuntimeError(f"{werkzeug} fehlt - {hinweis}")


def kerne():
    gefundene = []
    for muster in ("/boot/vmlinuz-*", "/lib/modules/*/vmlinuz*"):
        gefundene = gefundene + [p for p in glob.glob(muster) if os.access(p, os.R_OK)]
    return sorted(gefundene, reverse=True)


def _python_saehen(wurzel):
    ort = os.path.join(wurzel, "farb-os", "python")
    if os.path.exists(os.path.join(ort, "bin", "python3")):
        return ort
    tar_pfad = os.path.join(BOOT_ORDNER, PYTHON_TAR)
    if not os.path.exists(tar_pfad):
        os.makedirs(BOOT_ORDNER, exist_ok=True)
        print(f"[BOOTSATZ] hole Python von {BODEN_PYTHON_URL}")
        urllib.request.urlretrieve(BODEN_PYTHON_URL, tar_pfad)
    with tarfile.open(tar_pfad) as tar:
        try:
            tar.extractall(wurzel, filter="data")
        except TypeError:
            tar.extractall(wurzel)
    shutil.move(os.path.join(wurzel, "python"), ort)
    return ort


INIT_SKRIPT = """#!/bin/sh
mount -t proc none /proc 2>/dev/null
mount -t sysfs none /sys 2>/dev/null
mount -t devtmpfs none /dev 2>/dev/null
mkdir -p /run /farb-os/home
mount -t tmpfs none /run 2>/dev/null
BODEN=$(cat /proc/cmdline | tr ' ' '\\n' | grep '^boden=PARTUUID=' | cut -d= -f3)
[ -n "$BODEN" ] && mount -t auto /dev/disk/by-partuuid/$BODEN /farb-os/home 2>/dev/null
grep -q ' /farb-os/home ' /proc/mounts || mount -t tmpfs none /farb-os/home 2>/dev/null
[ -e /farb-os/python/bin/python3 ] && echo [INIT] BIN_OK || echo [INIT] BIN_FEHLT
[ -e /lib64/ld-linux-x86-64.so.2 ] && echo [INIT] LDR_OK || echo [INIT] LDR_FEHLT
cd /farb-os/home
exec /farb-os/python/bin/python3 -u /farb-os/os/farb_os.py
"""


GRUB_CFG = """set timeout={timeout}
serial --unit=0 --speed=115200
terminal_input serial console
terminal_output serial console
menuentry "FARB-OS" {{
    linux /boot/vmlinuz console=tty0 console=ttyS0,115200
    initrd /boot/initramfs.img
}}
"""


# ============================================================
#  GLIBC-KRAM - Python braucht seinen Unterbau
# ============================================================

def _kram_kopieren(wurzel, programm):
    bericht = _lauf(["ldd", programm])
    zu_kopieren = []
    for loader in ("/lib64/ld-linux-x86-64.so.2", "/lib/ld-linux-x86-64.so.2"):
        if os.path.exists(loader):
            zu_kopieren.append(loader)
    for zeile in bericht.splitlines():
        teile = zeile.strip().split()
        if "=>" in teile and os.path.exists(teile[2]):
            zu_kopieren.append(teile[2])
        elif zeile.strip().startswith("/") and os.path.exists(zeile.strip().split()[0]):
            zu_kopieren.append(zeile.strip().split()[0])
    for quelle in set(zu_kopieren):
        ziel = os.path.join(wurzel, quelle.lstrip("/"))
        os.makedirs(os.path.dirname(ziel), exist_ok=True)
        shutil.copy2(quelle, ziel)
        os.chmod(ziel, 0o755)
    return len(set(zu_kopieren))


# ============================================================
#  INITRAMFS MIT DER WELT IM BAUCH
# ============================================================

def baue_initramfs(ordner=BOOT_ORDNER):
    _brauche("cpio", "auf Debian/Ubuntu: sudo apt install cpio")
    _brauche("gzip", "grundlegend - sollte nie fehlen")
    kernel = kerne()
    if not kernel:
        raise RuntimeError("kein lesbarer Kernel in /boot - der Keim borgt ihn vom Host")
    kernel = kernel[0]

    wurzel = os.path.join(ordner, BODEN_INITRAMFS_ORDNER)
    if os.path.exists(wurzel):
        shutil.rmtree(wurzel)
    for pfad in ("bin", "dev", "proc", "sys", "run", "farb-os/home", "farb-os/os"):
        os.makedirs(os.path.join(wurzel, pfad), exist_ok=True)

    _brauche("busybox", "auf Debian/Ubuntu: sudo apt install busybox-static")
    busybox = shutil.which("busybox") or shutil.which("busybox.static")
    shutil.copy(busybox, os.path.join(wurzel, "bin", "busybox"))
    os.chmod(os.path.join(wurzel, "bin", "busybox"), 0o755)
    for werkzeug in ("sh", "mount", "mkdir", "cat", "sleep", "sync", "tr", "grep", "cut"):
        os.symlink("busybox", os.path.join(wurzel, "bin", werkzeug))

    python_bin = _python_saehen(wurzel)
    kram = _kram_kopieren(wurzel, python_bin + "/bin/python3")
    print(f"[BOOTSATZ] Python gesaet: {python_bin} | Bibliotheken: {kram}")

    probe = subprocess.run([python_bin + "/bin/python3", "--version"], capture_output=True, text=True)
    if probe.returncode != 0:
        raise RuntimeError(f"das gesaete Python spricht nicht: {probe.stderr.strip()[:200]}")
    print("[BOOTSATZ] Probe:", probe.stdout.strip() or probe.stderr.strip())

    os_dir = os.path.dirname(os.path.abspath(__file__))
    for datei in os.listdir(os_dir):
        if datei.endswith(".py"):
            shutil.copy(os.path.join(os_dir, datei), os.path.join(wurzel, "farb-os", "os", datei))

    with open(os.path.join(wurzel, "init"), "w") as f:
        f.write(INIT_SKRIPT)
    os.chmod(os.path.join(wurzel, "init"), 0o755)

    cpio_pfad = os.path.join(ordner, "initramfs.img")
    listing = _lauf(["find", "."], cwd=wurzel)
    with open(cpio_pfad, "wb") as aus:
        hinaus = subprocess.run(["cpio", "-o", "-H", "newc"], cwd=wurzel,
                                input=listing.encode(), stdout=aus)
        if hinaus.returncode != 0:
            raise RuntimeError("cpio fiel aus")
    _lauf(["gzip", "-f", cpio_pfad])

    inhalt = _lauf(["sh", "-c", f"zcat {cpio_pfad}.gz | cpio -it"])
    for pfad in ("./farb-os/python/bin/python3", "./lib64/ld-linux-x86-64.so.2", "./init"):
        if pfad not in inhalt:
            raise RuntimeError(f"{pfad} fehlt im initramfs")

    return kernel, cpio_pfad + ".gz"


# ============================================================
#  ISO - das Medium, das man vor Staub ansteckt
# ============================================================

def baue_iso(ordner=BOOT_ORDNER):
    _brauche("grub-mkrescue", "auf Debian/Ubuntu: sudo apt install xorriso grub-pc-bin")
    kernel, initramfs = baue_initramfs(ordner)

    iso_wurzel = os.path.join(ordner, "iso_wurzel")
    if os.path.exists(iso_wurzel):
        shutil.rmtree(iso_wurzel)
    os.makedirs(os.path.join(iso_wurzel, "boot", "grub"), exist_ok=True)
    shutil.copy(kernel, os.path.join(iso_wurzel, "boot", "vmlinuz"))
    shutil.copy(initramfs, os.path.join(iso_wurzel, "boot", "initramfs.img"))
    with open(os.path.join(iso_wurzel, "boot", "grub", "grub.cfg"), "w") as f:
        f.write(GRUB_CFG.format(timeout=BOOT_TIMEOUT))

    iso_pfad = os.path.join(ordner, "bootsatz.iso")
    _lauf(["grub-mkrescue", "-o", iso_pfad, iso_wurzel])
    print(f"[BOOTSATZ] Medium fertig: {iso_pfad}")
    return iso_pfad


if __name__ == "__main__":
    try:
        if "--iso" in sys.argv:
            baue_iso()
        else:
            kernel, initramfs = baue_initramfs()
            print(f"[BOOTSATZ] Kernel: {kernel}")
            print(f"[BOOTSATZ] Initramfs: {initramfs}")
    except RuntimeError as weh:
        print(f"[BOOTSATZ] Verweigert: {weh}")
        sys.exit(1)
