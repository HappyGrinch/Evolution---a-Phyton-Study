# simulation.py

import tkinter as tk
import random
import time
from globals import beuten, jaegers, simulation_start, simulation_over, unique_object_counter, global_oxygen, global_co2, co2_text_id, available_genomes_beute, available_genomes_jaeger, paused

from entities import Beute, Jaeger  # Importiere die Objekte
from globals import mutation_loss_rate

def update_environment(canvas):
    global global_oxygen, global_co2, beuten, jaegers, co2_text_id, paused
    if paused:
        canvas.after(100, lambda: update_environment(canvas))
        return
    # Setze global_co2 neu: Alle Jäger produzieren 2 Einheiten CO2 pro Sekunde
    global_co2 = len(jaegers) * 2
    # Sauerstoff akkumuliert:
    global_oxygen += len(beuten) * 1
    # Verbrauch: Für jedes Beute-Objekt mit "essen" wird 1 Einheit CO2 abgezogen, falls verfügbar:
    for obj in beuten:
        if obj.genome.get("essen"):
            if global_co2 >= 1:
                global_co2 -= 1
                if obj.starving:
                    obj.starving = False
                    if obj.starve_job is not None:
                        obj.canvas.after_cancel(obj.starve_job)
                        obj.starve_job = None
            else:
                if not obj.starving:
                    obj.starving = True
                    delay = random.randint(1000,3000)
                    obj.starve_job = obj.canvas.after(delay, lambda o=obj: o.destroy())
                    obj.start_blinking()
    if global_co2 < 0:
        global_co2 = 0
    canvas.itemconfigure(co2_text_id, text="CO2: " + str(global_co2))
    canvas.after(1000, lambda: update_environment(canvas))

def kollidieren(obj1, obj2):
    return (obj1.x < obj2.x + obj2.size and
            obj1.x + obj1.size > obj2.x and
            obj1.y < obj2.y + obj2.size and
            obj1.y + obj1.size > obj2.y)

def check_collisions(canvas):
    global beuten, jaegers, simulation_over, simulation_start, paused
    if paused:
        canvas.after(100, lambda: check_collisions(canvas))
        return
    if simulation_over:
        return
    current_time = time.time()
    to_remove_beute = set()
    for j in jaegers:
        if "jagen" not in j.genome:
            continue
        if current_time - j.last_meal > 60:
            j.destroy()
            continue
        if j.fressen_count < 6:
            for b in beuten:
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
                        delay = random.randint(1000,30000)
                        j.canvas.after(delay, j.duplicate)
    for b in to_remove_beute:
        b.destroy()
    beuten[:] = [b for b in beuten if b.alive]
    jaegers[:] = [j for j in jaegers if j.alive]
    n = len(beuten)
    for i in range(n):
        for k in range(i+1, n):
            b1 = beuten[i]
            b2 = beuten[k]
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
    beuten[:] = [b for b in beuten if b.alive]
    if len(beuten)==0 or len(jaegers)==0:
        simulation_over = True
        winner = "Jäger"
