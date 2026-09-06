# Colorverse - Complete Documentation

## 📖 Overview

**Colorverse** is a multi-layered cellular simulation system written in Python, themed around a cosmic/astronomical aesthetic. It models emergent behavior through a 6-level hierarchy where simple cell-level rules propagate upward to create complex global patterns.

---

## 🏗️ Architecture

The simulation builds a world in **6 nested levels**, each composed of the level below it:

```
UniverseNode (Level 6) ← Top-level container, global feedback
    ↑
MetaSphere (Level 5) ← Aggregates Spheres
    ↑
Sphere (Level 4) ← Aggregates Rings
    ↑
Ring (Level 3) ← Aggregates Clusters
    ↑
Cluster (Level 2) ← Groups of 11 Cells with internal roles
    ↑
Zelle (Level 1) ← Atomic unit with color properties
```

Each level **aggregates** the properties of the level below it, and the **SaturnHexagon** rule kernel applies orbital mechanics to influence cell color evolution.

---

## 📁 File Structure

```
Colorverse/
├── config.py              # Central configuration
├── main.py                # Main entry point (replaces saturings.py)
├── engine.py              # Evolution engine (main loop)
├── Zelle.py               # Cell unit (Level 1)
├── Cluster.py             # Cluster unit (Level 2)
├── Ring.py                # Ring unit (Level 3)
├── Sphere.py              # Sphere unit (Level 4)
├── MetaSphere.py          # MetaSphere unit (Level 5)
├── UniverseNode.py        # UniverseNode (Level 6)
├── saturn_hexagon_core.py # Rule kernel (orbital mechanics)
├── DOCUMENTATION.md       # This file
└── README.md              # Project overview
```

---

## 🎛️ Configuration (config.py)

All simulation parameters are defined in `config.py`:

### Feature Toggles
```python
ENABLE_CLUSTER = True      # Enable Cluster layer (Level 2)
ENABLE_RING = True         # Enable Ring layer (Level 3)
ENABLE_SPHERE = True        # Enable Sphere layer (Level 4)
ENABLE_METASPHERE = True    # Enable MetaSphere layer (Level 5)
ENABLE_UNIVERSE = True     # Enable UniverseNode (Level 6)
```

### World Parameters
```python
WORLD_SIZE = 1000          # Number of cells
CLUSTER_SIZE = 11         # Cells per cluster (must be 11)
RING_COUNT = 1            # Number of rings
```

### Initial Values
```python
START_HUE_RANGE = (0, 360)     # Initial hue range (degrees)
START_SAT_RANGE = (0.3, 0.8)   # Initial saturation range
START_BRI_RANGE = (0.3, 0.8)   # Initial brightness range
START_ENERGY_RANGE = (0.4, 1.0) # Initial energy range

GLOBAL_HARMONIE_START = 1.0   # Initial global harmony
GLOBAL_DRIFT_START = 0.4      # Initial global drift
GLOBAL_STOER_START = 0.9      # Initial disturbance impulses
```

### Evolution Parameters
```python
DRIFT_THRESHOLD = 0.40      # Critical drift threshold
ENERGY_THRESHOLD = 0.60     # Minimum energy for evolution
HARMONIE_THRESHOLD = 0.50   # Minimum harmony for stability
KEIM_MINIMUM = 11           # Minimum seeds for evolution
```

### Engine Parameters
```python
ENGINE_STEPS_PER_TICK = 1   # Steps per tick
DEBUG_INTERVAL = 20         # Debug output interval
ENABLE_LOGGING = True       # Enable debug output
```

### Rule Kernel
```python
HEXAGON_CORE = "saturn"     # Rule kernel: "saturn" for orbital mechanics
```

---

## 🔧 Component Details

### Zelle (Cell) - Level 1

**File:** `Zelle.py`

The atomic unit of Colorverse. Each cell has:

**Properties:**
- `hue`: Color hue in degrees [0, 360)
- `saturation`: Color saturation [0, 1]
- `brightness`: Color brightness [0, 1]
- `energy`: Cell energy [0, 1]
- `drift`: Color drift metric [0, 1]
- `harmonie`: Harmony metric [0, 1]
- `nachbarn`: List of 6 neighboring cells
- `hex`: SaturnHexagon rule kernel
- `in_cluster`: Whether cell is in a cluster
- `evolutionskeim`: Whether cell is an evolution seed

**Methods:**
- `clamp()`: Clamp all values to valid ranges
- `berechne_drift()`: Calculate drift as average hue difference to neighbors
- `berechne_harmonie()`: Calculate harmony as 1 - normalized hue variance
- `failsafe()`: Safety mechanism to prevent extreme states (resets to safe middle values)
- `stabilisierung()`: Stabilize properties based on neighbors
- `update()`: Main update cycle

