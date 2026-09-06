# Sphere.py – Colorverse Sphere Unit (Optimized)
# Fixed: Removed debug prints
from config import *


class Sphere:
    """
    Sphere of Rings.
    
    Aggregates color and metric values from all rings in the sphere.
    Also calculates meta-values (energy, harmony, drift) based on color properties.
    
    Attributes:
        ringe: List of Ring objects
        hue_avg, sat_avg, bri_avg: Average color values
        energy_avg, harmonie_avg, drift_avg: Meta values
    """
    
    def __init__(self, ring_liste):
        """
        Initialize a Sphere with a list of Rings.
        
        Args:
            ring_liste: List of Ring objects
        """
        self.ringe = ring_liste

        # Aggregated color values
        self.hue_avg = 0.0
        self.sat_avg = 0.0
        self.bri_avg = 0.0

        # Meta values
        self.energy_avg = 0.0
        self.harmonie_avg = 0.0
        self.drift_avg = 0.0

    def update(self):
        """Update the Sphere by updating all rings and aggregating values."""
        self.update_sphere()

    def update_sphere(self):
        """
        Core Sphere update:
        1. Update all rings
        2. Aggregate color values
        3. Calculate meta values
        """
        # Update all rings
        for r in self.ringe:
            r.update()

        # Aggregate color values and calculate meta values
        self.berechne_sphere_farbsatz()

    def berechne_sphere_farbsatz(self):
        """
        Calculate aggregated color values and meta values from all rings.
        
        Meta values:
        - energy: Derived from brightness (best energy proxy in Colorverse)
        - harmonie: Based on hue stability (1 - hue variance)
        - drift: Based on saturation variation
        """
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
            # Ring color values
            h, s, b = r.get_farbsatz()
            hues.append(h)
            sats.append(s)
            bris.append(b)

            # Meta values: Brightness is the best energy proxy
            energies.append(b)

            # Harmony: Based on hue stability (distance from average)
            if self.hue_avg != 0:
                harmonies.append(1.0 - abs(h - self.hue_avg) / 360)
            else:
                harmonies.append(1.0)
            
            # Drift: Based on saturation variation
            drifts.append(abs(s - self.sat_avg))

        # Calculate averages
        self.hue_avg = sum(hues) / len(hues)
        self.sat_avg = sum(sats) / len(sats)
        self.bri_avg = sum(bris) / len(bris)
        self.energy_avg = sum(energies) / len(energies)
        self.harmonie_avg = sum(harmonies) / len(harmonies)
        self.drift_avg = sum(drifts) / len(drifts)

    def get_farbsatz(self):
        """Return the aggregated color set for MetaSphere."""
        return (self.hue_avg, self.sat_avg, self.bri_avg)
