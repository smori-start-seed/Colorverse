# main.py – Colorverse Evolution Main Entry Point
# ============================================================
# This is the main entry point for the Colorverse simulation.
# It replaces the old saturings.py file with a cleaner structure.
# ============================================================

import random
import time
from config import *
from Zelle import Zelle
from Cluster import Cluster
from Ring import Ring
from Sphere import Sphere
from MetaSphere import MetaSphere
from UniverseNode import UniverseNode
from engine import Engine
from saturn_hexagon_core import SaturnHexagon


# ============================================================
# HEX NEIGHBORS
# ============================================================

def set_initial_hex_neighbors(zellen):
    """
    Set initial hexagonal neighbors for all cells.
    Each cell gets 6 neighbors at distances -1, -2, -3, +1, +2, +3.
    
    Args:
        zellen: List of Zelle objects
    """
    n = len(zellen)
    for i, z in enumerate(zellen):
        z.nachbarn = [
            zellen[(i - 1) % n],
            zellen[(i + 1) % n],
            zellen[(i - 2) % n],
            zellen[(i + 2) % n],
            zellen[(i - 3) % n],
            zellen[(i + 3) % n],
        ]


# ============================================================
# WORLD BUILDER
# ============================================================

def build_world(engine: Engine):
    """
    Build the complete Colorverse world with all hierarchical layers.
    
    Creates:
    1. Cells (Ebene 1)
    2. Clusters (Ebene 2)
    3. Rings (Ebene 3)
    4. Spheres (Ebene 4)
    5. MetaSphere (Ebene 5)
    6. UniverseNode (Ebene 6)
    
    Args:
        engine: Engine instance to populate
    """
    # =====================================================
    # Ebene 1: Zellen (Cells)
    # =====================================================
    engine.zellen = [
        Zelle(
            hue=random.uniform(*START_HUE_RANGE),
            saturation=random.uniform(*START_SAT_RANGE),
            brightness=random.uniform(*START_BRI_RANGE),
            energy=random.uniform(*START_ENERGY_RANGE)
        )
        for _ in range(WORLD_SIZE)
    ]

    # =====================================================
    # Assign SaturnHexagon rule kernel to all cells
    # =====================================================
    hexagon = SaturnHexagon()
    for z in engine.zellen:
        z.hex = hexagon
        z.in_cluster = False
        z.evolutionskeim = False

    # =====================================================
    # Set initial hexagonal neighbors
    # =====================================================
    set_initial_hex_neighbors(engine.zellen)

    # =====================================================
    # Ebene 2: Cluster
    # =====================================================
    engine.cluster = []
    if ENABLE_CLUSTER:
        for i in range(0, len(engine.zellen), CLUSTER_SIZE):
            chunk = engine.zellen[i:i+CLUSTER_SIZE]
            if len(chunk) == CLUSTER_SIZE:
                engine.cluster.append(Cluster(chunk, engine=engine))

    # =====================================================
    # Ebene 3: Ring
    # =====================================================
    engine.ringe = []
    if ENABLE_RING:
        engine.ringe = [Ring(engine.cluster)]

    # =====================================================
    # Ebene 4: Sphere
    # =====================================================
    engine.spheren = []
    if ENABLE_SPHERE:
        engine.spheren = [Sphere(engine.ringe)]

    # =====================================================
    # Ebene 5: MetaSphere
    # Created HERE (not in Engine.__init__) to avoid empty list issues
    # =====================================================
    if ENABLE_METASPHERE:
        engine.metasphere = MetaSphere(engine.spheren)

    # =====================================================
    # Ebene 6: UniverseNode
    # Created HERE (not in Engine.__init__) to avoid circular references
    # =====================================================
    if ENABLE_UNIVERSE:
        engine.universe = UniverseNode(engine, engine.metasphere)


# ============================================================
# DEBUG OUTPUT
# ============================================================