**Key Fixes:**
- ✅ Sanfter failsafe (resets to middle values, not 0)
- ✅ Removed debug prints
- ✅ Improved stability

---

### Cluster - Level 2

**File:** `Cluster.py`

A group of **exactly 11 cells** with internal role differentiation:

**Roles:**
- **Kern (Cells 0-2)**: Core cells with high stability
- **Sub-Moleküle (Cells 3-9)**: Dynamic cells with moderate stability
- **Edger (Cell 10)**: Edge cell with recruitment role

**Properties:**
- `zellen`: List of 11 cells
- `engine`: Reference to the Engine
- `hue_avg, sat_avg, bri_avg`: Average color values
- `energy_avg`: Average energy
- `harmonie_avg, drift_avg`: Average metrics
- `farbsatz_*`: Aggregated color set for Ring
- `varianz`: Hue variance within cluster

**Methods:**
- `update()`: Update cluster (cells, values, color set, mutation)
- `update_cluster()`: Core update logic
- `berechne_clusterwerte()`: Calculate average values
- `berechne_farbsatz()`: Calculate color set
- `mutation()`: Apply role-based mutations
- `get_farbsatz()`: Return color set for Ring

**Key Fixes:**
- ✅ Removed neighbor overwriting in mutation()
- ✅ Cluster size remains fixed at 11
- ✅ New cells are marked for Engine to create new clusters

---

### Ring - Level 3

**File:** `Ring.py`

Aggregates clusters into a ring structure.

**Properties:**
- `cluster`: List of Cluster objects
- `hue_avg, sat_avg, bri_avg`: Average color values

**Methods:**
- `update()`: Update ring by updating clusters and aggregating values
- `update_ring()`: Core update logic
- `berechne_ring_farbsatz()`: Calculate average color values
- `get_farbsatz()`: Return color set for Sphere

**Key Fixes:**
- ✅ Removed debug prints

---

### Sphere - Level 4

**File:** `Sphere.py`

Aggregates rings and calculates meta-values.

**Properties:**
- `ringe`: List of Ring objects
- `hue_avg, sat_avg, bri_avg`: Average color values
- `energy_avg, harmonie_avg, drift_avg`: Meta values

**Methods:**
- `update()`: Update sphere by updating rings and aggregating values
- `update_sphere()`: Core update logic
- `berechne_sphere_farbsatz()`: Calculate color and meta values
- `get_farbsatz()`: Return color set for MetaSphere

**Key Fixes:**
- ✅ Removed debug prints
- ✅ Improved meta-value calculation

---

### MetaSphere - Level 5

**File:** `MetaSphere.py`

Top-level aggregation unit for Spheres.

**Properties:**
- `spheren`: List of Sphere objects
- `hue_avg, sat_avg, bri_avg`: Average color values
- `energy_avg, harmonie_avg, drift_avg`: Average meta values

**Methods:**
- `update()`: Update MetaSphere by updating spheres and aggregating values
- `update_metasphere()`: Core update logic
- `berechne_metasphere()`: Aggregate all values
- `get_meta()`: Return all meta values as dictionary
- `get_farbsatz()`: Return color set for UniverseNode

**Key Fixes:**
- ✅ Removed debug prints

---

### UniverseNode - Level 6

**File:** `UniverseNode.py`

Top-level container that tracks global coherence and provides feedback.

**Modes:**
- `"sanft"` (gentle): High harmony (>0.7) and low drift (<0.3)
- `"chaotisch"` (chaotic): High drift (>0.5) or high energy (>0.8)
- `"intelligent"` (intelligent): All other cases

**Properties:**
- `engine`: Reference to the Engine
- `metasphere`: Reference to the MetaSphere
- `harmonie, drift, energy`: Global state values
- `harmonie_trend, drift_trend, energy_trend`: Historical trends (last 200 steps)
- `modus`: Current evolution mode

**Methods:**
- `update()`: Update UniverseNode
- `update_universe()`: Core update logic
- `berechne_universe_farbsatz()`: Calculate universe-level values
- `berechne_trends()`: Update trend history
- `waehle_modus()`: Select evolution mode
- `rueckkopplung_ins_evolutionsfeld()`: Apply feedback to harmony field

**Key Fixes:**
- ✅ Removed debug prints

---

### SaturnHexagon - Rule Kernel

**File:** `saturn_hexagon_core.py`

The rule kernel that applies orbital mechanics to influence cell evolution.

**Orbital System:**
- **A**: Center body (global drift anchor)
- **B & C**: Orbiting pair (180 degrees apart)

**Orbital Factors:**
- `af`: Hue frequency factor
- `pf`: Saturation position factor
- `rf`: Brightness radius factor

**Methods:**
- `_update_saturn()`: Update orbital positions
- `apply(z)`: Apply rules to a cell

**Key Fixes:**
- ✅ Reduced randomness (only minimal random for hue)
- ✅ More deterministic behavior
- ✅ Energy now based on drift (self-regulation)

