class ValidationError(Exception):
    """Error de validación de datos"""

    pass


class Libro:
    def __init__(self, title, author, year, id, borrowed=False):
        if not title or not author:
            raise ValidationError("Título y autor no pueden estar vacíos")
        if not (1000 <= year <= 2100):
            raise ValidationError("Año inválido")
        
        self.title = title.lower().strip()
        self.author = author.lower().strip()
        self.year = year
        self.borrowed = borrowed
        self.id = id

    # Serializar 
    def to_dict(self) -> dict:
        """Serializa un objeto a formato diccionario"""
        return {
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "borrowed": self.borrowed,
            "id": self.id,
        }

    # Deserializar
    @classmethod
    def from_dict(cls, data: dict):
        """Recibe los datos en formato diccionario y los instancia nuevamente"""
        try:
            return cls(
                title=data["title"],
                author=data["author"],
                year=data["year"],
                id=data["id"],
                borrowed=data["borrowed"],
            )
        except KeyError as e:
            raise ValidationError(e)

    # ====== CRUD ======

    def prestar(self):
        """Cambia el estado de prestado del libro (borrowed -> True)"""

        if self.borrowed:
            raise ValidationError("Ya se ha prestado el libro a otro usuario")

        self.borrowed = True
        return True

    def devolver(self):
        """Cambia el estado de prestado del libro (borrowed -> False)"""
        if not self.borrowed:
            raise ValidationError(
                "No se puede devolver un libro que no ha sido prestado"
            )

        self.borrowed = False
        return True

    def __str__(self) -> str:
        """Mostrar datos del libro al usuario"""
        return f"Título: {self.title.capitalize()}\
                 \nAutor: {self.author.title()}\
                \nAño publicación: {str(self.year)}\
                \nPrestado: {self.borrowed}\n"


class Usuario:  #
    def __init__(self, nombre, id, libros_prestados=None) -> None:
        self.nombre = nombre
        self.id = id
        self.libros_prestados = [] if not libros_prestados else libros_prestados

    # Serializar
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "libros_prestados": self.libros_prestados,
        }

    # Deserializar
    @classmethod
    def from_dict(cls, data):
        try:
            return cls(
                nombre=data["nombre"],
                id=data["id"],
                libros_prestados=data["libros_prestados"],
            )
        except KeyError as e:
            print(f"[Error] - {e}")

    # ====== CRUD ======
    # Añadir libro a lista de libros prestados
    def tomar_prestado(self, id_libro):
        """Añadir un libro a la lista de libros prestados"""

        if len(self.libros_prestados) > 3:
            raise ValidationError(
                "El usuario ya tiene 3 libros prestados. No puede recibir otro."
            )

        if id_libro in self.libros_prestados:
            raise ValidationError("El libro ya esta en la lista de prestados")

        # Cambiar estado libro a prestado
        self.libros_prestados.append(id_libro)
        return True

    def devolver_libro(self, id_libro):
        """Retirar un libro de la lista de libros prestados"""

        if id_libro not in self.libros_prestados:
            raise ValidationError("El libro no esta en la lista de prestados")
        else:
            self.libros_prestados.remove(id_libro)
            return True

    def __str__(self):
        """Mostrar datos del usuario"""
        return f"{self.nombre.title()} se le han prestado {len(self.libros_prestados)} libros"
