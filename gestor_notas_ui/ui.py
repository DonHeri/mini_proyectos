import tkinter as tk
import funciones as fc
from temas import TEMAS



class GestorNotasApp(tk.Tk):
    def __init__(self, tema="oceano"):
        super().__init__()
        self.title("Gestor de Notas")
        self.geometry("550x750")
        self.minsize(400, 500)
        # Ruta icono
        self.iconbitmap(fc.resource_path("icono.ico"))

        # Estado / tema
        self.tema_nombre = tema
        self.tema = TEMAS[self.tema_nombre]
        self.mensaje_defecto = "Esperando acción..."
        self.mensaje = tk.StringVar(value=self.mensaje_defecto)
        self.nota_actual = tk.StringVar()

        # Posición de ventana previa
        pos = fc.cargar_coord_ventana()
        if pos:
            self.geometry(f"550x750+{pos[0]}+{pos[1]}")
        else:
            fc.centrar_existente(self)

        self._crear_widgets()
        fc.aplicar_tema(self)  # pinta el tema
        fc.cargar_notas_archivo(self)  # opcional: pregunta para cargar
        self.protocol(
            "WM_DELETE_WINDOW", lambda: (fc.guardar_coord_ventana(self), self.destroy())
        )

    # ---------- UI ----------
    def _crear_widgets(self):
        # Contenedor
        self.frame_root = tk.Frame(self)
        self.frame_root.pack(fill="both", expand=True, padx=16, pady=16)

        # Label de estado (parte superior, bajo el título de la ventana)
        self.lbl_mensaje = tk.Label(
            self.frame_root,
            textvariable=self.mensaje,
            relief="raised",
            height=1,  # un poco más alto visualmente
        )
        self.lbl_mensaje.pack(fill="x", pady=(0, 10))

        # Botones principales
        self.frame_botones = tk.Frame(self.frame_root, bg="darkblue")
        self.frame_botones.pack(fill="x", pady=(5, 5), padx=(10, 10), ipady=5)

        # Panel de notas
        self.frame_notas = tk.Frame(self.frame_root)
        self.frame_notas.pack(padx=14, pady=10, fill="both", expand=True)

        # Listbox + Scroll
        self.frame_listbox = tk.Frame(self.frame_notas)
        self.frame_listbox.pack(fill="both", expand=True, padx=6, pady=6)

        self.listbox_notas = tk.Listbox(self.frame_listbox, height=12)
        self.listbox_notas.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(
            self.frame_listbox, command=self.listbox_notas.yview
        )
        self.scrollbar.pack(side="right", fill="y")
        self.listbox_notas.config(yscrollcommand=self.scrollbar.set)

        self.listbox_notas.bind("<Double-Button-1>", lambda e: fc.editar_nota(self))

        self.bt_nueva_nota = tk.Button(
            self.frame_botones,
            text="Nueva nota",
            relief="groove",
            command=lambda: fc.crear_nota(self),
        )
        self.bt_nueva_nota.pack(side="left", padx=8, ipadx=10, ipady=5)

        self.bt_eliminar_nota = tk.Button(
            self.frame_notas,
            text="Eliminar nota",
            relief="groove",
            command=lambda: fc.eliminar_nota(self),
        )
        self.bt_eliminar_nota.pack(side="bottom", padx=6, ipadx=8, ipady=4, pady=2)

        self.bt_guardar_en_archivo = tk.Button(
            self.frame_botones,
            text="Guardar en archivo",
            relief="groove",
            command=lambda: fc.guardar_notas_archivo(self),
        )
        self.bt_guardar_en_archivo.pack(side="right", padx=8, ipadx=10, ipady=5)

        # Botón de tema (pequeño, lateral)
        # Botón de tema (pequeño, disimulado abajo a la derecha)
        self.bt_cambiar_tema = tk.Button(
            self.frame_root,
            text="⊡",
            relief="ridge",
            command=lambda: fc.cambiar_tema(self),
            font=("Consolas", 10, "bold"),
        )
        self.bt_cambiar_tema.pack(side="right", anchor="se", padx=6, pady=6)
        self.bt_cambiar_tema.config(width=2, height=1)

    def run(self):
        self.mainloop()
