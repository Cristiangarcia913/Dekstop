import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
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
        self.celdas      = self.cargar_datos("celdas")
        self.visitas     = self.cargar_datos("visitas")

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
        from menu import Aplicacion
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

    # === Módulo Prisioneros ===
    def abrir_prisioneros(self):
        win = tk.Toplevel(self.master)
        win.title("Prisioneros")
        win.geometry("700x400")

        cols = ("id", "nombre", "edad", "delito", "fecha_ingreso", "celda_id")
        tree = ttk.Treeview(win, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c.capitalize())
            tree.column(c, width=100)
        tree.pack(fill="both", expand=True, side="left", padx=5, pady=5)

        def refrescar():
            tree.delete(*tree.get_children())
            for p in self.prisioneros:
                tree.insert("", "end", values=(
                    p["id"], p["nombre"], p["edad"],
                    p["delito"], p["fecha_ingreso"], p.get("celda_id", "")
                ))

        def añadir():
            # Pedir datos al usuario
            nombre = simpledialog.askstring("Nombre", "Nombre del prisionero:", parent=win)
            if not nombre: return
            edad = simpledialog.askinteger("Edad", "Edad:", parent=win)
            delito = simpledialog.askstring("Delito", "Delito:", parent=win)
            fecha = datetime.now().strftime("%Y-%m-%d")
            nid = max([p["id"] for p in self.prisioneros], default=0) + 1
            self.prisioneros.append({
                "id": nid, "nombre": nombre,
                "edad": edad, "delito": delito,
                "fecha_ingreso": fecha, "celda_id": None
            })
            self.guardar_datos("prisioneros", self.prisioneros)
            refrescar()

        def eliminar():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Eliminar", "Seleccione un prisionero")
                return
            idx = tree.item(sel[0])["values"][0]
            if messagebox.askyesno("Confirmar", f"Eliminar prisionero ID {idx}?"):
                self.prisioneros = [p for p in self.prisioneros if p["id"] != idx]
                self.guardar_datos("prisioneros", self.prisioneros)
                refrescar()

        btn_frame = tk.Frame(win)
        btn_frame.pack(side="right", fill="y", padx=5)
        tk.Button(btn_frame, text="Añadir", command=añadir).pack(fill="x", pady=5)
        tk.Button(btn_frame, text="Eliminar", command=eliminar).pack(fill="x", pady=5)

        refrescar()

    # === Módulo Celdas ===
    def abrir_celdas(self):
        win = tk.Toplevel(self.master)
        win.title("Celdas")
        win.geometry("500x350")

        cols = ("id", "nombre", "capacidad")
        tree = ttk.Treeview(win, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c.capitalize())
            tree.column(c, width=120)
        tree.pack(fill="both", expand=True, side="left", padx=5, pady=5)

        def refrescar():
            tree.delete(*tree.get_children())
            for c in self.celdas:
                tree.insert("", "end", values=(c["id"], c["nombre"], c["capacidad"]))

        def añadir():
            nombre = simpledialog.askstring("Nombre", "Nombre de la celda:", parent=win)
            if not nombre: return
            cap = simpledialog.askinteger("Capacidad", "Capacidad:", parent=win)
            nid = max([c["id"] for c in self.celdas], default=0) + 1
            self.celdas.append({"id": nid, "nombre": nombre, "capacidad": cap})
            self.guardar_datos("celdas", self.celdas)
            refrescar()

        def eliminar():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Eliminar", "Seleccione una celda")
                return
            idx = tree.item(sel[0])["values"][0]
            if messagebox.askyesno("Confirmar", f"Eliminar celda ID {idx}?"):
                self.celdas = [c for c in self.celdas if c["id"] != idx]
                self.guardar_datos("celdas", self.celdas)
                refrescar()

        btn_frame = tk.Frame(win)
        btn_frame.pack(side="right", fill="y", padx=5)
        tk.Button(btn_frame, text="Añadir", command=añadir).pack(fill="x", pady=5)
        tk.Button(btn_frame, text="Eliminar", command=eliminar).pack(fill="x", pady=5)

        refrescar()

    # === Módulo Visitas ===
    def abrir_visitas(self):
        win = tk.Toplevel(self.master)
        win.title("Visitas")
        win.geometry("700x400")

        cols = ("id", "prisionero", "visitante", "fecha")
        tree = ttk.Treeview(win, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c.capitalize())
            tree.column(c, width=150)
        tree.pack(fill="both", expand=True, side="left", padx=5, pady=5)

        def refrescar():
            tree.delete(*tree.get_children())
            for v in self.visitas:
                # encontrar nombre del prisionero
                pr = next((p["nombre"] for p in self.prisioneros if p["id"] == v["prisionero_id"]), "")
                tree.insert("", "end", values=(v["id"], pr, v["visitante"], v["fecha"]))

        def añadir():
            if not self.prisioneros:
                messagebox.showwarning("Sin prisioneros", "No hay prisioneros registrados.")
                return
            # seleccionar prisionero por ID
            pid = simpledialog.askinteger("Prisionero ID", f"IDs existentes: {[p['id'] for p in self.prisioneros]}", parent=win)
            if pid not in [p["id"] for p in self.prisioneros]:
                messagebox.showerror("Error", "ID de prisionero inválido.")
                return
            visitante = simpledialog.askstring("Visitante", "Nombre del visitante:", parent=win)
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
            nid = max([v["id"] for v in self.visitas], default=0) + 1
            self.visitas.append({
                "id": nid, "prisionero_id": pid,
                "visitante": visitante, "fecha": fecha
            })
            self.guardar_datos("visitas", self.visitas)
            refrescar()

        def eliminar():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Eliminar", "Seleccione una visita")
                return
            idx = tree.item(sel[0])["values"][0]
            if messagebox.askyesno("Confirmar", f"Eliminar visita ID {idx}?"):
                self.visitas = [v for v in self.visitas if v["id"] != idx]
                self.guardar_datos("visitas", self.visitas)
                refrescar()

        btn_frame = tk.Frame(win)
        btn_frame.pack(side="right", fill="y", padx=5)
        tk.Button(btn_frame, text="Añadir", command=añadir).pack(fill="x", pady=5)
        tk.Button(btn_frame, text="Eliminar", command=eliminar).pack(fill="x", pady=5)

        refrescar()

    # === Módulo Reportes ===
    def generar_reportes(self):
        win = tk.Toplevel(self.master)
        win.title("Reportes")
        win.geometry("500x400")

        text = tk.Text(win, wrap="word")
        text.pack(fill="both", expand=True, padx=5, pady=5)

        total_pr = len(self.prisioneros)
        total_ce = len(self.celdas)
        total_vis = len(self.visitas)
        cap_total = sum(c["capacidad"] for c in self.celdas)
        ocupados = total_pr
        libres = cap_total - ocupados

        rep = (
            f"**Reporte de la Prisión**\n\n"
            f"- Prisioneros totales: {total_pr}\n"
            f"- Celdas totales: {total_ce}\n"
            f"- Capacidad total de celdas: {cap_total}\n"
            f"- Espacios ocupados: {ocupados}\n"
            f"- Espacios libres: {libres}\n"
            f"- Visitas registradas: {total_vis}\n\n"
            "Visitas por prisionero:\n"
        )
        conteo_vis = {}
        for v in self.visitas:
            conteo_vis[v["prisionero_id"]] = conteo_vis.get(v["prisionero_id"], 0) + 1
        for pid, cnt in conteo_vis.items():
            nombre = next((p["nombre"] for p in self.prisioneros if p["id"] == pid), f"ID {pid}")
            rep += f"  • {nombre}: {cnt}\n"

        text.insert("1.0", rep)
        text.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = DesktopCarcelero(root)
    root.mainloop()
