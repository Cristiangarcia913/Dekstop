import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime, timedelta
import random
import time

class DesktopPrisionero:
    def __init__(self, master):
        self.master = master
        self.master.title("Desktop - Prisionero")
        self.master.geometry("1024x768")
        self.master.configure(bg="#333333")

        self.menu_abierto = False
        self.frame_menu = None

        self.carpeta_datos = "datos_prision"
        self.crear_estructura_datos()

        self.prisioneros = self.cargar_datos("prisioneros")
        self.celdas = self.cargar_datos("celdas")
        self.visitas = self.cargar_datos("visitas")
        self.solicitudes = self.cargar_datos("solicitudes")
        self.quejas = self.cargar_datos("quejas")

        # Datos del prisionero actual (simulado)
        self.prisionero_actual = {
            "id": 1,
            "nombre": "Juan Pérez",
            "edad": 35,
            "delito": "Fraude",
            "fecha_ingreso": "2022-05-15",
            "fecha_libertad": "2025-11-20",  # Nueva fecha de libertad
            "celda_id": 101
        }

        self.crear_interfaz()

    def crear_estructura_datos(self):
        for subcarpeta in ["prisioneros", "celdas", "visitas", "solicitudes", "quejas"]:
            os.makedirs(f"{self.carpeta_datos}/{subcarpeta}", exist_ok=True)
        for archivo in ["prisioneros.json", "celdas.json", "visitas.json", "solicitudes.json", "quejas.json"]:
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

    def cerrar_sesion(self):
        self.master.destroy()
        # Aquí podrías agregar código para volver a la pantalla de login si es necesario
        # from dekstop import Aplicacion  # Asumiendo que existe un módulo de login
        # root = tk.Tk()
        # Aplicacion(root)
        # root.mainloop()

    def crear_interfaz(self):
        self.desktop = tk.Frame(self.master, bg="#333333")
        self.desktop.pack(fill="both", expand=True)

        # Barra de tareas
        self.barra_tareas = tk.Frame(self.master, bg="#1E1E1E", height=50)
        self.barra_tareas.pack(side="bottom", fill="x")

        # Botones en barra de tareas
        botones_barra = [
            ("🏠 Inicio", self.menu_inicio),
            ("👤 Mi Perfil", self.mostrar_perfil),
            ("⏳ Contador", self.mostrar_contador),
            ("🚪 Salir", self.cerrar_sesion),
        ]
        for texto, comando in botones_barra:
            btn = tk.Button(
                self.barra_tareas,
                text=texto,
                bg="#1E1E1E",
                fg="white",
                font=("Arial", 10, "bold"),
                relief="flat",
                command=comando
            )
            btn.pack(side="left", padx=5)

        # Mostrar información del prisionero y días restantes
        dias_restantes = self.calcular_dias_restantes()
        self.lbl_info = tk.Label(
            self.desktop,
            text=f"Prisionero: {self.prisionero_actual['nombre']} | Celda: {self.prisionero_actual['celda_id']} | Días restantes: {dias_restantes}",
            bg="#333333",
            fg="white",
            font=("Arial", 12, "bold")
        )
        self.lbl_info.place(x=10, y=10)

        self.crear_iconos()

    def calcular_dias_restantes(self):
        try:
            fecha_libertad = datetime.strptime(self.prisionero_actual["fecha_libertad"], "%Y-%m-%d")
            hoy = datetime.now()
            diferencia = fecha_libertad - hoy
            return max(0, diferencia.days)
        except:
            return "N/A"

    def crear_iconos(self):
        iconos = [
            ("Mis Visitas", "👥", self.abrir_mis_visitas),
            ("Solicitar Visita", "📝", self.solicitar_visita),
            ("Mis Quejas", "⚠️", self.abrir_quejas),
            ("Registrar Queja", "✏️", self.registrar_queja),
            ("Reglamento", "📜", self.mostrar_reglamento),
            ("Actividades", "🏀", self.mostrar_actividades),
            ("Juego: Snake", "🐍", self.jugar_snake),
            ("Juego: Tetris", "🧊", self.jugar_tetris),
        ]
        for i, (nombre, emoji, comando) in enumerate(iconos):
            frame = tk.Frame(self.desktop, bg="#333333")
            frame.place(x=50 + (i%4)*220, y=80 + (i//4)*180)

            lbl_icono = tk.Label(
                frame,
                text=emoji,
                font=("Arial", 64),
                bg="#333333",
                fg="white",
                cursor="hand2"
            )
            lbl_icono.pack()
            lbl_icono.bind("<Button-1>", lambda e, cmd=comando: cmd())

            tk.Label(
                frame,
                text=nombre,
                bg="#333333",
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
                bg="#1E1E1E",
                bd=0,
                highlightthickness=1,
                highlightbackground="#555555"
            )
            self.frame_menu.place(x=10, y=718, width=250, height=250)

            opciones = [
                ("👤 Mi Perfil", self.mostrar_perfil),
                ("⏳ Contador Días", self.mostrar_contador),
                ("👥 Mis Visitas", self.abrir_mis_visitas),
                ("📝 Solicitar Visita", self.solicitar_visita),
                ("⚠️ Mis Quejas", self.abrir_quejas),
                ("✏️ Registrar Queja", self.registrar_queja),
                ("📜 Reglamento", self.mostrar_reglamento),
                ("🏀 Actividades", self.mostrar_actividades),
                ("🐍 Jugar Snake", self.jugar_snake),
                ("🧊 Jugar Tetris", self.jugar_tetris),
                ("🚪 Salir", self.cerrar_sesion)
            ]
            for texto, comando in opciones:
                btn = tk.Button(
                    self.frame_menu,
                    text=texto,
                    bg="#1E1E1E",
                    fg="white",
                    font=("Arial", 10),
                    anchor="w",
                    relief="flat",
                    command=comando
                )
                btn.pack(fill="x", padx=5, pady=2)

            self.menu_abierto = True

    def mostrar_contador(self):
        win = tk.Toplevel(self.master)
        win.title("Contador de Días")
        win.geometry("400x200")
        
        dias_restantes = self.calcular_dias_restantes()
        fecha_libertad = datetime.strptime(self.prisionero_actual["fecha_libertad"], "%Y-%m-%d").strftime("%d/%m/%Y")
        
        tk.Label(win, 
                text=f"Días restantes de condena:",
                font=("Arial", 14)).pack(pady=10)
        
        tk.Label(win, 
                text=f"{dias_restantes} días",
                font=("Arial", 24, "bold"),
                fg="green").pack()
        
        tk.Label(win, 
                text=f"Fecha estimada de libertad: {fecha_libertad}",
                font=("Arial", 12)).pack(pady=10)
        
        # Actualizar el contador cada día
        def actualizar_contador():
            nuevos_dias = self.calcular_dias_restantes()
            self.lbl_info.config(text=f"Prisionero: {self.prisionero_actual['nombre']} | Celda: {self.prisionero_actual['celda_id']} | Días restantes: {nuevos_dias}")
            win.after(86400000, actualizar_contador)  # Actualizar cada 24 horas
        
        actualizar_contador()

    def mostrar_perfil(self):
        win = tk.Toplevel(self.master)
        win.title("Mi Perfil")
        win.geometry("400x350")

        dias_restantes = self.calcular_dias_restantes()
        fecha_libertad = datetime.strptime(self.prisionero_actual["fecha_libertad"], "%Y-%m-%d").strftime("%d/%m/%Y")
        
        info = (
            f"ID: {self.prisionero_actual['id']}\n"
            f"Nombre: {self.prisionero_actual['nombre']}\n"
            f"Edad: {self.prisionero_actual['edad']}\n"
            f"Delito: {self.prisionero_actual['delito']}\n"
            f"Fecha de ingreso: {self.prisionero_actual['fecha_ingreso']}\n"
            f"Días restantes: {dias_restantes}\n"
            f"Fecha libertad: {fecha_libertad}\n"
            f"Celda: {self.prisionero_actual['celda_id']}\n"
        )

        tk.Label(win, text=info, font=("Arial", 12), justify="left").pack(pady=10)

        celda = next((c for c in self.celdas if c["id"] == self.prisionero_actual["celda_id"]), None)
        if celda:
            tk.Label(win, text=f"\nInformación de la celda:\n"
                              f"Nombre: {celda['nombre']}\n"
                              f"Capacidad: {celda['capacidad']}", 
                    font=("Arial", 10)).pack()

    def abrir_mis_visitas(self):
        win = tk.Toplevel(self.master)
        win.title("Mis Visitas")
        win.geometry("600x400")

        cols = ("id", "visitante", "fecha", "estado")
        tree = ttk.Treeview(win, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c.capitalize())
            tree.column(c, width=120)
        tree.pack(fill="both", expand=True, padx=5, pady=5)

        # Filtrar visitas del prisionero actual
        mis_visitas = [v for v in self.visitas if v["prisionero_id"] == self.prisionero_actual["id"]]
        
        for v in mis_visitas:
            tree.insert("", "end", values=(v["id"], v["visitante"], v["fecha"], v.get("estado", "Pendiente")))

    def solicitar_visita(self):
        win = tk.Toplevel(self.master)
        win.title("Solicitar Visita")
        win.geometry("400x300")

        tk.Label(win, text="Solicitud de Visita", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(win, text="Nombre del visitante:").pack()
        entry_visitante = tk.Entry(win, width=30)
        entry_visitante.pack(pady=5)

        tk.Label(win, text="Parentesco:").pack()
        entry_parentesco = tk.Entry(win, width=30)
        entry_parentesco.pack(pady=5)

        tk.Label(win, text="Fecha solicitada (DD-MM-YYYY):").pack()
        entry_fecha = tk.Entry(win, width=30)
        entry_fecha.pack(pady=5)

        def enviar_solicitud():
            visitante = entry_visitante.get()
            parentesco = entry_parentesco.get()
            fecha = entry_fecha.get()

            if not all([visitante, parentesco, fecha]):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return

            nid = max([s["id"] for s in self.solicitudes], default=0) + 1
            nueva_solicitud = {
                "id": nid,
                "prisionero_id": self.prisionero_actual["id"],
                "prisionero_nombre": self.prisionero_actual["nombre"],
                "visitante": visitante,
                "parentesco": parentesco,
                "fecha_solicitada": fecha,
                "fecha_solicitud": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "estado": "Pendiente"
            }

            self.solicitudes.append(nueva_solicitud)
            self.guardar_datos("solicitudes", self.solicitudes)
            messagebox.showinfo("Éxito", "Solicitud enviada correctamente")
            win.destroy()

        tk.Button(win, text="Enviar Solicitud", command=enviar_solicitud).pack(pady=15)

    def abrir_quejas(self):
        win = tk.Toplevel(self.master)
        win.title("Mis Quejas")
        win.geometry("600x400")

        cols = ("id", "tipo", "fecha", "estado")
        tree = ttk.Treeview(win, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c.capitalize())
            tree.column(c, width=120)
        tree.pack(fill="both", expand=True, padx=5, pady=5)

        # Filtrar quejas del prisionero actual
        mis_quejas = [q for q in self.quejas if q["prisionero_id"] == self.prisionero_actual["id"]]
        
        for q in mis_quejas:
            tree.insert("", "end", values=(q["id"], q["tipo"], q["fecha"], q.get("estado", "Pendiente")))

    def registrar_queja(self):
        win = tk.Toplevel(self.master)
        win.title("Registrar Queja")
        win.geometry("400x400")

        tk.Label(win, text="Registro de Queja", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(win, text="Tipo de queja:").pack()
        tipo_var = tk.StringVar(win)
        tipos = ["Alimentación", "Seguridad", "Salud", "Trato", "Otro"]
        tipo_var.set(tipos[0])
        tk.OptionMenu(win, tipo_var, *tipos).pack(pady=5)

        tk.Label(win, text="Descripción:").pack()
        text_desc = tk.Text(win, height=8, width=40)
        text_desc.pack(pady=5)

        def enviar_queja():
            tipo = tipo_var.get()
            descripcion = text_desc.get("1.0", "end-1c")

            if not descripcion:
                messagebox.showerror("Error", "La descripción es obligatoria")
                return

            nid = max([q["id"] for q in self.quejas], default=0) + 1
            nueva_queja = {
                "id": nid,
                "prisionero_id": self.prisionero_actual["id"],
                "prisionero_nombre": self.prisionero_actual["nombre"],
                "tipo": tipo,
                "descripcion": descripcion,
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "estado": "Pendiente"
            }

            self.quejas.append(nueva_queja)
            self.guardar_datos("quejas", self.quejas)
            messagebox.showinfo("Éxito", "Queja registrada correctamente")
            win.destroy()

        tk.Button(win, text="Enviar Queja", command=enviar_queja).pack(pady=15)

    def mostrar_reglamento(self):
        win = tk.Toplevel(self.master)
        win.title("Reglamento de la Prisión")
        win.geometry("600x500")

        text = tk.Text(win, wrap="word", font=("Arial", 11))
        text.pack(fill="both", expand=True, padx=10, pady=10)

        reglamento = """
        REGLAMENTO DE LA PRISIÓN

        1. HORARIOS:
           - Levantarse: 6:00 AM
           - Desayuno: 6:30 AM - 7:00 AM
           - Trabajo/Actividades: 8:00 AM - 12:00 PM
           - Almuerzo: 12:30 PM - 1:30 PM
           - Tiempo libre: 1:30 PM - 3:00 PM
           - Cena: 6:00 PM - 7:00 PM
           - Descanso en celdas: 9:00 PM

        2. NORMAS DE CONDUCTA:
           - Respeto al personal y otros reclusos
           - Prohibido el uso de violencia
           - Mantener limpias las áreas comunes
           - Participar en las actividades asignadas
           - No poseer objetos prohibidos

        3. DERECHOS:
           - Recibir visitas según el reglamento
           - Recibir atención médica
           - Presentar quejas y solicitudes
           - Participar en actividades recreativas
           - Recibir correspondencia

        4. SANCIONES:
           - Aislamiento temporal por conductas violentas
           - Pérdida de privilegios (visitas, actividades)
           - Restricción de tiempo libre
           - Otras según gravedad de la falta
        """

        text.insert("1.0", reglamento)
        text.config(state="disabled")

    def mostrar_actividades(self):
        win = tk.Toplevel(self.master)
        win.title("Actividades Disponibles")
        win.geometry("500x400")

        actividades = [
            {"nombre": "Taller de carpintería", "horario": "Lunes y Miércoles 9:00-11:00", "cupos": 10},
            {"nombre": "Clases de educación", "horario": "Martes y Jueves 10:00-12:00", "cupos": 15},
            {"nombre": "Deportes", "horario": "Lunes a Viernes 15:00-17:00", "cupos": 20},
            {"nombre": "Taller de arte", "horario": "Viernes 13:00-15:00", "cupos": 8},
            {"nombre": "Biblioteca", "horario": "Diario 14:00-18:00", "cupos": 5},
        ]

        text = tk.Text(win, wrap="word", font=("Arial", 11))
        text.pack(fill="both", expand=True, padx=10, pady=10)

        for act in actividades:
            text.insert("end", f"• {act['nombre']}\n"
                              f"  Horario: {act['horario']}\n"
                              f"  Cupos disponibles: {act['cupos']}\n\n")

        text.config(state="disabled")

    def jugar_snake(self):
        snake_win = tk.Toplevel(self.master)
        snake_win.title("Snake Game")
        snake_win.resizable(False, False)
        
        canvas_width = 400
        canvas_height = 400
        canvas = tk.Canvas(snake_win, width=canvas_width, height=canvas_height, bg="black")
        canvas.pack()

        cell_size = 20
        snake = [(100, 100), (80, 100), (60, 100)]
        snake_direction = "Right"
        food = self.create_food(canvas, canvas_width, canvas_height, cell_size, snake)
        score = 0
        game_over = False

        score_label = tk.Label(snake_win, text=f"Puntuación: {score}", font=("Arial", 12))
        score_label.pack()

        def change_direction(new_dir):
            nonlocal snake_direction
            if (new_dir == "Up" and snake_direction != "Down") or \
               (new_dir == "Down" and snake_direction != "Up") or \
               (new_dir == "Left" and snake_direction != "Right") or \
               (new_dir == "Right" and snake_direction != "Left"):
                snake_direction = new_dir

        def game_loop():
            nonlocal snake, food, score, game_over
            
            if game_over:
                return

            # Mover la serpiente
            head_x, head_y = snake[0]
            if snake_direction == "Up":
                new_head = (head_x, head_y - cell_size)
            elif snake_direction == "Down":
                new_head = (head_x, head_y + cell_size)
            elif snake_direction == "Left":
                new_head = (head_x - cell_size, head_y)
            elif snake_direction == "Right":
                new_head = (head_x + cell_size, head_y)

            # Verificar colisiones
            if (new_head in snake or 
                new_head[0] < 0 or new_head[0] >= canvas_width or 
                new_head[1] < 0 or new_head[1] >= canvas_height):
                game_over = True
                canvas.create_text(canvas_width/2, canvas_height/2, 
                                 text="GAME OVER", fill="red", font=("Arial", 30))
                return

            snake.insert(0, new_head)

            # Verificar si comió la comida
            if new_head == food:
                score += 10
                score_label.config(text=f"Puntuación: {score}")
                food = self.create_food(canvas, canvas_width, canvas_height, cell_size, snake)
            else:
                snake.pop()

            # Redibujar
            canvas.delete("all")
            for segment in snake:
                canvas.create_rectangle(segment[0], segment[1], 
                                      segment[0]+cell_size, segment[1]+cell_size, 
                                      fill="green")
            canvas.create_oval(food[0], food[1], 
                              food[0]+cell_size, food[1]+cell_size, 
                              fill="red")

            snake_win.after(100, game_loop)

        snake_win.bind("<Up>", lambda e: change_direction("Up"))
        snake_win.bind("<Down>", lambda e: change_direction("Down"))
        snake_win.bind("<Left>", lambda e: change_direction("Left"))
        snake_win.bind("<Right>", lambda e: change_direction("Right"))

        game_loop()

    def create_food(self, canvas, width, height, cell_size, snake):
        while True:
            x = random.randint(0, (width - cell_size) // cell_size) * cell_size
            y = random.randint(0, (height - cell_size) // cell_size) * cell_size
            if (x, y) not in snake:
                return (x, y)

    def jugar_tetris(self):
        tetris_win = tk.Toplevel(self.master)
        tetris_win.title("Tetris Game")
        tetris_win.resizable(False, False)

        # Configuración del juego
        cell_size = 25
        cols = 10
        rows = 20
        width = cols * cell_size
        height = rows * cell_size

        canvas = tk.Canvas(tetris_win, width=width, height=height, bg="black")
        canvas.pack()

        # Formas de las piezas
        shapes = [
            [[1, 1, 1, 1]],  # I
            [[1, 1], [1, 1]],  # O
            [[1, 1, 1], [0, 1, 0]],  # T
            [[1, 1, 1], [1, 0, 0]],  # L
            [[1, 1, 1], [0, 0, 1]],  # J
            [[0, 1, 1], [1, 1, 0]],  # S
            [[1, 1, 0], [0, 1, 1]]   # Z
        ]
        colors = ["cyan", "yellow", "purple", "orange", "blue", "green", "red"]

        class Piece:
            def __init__(self):
                self.shape_idx = random.randint(0, len(shapes) - 1)
                self.shape = shapes[self.shape_idx]
                self.color = colors[self.shape_idx]
                self.x = cols // 2 - len(self.shape[0]) // 2
                self.y = 0

        # Estado del juego
        board = [[0 for _ in range(cols)] for _ in range(rows)]
        current_piece = Piece()
        score = 0
        game_over = False

        score_label = tk.Label(tetris_win, text=f"Puntuación: {score}", font=("Arial", 12))
        score_label.pack()

        def draw_piece(piece, clear=False):
            for y, row in enumerate(piece.shape):
                for x, cell in enumerate(row):
                    if cell:
                        canvas_x = (piece.x + x) * cell_size
                        canvas_y = (piece.y + y) * cell_size
                        if clear:
                            canvas.create_rectangle(canvas_x, canvas_y, 
                                                  canvas_x + cell_size, canvas_y + cell_size, 
                                                  fill="black", outline="black")
                        else:
                            canvas.create_rectangle(canvas_x, canvas_y, 
                                                  canvas_x + cell_size, canvas_y + cell_size, 
                                                  fill=piece.color, outline="white")

        def draw_board():
            for y in range(rows):
                for x in range(cols):
                    if board[y][x]:
                        canvas.create_rectangle(x * cell_size, y * cell_size,
                                              (x + 1) * cell_size, (y + 1) * cell_size,
                                              fill=colors[board[y][x] - 1], outline="white")

        def check_collision(piece, dx=0, dy=0):
            for y, row in enumerate(piece.shape):
                for x, cell in enumerate(row):
                    if cell:
                        new_x = piece.x + x + dx
                        new_y = piece.y + y + dy
                        if (new_x < 0 or new_x >= cols or 
                            new_y >= rows or 
                            (new_y >= 0 and board[new_y][new_x])):
                            return True
            return False

        def rotate_piece(piece):
            # Rotar la forma de la pieza
            rotated = [[piece.shape[y][x] for y in range(len(piece.shape)-1, -1, -1)] 
                      for x in range(len(piece.shape[0]))]
            
            old_shape = piece.shape
            piece.shape = rotated
            
            # Si hay colisión después de rotar, revertir
            if check_collision(piece):
                piece.shape = old_shape

        def move_piece(dx, dy):
            if not check_collision(current_piece, dx, dy):
                draw_piece(current_piece, clear=True)
                current_piece.x += dx
                current_piece.y += dy
                draw_piece(current_piece)
                return True
            return False

        def drop_piece():
            nonlocal current_piece, score, game_over
            
            while move_piece(0, 1):
                pass
            
            # Fijar la pieza al tablero
            for y, row in enumerate(current_piece.shape):
                for x, cell in enumerate(row):
                    if cell and current_piece.y + y >= 0:
                        board[current_piece.y + y][current_piece.x + x] = current_piece.shape_idx + 1
            
            # Verificar líneas completas
            lines_cleared = 0
            for y in range(rows):
                if all(board[y]):
                    lines_cleared += 1
                    for y2 in range(y, 0, -1):
                        board[y2] = board[y2-1][:]
                    board[0] = [0] * cols
            
            # Actualizar puntuación
            if lines_cleared > 0:
                score += lines_cleared * 100
                score_label.config(text=f"Puntuación: {score}")
            
            # Nueva pieza
            current_piece = Piece()
            if check_collision(current_piece):
                game_over = True
                canvas.create_text(width/2, height/2, 
                                 text="GAME OVER", fill="red", font=("Arial", 30))

        def game_loop():
            if not game_over:
                if not move_piece(0, 1):
                    drop_piece()
                draw_board()
                draw_piece(current_piece)
                tetris_win.after(500, game_loop)

        # Controles
        tetris_win.bind("<Left>", lambda e: move_piece(-1, 0))
        tetris_win.bind("<Right>", lambda e: move_piece(1, 0))
        tetris_win.bind("<Down>", lambda e: move_piece(0, 1))
        tetris_win.bind("<Up>", lambda e: rotate_piece(current_piece))
        tetris_win.bind("<space>", lambda e: drop_piece())

        game_loop()

if __name__ == "__main__":
    root = tk.Tk()
    app = DesktopPrisionero(root)
    root.mainloop()
