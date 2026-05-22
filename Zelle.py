import math
from config import *
class Zelle:
    def __init__(self, hue=0.0, saturation=0.5, brightness=0.5, energy=1.0):
        # Grundwerte
        self.hue = hue
        self.saturation = saturation
        self.brightness = brightness
        self.energy = energy

        # Dynamische Werte
        self.drift = 0.0
        self.harmonie = 1.0

        # Nachbarn (Engine setzt das)
        self.nachbarn = []

        # Parameter
        self.alpha = 0.05
        self.beta  = 0.03
        self.gamma = 0.02

        # Micro‑Hexagon
        self.hex = None

        # Cluster‑Status
        self.in_cluster = False

        # Evolutionskeim
        self.evolutionskeim = False

    def clamp(self):
        self.hue %= 360
        self.saturation = max(0, min(1, self.saturation))
        self.brightness = max(0, min(1, self.brightness))
        self.energy = max(0, min(1, self.energy))
        self.drift = max(0, min(1, self.drift))
        self.harmonie = max(0, min(1, self.harmonie))

    def berechne_drift(self):
        if not self.nachbarn:
            self.drift = 0.0
            return

        diffs = []
        for n in self.nachbarn:
            d = abs(self.hue - n.hue)
            d = min(d, 360 - d)
            diffs.append(d)

        self.drift = (sum(diffs) / len(diffs)) / 180.0

    def berechne_harmonie(self):
        if not self.nachbarn:
            self.harmonie = 1.0
            return

        hues = [n.hue for n in self.nachbarn]
        avg = sum(hues) / len(hues)
        var = sum((h - avg)**2 for h in hues) / len(hues)

        self.harmonie = 1.0 - min(1.0, var / 180.0)

    def failsafe(self):
        if (self.saturation < 0.15 or
            self.brightness < 0.05 or
            self.drift > 0.7 or
            self.harmonie < 0.2):

            self.hue = 0
            self.saturation = 0
            self.brightness = 0
            self.drift = 0
            self.harmonie = 1
            return True

        if (self.saturation > 0.85 and
            self.brightness > 0.95 and
            self.harmonie > 0.8):

            self.hue = 0
            self.saturation = 0
            self.brightness = 1
            self.drift = 0
            self.harmonie = 1
            return True

        return False

    def stabilisierung(self):
        if not self.nachbarn:
            return

        avg_hue = sum(n.hue for n in self.nachbarn) / len(self.nachbarn)
        self.hue = (1 - self.alpha) * self.hue + self.alpha * avg_hue

        self.saturation += self.beta * (self.harmonie - 0.5)
        self.brightness -= self.gamma * self.drift

        self.clamp()

    def update(self):
        if self.hex:
            self.hex.apply(self)
            print(f"[ZELLE] hue={self.hue:.2f} sat={self.saturation:.2f} bri={self.brightness:.2f} energy={self.energy:.2f}")


        self.clamp()
        self.berechne_drift()
        self.berechne_harmonie()

        if self.failsafe():
            return

        self.stabilisierung()
        
