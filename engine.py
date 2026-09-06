# engine.py – Colorverse Evolution Engine (Optimized)
# Fixed: Removed double updates, corrected initialization, single harmonie_feld update
from config import *


class Engine:
    def __init__(self):
        """
        Initialize the Colorverse engine with empty containers.
        MetaSphere and UniverseNode are created in build_world() to avoid
        circular references and empty list issues.
        """
        self.zellen = []
        self.cluster = []
        self.ringe = []
        self.spheren = []
        self.metasphere = None  # Will be created in build_world
        self.universe = None    # Will be created in build_world
        
        # Global harmony field - initialized with config defaults
        self.harmonie_feld = {
            "global_harmonie": GLOBAL_HARMONIE_START,
            "global_drift": GLOBAL_DRIFT_START,
            "stoerimpulse": GLOBAL_STOER_START,
        }
        self.step_count = 0

    def hexagon_fluidity(self):
        """
        Dynamic neighbor assignment based on drift and harmony.
        Cells in clusters are skipped as they have fixed neighbors.
        """
        n = len(self.zellen)
        for idx, z in enumerate(self.zellen):
            # Cluster cells have fixed neighbors
            if z.in_cluster:
                continue

            # Only apply fluidity if cell has sufficient drift and energy
            if z.drift > 0.2 and z.energy > 0.3:
                # Calculate shift based on drift and disharmony
                shift = int((z.drift + (1 - z.harmonie)) * 6)
                shift = (shift + idx) % n

                # Assign 6 hexagonal neighbors
                z.nachbarn = [
                    self.zellen[(idx - 1 + shift) % n],
                    self.zellen[(idx + 1 + shift) % n],
                    self.zellen[(idx - 2 + shift) % n],
                    self.zellen[(idx + 2 + shift) % n],
                    self.zellen[(idx - 3 + shift) % n],
                    self.zellen[(idx + 3 + shift) % n],
                ]

    def step(self):
        """
        Main evolution step. Updates all layers in hierarchy:
        1. Cells (atomic units)
        2. Clusters (aggregation only, no cell updates)
        3. Rings
        4. Spheres
        5. MetaSphere
        6. UniverseNode
        7. Dynamic neighbors
        8. Global harmony field (single update)
        9. Evolution system (seeds, disturbances)
        """
        self.step_count += 1

        # =====================================================
        # 1. Update all cells (ONLY HERE - no duplicates!)
        # =====================================================
        for z in self.zellen:
            z.update()

        # =====================================================
        # 2. Update clusters (aggregation only)
        # =====================================================
        for c in self.cluster:
            c.update()

        # =====================================================
        # 3. Update rings
        # =====================================================
        for r in self.ringe:
            r.update()

        # =====================================================
        # 4. Update spheres
        # =====================================================
        for s in self.spheren:
            s.update()

        # =====================================================
        # 5. Update MetaSphere
        # =====================================================
        if self.metasphere:
            self.metasphere.update()

        # =====================================================
        # 6. Update UniverseNode
        # =====================================================
        if ENABLE_UNIVERSE and self.universe:
            self.universe.update_universe()

        # =====================================================
        # 7. Dynamic neighbor assignment
        # =====================================================
        self.hexagon_fluidity()

        # =====================================================
        # 8. Update global harmony field (SINGLE UPDATE!)
        # =====================================================
        if self.zellen:
            self.harmonie_feld["global_harmonie"] = (
                sum(z.harmonie for z in self.zellen) / len(self.zellen)
            )
            self.harmonie_feld["global_drift"] = (
                sum(z.drift for z in self.zellen) / len(self.zellen)
            )

        # =====================================================
        # 9. Evolution System
        # =====================================================
        
        # --- 9.1: Mark evolution seeds (free cells only) ---
        freie = [z for z in self.zellen if not z.in_cluster]
        for z in freie:
            z.evolutionskeim = (
                z.drift > DRIFT_THRESHOLD and
                z.energy > ENERGY_THRESHOLD and
                z.harmonie < HARMONIE_THRESHOLD
            )

        # --- 9.2: Create triple disturbances ---
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

        # --- 9.3: Apply harmony field resonance to all cells ---
        for z in self.zellen:
            z.drift += self.harmonie_feld["stoerimpulse"] * 0.01
            z.energy += (1 - self.harmonie_feld["global_harmonie"]) * 0.005

        # --- 9.4: Automatic cluster formation from evolution seeds ---
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

        # =====================================================
        # 10. Debug output (controlled by config)
        # =====================================================
        if ENABLE_LOGGING and self.step_count % DEBUG_INTERVAL == 0:
            print(f"[ENGINE] step={self.step_count} harm={self.harmonie_feld['global_harmonie']:.2f} "
                  f"drift={self.harmonie_feld['global_drift']:.2f} stoer={self.harmonie_feld['stoerimpulse']:.2f}")
