import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO

class Aplicacion:
    def __init__(self, master):
        self.master = master
        self.master.title("Seleccionar Usuario")
        self.master.geometry("800x600")  # Tamaño de la ventana principal
        self.master.configure(bg="#FF8C00")  # Color de fondo naranja oscuro

        # Agregar título en la parte superior
        self.titulo = tk.Label(self.master, text="SELECCIONE SU PERFIL", bg="#FF8C00", fg="#FFFFFF", font=("Arial", 30, "bold"))
        self.titulo.pack(pady=20)

        # Crear botones para seleccionar usuario
        self.crear_botones()

    def crear_botones(self):
        # Estilo de los botones
        boton_color = "#FFD700"  # Color de fondo para ambos botones (amarillo)
        button_style = {
            "bg": boton_color,
            "fg": "#000000",  # Color del texto en negro
            "font": ("Arial", 24, "bold"),  # Fuente
            "relief": "solid",  # Borde sólido
            "borderwidth": 2,  # Ancho del borde
            "highlightbackground": "#000000",  # Color del borde
            "activebackground": "#FFC300",  # Color de fondo al hacer hover
            "activeforeground": "#000000",  # Color del texto al hacer hover
            "padx": 20,
            "pady": 20,
            "width": 10,
            "height": 4,
            "compound": "top"  # Texto debajo de la imagen
        }

        # Cargar imagen del prisionero
        url_prisionero = "https://img.freepik.com/vector-premium/icono-joven-prision-contorno-joven-carcel-icono-vectorial-color-plano-aislado_96318-126520.jpg"
        img_tk_prisionero = self.cargar_imagen(url_prisionero)

        # Botón de prisionero
        boton_prisionero = tk.Button(self.master, command=lambda: self.seleccionar_usuario('prisionero'), **button_style)
        boton_prisionero.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        if img_tk_prisionero:
            boton_prisionero.config(image=img_tk_prisionero, text="PRISIONERO")
            boton_prisionero.image = img_tk_prisionero

        # Cargar imagen del carcelero
        url_carcelero = "https://cdn-icons-png.flaticon.com/512/14167/14167711.png"
        img_tk_carcelero = self.cargar_imagen(url_carcelero)

        # Botón de carcelero
        boton_carcelero = tk.Button(self.master, command=lambda: self.seleccionar_usuario('carcelero'), **button_style)
        boton_carcelero.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        if img_tk_carcelero:
            boton_carcelero.config(image=img_tk_carcelero, text="CARCELERO")
            boton_carcelero.image = img_tk_carcelero

    def cargar_imagen(self, url):
        """ Descarga y redimensiona una imagen desde una URL """
        try:
            response = requests.get(url)
            response.raise_for_status()  # Genera error si la descarga falla
            img_data = response.content
            img = Image.open(BytesIO(img_data)).convert("RGBA").resize((100, 100), Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")
            return None

    def seleccionar_usuario(self, tipo_usuario):
        messagebox.showinfo("Resultado", f"Eres {tipo_usuario}.")
        self.master.destroy()

# Crear la ventana principal
root = tk.Tk()
root.attributes('-fullscreen', False)
app = Aplicacion(root)
root.mainloop()
