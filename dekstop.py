# aplicacion.py

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO

class Aplicacion:
    def __init__(self, master):
        self.master = master
        self.master.title("Seleccionar Usuario")
        self.master.geometry("800x600")
        self.master.configure(bg="#FF8C00")

        self.titulo = tk.Label(
            self.master, 
            text="SELECCIONE SU PERFIL",
            bg="#FF8C00",
            fg="#FFFFFF",
            font=("Arial", 30, "bold")
        )
        self.titulo.pack(pady=20)

        self.crear_botones()

    def crear_botones(self):
        boton_color = "#FFD700"
        button_style = {
            "bg": boton_color,
            "fg": "#000000",
            "font": ("Arial", 24, "bold"),
            "relief": "solid",
            "borderwidth": 2,
            "highlightbackground": "#000000",
            "activebackground": "#FFC300",
            "activeforeground": "#000000",
            "padx": 20,
            "pady": 20,
            "width": 10,
            "height": 4,
            "compound": "top"
        }

        # Botón Prisionero
        img_prisionero = self.cargar_imagen(
            "https://img.freepik.com/vector-premium/icono-joven-prision-contorno-joven-carcel-icono-vectorial-color-plano-aislado_96318-126520.jpg"
        )
        btn_prisionero = tk.Button(
            self.master,
            command=lambda: self.seleccionar_usuario('prisionero'),
            **button_style
        )
        btn_prisionero.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        if img_prisionero:
            btn_prisionero.config(image=img_prisionero, text="PRISIONERO")
            btn_prisionero.image = img_prisionero

        # Botón Carcelero
        img_carcelero = self.cargar_imagen(
            "https://cdn-icons-png.flaticon.com/512/14167/14167711.png"
        )
        btn_carcelero = tk.Button(
            self.master,
            command=lambda: self.seleccionar_usuario('carcelero'),
            **button_style
        )
        btn_carcelero.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        if img_carcelero:
            btn_carcelero.config(image=img_carcelero, text="CARCELERO")
            btn_carcelero.image = img_carcelero

    def cargar_imagen(self, url):
        try:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content)).convert("RGBA").resize((100, 100), Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception:
            return None

    def seleccionar_usuario(self, tipo_usuario):
        self.master.destroy()
        if tipo_usuario == 'carcelero':
            from carcelero import DesktopCarcelero
            root = tk.Tk()
            DesktopCarcelero(root)
            root.mainloop()
        elif tipo_usuario == 'prisionero':
            from prisionero import DesktopPrisionero
            root = tk.Tk()
            DesktopPrisionero(root)
            root.mainloop()
        else:
            messagebox.showinfo("En desarrollo", "Módulo no disponible")

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()
