# Ring.py – Colorverse Ring Unit (Optimized)
# Fixed: Removed debug prints
from config import *


class Ring:
    """
    Ring of Clusters.
    
    Aggregates color and metric values from all clusters in the ring.
    
    Attributes:
        cluster: List of Cluster objects
        hue_avg, sat_avg, bri_avg: Average color values
    """
    
    def __init__(self, cluster_liste):
        """
        Initialize a Ring with a list of Clusters.
        
        Args:
            cluster_liste: List of Cluster objects
        """
        self.cluster = cluster_liste

        # Aggregated color values
        self.hue_avg = 0.0
        self.sat_avg = 0.0
        self.bri_avg = 0.0

    def update(self):
        """Update the Ring by updating all clusters and aggregating values."""
        self.update_ring()

    def update_ring(self):
        """
        Core Ring update:
        1. Update all clusters
        2. Aggregate color values
        """
        # Update all clusters
        for c in self.cluster:
            c.update()

        # Aggregate color values
        self.berechne_ring_farbsatz()

    def berechne_ring_farbsatz(self):
        """
        Calculate average color values from all clusters.
        If no clusters, all values are set to 0.
        """
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

    def get_farbsatz(self):
        """Return the aggregated color set for Sphere."""
        return (self.hue_avg, self.sat_avg, self.bri_avg)
