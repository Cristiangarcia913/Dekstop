# Sistema de Gestión de Prisión 🏛️🔐

Este sistema de escritorio, desarrollado en Python con `tkinter`, simula la gestión de una prisión desde dos tipos de usuarios: **Carcelero** y **Prisionero**. Permite registrar, visualizar y administrar información de internos, visitas, quejas y mucho más.

## 📦 Requisitos del Sistema

- Python 3.8 o superior
- Ubuntu/Debian (o compatible)
- Librerías necesarias:

```bash
sudo apt update
sudo apt install python3-tk python3-pip -y
pip install pillow requests
```

## 🚀 Ejecución

Desde terminal, en la carpeta del proyecto, ejecutar:

```bash
python3 dekstop.py
```

## 👥 Tipos de Usuario

### 👮 Modo Carcelero

- Gestión de prisioneros y celdas
- Registro de visitas
- Generación de reportes
- Botón para ejecutar `mishell.sh` (opcional)

### 👤 Modo Prisionero

- Visualización de perfil y días restantes
- Solicitud de visitas
- Registro de quejas
- Acceso a juegos (Snake y Tetris)
- Reglamento y actividades disponibles

## 🗂 Estructura de Datos

Se genera automáticamente la carpeta `datos_prision/` con los siguientes archivos:

```
datos_prision/
├── prisioneros/
├── celdas/
├── visitas/
├── solicitudes/
├── quejas/
├── reportes/
```

Cada módulo gestiona y guarda su información en archivos `.json`.

## 📝 Notas Finales

- Para usar el botón “🐚 Mishell” en modo carcelero, se debe crear un script ejecutable llamado `mishell.sh`.
- Interfaz optimizada para resolución 1024x768.
- Aplicación con fines educativos y de simulación.

---
