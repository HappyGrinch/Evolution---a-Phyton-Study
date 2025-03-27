<<<<<<< HEAD
# config.py

import tkinter as tk
from globals import available_genomes_beute, default_beute, available_genomes_jaeger, default_jaeger

def config_page():
    config_root = tk.Tk()
    config_root.title("Konfigurationsseite")
    tk.Label(config_root, text="Anzahl Beute:").grid(row=0, column=0, sticky="w")
    beute_count_var = tk.StringVar(value="3")
    tk.Entry(config_root, textvariable=beute_count_var, width=5).grid(row=0, column=1, sticky="w")

    tk.Label(config_root, text="Anzahl Jäger:").grid(row=1, column=0, sticky="w")
    jaeger_count_var = tk.StringVar(value="3")
    tk.Entry(config_root, textvariable=jaeger_count_var, width=5).grid(row=1, column=1, sticky="w")

    tk.Label(config_root, text="Mutation Verlust Genom [%]:").grid(row=2, column=0, sticky="w")
    mutation_loss_var = tk.StringVar(value="3")
    tk.Entry(config_root, textvariable=mutation_loss_var, width=5).grid(row=2, column=1, sticky="w")

    beute_frame = tk.LabelFrame(config_root, text="Beute Genome")
    beute_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="we")
    beute_vars = []
    for i in range(3):
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

    jaeger_frame = tk.LabelFrame(config_root, text="Jäger Genome")
    jaeger_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="we")
    jaeger_vars = []
    for i in range(3):
        row = i
        tk.Label(jaeger_frame, text=f"Jäger {i+1}:").grid(row=row, column=0, sticky="w")
        var_dict = {}
        col = 1
        for genome in available_genomes_jaeger:
            var = tk.BooleanVar(value=default_jaeger.get(genome, False))
            chk = tk.Checkbutton(jaeger_frame, text=genome, variable=var)
            chk.grid(row=row, column=col, sticky="w")
            var_dict[genome] = var
            col += 1
        jaeger_vars.append(var_dict)

    def start_simulation():
        from globals import mutation_loss_rate
        try:
            num_beute = int(beute_count_var.get())
            num_jaeger = int(jaeger_count_var.get())
            mut_loss_percent = float(mutation_loss_var.get())
        except:
            num_beute = 3
            num_jaeger = 3
            mut_loss_percent = 3.0
        mutation_loss_rate = mut_loss_percent / 100.0
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
    start_button.grid(row=5, column=0, columnspan=2, pady=10)

    config_root.mainloop()

if __name__ == "__main__":
    config_page()
=======
# config.py

import tkinter as tk
from globals import available_genomes_beute, default_beute, available_genomes_jaeger, default_jaeger

def config_page():
    config_root = tk.Tk()
    config_root.title("Konfigurationsseite")
    tk.Label(config_root, text="Anzahl Beute:").grid(row=0, column=0, sticky="w")
    beute_count_var = tk.StringVar(value="3")
    tk.Entry(config_root, textvariable=beute_count_var, width=5).grid(row=0, column=1, sticky="w")

    tk.Label(config_root, text="Anzahl Jäger:").grid(row=1, column=0, sticky="w")
    jaeger_count_var = tk.StringVar(value="3")
    tk.Entry(config_root, textvariable=jaeger_count_var, width=5).grid(row=1, column=1, sticky="w")

    # Neues Zahlenfeld für Mutation-Verlust-Rate:
    tk.Label(config_root, text="Mutation Verlust Genom [%]:").grid(row=2, column=0, sticky="w")
    mutation_loss_var = tk.StringVar(value="3")
    tk.Entry(config_root, textvariable=mutation_loss_var, width=5).grid(row=2, column=1, sticky="w")

    beute_frame = tk.LabelFrame(config_root, text="Beute Genome")
    beute_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="we")
    beute_vars = []
    for i in range(3):
        row = i
        tk.Label(beute_frame, text=f"Beute {i+1}:").grid(row=row, column=0, sticky="w")
        var_dict = {}
        col = 1
        for genome in available_genomes_beute:
            # Für Beute wird "Kooperation" NICHT als Standard gesetzt
            default_val = default_beute.get(genome, False)
            var = tk.BooleanVar(value=default_val)
            chk = tk.Checkbutton(beute_frame, text=genome, variable=var)
            chk.grid(row=row, column=col, sticky="w")
            var_dict[genome] = var
            col += 1
        beute_vars.append(var_dict)

    jaeger_frame = tk.LabelFrame(config_root, text="Jäger Genome")
    jaeger_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="we")
    jaeger_vars = []
    for i in range(3):
        row = i
        tk.Label(jaeger_frame, text=f"Jäger {i+1}:").grid(row=row, column=0, sticky="w")
        var_dict = {}
        col = 1
        for genome in available_genomes_jaeger:
            var = tk.BooleanVar(value=default_jaeger.get(genome, False))
            chk = tk.Checkbutton(jaeger_frame, text=genome, variable=var)
            chk.grid(row=row, column=col, sticky="w")
            var_dict[genome] = var
            col += 1
        jaeger_vars.append(var_dict)

    def start_simulation():
        global mutation_loss_rate
        try:
            num_beute = int(beute_count_var.get())
            num_jaeger = int(jaeger_count_var.get())
            mut_loss_percent = float(mutation_loss_var.get())
        except:
            num_beute = 3
            num_jaeger = 3
            mut_loss_percent = 3.0
        mutation_loss_rate = mut_loss_percent / 100.0
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
        config_root.destroy()
        # Übergabe an die Simulationsseite:
        from simulation import simulation_page
        simulation_page(beute_configs, jaeger_configs)

    start_button = tk.Button(config_root, text="Simulation starten", command=start_simulation)
    start_button.grid(row=5, column=0, columnspan=2, pady=10)

    config_root.mainloop()

if __name__ == "__main__":
    config_page()
>>>>>>> 8c9e4f4916dfd7836593ab546b60feed94cdf472
