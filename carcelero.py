import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class DesktopCarcelero:
    def __init__(self, master):
        self.master = master
        self.master.title("Desktop - Carcelero")
        self.master.geometry("1024x768")
        self.master.configure(bg="#0078D7")

        self.menu_abierto = False
        self.frame_menu = None

        self.carpeta_datos = "datos_prision"
        self.crear_estructura_datos()

        self.prisioneros = self.cargar_datos("prisioneros")
        self.celdas = self.cargar_datos("celdas")
        self.visitas = self.cargar_datos("visitas")

        self.crear_interfaz()

    def crear_estructura_datos(self):
        for subcarpeta in ["prisioneros", "celdas", "visitas", "reportes"]:
            os.makedirs(f"{self.carpeta_datos}/{subcarpeta}", exist_ok=True)
        for archivo in ["prisioneros.json", "celdas.json", "visitas.json"]:
            ruta = f"{self.carpeta_datos}/{archivo.split('.')[0]}/{archivo}"
            if not os.path.exists(ruta):
                with open(ruta, "w") as f:
                    json.dump([], f)

    def cargar_datos(self, tipo):
        try:
            with open(f"{self.carpeta_datos}/{tipo}/{tipo}.json", "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def guardar_datos(self, tipo, datos):
        with open(f"{self.carpeta_datos}/{tipo}/{tipo}.json", "w") as f:
            json.dump(datos, f, indent=4)

    def crear_interfaz(self):
        # Frame principal
        self.desktop = tk.Frame(self.master, bg="#0078D7")
        self.desktop.pack(fill="both", expand=True)

        # --- Botón de regreso al menú principal ---
        btn_volver = tk.Button(
            self.desktop,
            text="↩ Volver al Menú",
            bg="#2B2B2B",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="raised",
            command=self.volver_a_seleccion_usuario
        )
        btn_volver.place(x=10, y=10)

        # Barra de tareas
        self.barra_tareas = tk.Frame(self.master, bg="#2B2B2B", height=50)
        self.barra_tareas.pack(side="bottom", fill="x")

        # Botones en barra de tareas
        botones_barra = [
            ("🏠 Inicio", self.menu_inicio),
            ("👤 Usuarios", self.volver_a_seleccion_usuario),
        ]
        for texto, comando in botones_barra:
            btn = tk.Button(
                self.barra_tareas,
                text=texto,
                bg="#2B2B2B",
                fg="white",
                font=("Arial", 10, "bold"),
                relief="flat",
                command=comando
            )
            btn.pack(side="left", padx=5)

        self.crear_iconos()

    def volver_a_seleccion_usuario(self):
        self.master.destroy()
        from dekstop import Aplicacion   # asegúrate de que tu primer script esté en menu.py
        root = tk.Tk()
        Aplicacion(root)
        root.mainloop()

    def crear_iconos(self):
        iconos = [
            ("Prisioneros", "📋", self.abrir_prisioneros),
            ("Celdas",      "🚪", self.abrir_celdas),
            ("Visitas",     "👥", self.abrir_visitas),
            ("Reportes",    "📊", self.generar_reportes),
        ]
        for i, (nombre, emoji, comando) in enumerate(iconos):
            frame = tk.Frame(self.desktop, bg="#0078D7")
            frame.place(x=50 + i*120, y=80)

            lbl_icono = tk.Label(
                frame,
                text=emoji,
                font=("Arial", 64),
                bg="#0078D7",
                cursor="hand2"
            )
            lbl_icono.pack()
            lbl_icono.bind("<Button-1>", lambda e, cmd=comando: cmd())

            tk.Label(
                frame,
                text=nombre,
                bg="#0078D7",
                fg="white",
                font=("Arial", 12, "bold")
            ).pack()

    def menu_inicio(self):
        if self.menu_abierto:
            self.frame_menu.destroy()
            self.menu_abierto = False
        else:
            self.frame_menu = tk.Frame(
                self.master,
                bg="#2B2B2B",
                bd=0,
                highlightthickness=1,
                highlightbackground="#555555"
            )
            self.frame_menu.place(x=10, y=718, width=250, height=200)

            opciones = [
                ("📋 Prisioneros", self.abrir_prisioneros),
                ("🚪 Celdas",      self.abrir_celdas),
                ("👥 Visitas",     self.abrir_visitas),
                ("📊 Reportes",    self.generar_reportes),
                ("⏻ Salir",        self.master.destroy)
            ]
            for texto, comando in opciones:
                btn = tk.Button(
                    self.frame_menu,
                    text=texto,
                    bg="#2B2B2B",
                    fg="white",
                    font=("Arial", 10),
                    anchor="w",
                    relief="flat",
                    command=comando
                )
                btn.pack(fill="x", padx=5, pady=2)

            self.menu_abierto = True

    # === Métodos stub para evitar AttributeError ===
    def abrir_prisioneros(self):
        messagebox.showinfo("Prisioneros", "Módulo de prisioneros en desarrollo.")

    def abrir_celdas(self):
        messagebox.showinfo("Celdas", "Módulo de celdas en desarrollo.")

    def abrir_visitas(self):
        messagebox.showinfo("Visitas", "Módulo de visitas en desarrollo.")

    def generar_reportes(self):
        messagebox.showinfo("Reportes", "Generación de reportes en desarrollo.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DesktopCarcelero(root)
    root.mainloop()
