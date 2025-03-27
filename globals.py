# globals.py

# Globale Listen für Objekte
beuten = []
jaegers = []

# Zeit- und Zähler-Variablen
simulation_start = None
simulation_over = False
unique_object_counter = 0

# Umweltvariablen
global_oxygen = 0
global_co2 = 0  # Dieses Reservoir wird in jedem Sekundentakt neu gesetzt
co2_text_id = None  # Wird in der Simulation verwendet

# Pausenflag
paused = False

# Mutationseinstellungen
mutation_loss_rate = 0.03  # Standard: 3% (wird in config.py überschrieben)

# Gewinn-Wahrscheinlichkeiten für Genome (als Fließkommazahlen, z.B. 0.02 entspricht 2%)
prey_cooperation_probability = 0.02
prey_schneller_metabolismus_probability = 0.04
jaeger_angriff_probability = 0.05

# Mögliche Genome und Default-Einstellungen
available_genomes_beute = ["essen", "bewegen", "Kooperation", "Schneller Metabolismus", "geruchlos"]
# Wichtig: "Kooperation" wird absichtlich NICHT in den Default-Werten gesetzt,
# damit es nur durch Mutation hinzugefügt wird.
default_beute = {"essen": True, "bewegen": True, "Schneller Metabolismus": False, "geruchlos": False}

available_genomes_jaeger = ["Fortbewegung", "jagen", "Orientierung", "Angriff"]
default_jaeger = {"Fortbewegung": True, "jagen": True, "Orientierung": True, "Angriff": False}
