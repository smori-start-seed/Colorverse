# Ring.py – Colorverse Evolution
from config import *
class Ring:
    def __init__(self, cluster_liste):
        # Liste von Clustern (11 Zellen pro Cluster)
        self.cluster = cluster_liste

        # Aggregierte Farbsätze
        self.hue_avg = 0.0
        self.sat_avg = 0.0
        self.bri_avg = 0.0

    # ---------------------------------------------------------
    # 1. Öffentliche Update-Methode
    # ---------------------------------------------------------
    def update(self):
        self.update_ring()

    # ---------------------------------------------------------
    # 2. Ring-Update: Cluster updaten + Farbsatz aggregieren
    # ---------------------------------------------------------
    def update_ring(self):

        # 2.1 Alle Cluster updaten
        for c in self.cluster:
            c.update()

        # 2.2 Farbsatz aggregieren
        self.berechne_ring_farbsatz()
        print(f"[RING] hue={self.hue_avg:.2f} sat={self.sat_avg:.2f} bri={self.bri_avg:.2f}")

    # ---------------------------------------------------------
    # 3. Aggregierten Farbsatz berechnen
    # ---------------------------------------------------------
    def berechne_ring_farbsatz(self):
        if not self.cluster:
            self.hue_avg = 0.0
            self.sat_avg = 0.0
            self.bri_avg = 0.0
            return

        hues = []
        sats = []
        bris = []

        for c in self.cluster:
            h, s, b = c.get_farbsatz()
            hues.append(h)
            sats.append(s)
            bris.append(b)

        self.hue_avg = sum(hues) / len(hues)
        self.sat_avg = sum(sats) / len(sats)
        self.bri_avg = sum(bris) / len(bris)

    # ---------------------------------------------------------
    # 4. Ausgabe für Sphere / MetaSphere
    # ---------------------------------------------------------
    def get_farbsatz(self):
        return (self.hue_avg, self.sat_avg, self.bri_avg)

