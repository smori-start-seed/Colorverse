# ============================================================
#  CONFIG.PY – Zentrale Konfiguration für das Colorverse
#  Vollständige, harmonische, ring-basierte Evolution
# ============================================================


# ------------------------------------------------------------
# 1) Feature-Toggles – Aktiviert/Deaktiviert ganze Ebenen
# ------------------------------------------------------------

ENABLE_CLUSTER = True          # Ebene 2: Clusterbildung
ENABLE_RING = True             # Ebene 3: Ring (harmonische Glättung)
ENABLE_SPHERE = True           # Ebene 4: Sphere (globale Muster)
ENABLE_METASPHERE = True       # Ebene 5: MetaSphere (Meta-Muster)
ENABLE_UNIVERSE = True         # Ebene 6: UniverseNode (Aggregat)


# ------------------------------------------------------------
# 2) Welt-Parameter – Grundstruktur des Colorverse
# ------------------------------------------------------------

WORLD_SIZE = 1000              # Anzahl der Zellen im Colorverse
CLUSTER_SIZE = 11              # Zellen pro Cluster (harmonisch)
RING_COUNT = 1                 # Anzahl der Ringe (meist 1)


# ------------------------------------------------------------
# 3) Startwerte für Zellen – Initialisierung der Welt
# ------------------------------------------------------------

START_HUE_RANGE = (0, 360)     # Start-Farbwinkel
START_SAT_RANGE = (0.3, 0.8)   # Start-Sättigung
START_BRI_RANGE = (0.3, 0.8)   # Start-Helligkeit
START_ENERGY_RANGE = (0.4, 1.0)# Start-Energie

# Globale Start-Harmonie
GLOBAL_HARMONIE_START = 1.0
GLOBAL_DRIFT_START = 0.4
GLOBAL_STOER_START = 0.9


# ------------------------------------------------------------
# 4) MicroHexagon – Mikroevolution der Zellen
# ------------------------------------------------------------

MICRO_ENERGY_DECAY = 0.01      # Energieverlust pro Schritt
MICRO_HUE_SHIFT = 0.001        # Farbdrift pro Schritt
MICRO_BRIGHTNESS_DRIFT = 0.002 # Helligkeitsdrift pro Schritt


# ------------------------------------------------------------
# 5) Evolutionsparameter – Schwellen & Dynamik
# ------------------------------------------------------------

DRIFT_THRESHOLD = 0.40         # Ab wann Drift kritisch wird
ENERGY_THRESHOLD = 0.60        # Mindestenergie für Evolution
HARMONIE_THRESHOLD = 0.50      # Mindestharmonie für Stabilität

KEIM_MINIMUM = 11              # Mindestgröße für Evolutionskeime


# ------------------------------------------------------------
# 6) Engine-Parameter – Simulationssteuerung
# ------------------------------------------------------------

ENGINE_STEPS_PER_TICK = 1      # Schritte pro Engine-Tick
DEBUG_INTERVAL = 20            # Ausgabeintervall
ENABLE_LOGGING = True          # Debug-Ausgabe aktivieren


# ------------------------------------------------------------
# 7) Regelkern-Auswahl – Hexagon-Logik
# ------------------------------------------------------------

HEXAGON_CORE = "saturn"        # "saturn" = harmonische Evolution

def load_hexagon():
    if HEXAGON_CORE == "saturn":
        from saturn_hexagon_core import SaturnHexagon
        return SaturnHexagon()
    else:
        raise ValueError(f"Unbekannter Regelkern: {HEXAGON_CORE}")


# ------------------------------------------------------------
# 8) UI-Parameter – Darstellung & Debug
# ------------------------------------------------------------

UI_THEME = "dark"
UI_SHOW_CLUSTER = True
UI_SHOW_NEIGHBORS = False
UI_ANIMATION_SPEED = 1.0


# ------------------------------------------------------------
# 9) Systeminfo
# ------------------------------------------------------------

COLORVERSE_VERSION = "1.1.0-harmony"


# ------------------------------------------------------------
# 10) FARB-OS - Persistenz, Gate & Schattenlauf
# ------------------------------------------------------------

GEDAECHTNIS_DATEI = "colorverse_geist.bin"   # Unikat-Speicher (HW-gebunden)
HASH_DURCHLAEUFE = 100000                    # Schluesselableitung

GATE_LEDGER_DATEI = "vereinbarungen.json"    # Zustimmungen des Interactors
GATE_LOG_DATEI = "gate_log.json"             # Jeder Austauschversuch wird notiert

SCHATTEN_SCHRITTE = 30                       # Simulations-Horizont vor/nach Umsetzung
SCHATTEN_TOLERANZ = 0.05                     # Maximal akzeptierte Verschlechterung

SNAPSHOT_INTERVALL = 100                     # Erinnerung alle N Schritte
DEBUG_ZELLE = False                          # Zell-Druck (sonst nur Engine-Ebene)


# ------------------------------------------------------------
# 11) KONSOLE - ANSI-Renderer
# ------------------------------------------------------------

ENABLE_KONSOLE = True
KONSOLE_INTERVALL = 10
TERMINAL_BREITE = 60
TERMINAL_HOEHE = 10


# ------------------------------------------------------------
# 12) KLANG - Audio-Ausgabe
# ------------------------------------------------------------

ENABLE_KLANG = True
KLANG_INTERVALL = 50
KLANG_DAUER = 2.0
KLANG_DATEI = "klang.wav"
KLANG_MIN_FREQ = 110.0
KLANG_MAX_FREQ = 440.0


# ------------------------------------------------------------
# 13) HW-SCAN - Individualisierung durch Abweichung
# ------------------------------------------------------------

ENABLE_HWSCAN = True


# ------------------------------------------------------------
# 14) EMACK - Puls-Kopplung zu Urasil_light
# ------------------------------------------------------------

ENABLE_EMACK = True
EMACK_URASIL_PFAD = ["../Urasil_light", "../github__smori-start-seed__Urasil_light"]
EMACK_SYNC_STAERKE = 0.1
EMACK_MUTATION = 0.02


# ------------------------------------------------------------
# 14a) DIALOG - das Gespraech mit dem Interactor
# ------------------------------------------------------------

DIALOG_INTERVALL = 25
DIALOG_EINGANG_DATEI = "eingang.json"
DIALOG_AUSGANG_DATEI = "ausgang.json"
DIALOG_KANAL_HINAUF = "interactor-hinauf"
DIALOG_KANAL_HERAB = "interactor-herab"


# ------------------------------------------------------------
# 15) GEBURT - Attestierung der Identitaet
# ------------------------------------------------------------

GEBURTSAKT_DATEI = "geburtsakt.bin"


# ------------------------------------------------------------
# 16) ZUSTIMMUNG - Ablauf in Schritten des Colorverse
# ------------------------------------------------------------

ZUSTIMMUNG_DAUER = 500   # Schritte, danach fragt das Gate erneut

