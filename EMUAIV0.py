#!/usr/bin/env python3
import threading
import tkinter as tk
from tkinter import ttk, filedialog
import numpy as np
import random
import time
from PIL import Image, ImageTk

# Welcome message with ultra vibes
print("[🌌] WELCOME TO FLAME64: ULTRAHLE CHAOS CORE INITIATED")

# ------------------------------------------------------------------------------
# Chaos Engine - The heart of the chaos
# ------------------------------------------------------------------------------
class ChaosEngine:
    def __init__(self):
        # Allocate 4MB for ROM data
        self.memory = bytearray(4 * 1024 * 1024)
        # 64x64 state array (seeded with random chaos)
        self.state = np.random.rand(64, 64)
        # Running flag for clean thread termination
        self.running = False
        # 240x320 RGB frame for display output
        self.frame = np.zeros((240, 320, 3), dtype=np.uint8)
        # Thread lock for safe concurrent access
        self.lock = threading.Lock()

    def load_rom(self, rom_data):
        """
        Loads ROM data (up to 4MB) and uses its first 4096 bytes
        to seed the internal chaos state.
        """
        rom_data = rom_data[:len(self.memory)]
        self.memory[:len(rom_data)] = rom_data
        # Use the first 4096 bytes, pad with zeros if needed, then normalize
        buffer = rom_data[:4096].ljust(4096, b'\x00')
        self.state = np.frombuffer(buffer, dtype=np.uint8).reshape(64, 64) / 255.0
        print(f"[🌀] Chaos ingested: {len(rom_data)} bytes mutated into state")

    def reset(self):
        """
        Resets the chaos state to a fresh random configuration and clears the frame.
        """
        with self.lock:
            self.state = np.random.rand(64, 64)
            self.frame.fill(0)
        print("[🔄] Chaos reset to primal state")

    def evolve(self):
        """
        Evolves the chaos state by updating each cell based on its neighbors,
        adding a touch of randomness, and then rendering the new frame.
        """
        with self.lock:
            new_state = self.state.copy()
            for i in range(64):
                for j in range(64):
                    # Sum of neighboring cells (exclude the center)
                    neighbors = (
                        self.state[max(0, i-1):i+2, max(0, j-1):j+2].sum()
                        - self.state[i, j]
                    )
                    new_state[i, j] = (
                        self.state[i, j]
                        + neighbors * 0.1
                        + random.random() * 0.05
                    ) % 1.0
            self.state = new_state
            self.render_chaos()

    def render_chaos(self):
        """
        Renders the internal state to a 240x320 RGB frame,
        modulated by time for ultra-dynamic colors.
        """
        current_time = time.time()
        for y in range(240):
            sy = int(y / 3.75)
            for x in range(320):
                sx = int(x / 5)
                val = self.state[sy, sx]
                self.frame[y, x] = [
                    int(val * 127.5 * (1 + np.sin(current_time))),
                    int(val * 127.5 * (1 + np.cos(current_time * 1.1))),
                    int(val * 127.5 * (1 + np.sin(current_time * 1.2)))
                ]

# ------------------------------------------------------------------------------
# Core Emulator Backend (ChaosCore)
# ------------------------------------------------------------------------------
class ChaosCore:
    def __init__(self):
        self.engine = ChaosEngine()
        self.thread = None

    def load_rom(self, filepath):
        """
        Reads a ROM file from disk, seeds the chaos engine, and starts the chaos thread.
        """
        try:
            with open(filepath, 'rb') as f:
                rom_data = f.read()
            self.engine.load_rom(rom_data)
            self.start_chaos()
        except Exception as e:
            print(f"[❌] Unable to load ROM: {e}")

    def reset_rom(self):
        """
        Resets the chaos engine's state.
        """
        self.engine.reset()

    def launch_debugger(self):
        """
        Placeholder for a debugger plug-in.
        """
        print("[🐞] Chaos Debugger: Observing entropy flow…")

    def launch_inspector(self):
        """
        Placeholder for an inspector plug-in.
        """
        print("[🧠] Chaos Inspector: Peering into the void…")

    def start_chaos(self):
        """
        Starts (or restarts) the chaos engine's background evolution thread.
        """
        if self.thread and self.thread.is_alive():
            self.engine.running = False
            self.thread.join()
        self.engine.running = True
        self.thread = threading.Thread(target=self.run_chaos, daemon=True)
        self.thread.start()

    def run_chaos(self):
        """
        The background loop evolving chaos at roughly 60 FPS.
        """
        while self.engine.running:
            self.engine.evolve()
            time.sleep(0.016)

    def stop_chaos(self):
        """
        Gracefully stops the chaos engine.
        """
        self.engine.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join()