---

### Engine - Evolution Driver

**File:** `engine.py`

The main evolution engine that drives the simulation forward.

**Properties:**
- `zellen`: List of all cells
- `cluster`: List of all clusters
- `ringe`: List of all rings
- `spheren`: List of all spheres
- `metasphere`: MetaSphere instance
- `universe`: UniverseNode instance
- `harmonie_feld`: Global harmony field
- `step_count`: Current step number

**Methods:**
- `__init__()`: Initialize with empty containers (MetaSphere/Universe created in build_world)
- `hexagon_fluidity()`: Dynamic neighbor assignment
- `step()`: Main evolution step

**Key Fixes:**
- ✅ **FIXED: Removed double updates** (cells only updated once per step)
- ✅ **FIXED: Corrected initialization** (MetaSphere/Universe created in build_world)
- ✅ **FIXED: Single harmony field update** (only once per step)
- ✅ Removed debug prints (controlled by ENABLE_LOGGING)

---

### Main Entry Point

**File:** `main.py` (replaces `saturings.py`)

**Functions:**
- `set_initial_hex_neighbors(zellen)`: Set initial hexagonal neighbors
- `build_world(engine)`: Build complete world with all layers
- `print_debug_info(engine, step_count)`: Print comprehensive debug output
- `main(steps, delay)`: Main simulation loop

**Key Fixes:**
- ✅ Removed dead code (MicroHexagon)
- ✅ Corrected initialization order
- ✅ Improved debug output
- ✅ Better error handling

---

## 🚀 Running the Simulation

### Basic Usage

```bash
# Run with default settings (infinite, 0.05s delay)
python main.py

# Run for 100 steps with 0.01s delay
python main.py 100 0.01
```

Or modify `main.py`:

```python
if __name__ == "__main__":
    main(steps=100, delay=0.01)
```

### Configuration

Edit `config.py` to customize the simulation:

```python
# Smaller world for faster testing
WORLD_SIZE = 100

# More frequent debug output
DEBUG_INTERVAL = 10

# Disable some layers for testing
ENABLE_SPHERE = False
ENABLE_METASPHERE = False
```

---

## 🔍 Debug Output

When `ENABLE_LOGGING = True`, the simulation prints comprehensive debug information every `DEBUG_INTERVAL` steps:

```
==================================================
COLORVERSE DEBUG OUTPUT
==================================================
STEP: 20
--------------------------------------------------
ZELLEN: hue=123.45 sat=0.65 bri=0.72 energy=0.58 drift=0.32 harm=0.78
CLUSTER: hue=120.34 sat=0.68 bri=0.75 harm=0.82 drift=0.28
RING: hue=121.56 sat=0.67 bri=0.73
SPHERE: hue=122.12 sat=0.66 bri=0.74 energy=0.59 harm=0.80 drift=0.30
METASPHERE: hue=122.12 sat=0.66 bri=0.74 energy=0.59 harm=0.80 drift=0.30
UNIVERSE: mode=sanft harm=0.80 drift=0.30 energy=0.59
HARMONIE_FELD: harm=0.78 drift=0.32 stoer=0.45
CELL STATS: total=1000 free=890 clustered=110
==================================================
```

---

## 🐛 Bug Fixes Applied

This optimized version fixes all critical bugs from the original code:

### 1. ✅ Double Updates (CRITICAL)
**Problem:** Cells were being updated 3 times per step (Engine → Cluster → Zelle).
**Fix:** Cluster.update() no longer calls z.update(). Only Engine.step() updates cells.

### 2. ✅ Initialization Chaos (CRITICAL)
**Problem:** MetaSphere and UniverseNode were created with empty lists in Engine.__init__().
**Fix:** MetaSphere and UniverseNode are now created in build_world() after all layers exist.

### 3. ✅ Neighbor Overwriting
**Problem:** Multiple components were overwriting cell neighbors.
**Fix:** Cluster.mutation() no longer overwrites neighbors. Only Engine.hexagon_fluidity() sets dynamic neighbors.

### 4. ✅ Excessive Randomness
**Problem:** SaturnHexagon had too much randomness causing chaotic behavior.
**Fix:** Reduced randomness to minimal levels. Most evolution is now deterministic.

### 5. ✅ Harsh Failsafe
**Problem:** Failsafe reset cells to 0, killing the simulation.
**Fix:** Failsafe now resets to safe middle values (hue=random, sat=0.5, bri=0.5, etc.).

### 6. ✅ Multiple Harmony Field Updates
**Problem:** harmony_feld was updated multiple times per step.
**Fix:** harmony_feld is now updated only once per step in Engine.step().

### 7. ✅ Debug Print Overload
**Problem:** Every cell, ring, and sphere was printing debug info every step.
**Fix:** All debug prints removed except in main.py's controlled debug output.

