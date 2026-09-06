# Zelle.py – Colorverse Cell Unit (Optimized)
# Fixed: Sanfter failsafe, removed debug prints, improved stability
import math
import random
from config import *


class Zelle:
    """
    Atomic unit of the Colorverse.
    
    Attributes:
        hue: Color hue in degrees [0, 360)
        saturation: Color saturation [0, 1]
        brightness: Color brightness [0, 1]
        energy: Cell energy [0, 1]
        drift: Color drift metric [0, 1]
        harmonie: Harmony metric [0, 1]
        nachbarn: List of 6 neighboring cells
        hex: SaturnHexagon rule kernel
        in_cluster: Whether cell is part of a cluster
        evolutionskeim: Whether cell is an evolution seed
    """
    
    def __init__(self, hue=0.0, saturation=0.5, brightness=0.5, energy=1.0):
        # Core color properties
        self.hue = hue
        self.saturation = saturation
        self.brightness = brightness
        self.energy = energy

        # Dynamic metrics
        self.drift = 0.0
        self.harmonie = 1.0

        # Neighbors (set by Engine)
        self.nachbarn = []

        # Stabilization parameters
        self.alpha = 0.05  # Hue stabilization factor
        self.beta = 0.03   # Saturation stabilization factor
        self.gamma = 0.02  # Brightness stabilization factor

        # Rule kernel (SaturnHexagon)
        self.hex = None

        # Cluster status
        self.in_cluster = False
        self.evolutionskeim = False

    def clamp(self):
        """Clamp all values to valid ranges."""
        self.hue %= 360
        self.saturation = max(0, min(1, self.saturation))
        self.brightness = max(0, min(1, self.brightness))
        self.energy = max(0, min(1, self.energy))
        self.drift = max(0, min(1, self.drift))
        self.harmonie = max(0, min(1, self.harmonie))

    def berechne_drift(self):
        """
        Calculate drift as average hue difference to neighbors.
        Drift is normalized to [0, 1] where 0 = no drift, 1 = max drift.
        """
        if not self.nachbarn:
            self.drift = 0.0
            return

        diffs = []
        for n in self.nachbarn:
            d = abs(self.hue - n.hue)
            d = min(d, 360 - d)  # Shortest angular distance
            diffs.append(d)

        # Normalize: max angular difference is 180 degrees
        self.drift = (sum(diffs) / len(diffs)) / 180.0

    def berechne_harmonie(self):
        """
        Calculate harmony as 1 - normalized hue variance.
        Harmony is [0, 1] where 1 = perfect harmony (all neighbors same hue).
        """
        if not self.nachbarn:
            self.harmonie = 1.0
            return

        hues = [n.hue for n in self.nachbarn]
        avg = sum(hues) / len(hues)
        var = sum((h - avg)**2 for h in hues) / len(hues)

        # Normalize: max variance is ~180^2 for hue
        self.harmonie = 1.0 - min(1.0, var / 180.0)

    def failsafe(self):
        """
        Safety mechanism to prevent extreme states.
        Instead of resetting to 0, we reset to safe middle values
        to maintain system stability.
        
        Returns: True if failsafe was triggered, False otherwise
        """
        # Trigger failsafe for extreme low values
        if (self.saturation < 0.15 or
            self.brightness < 0.05 or
            self.drift > 0.7 or
            self.harmonie < 0.2):

            # Reset to safe middle values (NOT 0!)
            self.hue = random.uniform(0, 360)
            self.saturation = 0.5
            self.brightness = 0.5
            self.drift = 0.1
            self.harmonie = 0.8
            self.energy = 0.5
            return True

        # Trigger failsafe for extreme high values
        if (self.saturation > 0.85 and
            self.brightness > 0.95 and
            self.harmonie > 0.8):

            # Reset to safe middle values
            self.hue = random.uniform(0, 360)
            self.saturation = 0.5
            self.brightness = 0.5
            self.drift = 0.1
            self.harmonie = 0.8
            self.energy = 0.5
            return True

        return False

    def stabilisierung(self):
        """
        Stabilize cell properties based on neighbors:
        - Hue: Move toward average neighbor hue
        - Saturation: Increase with harmony
        - Brightness: Decrease with drift
        """
        if not self.nachbarn:
            return

        avg_hue = sum(n.hue for n in self.nachbarn) / len(self.nachbarn)
        self.hue = (1 - self.alpha) * self.hue + self.alpha * avg_hue

        self.saturation += self.beta * (self.harmonie - 0.5)
        self.brightness -= self.gamma * self.drift

        self.clamp()

    def update(self):
        """
        Main update cycle for a cell:
        1. Apply SaturnHexagon rules (if available)
        2. Clamp values
        3. Calculate drift
        4. Calculate harmony
        5. Check failsafe
        6. Stabilize with neighbors
        
        Note: No debug prints here - controlled by Engine
        """
        if self.hex:
            self.hex.apply(self)

        self.clamp()
        self.berechne_drift()
        self.berechne_harmonie()

        if self.failsafe():
            return

        self.stabilisierung()
