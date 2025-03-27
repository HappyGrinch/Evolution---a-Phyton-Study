# simulation.py

import tkinter as tk
import random
import time
import globals
from entities import Beute, Jaeger

def update_environment(canvas):
    if globals.paused:
        canvas.after(100, lambda: update_environment(canvas))
        return
    globals.global_co2 = len(globals.jaegers) * 2
    globals.global_oxygen += len(globals.beuten) * 1
    for obj in globals.beuten:
        if obj.genome.get("essen"):
            if globals.global_co2 >= 1:
                globals.global_co2 -= 1
                if obj.starving:
                    obj.starving = False
                    if obj.starve_job is not None:
                        obj.canvas.after_cancel(obj.starve_job)
                        obj.starve_job = None
            else:
                if not obj.starving:
                    obj.starving = True
                    delay = random.randint(1000, 3000)
                    obj.starve_job = obj.canvas.after(delay, lambda o=obj: o.destroy())
                    obj.start_blinking()
    if globals.global_co2 < 0:
        globals.global_co2 = 0
    canvas.itemconfigure(globals.co2_text_id, text="CO2: " + str(globals.global_co2))
    canvas.after(1000, lambda: update_environment(canvas))

def kollidieren(obj1, obj2):
    return (obj1.x < obj2.x + obj2.size and
            obj1.x + obj1.size > obj2.x and
            obj1.y < obj2.y + obj2.size and
            obj1.y + obj1.size > obj2.y)

def check_collisions(canvas):
    if globals.paused:
        canvas.after(100, lambda: check_collisions(canvas))
        return
    if globals.simulation_over:
        return
    current_time = time.time()
    to_remove_beute = set()
    for j in globals.jaegers:
        if "jagen" not in j.genome:
            continue
        if current_time - globals.simulation_start > 60:
            j.destroy()
            continue
        if j.fressen_count < 6:
            for b in globals.beuten:
                if b.immune and not ("Angriff" in j.genome and j.genome["Angriff"]=="Killer"):
                    continue
                if b.alive and kollidieren(j, b):
                    to_remove_beute.add(b)
                    j.last_meal = current_time
                    if j.fressen_count < 6:
                        j.fressen_count += 1
                    if not j.duplication_scheduled:
                        j.duplication_scheduled = True
                        j.start_blinking()
                        delay = random.randint(1000, 30000)
                        j.canvas.after(delay, j.duplicate)
    for b in to_remove_beute:
        b.destroy()
    globals.beuten[:] = [b for b in globals.beuten if b.alive]
    globals.jaegers[:] = [j for j in globals.jaegers if j.alive]
    n = len(globals.beuten)
    for i in range(n):
        for k in range(i+1, n):
            b1 = globals.beuten[i]
            b2 = globals.beuten[k]
            if not b1.alive or not b2.alive:
                continue
            if b1.genome.get("Kooperation") is True and not b1.immune:
                if kollidieren(b1, b2):
                    b1.size *= 2
                    b1.immune = True
                    del b1.genome["Kooperation"]
                    b1.canvas.itemconfigure(b1.rect_id, fill="#FFD700")
                    b1.canvas.coords(b1.rect_id, b1.x, b1.y, b1.x+b1.size, b1.y+b1.size)
                    b2.destroy()
    globals.beuten[:] = [b for b in globals.beuten if b.alive]
    if len(globals.beuten) == 0 or len(globals.jaegers) == 0:
        globals.simulation_over = True
        winner = "Jäger" if len(globals.beuten)==0 else "Beute"
        sim_time = current_time - globals.simulation_start
        message = f"Der Sieger: {winner}\nZeit: {sim_time:.1f} Sekunden\n"
        message += f"\nGesamter Sauerstoff: {globals.global_oxygen} Einheiten"
        message += f"\nGesamtes Kohlendioxid: {globals.global_co2} Einheiten"
        remaining = globals.jaegers if winner=="Jäger" else globals.beuten
        for obj in remaining:
            genome_list = ", ".join([f"{k}" if obj.genome[k] is True else f"{k}:{obj.genome[k]}" for k in obj.genome])
            message += f"\n{obj.obj_id} ({genome_list})"
        canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                           text=message, fill="black", font=("Helvetica",10))
        end_btn = tk.Button(canvas.master, text="Simulation beenden", command=canvas.master.destroy)
        canvas.create_window(canvas.winfo_width()/2, canvas.winfo_height()-30, window=end_btn)
    else:
        canvas.after(100, lambda: check_collisions(canvas))

def toggle_pause(event):
    import globals
    globals.paused = not globals.paused

def simulation_page(beute_configs, jaeger_configs):
    import globals
    globals.beuten.clear()
    globals.jaegers.clear()
    globals.simulation_over = False
    globals.unique_object_counter = 0
    globals.global_oxygen = 0
    globals.global_co2 = 0
    root = tk.Tk()
    root.title("Simulation")
    root.attributes("-fullscreen", True)
    root.bind("p", toggle_pause)
    root.update()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg="white")
    canvas.pack(fill=tk.BOTH, expand=True)
    root.update()
    canvas.create_text(10, 10, text="Prototyp Evolution by Andreas Wahl\nChatgpt O3 High\nVersion 0.26",
                       anchor="nw", fill="black", font=("Helvetica",9))
    globals.co2_text_id = canvas.create_text(screen_width - 10, 10, text="CO2: " + str(globals.global_co2),
                                              anchor="ne", fill="black", font=("Helvetica",11))
    globals.simulation_start = time.time()
    beute_x = 50
    num_beute = len(beute_configs)
    for config in beute_configs:
        for key in globals.available_genomes_beute:
            if key not in config:
                config[key] = False
    for config in jaeger_configs:
        for key in globals.available_genomes_jaeger:
            if key not in config:
                config[key] = False

    for i, config in enumerate(beute_configs):
        y = (i+1) * screen_height / (num_beute+1)
        new_beute = Beute(canvas, beute_x, y, genome=config)
        globals.beuten.append(new_beute)
    jaeger_x = screen_width - 70
    num_jaeger = len(jaeger_configs)
    for i, config in enumerate(jaeger_configs):
        y = (i+1) * screen_height / (num_jaeger+1)
        new_jaeger = Jaeger(canvas, jaeger_x, y, genome=config)
        globals.jaegers.append(new_jaeger)
    canvas.after(100, lambda: check_collisions(canvas))
    canvas.after(1000, lambda: update_environment(canvas))
    root.mainloop()
