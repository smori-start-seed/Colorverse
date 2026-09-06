# UniverseNode.py – Colorverse Universe Node (Optimized)
# Fixed: Removed debug prints
from config import *


class UniverseNode:
    """
    Top-level container for the Colorverse.
    
    Tracks global coherence metrics and provides feedback to the system
    through the harmony field. Operates in three modes:
    - "sanft" (gentle): High harmony, low drift
    - "chaotisch" (chaotic): High drift or energy
    - "intelligent" (intelligent): Default balanced mode
    
    Attributes:
        engine: Reference to the Engine
        metasphere: Reference to the MetaSphere
        harmonie, drift, energy: Global state values
        harmonie_trend, drift_trend, energy_trend: Historical trends
        modus: Current evolution mode
    """
    
    def __init__(self, engine, metasphere):
        """
        Initialize the UniverseNode.
        
        Args:
            engine: Reference to the Engine
            metasphere: Reference to the MetaSphere
        """
        self.engine = engine
        self.metasphere = metasphere

        # Global state values
        self.harmonie = 1.0
        self.drift = 0.3
        self.energy = 0.2

        # Trend history (last 200 steps)
        self.harmonie_trend = []
        self.drift_trend = []
        self.energy_trend = []

        # Current evolution mode
        self.modus = "sanft"

    def update(self):
        """Update the UniverseNode and print status."""
        self.update_universe()

    def update_universe(self):
        """
        Core UniverseNode update:
        1. Calculate universe color values from MetaSphere
        2. Update trend history
        3. Select evolution mode
        4. Apply feedback to harmony field
        """
        self.berechne_universe_farbsatz()
        self.berechne_trends()
        self.waehle_modus()
        self.rueckkopplung_ins_evolutionsfeld()

    def berechne_universe_farbsatz(self):
        """
        Calculate universe-level values from MetaSphere.
        If MetaSphere is not available, values remain unchanged.
        """
        if not self.metasphere:
            return

        self.harmonie = self.metasphere.harmonie_avg
        self.drift = self.metasphere.drift_avg
        self.energy = self.metasphere.energy_avg

    def berechne_trends(self):
        """
        Update trend history with current values.
        Keeps only the last 200 values for each metric.
        """
        self.harmonie_trend.append(self.harmonie)
        self.drift_trend.append(self.drift)
        self.energy_trend.append(self.energy)

        # Limit trend history to 200 steps
        if len(self.harmonie_trend) > 200:
            self.harmonie_trend.pop(0)
            self.drift_trend.pop(0)
            self.energy_trend.pop(0)

    def waehle_modus(self):
        """
        Select the evolution mode based on current state:
        - "sanft": High harmony (>0.7) and low drift (<0.3)
        - "chaotisch": High drift (>0.5) or high energy (>0.8)
        - "intelligent": Default for all other cases
        """
        if self.harmonie > 0.7 and self.drift < 0.3:
            self.modus = "sanft"
        elif self.drift > 0.5 or self.energy > 0.8:
            self.modus = "chaotisch"
        else:
            self.modus = "intelligent"

    def rueckkopplung_ins_evolutionsfeld(self):
        """
        Apply feedback to the global harmony field based on current mode.
        
        Different modes apply different feedback strategies:
        - sanft: Reduce drift and disturbances, increase harmony
        - chaotisch: Increase drift and disturbances, reduce harmony
        - intelligent: Balanced feedback
        """
        feld = self.engine.harmonie_feld

        if self.modus == "sanft":
            # Gentle mode: Stabilize the system
            feld["global_harmonie"] = min(1.0, feld["global_harmonie"] * 0.98 + self.harmonie * 0.02)
            feld["global_drift"] *= 0.9
            feld["stoerimpulse"] *= 0.9

        elif self.modus == "chaotisch":
            # Chaotic mode: Introduce more variation
            feld["global_harmonie"] *= 0.9
            feld["global_drift"] = min(1.0, feld["global_drift"] * 1.1 + self.drift * 0.1)
            feld["stoerimpulse"] = min(1.0, feld["stoerimpulse"] * 1.1 + 0.05)

        else:  # intelligent
            # Balanced mode: Smooth feedback
            feld["global_harmonie"] = (feld["global_harmonie"] * 0.95 +
                                       self.harmonie * 0.05)
            feld["global_drift"] = (feld["global_drift"] * 0.95 +
                                    self.drift * 0.05)
            feld["stoerimpulse"] *= 0.97
