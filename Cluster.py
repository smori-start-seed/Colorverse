# Cluster.py – Colorverse Cluster Unit (Optimized)
# Fixed: Removed neighbor overwriting in mutation(), improved stability
import math
from config import *


class Cluster:
    """
    Cluster of 11 cells with internal role differentiation.
    
    Roles:
        - Kern (Cells 0-2): Core cells, high stability
        - Sub-Moleküle (Cells 3-9): Dynamic cells, moderate stability
        - Edger (Cell 10): Edge cell, recruitment role
    
    Attributes:
        zellen: List of 11 cells
        engine: Reference to the Engine
        hue_avg, sat_avg, bri_avg: Average color values
        energy_avg: Average energy
        harmonie_avg, drift_avg: Average metrics
        farbsatz_*: Aggregated color set for Ring
        varianz: Hue variance within cluster
    """
    
    def __init__(self, zellen, engine=None):
        """
        Initialize a cluster with exactly 11 cells.
        
        Args:
            zellen: List of exactly 11 Zelle objects
            engine: Reference to the Engine (optional)
        """
        if len(zellen) != 11:
            raise ValueError("Ein Cluster besteht aus genau 11 Zellen.")

        self.zellen = zellen
        self.engine = engine

        # Aggregated values (for Ring + Sphere)
        self.hue_avg = 0.0
        self.sat_avg = 0.0
        self.bri_avg = 0.0
        self.energy_avg = 0.0

        # Meta values
        self.harmonie_avg = 0.0
        self.drift_avg = 0.0
        self.varianz = 0.0

        # Color set (for get_farbsatz)
        self.farbsatz_hue = 0.0
        self.farbsatz_saturation = 0.0
        self.farbsatz_brightness = 0.0

    def update(self):
        """
        Update cluster:
        1. Update all cells
        2. Calculate cluster values
        3. Calculate color set
        4. Apply mutation
        5. Set internal neighbors (without overwriting Engine neighbors)
        """
        self.update_cluster()

        # Internal neighbors for cluster cells (only for stabilization within cluster)
        # This does NOT overwrite the main neighbors set by Engine!
        for i, z in enumerate(self.zellen):
            left = self.zellen[(i - 1) % len(self.zellen)]
            right = self.zellen[(i + 1) % len(self.zellen)]
            # Only set if cell doesn't already have neighbors from Engine
            if not z.nachbarn:
                z.nachbarn = [left, right]

    def update_cluster(self):
        """
        Core cluster update:
        1. Update all cells
        2. Calculate cluster values
        3. Calculate color set
        4. Apply mutation
        """
        # 1. Update all cells
        for z in self.zellen:
            z.update()

        # 2. Calculate cluster values
        self.berechne_clusterwerte()
        self.berechne_farbsatz()

        # 3. Apply mutation
        self.mutation()

    def berechne_clusterwerte(self):
        """Calculate average values for all cells in the cluster."""
        hues = [z.hue for z in self.zellen]
        sats = [z.saturation for z in self.zellen]
        bris = [z.brightness for z in self.zellen]
        energies = [z.energy for z in self.zellen]
        drifts = [z.drift for z in self.zellen]
        harmonien = [z.harmonie for z in self.zellen]

        # Average values
        self.hue_avg = sum(hues) / len(hues)
        self.sat_avg = sum(sats) / len(sats)
        self.bri_avg = sum(bris) / len(bris)
        self.energy_avg = sum(energies) / len(energies)

        self.drift_avg = sum(drifts) / len(drifts)
        self.harmonie_avg = sum(harmonien) / len(harmonien)

        # Variance for color dynamics
        self.varianz = sum((h - self.hue_avg)**2 for h in hues) / len(hues)

    def berechne_farbsatz(self):
        """
        Calculate color set for Ring aggregation.
        Adds variance-based adjustments to create unique cluster colors.
        """
        self.farbsatz_hue = (self.hue_avg + (self.varianz / 180.0) * 5.0) % 360
        self.farbsatz_saturation = max(0.0, min(1.0, self.sat_avg + 0.1 * (self.harmonie_avg - 0.5)))
        self.farbsatz_brightness = max(0.0, min(1.0, self.bri_avg - 0.1 * self.drift_avg))

    def mutation(self):
        """
        Apply role-based mutations to cluster cells:
        - Kern (0-2): Stabilize
        - Sub-Moleküle (3-9): Dynamic adjustments
        - Edger (10): Recruitment (but does NOT modify cluster size)
        
        Note: Cluster size remains fixed at 11 cells.
        New cells are marked for Engine to create new clusters.
        """
        if self.engine is None:
            return

        # Kern (Cells 0-2): High stability
        for z in self.zellen[:3]:
            z.drift *= 0.8
            z.harmonie = min(1.0, z.harmonie + 0.05)

        # Sub-Moleküle (Cells 3-9): Dynamic behavior
        for z in self.zellen[3:10]:
            z.hue += z.drift * 2.0
            z.saturation += (z.energy - 0.5) * 0.05
            z.brightness += (1 - self.engine.harmonie_feld["global_harmonie"]) * 0.02
            z.clamp()

        # Edger (Cell 10): Recruitment role
        # Find free cells that match the edger's hue and have high drift
        edger = self.zellen[10]
        freie = [z for z in self.engine.zellen if not z.in_cluster]

        for f in freie:
            if abs(f.hue - edger.hue) < 20 and f.drift > 0.3:
                # Mark for cluster formation (Engine will handle)
                f.in_cluster = True
                f.energy *= 0.5
                f.drift *= 0.3
                f.harmonie = 1.0
                
                # DO NOT add to this cluster - size must stay at 11
                # Instead, let Engine create new clusters from marked cells

    def get_farbsatz(self):
        """Return the aggregated color set for Ring."""
        return (
            self.farbsatz_hue,
            self.farbsatz_saturation,
            self.farbsatz_brightness
        )
