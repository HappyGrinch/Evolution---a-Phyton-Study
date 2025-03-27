# entities.py

import tkinter as tk
import random
import time
import globals

def berechne_farbe_beute(generation):
    green_value = max(255 - (generation - 1) * 20, 0)
    return f"#00{green_value:02x}00"

def berechne_farbe_jaeger(generation):
    blue_value = max(255 - (generation - 1) * 20, 0)
    return f"#0000{blue_value:02x}"

def kollidieren(obj1, obj2):
    return (obj1.x < obj2.x + obj2.size and
            obj1.x + obj1.size > obj2.x and
            obj1.y < obj2.y + obj2.size and
            obj1.y + obj1.size > obj2.y)

class Beute:
    def __init__(self, canvas, x, y, size=20, generation=1, genome=None):
        self.canvas = canvas
        self.size = size
        self.x = x
        self.y = y
        self.generation = generation
        # Wenn kein Genom übergeben wird, werden nur "essen" und "bewegen" gesetzt.
        if genome is None:
            self.genome = {"essen": True, "bewegen": True}
        else:
            self.genome = genome.copy()
        self.alive = True
        self.immune = False
        self.stripe_id = None  # Für "Schneller Metabolismus"
        self.starving = False
        self.starve_job = None
        self.blinking = False

        globals.unique_object_counter += 1
        self.obj_id = f"{self.generation}-{globals.unique_object_counter}"

        self.color = berechne_farbe_beute(self.generation)
        self.rect_id = self.canvas.create_rectangle(self.x, self.y, self.x+self.size, self.y+self.size,
                                                     fill=self.color, outline="")
        self.text_id = self.canvas.create_text(self.x+self.size/2, self.y+self.size/2,
                                                 text=self.obj_id, fill="white")
        # Linksklick-Zerstörung:
        self.canvas.tag_bind(self.rect_id, "<Button-1>", lambda event, obj=self: obj.destroy())
        self.canvas.tag_bind(self.text_id, "<Button-1>", lambda event, obj=self: obj.destroy())
        if self.genome.get("Schneller Metabolismus"):
            self.stripe_id = self.canvas.create_line(self.x, self.y, self.x+self.size, self.y+self.size,
                                                      fill="turquoise", width=2)
            self.canvas.tag_bind(self.stripe_id, "<Button-1>", lambda event, obj=self: obj.destroy())
        # Tooltip-Bindings (nur im Pausenmodus)
        self.canvas.tag_bind(self.rect_id, "<Enter>", self.show_tooltip)
        self.canvas.tag_bind(self.text_id, "<Enter>", self.show_tooltip)
        self.canvas.tag_bind(self.rect_id, "<Leave>", self.hide_tooltip)
        self.canvas.tag_bind(self.text_id, "<Leave>", self.hide_tooltip)
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        if self.genome.get("bewegen"):
            self.move()
        self.schedule_duplication()

    def move(self):
        if not self.alive:
            return
        if globals.paused:
            self.canvas.after(50, self.move)
            return
        self.vx += random.uniform(-0.5, 0.5)
        self.vy += random.uniform(-0.5, 0.5)
        max_speed = 3
        speed = (self.vx**2 + self.vy**2)**0.5
        if speed > max_speed:
            scale = max_speed/speed
            self.vx *= scale
            self.vy *= scale
        self.x += self.vx
        self.y += self.vy
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if self.x < 0:
            self.x = 0; self.vx = -self.vx
        elif self.x + self.size > width:
            self.x = width - self.size; self.vx = -self.vx
        if self.y < 0:
            self.y = 0; self.vy = -self.vy
        elif self.y + self.size > height:
            self.y = height - self.size; self.vy = -self.vy
        self.canvas.coords(self.rect_id, self.x, self.y, self.x+self.size, self.y+self.size)
        self.canvas.coords(self.text_id, self.x+self.size/2, self.y+self.size/2)
        if self.stripe_id is not None:
            self.canvas.coords(self.stripe_id, self.x, self.y, self.x+self.size, self.y+self.size)
        self.canvas.after(50, self.move)

    def schedule_duplication(self):
        if self.immune or globals.paused:
            return
        if "essen" not in self.genome and "jagen" not in self.genome:
            return
        if self.genome.get("Schneller Metabolismus"):
            delay = random.randint(1000, 5000)
        else:
            delay = random.randint(1000, 30000)
        self.canvas.after(delay, self.duplicate)

    def duplicate(self):
        if not self.alive or self.immune:
            return
        if globals.paused:
            self.canvas.after(1000, self.duplicate)
            return
        if "essen" not in self.genome and "jagen" not in self.genome:
            return
        child_genome = self.genome.copy()
        # Berücksichtige nur aktive Gene
        active_genes = [gene for gene, value in child_genome.items() if value]
        if active_genes and random.random() < globals.mutation_loss_rate:
            lost_gene = random.choice(active_genes)
            del child_genome[lost_gene]
        if "Kooperation" not in child_genome and random.random() < 0.02:
            child_genome["Kooperation"] = True
        if "Schneller Metabolismus" in self.genome:
            if random.random() >= 0.20:
                child_genome.pop("Schneller Metabolismus", None)
        else:
            if random.random() < 0.04:
                child_genome["Schneller Metabolismus"] = True
        new_child = Beute(self.canvas, self.x, self.y, self.size,
                          generation=self.generation+1, genome=child_genome)
        globals.beuten.append(new_child)
        self.schedule_duplication()

    def show_tooltip(self, event):
        if not globals.paused:
            return
        self.tooltip = tk.Toplevel(self.canvas)
        self.tooltip.wm_overrideredirect(True)
        label = tk.Label(self.tooltip, text=", ".join([f"{k}" if self.genome[k] is True else f"{k}:{self.genome[k]}" for k in self.genome]),
                          background="yellow", font=("Helvetica", 8))
        label.pack()
        self.tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")

    def hide_tooltip(self, event):
        if hasattr(self, "tooltip"):
            self.tooltip.destroy()
            del self.tooltip

    def start_blinking(self):
        self.blinking = True
        self.blink()

    def blink(self):
        if not self.blinking:
            return
        current_state = self.canvas.itemcget(self.rect_id, "state")
        new_state = "hidden" if current_state == "normal" else "normal"
        self.canvas.itemconfigure(self.rect_id, state=new_state)
        self.canvas.itemconfigure(self.text_id, state=new_state)
        if self.stripe_id is not None:
            self.canvas.itemconfigure(self.stripe_id, state=new_state)
        self.canvas.after(500, self.blink)

    def stop_blinking(self):
        self.blinking = False
        self.canvas.itemconfigure(self.rect_id, state="normal")
        self.canvas.itemconfigure(self.text_id, state="normal")
        if self.stripe_id is not None:
            self.canvas.itemconfigure(self.stripe_id, state="normal")

    def destroy(self):
        if self.alive:
            self.alive = False
            self.canvas.delete(self.rect_id)
            self.canvas.delete(self.text_id)
            if self.stripe_id is not None:
                self.canvas.delete(self.stripe_id)

