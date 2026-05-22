# Sphere.py – Colorverse Evolution (Ring-basiert, harmonisch)
from config import *

class Sphere:
    def __init__(self, ring_liste):
        # Liste von Ringen (jeder Ring enthält Cluster)
        self.ringe = ring_liste

        # Aggregierte Farbsätze der Sphere
        self.hue_avg = 0.0
        self.sat_avg = 0.0
        self.bri_avg = 0.0

        # Meta-Werte der Sphere
        self.energy_avg = 0.0
        self.harmonie_avg = 0.0
        self.drift_avg = 0.0

    # ---------------------------------------------------------
    # 1. Öffentliche Update-Methode
    # ---------------------------------------------------------
    def update(self):
        self.update_sphere()

    # ---------------------------------------------------------
    # 2. Sphere-Update: Ringe updaten + Farbsatz aggregieren
    # ---------------------------------------------------------
    def update_sphere(self):

        # 2.1 Alle Ringe updaten
        for r in self.ringe:
            r.update()

        # 2.2 Farbsatz aggregieren
        self.berechne_sphere_farbsatz()
        print(f"[SPHERE] hue={self.hue_avg:.2f} sat={self.sat_avg:.2f} bri={self.bri_avg:.2f} energy={self.energy_avg:.2f} harm={self.harmonie_avg:.2f} drift={self.drift_avg:.2f}")


    # ---------------------------------------------------------
    # 3. Aggregierten Farbsatz berechnen
    # ---------------------------------------------------------
    def berechne_sphere_farbsatz(self):
        if not self.ringe:
            self.hue_avg = 0.0
            self.sat_avg = 0.0
            self.bri_avg = 0.0
            self.energy_avg = 0.0
            self.harmonie_avg = 0.0
            self.drift_avg = 0.0
            return

        hues = []
        sats = []
        bris = []
        energies = []
        harmonies = []
        drifts = []

        for r in self.ringe:
            # Ring-Farbsatz
            h, s, b = r.get_farbsatz()
            hues.append(h)
            sats.append(s)
            bris.append(b)

            # Harmonische Energie-Ableitung:
            # Helligkeit ist im Colorverse der beste Energie-Proxy
            energies.append(b)

            # Harmonische Meta-Werte:
            # Drift = Sättigungsvariation, Harmonie = Farbstabilität
            harmonies.append(1.0 - abs(h - self.hue_avg) / 360 if self.hue_avg != 0 else 1.0)
            drifts.append(abs(s - self.sat_avg))

        # Durchschnittswerte
        self.hue_avg = sum(hues) / len(hues)
        self.sat_avg = sum(sats) / len(sats)
        self.bri_avg = sum(bris) / len(bris)
        self.energy_avg = sum(energies) / len(energies)
        self.harmonie_avg = sum(harmonies) / len(harmonies)
        self.drift_avg = sum(drifts) / len(drifts)

    # ---------------------------------------------------------
    # 4. Ausgabe für MetaSphere / Universe
    # ---------------------------------------------------------
    def get_farbsatz(self):
        return (self.hue_avg, self.sat_avg, self.bri_avg)