def print_debug_info(engine, step_count):
    """
    Print comprehensive debug information for all layers.
    Called every DEBUG_INTERVAL steps.
    
    Args:
        engine: Engine instance
        step_count: Current step number
    """
    sphere = engine.spheren[0] if engine.spheren else None
    meta = engine.metasphere
    uni = engine.universe

    print("\n" + "=" * 50)
    print("COLORVERSE DEBUG OUTPUT")
    print("=" * 50)
    print(f"STEP: {step_count}")
    print("-" * 50)

    # Zellen (Cells) - Average values only
    if engine.zellen:
        z_hue = sum(z.hue for z in engine.zellen) / len(engine.zellen)
        z_sat = sum(z.saturation for z in engine.zellen) / len(engine.zellen)
        z_bri = sum(z.brightness for z in engine.zellen) / len(engine.zellen)
        z_energy = sum(z.energy for z in engine.zellen) / len(engine.zellen)
        z_drift = sum(z.drift for z in engine.zellen) / len(engine.zellen)
        z_harmonie = sum(z.harmonie for z in engine.zellen) / len(engine.zellen)
        print(f"ZELLEN: hue={z_hue:.2f} sat={z_sat:.2f} bri={z_bri:.2f} "
              f"energy={z_energy:.2f} drift={z_drift:.2f} harm={z_harmonie:.2f}")

    # Cluster
    if engine.cluster:
        c = engine.cluster[0]
        print(f"CLUSTER: hue={c.farbsatz_hue:.2f} sat={c.farbsatz_saturation:.2f} "
              f"bri={c.farbsatz_brightness:.2f} harm={c.harmonie_avg:.2f} drift={c.drift_avg:.2f}")

    # Ring
    if engine.ringe:
        r = engine.ringe[0]
        print(f"RING: hue={r.hue_avg:.2f} sat={r.sat_avg:.2f} bri={r.bri_avg:.2f}")

    # Sphere
    if sphere:
        print(f"SPHERE: hue={sphere.hue_avg:.2f} sat={sphere.sat_avg:.2f} bri={sphere.bri_avg:.2f} "
              f"energy={sphere.energy_avg:.2f} harm={sphere.harmonie_avg:.2f} drift={sphere.drift_avg:.2f}")

    # MetaSphere
    if meta:
        print(f"METASPHERE: hue={meta.hue_avg:.2f} sat={meta.sat_avg:.2f} bri={meta.bri_avg:.2f} "
              f"energy={meta.energy_avg:.2f} harm={meta.harmonie_avg:.2f} drift={meta.drift_avg:.2f}")

    # Universe
    if uni:
        print(f"UNIVERSE: mode={uni.modus} harm={uni.harmonie:.2f} drift={uni.drift:.2f} energy={uni.energy:.2f}")

    # Global Harmony Field
    print(f"HARMONIE_FELD: harm={engine.harmonie_feld['global_harmonie']:.2f} "
          f"drift={engine.harmonie_feld['global_drift']:.2f} stoer={engine.harmonie_feld['stoerimpulse']:.2f}")

    # Cluster statistics
    free_cells = sum(1 for z in engine.zellen if not z.in_cluster)
    clustered_cells = sum(1 for z in engine.zellen if z.in_cluster)
    print(f"CELL STATS: total={len(engine.zellen)} free={free_cells} clustered={clustered_cells}")
    print("=" * 50 + "\n")


# ============================================================
# MAIN LOOP
# ============================================================

def main(steps=500, delay=0.05):
    """
    Main simulation loop.
    
    Args:
        steps: Number of steps to run (None for infinite)
        delay: Delay between steps in seconds
    """
    # Initialize engine and build world
    engine = Engine()
    build_world(engine)

    step_count = 0
    
    print("\n" + "=" * 50)
    print("COLORVERSE EVOLUTION STARTED")
    print("=" * 50)
    print(f"World Size: {WORLD_SIZE}")
    print(f"Cluster Size: {CLUSTER_SIZE}")
    print(f"Enabled Layers: ", end="")
    layers = []
    if ENABLE_CLUSTER: layers.append("Cluster")
    if ENABLE_RING: layers.append("Ring")
    if ENABLE_SPHERE: layers.append("Sphere")
    if ENABLE_METASPHERE: layers.append("MetaSphere")
    if ENABLE_UNIVERSE: layers.append("Universe")
    print(", ".join(layers))
    print("=" * 50 + "\n")

    try:
        while True:
            # Run one evolution step
            engine.step()
            step_count += 1

            # Debug output at intervals
            if ENABLE_LOGGING and step_count % DEBUG_INTERVAL == 0:
                print_debug_info(engine, step_count)

            # Check stop condition
            if steps is not None and step_count >= steps:
                print(f"\nSimulation completed {steps} steps.")
                break

            # Sleep between steps
            time.sleep(delay)

    except KeyboardInterrupt:
        print(f"\nSimulation interrupted by user at step {step_count}.")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    # Run with default settings from config.py
    main(steps=None, delay=0.05)
