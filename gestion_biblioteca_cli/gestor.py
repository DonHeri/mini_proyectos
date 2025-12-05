"""
Módulo de gestión de biblioteca.

Contiene la lógica de negocio principal. Gestiona libros, usuarios,
préstamos, devoluciones y coordina con la capa de persistencia.
"""

from modelos import ValidationError, Libro, Usuario
from persistencia import ArchivoDatos


class GestorBiblioteca:
    """
    Gestor central de la biblioteca.
    
    Administra la lógica de negocio para préstamos, devoluciones y consultas.
    Coordina la persistencia de datos con ArchivoDatos.
    """
    # Crear gestor 
    def __init__(self, dir_data="data") -> None:
        self.archivo = ArchivoDatos(dir_data)
        self.libros = self.archivo.cargar_libros()
        self.usuarios = self.archivo.cargar_usuarios()

    def generar_id(self, filtro: str = "book") -> str:
        """
        Genera identificadores únicos secuenciales.
        
        Crea IDs con formato LBR-XXXX para libros o USR-XXXX para usuarios,
        continuando la secuencia del último ID registrado.
        
        Args:
            filtro (str): Tipo de ID a generar: "book" o "user"
            
        Returns:
            str: ID único generado (ej: LBR-0001, USR-0001)
        """

        if filtro == "book":
            # Separar parte numérica
            numeros = [int(id_.split("-")[1]) for id_ in self.libros]
            # No hay ingresos anteriores
            if not numeros:
                return f"LBR-0001"

            ultimo_id = max(numeros)
            siguiente_id = ultimo_id + 1

            return f"LBR-{siguiente_id:04d}"

        if filtro == "user":
            # Separar parte numérica
            numeros = [int(id_.split("-")[1]) for id_ in self.usuarios]
            # No hay ingresos anteriores
            if not numeros:
                return f"USR-0001"

            ultimo_id = max(numeros)
            siguiente_id = ultimo_id + 1

            return f"USR-{siguiente_id:04d}"
            # return f"LBR-{int(nueva + 1):.4d}"

    # ====== CRUD ======
    def agregar_libro(self, title: str, author: str, year: int) -> None:
        """
        Agrega un nuevo libro a la biblioteca.
        
        Args:
            title (str): Título del libro
            author (str): Autor del libro
            year (int): Año de publicación
            
        Raises:
            ValidationError: Si los datos no cumplen las validaciones
        """

        id_ = self.generar_id(filtro="book")
        self.libros[id_] = Libro(title, author, year, id_)
        print(f"Agregado libro {id_} - {title.title()}")
        print()
        self.guardar()

    def registrar_usuario(self, nombre: str) -> None:
        """
        Registra un nuevo usuario en la biblioteca.
        
        Args:
            nombre (str): Nombre del usuario
            
        Raises:
            ValidationError: Si el nombre está vacío
        """

        id_usuario = self.generar_id(filtro="user")

        self.usuarios[id_usuario] = Usuario(nombre, id_usuario)
        print(f"Agregado usuario {id_usuario} - {nombre.title()}")
        print()
        self.guardar()

    def prestar_libro(
        self,
        id_libro,
        id_usuario,
    ):
        """Cambiar el estado prestado del libro -> False"""
        id_libro = id_libro.upper()
        id_usuario = id_usuario.upper()

        if id_usuario not in self.usuarios:
            raise ValidationError("Usuario no registrado")

        if id_libro not in self.libros:
            raise ValidationError("Libro no disponible")

        usuario = self.usuarios[id_usuario]
        libro = self.libros[id_libro]

        # ====== Tramitar el préstamo en Usuario ======
        if usuario.tomar_prestado(id_libro):
            if libro.prestar():
                print("Libro prestado")
                print()
                self.guardar()
                return

    def devolver_libro(
        self,
        id_libro,
        id_usuario,
    ):
        """Cambiar el estado prestado del libro -> False"""
        id_libro = id_libro.upper()
        id_usuario = id_usuario.upper()

        if id_usuario not in self.usuarios or id_libro not in self.libros:
            raise ValidationError("No se pudo devolver el libro")

        usuario = self.usuarios[id_usuario]
        libro = self.libros[id_libro]

        # ====== Tramitar la devolución en Usuario ======
        if usuario.devolver_libro(id_libro):
            if libro.devolver():
                print("Libro devuelto")
                print()
                self.guardar()
                return

    
    def listar_libros(self, disponibles=False):
        return [
            (id, libro)
            for id, libro in self.libros.items()
            if libro.borrowed == disponibles
        ]

    
    def listar_usuarios(self):
        return self.usuarios

    def guardar(self):
        self.archivo.guardar_libros(self.libros)
        self.archivo.guardar_usuarios(self.usuarios)
