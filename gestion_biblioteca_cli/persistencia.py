"""
Módulo de persistencia de datos.

Maneja la serialización y deserialización de datos a archivos JSON.
Proporciona abstracción de la capa de datos.
"""

from pathlib import Path
from modelos import Libro, Usuario, ValidationError
import json


class ArchivoDatos:
    """
    Gestor de persistencia de datos en archivos JSON.
    
    Responsable de serializar y deserializar los objetos Libro y Usuario
    desde y hacia archivos JSON para la persistencia de datos.
    
    Attributes:
        base_path (Path): Directorio base donde se almacenan los archivos
        libros_path (Path): Ruta al archivo de libros JSON
        usuarios_path (Path): Ruta al archivo de usuarios JSON
    """
    
    def __init__(self, base_path: str = "data") -> None:
        self.base_path = Path(base_path)
        self.libros_path = self.base_path / "libros.json"
        self.usuarios_path = self.base_path / "usuarios.json"

        self.base_path.mkdir(parents=True, exist_ok=True)

    # ====== Serialización ======
    def guardar_usuarios(self, usuarios):
        """Serializar cada objeto llamando al método to_dict() del objeto usuario"""
        data = {id_: usuario.to_dict() for id_, usuario in usuarios.items()}
        self._guardar_json(self.usuarios_path, data)

    def guardar_libros(self, libros):
        """Serializar cada objeto libro llamando al método to_dict() del objeto usuario"""
        data = {id_: libro.to_dict() for id_, libro in libros.items()}
        self._guardar_json(self.libros_path, data)

    # ====== Deserialización ======
    def cargar_usuarios(self):
        """Recibe """
        # ====== No existe ningún archivo ======
        if not self.usuarios_path.exists():
            return {}

        data = self._cargar_json(self.usuarios_path)
        return {id_: Usuario.from_dict(usuario) for id_, usuario in data.items()}

    def cargar_libros(self):
        """Aquí debo convertir cada diccionario del archivo JSON a objeto de clase Libro nuevamente"""

        # ====== No existe ningún archivo ======
        if not self.libros_path.exists():
            return {}

        data = self._cargar_json(self.libros_path)
        return {id_: Libro.from_dict(libro) for id_, libro in data.items()}

    # ====== Guardar / Cargar ======
    def _guardar_json(self, path, data):
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def _cargar_json(self, path):
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
