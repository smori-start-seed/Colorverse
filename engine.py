# engine.py – Colorverse Evolution Engine
from config import *
from Cluster import Cluster
from Ring import Ring
from Sphere import Sphere
from MetaSphere import MetaSphere
from UniverseNode import UniverseNode

class Engine:
    def __init__(self):
        self.zellen = []
        self.cluster = []
        self.ringe = []
        self.spheren = []

        self.metasphere = MetaSphere(self.spheren)

        self.harmonie_feld = {
            "global_harmonie": 0.87,
            "global_drift": 0.4,
            "stoerimpulse": 0.515,
        }

        self.universe = UniverseNode(self, self.metasphere)
        self.step_count = 0


    def hexagon_fluidity(self):
        n = len(self.zellen)

        for idx, z in enumerate(self.zellen):

            # Cluster-Zellen bleiben stabil
            if z.in_cluster:
                continue

            # Fluidität abhängig von Drift + Harmonie + Energie
            if z.drift > 0.2 and z.energy > 0.3:

                # Fluiditätsfaktor: Drift + Disharmonie
                shift = int((z.drift + (1 - z.harmonie)) * 6)
                shift = (shift + idx) % n

                z.nachbarn = [
                    self.zellen[(idx - 1 + shift) % n],
                    self.zellen[(idx + 1 + shift) % n],
                    self.zellen[(idx - 2 + shift) % n],
                    self.zellen[(idx + 2 + shift) % n],
                    self.zellen[(idx - 3 + shift) % n],
                    self.zellen[(idx + 3 + shift) % n],
                ]

    # =====================================================================
    #  HAUPT-SCHRITT DER EVOLUTION
    # =====================================================================
    def step(self):
    
        self.step_count += 1
        # 1. Zellen updaten
        for z in self.zellen:
            z.update()

        # 2. Cluster updaten
        for c in self.cluster:
            c.update()
    
        # 3. Ringe updaten
        for r in self.ringe:
            r.update()

        # 4. Sphären updaten
        for s in self.spheren:
            s.update()

        # 5. MetaSphere updaten
        if self.metasphere:
            self.metasphere.update()

        # 6. UniverseNode updaten
        if ENABLE_UNIVERSE and self.universe:
            self.universe.update_universe()

        # 7. Hexagon-Fluidity (Dynamische Nachbarschaften)
        self.hexagon_fluidity()

        # 8. Optional: Wander-System
        # self.hexagon_wander()

        # ===================== EVOLUTIONSSYSTEM ==============
        # =====================================================

        #------------------------------------------------------
        # Harmonie-Feld aktualisieren
        #------------------------------------------------------
        if self.zellen:
            self.harmonie_feld["global_harmonie"] = (
                sum(z.harmonie for z in self.zellen) / len(self.zellen)
            )
            self.harmonie_feld["global_drift"] = (
                sum(z.drift for z in self.zellen) / len(self.zellen)
            )

        # ---------------------------------------------------------
        # freie Zellen sammeln
        # ---------------------------------------------------------
        freie = [z for z in self.zellen if not z.in_cluster]

        # ---------------------------------------------------------
        # freie Zellen → Evolutionskeime markieren
        # ---------------------------------------------------------
        for z in freie:
            z.evolutionskeim = (
                z.drift > 0.4 and
                z.energy > 0.6 and
                z.harmonie < 0.5
            )

        # ---------------------------------------------------------
        # 3er-Störimpulse erzeugen
        # ---------------------------------------------------------
        keime = [z for z in freie if z.evolutionskeim]
        dreier = [
            keime[i:i+3]
            for i in range(0, len(keime), 3)
            if len(keime[i:i+3]) == 3
        ]

        for gruppe in dreier:
            for z in gruppe:
                z.energy += 0.1
                z.drift += 0.05
            self.harmonie_feld["stoerimpulse"] += 0.2

        # ---------------------------------------------------------
        # Harmonie-Feld-Resonanz auf alle Zellen anwenden
        # ---------------------------------------------------------
        for z in self.zellen:
            z.drift += self.harmonie_feld["stoerimpulse"] * 0.01
            z.energy += (1 - self.harmonie_feld["global_harmonie"]) * 0.005

        # ---------------------------------------------------------
        # automatische Clusterbildung aus Evolutionskeimen
        # ---------------------------------------------------------
        neue_cluster = []
        keime = [z for z in self.zellen if z.evolutionskeim and not z.in_cluster]

        for i in range(0, len(keime), 11):
            chunk = keime[i:i+11]
            if len(chunk) == 11:
                c = Cluster(chunk, engine=self)
                neue_cluster.append(c)

                for z in chunk:
                    z.in_cluster = True
                    z.evolutionskeim = False
                    z.energy *= 0.5
                    z.drift *= 0.2
                    z.harmonie = 1.0

                self.harmonie_feld["stoerimpulse"] *= 0.5

        self.cluster.extend(neue_cluster)
        print(f"[ENGINE] step={self.step_count} harm={self.harmonie_feld['global_harmonie']:.2f} drift={self.harmonie_feld['global_drift']:.2f} stoer={self.harmonie_feld['stoerimpulse']:.2f}")