# ------------------------------------------------------------------------------
# Parallel Launcher-style GUI (Tkinter)
# ------------------------------------------------------------------------------
class ParallelLauncherGUI:
    def __init__(self, master, chaos_core):
        self.master = master
        self.core = chaos_core

        # Ultra-cool window settings
        self.master.title("🔥 FLAME64 - ULTRAHLE CHAOS CORE")
        self.master.geometry("1000x600")
        self.master.configure(bg="#1e1e1e")

        # -- Sidebar --
        sidebar = tk.Frame(master, bg="#2a2a2a", width=200)
        sidebar.pack(side="left", fill="y")

        # Status label with ultra-vibes
        self.status_label = tk.Label(
            sidebar,
            text="Ready",
            font=("Arial", 10),
            fg="white",
            bg="#2a2a2a",
            wraplength=180
        )
        self.status_label.pack(pady=5)

        tk.Label(
            sidebar,
            text="FLAME64",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#2a2a2a"
        ).pack(pady=10)

        ttk.Button(
            sidebar,
            text="Load ROM",
            command=self.load_rom_dialog
        ).pack(pady=5, padx=10, fill="x")

        ttk.Button(
            sidebar,
            text="Reset Entropy",
            command=self.reset_rom
        ).pack(pady=5, padx=10, fill="x")

        ttk.Button(
            sidebar,
            text="Debugger",
            command=self.core.launch_debugger
        ).pack(pady=5, padx=10, fill="x")

        ttk.Button(
            sidebar,
            text="Inspector",
            command=self.core.launch_inspector
        ).pack(pady=5, padx=10, fill="x")

        # -- Display Frame --
        display_frame = tk.Frame(master, bg="#1e1e1e")
        display_frame.pack(side="left", expand=True, fill="both")

        self.chaos_label = tk.Label(display_frame, bg="black")
        self.chaos_label.pack(pady=20)

        self.photo = None
        self.update_frame()

    def load_rom_dialog(self):
        """
        Opens a file dialog for ROM selection and loads the chosen file.
        """
        try:
            filepath = filedialog.askopenfilename(
                title="Open ROM",
                filetypes=[
                    ("N64 ROMs", "*.n64;*.z64;*.v64"),
                    ("All files", "*.*")
                ]
            )
            if filepath:
                self.status_label.config(text="Loading ROM...")
                self.master.update()
                self.core.load_rom(filepath)
                # Display only the file name in status
                self.status_label.config(text=f"Loaded: {filepath.split('/')[-1]}")
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")
            print(f"[❌] ROM loading error: {e}")

    def reset_rom(self):
        """
        Resets the chaos engine and updates the status.
        """
        try:
            self.status_label.config(text="Resetting...")
            self.master.update()
            self.core.reset_rom()
            self.status_label.config(text="Reset complete")
        except Exception as e:
            self.status_label.config(text=f"Reset error: {str(e)}")
            print(f"[❌] Reset error: {e}")

    def update_frame(self):
        """
        Updates the displayed chaos frame at roughly 60 FPS.
        """
        try:
            with self.core.engine.lock:
                img = Image.fromarray(self.core.engine.frame.copy(), 'RGB')
            self.photo = ImageTk.PhotoImage(image=img)
            self.chaos_label.configure(image=self.photo)
        except Exception as e:
            print(f"[⚠️] Frame update error: {e}")
        self.master.after(16, self.update_frame)


# ------------------------------------------------------------------------------
# Entry Point
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    root = tk.Tk()
    core = ChaosCore()
    gui = ParallelLauncherGUI(root, core)

    # Ensure a graceful shutdown of the chaos engine
    def on_close():
        core.stop_chaos()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()
