import os, json
import tkinter as tk
from tkinter import messagebox
from temas import TEMAS
import sys

# Rutas
RUTA_CARPETA = os.path.join(
    (
        os.path.dirname(sys.executable)
        if getattr(sys, "frozen", False)
        else os.path.dirname(__file__)
    ),
    "data",
)
os.makedirs(RUTA_CARPETA, exist_ok=True)

RUTA_NOTAS = os.path.join(RUTA_CARPETA, "notas.json")
RUTA_POS = os.path.join(RUTA_CARPETA, "posicion_ventana.json")
RUTA_ICO = os.path.join(
    (
        os.path.dirname(sys.executable)
        if getattr(sys, "frozen", False)
        else os.path.dirname(__file__)
    ),
    "icono.ico",
)


def resource_path(relative_path: str) -> str:
    """Devuelve ruta válida tanto en dev como en .exe de PyInstaller."""
    base = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base, relative_path)


# ---------- Utilidades ventana ----------
def centrar_existente(ventana):
    ventana.update_idletasks()
    w, h = ventana.winfo_width(), ventana.winfo_height()
    sw, sh = ventana.winfo_screenwidth(), ventana.winfo_screenheight()
    x, y = (sw // 2) - (w // 2), (sh // 2) - (h // 2)
    # aplicar la posición ANTES de mostrar la ventana
    ventana.geometry(f"{w}x{h}+{x}+{y}")
    ventana.update()  # asegura que se dibuje directamente centrada


def guardar_coord_ventana(app):
    with open(RUTA_POS, "w", encoding="utf-8") as f:
        json.dump({"x": app.winfo_x(), "y": app.winfo_y()}, f)


def cargar_coord_ventana():
    if not os.path.exists(RUTA_POS):
        return None
    with open(RUTA_POS, "r", encoding="utf-8") as f:
        d = json.load(f)
        return d["x"], d["y"]


# ---------- Temas ----------
def aplicar_tema(app):
    """Pinta todos los widgets con el tema actual (app.tema)."""
    t = app.tema

    # Ventana y frames
    app.configure(bg=t["fondo_principal"])
    app.frame_root.configure(bg=t["fondo_principal"])
    app.frame_botones.configure(bg=t["fondo_principal"])
    app.frame_notas.configure(bg=t["fondo_notas"])
    app.frame_listbox.configure(bg=t["fondo_notas"])

    # Lista
    app.listbox_notas.configure(bg=t["fondo_lista"], fg=t["texto_general"])

    # Label estado
    app.lbl_mensaje.configure(bg=t["fondo_notas"], fg="Black", font=t["label_font"])

    # Botones
    for b in (
        app.bt_eliminar_nota,
        app.bt_guardar_en_archivo,
        app.bt_cambiar_tema,
        app.bt_nueva_nota,
    ):
        b.configure(bg=t["boton"], fg=t["texto_boton"])


def cambiar_tema(app):
    """Alterna entre temas y repinta."""
    nombres = list(TEMAS.keys())
    i = (nombres.index(app.tema_nombre) + 1) % len(nombres)
    app.tema_nombre = nombres[i]
    app.tema = TEMAS[app.tema_nombre]
    aplicar_tema(app)
    flash(app, f"Tema: {app.tema_nombre}")


def crear_nota(app):
    abrir_editor_nota(app, modo="crear")


def abrir_editor_nota(app, modo="crear", texto_inicial="", idx=None):
    """Ventana para crear o editar una nota con mismo diseño."""
    t = app.tema

    win = tk.Toplevel(app)
    win.title("Nueva Nota" if modo == "crear" else "Editar Nota")
    win.geometry("400x300")
    win.config(bg=t["fondo_principal"])
    win.transient(app)

    # --- Frame principal ---
    frame = tk.Frame(win, bg=t["fondo_principal"])
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # --- Título ---
    lbl_titulo = tk.Label(
        frame,
        text="Título:",
        bg=t["fondo_principal"],
        fg=t["texto_general"],
        font=("Consolas", 10, "bold"),
        anchor="w",
    )
    lbl_titulo.pack(fill="x", pady=(0, 4))

    entry_titulo = tk.Entry(
        frame,
        bg=t["fondo_lista"],
        fg=t["texto_general"],
        font=("Consolas", 10),
    )
    entry_titulo.pack(fill="x", pady=(0, 10))

    # --- Contenido ---
    lbl_texto = tk.Label(
        frame,
        text="Contenido:",
        bg=t["fondo_principal"],
        fg=t["texto_general"],
        font=("Consolas", 10, "bold"),
        anchor="w",
    )
    lbl_texto.pack(fill="x", pady=(0, 4))

    text_contenido = tk.Text(
        frame,
        bg=t["fondo_lista"],
        fg=t["texto_general"],
        font=("Consolas", 10),
        wrap="word",
        height=8,
    )
    text_contenido.pack(fill="both", expand=True)

    # --- Si es edición → cargar contenido previo ---
    if modo == "editar" and texto_inicial:
        partes = texto_inicial.split(" — ", 1)
        entry_titulo.insert(0, partes[0])
        if len(partes) > 1:
            text_contenido.insert("1.0", partes[1])

    # --- Botón guardar ---
    def guardar():
        titulo = entry_titulo.get().strip()
        texto = text_contenido.get("1.0", "end-1c").strip()

        if not titulo and not texto:
            return flash(app, "Campos vacíos")

        resumen = (texto[:40] + "...") if len(texto) > 40 else texto
        item = f"{titulo} — {resumen}"

        if modo == "editar" and idx is not None:
            app.listbox_notas.delete(idx)
            app.listbox_notas.insert(idx, item)
            flash(app, "Nota actualizada")
        else:
            app.listbox_notas.insert(0, item)
            flash(app, "Nota creada")

        win.destroy()

    btn_guardar = tk.Button(
        frame,
        text="Guardar",
        bg=t["boton"],
        fg=t["texto_boton"],
        font=("Consolas", 10, "bold"),
        relief="ridge",
        command=guardar,
    )
    btn_guardar.pack(pady=10)

    # --- Mostrar ventana centrada ---
    centrar_existente(win)
    win.update_idletasks()
    win.grab_set()


def eliminar_nota(app):
    sel = app.listbox_notas.curselection()
    if not sel:
        return flash(app, "Seleccione una nota para eliminar")
    idx = sel[0]
    texto = app.listbox_notas.get(idx)
    if not messagebox.askyesno("Confirmar", f"¿Eliminar?\n\n{texto}", parent=app):
        return
    app.listbox_notas.delete(idx)
    flash(app, "Nota eliminada")


def editar_nota(app):
    sel = app.listbox_notas.curselection()
    if not sel:
        return flash(app, "Seleccione una nota para editar")
    idx = sel[0]
    texto = app.listbox_notas.get(idx)

    abrir_editor_nota(app, modo="editar", texto_inicial=texto, idx=idx)


def guardar_notas_archivo(app):
    notas = app.listbox_notas.get(0, tk.END)
    if not notas:
        return flash(app, "No hay notas para guardar")
    with open(RUTA_NOTAS, "w", encoding="utf-8") as f:
        json.dump(list(notas), f, ensure_ascii=False, indent=2)
    flash(app, "Notas guardadas en data/notas.json")



def cargar_notas_archivo(app):
    if not os.path.exists(RUTA_NOTAS):
        return
    with open(RUTA_NOTAS, "r", encoding="utf-8") as f:
        try:
            notas = json.load(f)
        except json.JSONDecodeError:
            flash(app, "Error al leer archivo de notas")
            return
    if not notas:
        return
    if messagebox.askyesno(
        "Cargar notas",
        "Hemos encontrado notas guardadas.\n¿Desea cargarlas?",
        parent=app,
    ):
        for n in notas:
            app.listbox_notas.insert(tk.END, n)
        flash(app, "Notas cargadas")



# ---------- Mensajes ----------
def flash(app, texto, ms=1200):
    app.mensaje.set(texto)
    if hasattr(app, "_flash_job") and app._flash_job:
        try:
            app.after_cancel(app._flash_job)
        except Exception:
            pass
    app._flash_job = app.after(ms, lambda: app.mensaje.set(app.mensaje_defecto))
