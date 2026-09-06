# MetaSphere.py – Colorverse MetaSphere Unit (Optimized)
# Fixed: Removed debug prints
from config import *


class MetaSphere:
    """
    MetaSphere of Spheres.
    
    Top-level aggregation unit that collects and averages values from all Spheres.
    Provides the final color and metric values for the UniverseNode.
    
    Attributes:
        spheren: List of Sphere objects
        hue_avg, sat_avg, bri_avg: Average color values
        energy_avg, harmonie_avg, drift_avg: Average meta values
    """
    
    def __init__(self, spheren_liste):
        """
        Initialize a MetaSphere with a list of Spheres.
        
        Args:
            spheren_liste: List of Sphere objects
        """
        self.spheren = spheren_liste

        # Aggregated values
        self.hue_avg = 0.3
        self.sat_avg = 0.2
        self.bri_avg = 0.4

        self.energy_avg = 0.2
        self.harmonie_avg = 0.4
        self.drift_avg = 0.3

    def update(self):
        """Update the MetaSphere by updating all spheres and aggregating values."""
        self.update_metasphere()

    def update_metasphere(self):
        """
        Core MetaSphere update:
        1. Update all spheres
        2. Aggregate all values
        """
        # Update all spheres
        for s in self.spheren:
            s.update()

        # Aggregate all values
        self.berechne_metasphere()

    def berechne_metasphere(self):
        """
        Aggregate all values from all spheres.
        If no spheres, values remain at their initial defaults.
        """
        if not self.spheren:
            return

        hues = []
        sats = []
        bris = []
        energies = []
        harmonies = []
        drifts = []

        for s in self.spheren:
            hues.append(s.hue_avg)
            sats.append(s.sat_avg)
            bris.append(s.bri_avg)

            energies.append(s.energy_avg)
            harmonies.append(s.harmonie_avg)
            drifts.append(s.drift_avg)

        # Calculate averages
        self.hue_avg = sum(hues) / len(hues)
        self.sat_avg = sum(sats) / len(sats)
        self.bri_avg = sum(bris) / len(bris)

        self.energy_avg = sum(energies) / len(energies)
        self.harmonie_avg = sum(harmonies) / len(harmonies)
        self.drift_avg = sum(drifts) / len(drifts)

    def get_meta(self):
        """
        Return all meta values as a dictionary.
        Used by UniverseNode for global state assessment.
        """
        return {
            "hue": self.hue_avg,
            "sat": self.sat_avg,
            "bri": self.bri_avg,
            "energy": self.energy_avg,
            "harmonie": self.harmonie_avg,
            "drift": self.drift_avg
        }

    def get_farbsatz(self):
        """Return the aggregated color set for UniverseNode."""
        return (self.hue_avg, self.sat_avg, self.bri_avg)
