import tkinter as tk
from tkinter import messagebox
import random
import threading
import time
import math  # 使用Python的math模块

class Firework:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.particles = []
        for _ in range(50):
            angle = random.uniform(0, 2 * math.pi)  # 使用math.pi
            speed = random.uniform(2, 5)
            self.particles.append([
                self.x,
                self.y,
                speed * math.cos(angle),  # 使用math.cos
                speed * math.sin(angle),  # 使用math.sin
                random.choice(['red', 'yellow', 'blue', 'white', 'orange'])
            ])

    def update(self):
        new_particles = []
        for px, py, vx, vy, color in self.particles:
            px += vx
            py += vy
            vy += 0.05  # gravity effect
            new_particles.append([px, py, vx, vy, color])

            # Draw particle
            self.canvas.create_oval(px-2, py-2, px+2, py+2, fill=color, outline=color)

        self.particles = new_particles

class SnakeYearGreetingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("蛇年祝福")
        self.root.geometry("800x600")

        self.canvas = tk.Canvas(root, width=800, height=600, bg='black')
        self.canvas.pack()

        self.fireworks = []

        # Display the greeting text
        self.greeting_label = tk.Label(
            root,
            text="祝您蛇年大吉，幸福安康！",
            font=("Helvetica", 24),
            fg="gold",
            bg="black"
        )
        self.greeting_label.pack(pady=20)

        # Button to trigger fireworks
        self.button = tk.Button(
            root,
            text="点击燃放烟花",
            command=self.launch_fireworks,
            bg="darkred",
            fg="white",
            font=("Helvetica", 16)
        )
        self.button.pack(pady=10)

        self.running = True
        self.animation_thread = threading.Thread(target=self.animate)
        self.animation_thread.start()

    def launch_fireworks(self):
        for _ in range(5):
            x = random.randint(100, 700)
            y = random.randint(50, 200)
            self.fireworks.append(Firework(self.canvas, x, y))

    def animate(self):
        while self.running:
            self.canvas.delete("all")  # Clear canvas
            for firework in self.fireworks:
                firework.update()
            self.root.update()
            time.sleep(0.03)  # Control animation speed

    def on_closing(self):
        self.running = False
        self.root.quit()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SnakeYearGreetingApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()