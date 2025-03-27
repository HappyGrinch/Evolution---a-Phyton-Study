# config.py

import tkinter as tk
from globals import available_genomes_beute, default_beute, available_genomes_jaeger, default_jaeger

MAX_OBJECTS = 12

def rebuild_config_frames(root, beute_frame, jaeger_frame, beute_vars, jaeger_vars, beute_count, jaeger_count):
    for widget in beute_frame.winfo_children():
        widget.destroy()
    for widget in jaeger_frame.winfo_children():
        widget.destroy()
    beute_vars.clear()
    jaeger_vars.clear()

    for i in range(beute_count):
        row = i
        tk.Label(beute_frame, text=f"Beute {i+1}:").grid(row=row, column=0, sticky="w")
        var_dict = {}
        col = 1
        for genome in available_genomes_beute:
            default_val = default_beute.get(genome, False)
            var = tk.BooleanVar(value=default_val)
            chk = tk.Checkbutton(beute_frame, text=genome, variable=var)
            chk.grid(row=row, column=col, sticky="w")
            var_dict[genome] = var
            col += 1
        beute_vars.append(var_dict)

    for i in range(jaeger_count):
        row = i
        tk.Label(jaeger_frame, text=f"Jäger {i+1}:").grid(row=row, column=0, sticky="w")
        var_dict = {}
        col = 1
        for genome in available_genomes_jaeger:
            default_val = default_jaeger.get(genome, False)
            var = tk.BooleanVar(value=default_val)
            chk = tk.Checkbutton(jaeger_frame, text=genome, variable=var)
            chk.grid(row=row, column=col, sticky="w")
            var_dict[genome] = var
            col += 1
        jaeger_vars.append(var_dict)

def config_page():
    config_root = tk.Tk()
    config_root.title("Konfigurationsseite")
    
    tk.Label(config_root, text="Anzahl Beute (max 12):").grid(row=0, column=0, sticky="w")
    beute_count_var = tk.StringVar(value="3")
    tk.Entry(config_root, textvariable=beute_count_var, width=5).grid(row=0, column=1, sticky="w")
    
    tk.Label(config_root, text="Anzahl Jäger (max 12):").grid(row=1, column=0, sticky="w")
    jaeger_count_var = tk.StringVar(value="3")
    tk.Entry(config_root, textvariable=jaeger_count_var, width=5).grid(row=1, column=1, sticky="w")
    
    tk.Label(config_root, text="Mutation Verlust Genom [%]:").grid(row=2, column=0, sticky="w")
    mutation_loss_var = tk.StringVar(value="3")
    tk.Entry(config_root, textvariable=mutation_loss_var, width=5).grid(row=2, column=1, sticky="w")
    
    # Neue Felder für die Gewinnwahrscheinlichkeiten (in Prozent)
    tk.Label(config_root, text="Beute Kooperation Wahrscheinlichkeit [%]:").grid(row=3, column=0, sticky="w")
    prey_coop_prob_var = tk.StringVar(value="2")  # Standard 2%
    tk.Entry(config_root, textvariable=prey_coop_prob_var, width=5).grid(row=3, column=1, sticky="w")
    
    tk.Label(config_root, text="Beute Schneller Metabolismus Wahrscheinlichkeit [%]:").grid(row=4, column=0, sticky="w")
    prey_sm_prob_var = tk.StringVar(value="4")  # Standard 4%
    tk.Entry(config_root, textvariable=prey_sm_prob_var, width=5).grid(row=4, column=1, sticky="w")
    
    tk.Label(config_root, text="Jäger Angriff Wahrscheinlichkeit [%]:").grid(row=5, column=0, sticky="w")
    jaeger_angriff_prob_var = tk.StringVar(value="5")  # Standard 5%
    tk.Entry(config_root, textvariable=jaeger_angriff_prob_var, width=5).grid(row=5, column=1, sticky="w")
    
    # Frames für die dynamische Konfiguration der Genome
    beute_frame = tk.LabelFrame(config_root, text="Beute Genome")
    beute_frame.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="we")
    jaeger_frame = tk.LabelFrame(config_root, text="Jäger Genome")
    jaeger_frame.grid(row=7, column=0, columnspan=2, padx=10, pady=5, sticky="we")
    
    beute_vars = []
    jaeger_vars = []
    
    def update_frames(*args):
        try:
            beute_count = int(beute_count_var.get())
        except:
            beute_count = 3
        try:
            jaeger_count = int(jaeger_count_var.get())
        except:
            jaeger_count = 3
        beute_count = min(max(beute_count, 1), MAX_OBJECTS)
        jaeger_count = min(max(jaeger_count, 1), MAX_OBJECTS)
        rebuild_config_frames(config_root, beute_frame, jaeger_frame, beute_vars, jaeger_vars, beute_count, jaeger_count)
    
    beute_count_var.trace_add("write", update_frames)
    jaeger_count_var.trace_add("write", update_frames)
    
    update_frames()
    
    def start_simulation():
        from globals import mutation_loss_rate, prey_cooperation_probability, prey_schneller_metabolismus_probability, jaeger_angriff_probability
        try:
            num_beute = int(beute_count_var.get())
            num_jaeger = int(jaeger_count_var.get())
            mut_loss_percent = float(mutation_loss_var.get())
        except:
            num_beute = 3
            num_jaeger = 3
            mut_loss_percent = 3.0
        mutation_loss_rate = mut_loss_percent / 100.0
        try:
            prey_coop = float(prey_coop_prob_var.get())
        except:
            prey_coop = 2.0
        prey_cooperation_probability = prey_coop / 100.0
        try:
            prey_sm = float(prey_sm_prob_var.get())
        except:
            prey_sm = 4.0
        prey_schneller_metabolismus_probability = prey_sm / 100.0
        try:
            jaeger_angriff = float(jaeger_angriff_prob_var.get())
        except:
            jaeger_angriff = 5.0
        jaeger_angriff_probability = jaeger_angriff / 100.0
        
        # Speichere diese Werte in globals (überschreibe die Standardwerte)
        import globals as g
        g.mutation_loss_rate = mutation_loss_rate
        g.prey_cooperation_probability = prey_cooperation_probability
        g.prey_schneller_metabolismus_probability = prey_schneller_metabolismus_probability
        g.jaeger_angriff_probability = jaeger_angriff_probability

        beute_configs = []
        for i in range(num_beute):
            if i < len(beute_vars):
                config = {}
                for genome in available_genomes_beute:
                    if beute_vars[i][genome].get():
                        config[genome] = True
                beute_configs.append(config)
            else:
                beute_configs.append(default_beute.copy())
        jaeger_configs = []
        for i in range(num_jaeger):
            if i < len(jaeger_vars):
                config = {}
                for genome in available_genomes_jaeger:
                    if jaeger_vars[i][genome].get():
                        if genome == "Fortbewegung":
                            config[genome] = "sprinten"
                        elif genome == "Orientierung":
                            config[genome] = "riechen"
                        elif genome == "Angriff":
                            config[genome] = "Killer"
                        else:
                            config[genome] = True
                jaeger_configs.append(config)
            else:
                jaeger_configs.append(default_jaeger.copy())
        print("Beute-Konfigurationen:", beute_configs)
        print("Jäger-Konfigurationen:", jaeger_configs)
        config_root.destroy()
        from simulation import simulation_page
        simulation_page(beute_configs, jaeger_configs)
    
    start_button = tk.Button(config_root, text="Simulation starten", command=start_simulation)
    start_button.grid(row=8, column=0, columnspan=2, pady=10)
    
    config_root.mainloop()

if __name__ == "__main__":
    config_page()