### 8. ✅ Dead Code
**Problem:** MicroHexagon class was defined but never used.
**Fix:** Removed MicroHexagon from main.py (was in saturings.py).

---

## 📊 Performance Considerations

For large simulations (WORLD_SIZE > 1000):

1. **Reduce DEBUG_INTERVAL**: Set to 100 or higher
2. **Disable ENABLE_LOGGING**: For maximum performance
3. **Use smaller CLUSTER_SIZE**: But keep at 11 for proper role differentiation
4. **Consider numpy**: For vectorized operations (future optimization)

---

## 🎨 Visualization (Future)

To visualize the simulation, you can:

1. **Use matplotlib** for 2D plots of hue values
2. **Use pygame** for real-time animation
3. **Export to CSV** and use external tools

Example matplotlib visualization:

```python
import matplotlib.pyplot as plt
import numpy as np

# In main.py, after engine.step():
if step_count % 10 == 0:
    hues = [z.hue for z in engine.zellen]
    plt.clf()
    plt.scatter(np.arange(len(hues)), hues, c=hues, cmap='hsv')
    plt.pause(0.01)
```

---

## 🔬 Testing the System

### Test 1: Basic Stability
```python
# In main.py
main(steps=100, delay=0)
```
Expected: No crashes, values stay within valid ranges.

### Test 2: Cluster Formation
```python
# In config.py
WORLD_SIZE = 100
DRIFT_THRESHOLD = 0.3
ENERGY_THRESHOLD = 0.5

# In main.py
main(steps=50, delay=0)
```
Expected: Clusters form from evolution seeds.

### Test 3: Mode Switching
```python
# Monitor UniverseNode mode changes
# In main.py, add to debug output:
print(f"UNIVERSE MODE: {uni.modus}")
```
Expected: Mode switches between "sanft", "chaotisch", and "intelligent".

---

## 📈 Expected Behavior

### Normal Operation
1. Cells start with random color/energy values
2. SaturnHexagon applies orbital mechanics to evolve colors
3. Cells with high drift and energy become evolution seeds
4. Seeds form clusters of 11 cells
5. Clusters aggregate into rings, spheres, etc.
6. UniverseNode monitors global state and provides feedback

### Stability
- All values (hue, saturation, brightness, energy, drift, harmony) stay within [0, 1] or [0, 360) for hue
- No cells are "killed" (reset to 0)
- System self-regulates through feedback loops

### Emergence
- Local cell rules create global patterns
- Clusters form naturally from evolution seeds
- Universe mode switches based on global state
- Harmony field influences cell behavior

---

## 🛠️ Extending Colorverse

### Adding New Rule Kernels
1. Create a new class in a new file (e.g., `new_kernel.py`)
2. Implement the `apply(z)` method
3. Add to `config.py`:
   ```python
   HEXAGON_CORE = "new"  # or add to load_hexagon()
   ```

### Adding New Layers
1. Create a new class (e.g., `Galaxy.py` for Level 7)
2. Update `build_world()` in `main.py`
3. Update `Engine.step()` to include the new layer

### Adding Visualization
1. Import visualization library (matplotlib, pygame, etc.)
2. Add visualization code to `main.py`
3. Call visualization in the main loop

---

## 📚 Glossary

| Term | German | Description |
|------|--------|-------------|
| Zelle | Cell | Atomic unit with color properties |
| Cluster | Cluster | Group of 11 cells with roles |
| Ring | Ring | Group of clusters |
| Sphere | Sphere | Group of rings |
| MetaSphere | MetaSphere | Group of spheres |
| UniverseNode | UniverseNode | Top-level container |
| SaturnHexagon | SaturnHexagon | Orbital rule kernel |
| drift | Drift | Color variation metric |
| harmonie | Harmony | Color stability metric |
| evolutionskeim | Evolution seed | Cell marked for cluster formation |
| stoerimpulse | Disturbance impulse | Global variation trigger |
| rueckkopplung | Feedback | System self-regulation |

---

## 🎯 Summary

This optimized version of **Colorverse** fixes all critical bugs and provides:

✅ **Stable evolution** (no double updates, no crashes)
✅ **Hierarchical aggregation** (6 levels working correctly)
✅ **Dynamic neighbors** (hexagon fluidity)
✅ **Self-regulation** (Universe feedback)
✅ **Deterministic behavior** (reduced randomness)
✅ **Clean code** (no dead code, proper documentation)
✅ **Comprehensive debugging** (controlled output)

The system is now ready for:
- **Visualization** (add matplotlib/pygame)
- **Audio mapping** (map harmony/drift to sound)
- **Data export** (log to CSV for analysis)
- **Machine learning** (use as generative model)
- **Further extension** (new layers, new rules)

---

**Enjoy exploring the Colorverse! 🌌**
