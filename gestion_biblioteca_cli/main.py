"""
Módulo principal - Interfaz de usuario CLI.

Proporciona el menú interactivo para que el usuario interactúe con
el gestor de biblioteca. Maneja la validación de entrada y presentación.
"""

import gestor
from modelos import ValidationError


def menu() -> None:
    """
    Muestra el menú principal de opciones al usuario.
    
    Imprime un menú formateado con las 7 opciones disponibles
    en la aplicación de gestión de biblioteca.
    """
    print(
        """
╔════════════════════════════╗
   📚 GESTOR DE BIBLIOTECA  
╚════════════════════════════╝

[1] 📖 Añadir libro
[2] 👤 Registrar usuario
[3] 📤 Prestar libro
[4] 📥 Devolver libro
[5] 📋 Ver libros
[6] 👥 Ver usuarios
[7] 🚪 Salir
"""
    )

def obtener_opcion_menu(opciones_validas: list = None) -> str:
    """
    Obtiene y valida la opción ingresada por el usuario.
    
    Continúa pidiendo entrada hasta que el usuario ingrese
    una opción válida.
    
    Args:
        opciones_validas (list): Lista de strings con opciones válidas.
                                Por defecto: ["1", "2", "3", "4", "5", "6", "7"]
    
    Returns:
        str: La opción válida ingresada por el usuario
    """
    if opciones_validas is None:
        opciones_validas = ["1", "2", "3", "4", "5", "6", "7"]
    while True:
        opcion = input("Escriba el número de la opción deseada.\n> ").strip()

        if opcion in opciones_validas:
            return opcion
        print("Opción no válida. Intente de nuevo.")
    
def obtener_año_valido() -> int:
    """
    Obtiene y valida un año de publicación del usuario.
    
    Continúa pidiendo entrada hasta que el usuario ingrese
    un año válido entre 1000 y 2100.
    
    Returns:
        int: Año validado en el rango [1000, 2100]
    """
        try:
            año = int(input("Año: "))
            if 1000 <= año <= 2100:
                return año
            print("Año debe estar entre 1000 y 2100")
        except ValueError:
            print("Debe ingresar un número válido")

def main() -> None:
    """
    Función principal que ejecuta el programa.
    
    Inicializa el gestor de biblioteca y ejecuta el bucle
    principal de la interfaz de usuario. Maneja todas las opciones
    del menú y proporciona manejo de errores.
    """
    gestor_biblioteca = gestor.GestorBiblioteca()

    while True:
        menu()
        opcion = obtener_opcion_menu()

        try:
            # ====== Añadir libro ======
            if opcion == "1":
                titulo = input("Título del libro: ")
                autor = input("Autor: ")
                anio = obtener_año_valido()
                gestor_biblioteca.agregar_libro(titulo, autor, anio)

            # ====== Registrar usuario ======
            elif opcion == "2":
                nombre = input("Nombre del usuario: ")
                gestor_biblioteca.registrar_usuario(nombre)

            # ====== Prestar libro ======
            elif opcion == "3":
                id_libro = input("ID del libro: ")
                id_usuario = input("ID del usuario: ")
                gestor_biblioteca.prestar_libro(id_libro, id_usuario)

            # ====== Devolver libro ======
            elif opcion == "4":
                id_libro = input("ID del libro: ")
                id_usuario = input("ID del usuario: ")
                gestor_biblioteca.devolver_libro(id_libro, id_usuario)

            # ====== Listar Libros ======
            elif opcion == "5":
                for libro in gestor_biblioteca.libros.values():
                    print(libro)

            # ====== Listar Usuarios ======
            elif opcion == "6":
                for usuario in gestor_biblioteca.usuarios.values():
                    print(usuario)

            # ====== Salir ======
            elif opcion == "7":
                # Guardar datos
                gestor_biblioteca.guardar()
                print("Hasta pronto")
                break
        except ValidationError as e:
            print(f"[ERROR] - {e}")


if __name__ == "__main__":

    main()
