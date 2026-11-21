# Gedaechtnis.py – HW-gebundene Erinnerung des Colorverse
# Das Unikat lebt nur auf seiner Hardware: Der Schluessel
# entsteht aus der Hardware-Signatur, ohne sie gibt es kein Lesen.
import hashlib
import json
import os
from config import *
from HwScan import scan as _hw_scan, stabile_signatur as _hw_stabil


# ============================================================
#  HARDWARE-SIGNATUR (ruhiger Kern - siehe installation.py)
# ============================================================

def hardware_signatur():
    return _hw_stabil(_hw_scan())


def _schluessel():
    sig = hardware_signatur().encode()
    s = sig
    for _ in range(HASH_DURCHLAEUFE):
        s = hashlib.sha256(s + sig).digest()
    return s


# ============================================================
#  VERSCHLUESSELUNG (Strom-Chiffre, stdlib-only)
# ============================================================

def _strom(laenge, nonce):
    schluessel = _schluessel()
    out = bytearray()
    block = hashlib.sha256(schluessel + nonce).digest()
    while len(out) < laenge:
        out += block
        block = hashlib.sha256(block + schluessel).digest()
    return bytes(out[:laenge])


def _verschluesseln(daten):
    nonce = os.urandom(16)
    strom = _strom(len(daten), nonce)
    return nonce + bytes(a ^ b for a, b in zip(daten, strom))


def _entschluesseln(paket):
    nonce, daten = paket[:16], paket[16:]
    strom = _strom(len(daten), nonce)
    return bytes(a ^ b for a, b in zip(daten, strom))


# ============================================================
#  ZUSTAND
# ============================================================

def _zustand(engine):
    return {
        "schritt": engine.step_count,
        "feld": dict(engine.harmonie_feld),
        "zellen": [
            {
                "hue": z.hue,
                "saturation": z.saturation,
                "brightness": z.brightness,
                "energy": z.energy,
                "drift": z.drift,
                "harmonie": z.harmonie,
                "in_cluster": z.in_cluster,
                "evolutionskeim": z.evolutionskeim,
            }
            for z in engine.zellen
        ],
    }


# ============================================================
#  SPEICHERN & LADEN
# ============================================================

def speichern(engine):
    zustand = _zustand(engine)
    zustand.pop("pruefsumme", None)
    pruefsumme = hashlib.sha256(json.dumps(zustand).encode()).hexdigest()
    zustand["pruefsumme"] = pruefsumme
    paket = _verschluesseln(json.dumps(zustand).encode())

    with open(GEDAECHTNIS_TEMPO, "wb") as f:
        f.write(paket)
        f.flush()
        os.fsync(f.fileno())
    os.replace(GEDAECHTNIS_TEMPO, GEDAECHTNIS_DATEI)
    return True


def laden(engine):
    if not os.path.exists(GEDAECHTNIS_DATEI):
        return False

    with open(GEDAECHTNIS_DATEI, "rb") as f:
        paket = f.read()

    try:
        zustand = json.loads(_entschluesseln(paket).decode())
    except (UnicodeDecodeError, json.JSONDecodeError):
        return False

    pruefsumme = zustand.pop("pruefsumme", None)
    if not pruefsumme:
        return False
    if hashlib.sha256(json.dumps(zustand).encode()).hexdigest() != pruefsumme:
        return False

    if len(zustand["zellen"]) != len(engine.zellen):
        return False

    for z, snap in zip(engine.zellen, zustand["zellen"]):
        z.hue = snap["hue"]
        z.saturation = snap["saturation"]
        z.brightness = snap["brightness"]
        z.energy = snap["energy"]
        z.drift = snap["drift"]
        z.harmonie = snap["harmonie"]
        z.in_cluster = snap["in_cluster"]
        z.evolutionskeim = snap["evolutionskeim"]

    engine.harmonie_feld.update(zustand["feld"])
    engine.step_count = zustand["schritt"]
    return True
