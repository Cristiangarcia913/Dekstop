import tkinter as tk
from tkinter import messagebox
class Aplicacion:
    def __init__(self, master):
        self.master = master
        self.master.title("Verificar Usuario")
        self.master.geometry("300x200")
        # Variable para almacenar el tipo de usuario
        self.tipo_usuario = None
        # Preguntar al usuario qué tipo de usuario es
        self.preguntar_usuario()
    def preguntar_usuario(self):
        respuesta = messagebox.askquestion("Seleccionar Usuario", "¿Eres prisionero?")
        if respuesta == 'yes':
            self.tipo_usuario = 'prisionero'
            messagebox.showinfo("Resultado", "Eres prisionero.")
            self.desactivar_botones()
        else:
            self.tipo_usuario = 'carcelero'
            messagebox.showinfo("Resultado", "Eres carcelero.")
            self.activar_botones()
    def desactivar_botones(self):
        # Aquí puedes desactivar o ocultar botones si es necesario
        pass
    def activar_botones(self):
        # Crear el botón de cámaras de seguridad
        boton_camaras = tk.Button(self.master, text="Cámaras de Seguridad", command=self.mostrar_camaras)
        boton_camaras.pack(pady=50)
    def mostrar_camaras(self):
        messagebox.showinfo("Cámaras de Seguridad", "Aquí se mostrarían las cámaras de seguridad.")
# Crear la ventana principal
root = tk.Tk()
app = Aplicacion(root)
# Iniciar el bucle principal de la aplicación
root.mainloop()
