import math
# Cluster.py – Harmonische Aggregation zwischen Zelle und Ring
from config import *

class Cluster:
    def __init__(self, zellen, engine=None):
        if len(zellen) != 11:
            raise ValueError("Ein Cluster besteht aus genau 11 Zellen.")

        self.zellen = zellen
        self.engine = engine

        # Aggregierte Werte (für Ring + Sphere)
        self.hue_avg = 0.0
        self.sat_avg = 0.0
        self.bri_avg = 0.0
        self.energy_avg = 0.0

        # Meta-Werte
        self.harmonie_avg = 0.0
        self.drift_avg = 0.0
        self.varianz = 0.0

        # Farbsatz (für get_farbsatz)
        self.farbsatz_hue = 0.0
        self.farbsatz_saturation = 0.0
        self.farbsatz_brightness = 0.0

    # ---------------------------------------------------------
    # Öffentliche Update-Methode
    # ---------------------------------------------------------
    def update(self):
        self.update_cluster()

        # interne Hex-Stabilisierung
        for i, z in enumerate(self.zellen):
            left = self.zellen[(i - 1) % len(self.zellen)]
            right = self.zellen[(i + 1) % len(self.zellen)]
            z.nachbarn = [left, right]

    # ---------------------------------------------------------
    # 1. Update aller Zellen + Mutation
    # ---------------------------------------------------------
    def update_cluster(self):

        # 1.1 Zellen updaten
        for z in self.zellen:
            z.update()

        # 1.2 Clusterwerte berechnen
        self.berechne_clusterwerte()
        self.berechne_farbsatz()

        # 1.3 Mutation anwenden
        self.mutation()

    # ---------------------------------------------------------
    # 2. Clusterwerte berechnen
    # ---------------------------------------------------------
    def berechne_clusterwerte(self):
        hues = [z.hue for z in self.zellen]
        sats = [z.saturation for z in self.zellen]
        bris = [z.brightness for z in self.zellen]
        energies = [z.energy for z in self.zellen]
        drifts = [z.drift for z in self.zellen]
        harmonien = [z.harmonie for z in self.zellen]

        # Durchschnittswerte
        self.hue_avg = sum(hues) / len(hues)
        self.sat_avg = sum(sats) / len(sats)
        self.bri_avg = sum(bris) / len(bris)
        self.energy_avg = sum(energies) / len(energies)

        self.drift_avg = sum(drifts) / len(drifts)
        self.harmonie_avg = sum(harmonien) / len(harmonien)

        # Varianz für Farbdynamik
        self.varianz = sum((h - self.hue_avg)**2 for h in hues) / len(hues)

    # ---------------------------------------------------------
    # 3. Farbsatz berechnen (für Ring)
    # ---------------------------------------------------------
    def berechne_farbsatz(self):
        self.farbsatz_hue = (self.hue_avg + (self.varianz / 180.0) * 5.0) % 360
        self.farbsatz_saturation = max(0.0, min(1.0, self.sat_avg + 0.1 * (self.harmonie_avg - 0.5)))
        self.farbsatz_brightness = max(0.0, min(1.0, self.bri_avg - 0.1 * self.drift_avg))

    # ---------------------------------------------------------
    # 4. Mutation
    # ---------------------------------------------------------
    def mutation(self):
        if self.engine is None:
            return

        # Kern (Zellen 0–2)
        for z in self.zellen[:3]:
            z.drift *= 0.8
            z.harmonie = min(1.0, z.harmonie + 0.05)

        # Sub-Moleküle (Zellen 3–9)
        for z in self.zellen[3:10]:
            z.hue += z.drift * 2.0
            z.saturation += (z.energy - 0.5) * 0.05
            z.brightness += (1 - self.engine.harmonie_feld["global_harmonie"]) * 0.02
            z.clamp()

        # Edger (Zelle 10)
        edger = self.zellen[10]
        freie = [z for z in self.engine.zellen if not z.in_cluster]

        for f in freie:
            if abs(f.hue - edger.hue) < 20 and f.drift > 0.3:
                f.in_cluster = True
                self.zellen.append(f)
                f.energy *= 0.5
                f.drift *= 0.3
                f.harmonie = 1.0

                # Cluster bleibt bei 11 Zellen
                if len(self.zellen) > 11:
                    self.zellen = self.zellen[-11:]

    # ---------------------------------------------------------
    # 5. Ausgabe für Ring
    # ---------------------------------------------------------
    def get_farbsatz(self):
        return (
            self.farbsatz_hue,
            self.farbsatz_saturation,
            self.farbsatz_brightness
        )

