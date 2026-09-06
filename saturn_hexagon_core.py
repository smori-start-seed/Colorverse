# saturn_hexagon_core.py – Colorverse Rule Kernel (Optimized)
# Fixed: Reduced randomness, more deterministic behavior
import math
import random
from config import *


class SaturnHexagon:
    """
    Rule kernel for Colorverse based on a 3-body orbital system (Saturn metaphor).
    
    The system consists of:
    - A: Center body (global drift anchor)
    - B & C: Orbiting pair (180 degrees apart)
    
    The orbital mechanics influence cell color properties:
    - Hue: Affected by orbital frequency factors (af)
    - Saturation: Affected by position factors (pf)
    - Brightness: Affected by radius factors (rf)
    
    All values are normalized to [0, 1] range.
    """
    
    def __init__(self):
        # A = Center (global drift anchor)
        self.A = {
            "af": 0.5,   # Hue frequency factor
            "pf": 0.5,   # Saturation position factor
            "rf": 0.5,   # Brightness radius factor
            "mass": 1000.0,
            "drift": 0.00005
        }

        # B = First orbiting body
        self.B = {
            "angle": 0.0,
            "density": 1.0,
            "af": 0.4,
            "pf": 0.6,
            "rf": 0.5
        }

        # C = Second orbiting body (180 degrees from B)
        self.C = {
            "angle": math.pi,
            "density": 0.7,
            "af": 0.6,
            "pf": 0.4,
            "rf": 0.5
        }

        self.RADIUS = 1.0

    def _update_saturn(self):
        """
        Update the orbital positions of B and C.
        
        B rotates at a fixed rate, C follows at 180 degrees.
        Frequency factors are influenced by density and drift.
        """
        B = self.B
        C = self.C
        A = self.A

        # B rotates
        B["angle"] += 0.015
        B["x"] = self.RADIUS * math.cos(B["angle"])
        B["y"] = self.RADIUS * math.sin(B["angle"])

        # C follows B (180° offset)
        C["angle"] = B["angle"] + math.pi
        C["x"] = self.RADIUS * math.cos(C["angle"])
        C["y"] = self.RADIUS * math.sin(C["angle"])

        # Frequency drift through density
        B["af"] += (A["af"] - B["af"]) * 0.02 * B["density"]
        C["af"] += (B["af"] - C["af"]) * 0.02 * C["density"]

        # Feedback to center
        A["af"] += (C["af"] - A["af"]) * A["drift"]

    def apply(self, z):
        """
        Apply SaturnHexagon rules to a cell.
        
        Deterministic color evolution based on orbital mechanics:
        - Hue: Influenced by average af of A, B, C
        - Saturation: Influenced by average pf of A, B, C
        - Brightness: Influenced by average rf of A, B, C
        - Energy: Deterministic drift-based adjustment
        - Small random component only for hue (minimal)
        
        Args:
            z: Zelle object to apply rules to
        """
        # Update orbital positions
        self._update_saturn()

        A = self.A
        B = self.B
        C = self.C

        # Calculate average orbital factors
        saturn_hue = (A["af"] + B["af"] + C["af"]) / 3.0
        saturn_sat = (A["pf"] + B["pf"] + C["pf"]) / 3.0
        saturn_bri = (A["rf"] + B["rf"] + C["rf"]) / 3.0

        # =====================================================
        # 1. Hue influence (deterministic + minimal random)
        # =====================================================
        # Deterministic component: based on orbital hue factor
        z.hue += (saturn_hue - 0.5) * 0.5
        
        # Minimal random component (only for natural variation)
        z.hue += (random.random() - 0.5) * 0.1

        # =====================================================
        # 2. Saturation influence (fully deterministic)
        # =====================================================
        z.saturation += (saturn_sat - 0.5) * 0.05

        # =====================================================
        # 3. Brightness influence (fully deterministic)
        # =====================================================
        z.brightness += (saturn_bri - 0.5) * 0.05

        # =====================================================
        # 4. Energy: Deterministic based on cell drift
        # Higher drift = more energy gain (system self-regulation)
        # =====================================================
        z.energy += (z.drift - 0.3) * 0.01

        # Note: No random components for energy, saturation, brightness
        # This ensures deterministic evolution while allowing hue variation