class Jaeger:
    def __init__(self, canvas, x, y, size=20, generation=1, genome=None):
        self.canvas = canvas
        self.size = size
        self.x = x
        self.y = y
        self.generation = generation
        if genome is None:
            self.genome = {"Fortbewegung": "sprinten", "jagen": True, "Orientierung": "riechen"}
        else:
            self.genome = genome.copy()
        self.alive = True
        self.last_meal = time.time()
        self.fressen_count = 0
        self.duplication_scheduled = False
        self.blinking = False
        globals.unique_object_counter += 1
        self.obj_id = f"{self.generation}-{globals.unique_object_counter}"
        if "Angriff" in self.genome and self.genome["Angriff"] == "Killer":
            self.color = "#ff0000"
        else:
            self.color = berechne_farbe_jaeger(self.generation)
        self.oval_id = self.canvas.create_oval(self.x, self.y, self.x+self.size, self.y+self.size,
                                                fill=self.color, outline="")
        self.text_id = self.canvas.create_text(self.x+self.size/2, self.y+self.size/2,
                                                text=self.obj_id, fill="white")
        self.canvas.tag_bind(self.oval_id, "<Button-1>", lambda event, obj=self: obj.destroy())
        self.canvas.tag_bind(self.text_id, "<Button-1>", lambda event, obj=self: obj.destroy())
        self.canvas.tag_bind(self.oval_id, "<Enter>", self.show_tooltip)
        self.canvas.tag_bind(self.text_id, "<Enter>", self.show_tooltip)
        self.canvas.tag_bind(self.oval_id, "<Leave>", self.hide_tooltip)
        self.canvas.tag_bind(self.text_id, "<Leave>", self.hide_tooltip)
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        if "Fortbewegung" in self.genome:
            self.move()

    def move(self):
        from globals import paused, beuten
        if not self.alive:
            return
        if paused:
            self.canvas.after(50, self.move)
            return
        if "Fortbewegung" not in self.genome:
            self.canvas.after(50, self.move)
            return
        if "Orientierung" in self.genome and self.genome["Orientierung"] == "riechen":
            # Geänderter sense_radius: 200
            sense_radius = 200
            ax, ay = 0, 0
            count = 0
            for prey in beuten:
                if not prey.alive or "geruchlos" in prey.genome:
                    continue
                prey_center_x = prey.x + prey.size/2
                prey_center_y = prey.y + prey.size/2
                jaeger_center_x = self.x + self.size/2
                jaeger_center_y = self.y + self.size/2
                dx = prey_center_x - jaeger_center_x
                dy = prey_center_y - jaeger_center_y
                distance = (dx**2 + dy**2)**0.5
                if distance < sense_radius and distance > 0:
                    weight = (sense_radius - distance) / sense_radius
                    ax += dx * weight
                    ay += dy * weight
                    count += 1
            if count > 0:
                # Erhöhter smell_factor: 0.1 statt 0.05
                smell_factor = 0.1
                self.vx += smell_factor * ax
                self.vy += smell_factor * ay
        sprint_multiplier = 1.5 if self.genome.get("Fortbewegung") == "sprinten" else 1.0
        self.vx += random.uniform(-0.5, 0.5)
        self.vy += random.uniform(-0.5, 0.5)
        max_speed = 3 * sprint_multiplier
        speed = (self.vx**2 + self.vy**2)**0.5
        if speed > max_speed:
            scale = max_speed/speed
            self.vx *= scale
            self.vy *= scale
        self.x += self.vx
        self.y += self.vy
        width = self.canvas.winfo_screenwidth()
        height = self.canvas.winfo_screenheight()
        if self.x < 0:
            self.x = 0; self.vx = -self.vx
        elif self.x + self.size > width:
            self.x = width - self.size; self.vx = -self.vx
        if self.y < 0:
            self.y = 0; self.vy = -self.vy
        elif self.y + self.size > height:
            self.y = height - self.size; self.vy = -self.vy
        self.canvas.coords(self.oval_id, self.x, self.y, self.x+self.size, self.y+self.size)
        self.canvas.coords(self.text_id, self.x+self.size/2, self.y+self.size/2)
        self.canvas.after(50, self.move)

    def show_tooltip(self, event):
        from globals import paused
        if not paused:
            return
        self.tooltip = tk.Toplevel(self.canvas)
        self.tooltip.wm_overrideredirect(True)
        label = tk.Label(self.tooltip, text=", ".join([f"{k}" if self.genome[k] is True else f"{k}:{self.genome[k]}" for k in self.genome]),
                          background="yellow", font=("Helvetica",8))
        label.pack()
        self.tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")

    def hide_tooltip(self, event):
        if hasattr(self, "tooltip"):
            self.tooltip.destroy()
            del self.tooltip

    def start_blinking(self):
        self.blinking = True
        self.blink()

    def blink(self):
        if not self.blinking:
            return
        current_state = self.canvas.itemcget(self.oval_id, "state")
        new_state = "hidden" if current_state == "normal" else "normal"
        self.canvas.itemconfigure(self.oval_id, state=new_state)
        self.canvas.itemconfigure(self.text_id, state=new_state)
        self.canvas.after(500, self.blink)

    def stop_blinking(self):
        self.blinking = False
        self.canvas.itemconfigure(self.oval_id, state="normal")
        self.canvas.itemconfigure(self.text_id, state="normal")

    def duplicate(self):
        if not self.alive or self.fressen_count == 0:
            return
        child_genome = self.genome.copy()
        active_genes = [gene for gene, value in child_genome.items() if value]
        if active_genes and random.random() < globals.mutation_loss_rate:
            lost_gene = random.choice(active_genes)
            del child_genome[lost_gene]
        if self.fressen_count >= 6 and "Angriff" not in child_genome and random.random() < 0.05:
            child_genome["Angriff"] = "Killer"
        new_child = Jaeger(self.canvas, self.x, self.y, self.size,
                           generation=self.generation+1, genome=child_genome)
        new_child.genome = child_genome
        if "Angriff" in new_child.genome and new_child.genome["Angriff"] == "Killer":
            new_child.color = "#ff0000"
            new_child.canvas.itemconfigure(new_child.oval_id, fill=new_child.color)
        from globals import jaegers
        jaegers.append(new_child)
        self.fressen_count = 0
        self.duplication_scheduled = False
        self.stop_blinking()

    def destroy(self):
        if self.alive:
            self.alive = False
            self.canvas.delete(self.oval_id)
            self.canvas.delete(self.text_id)
