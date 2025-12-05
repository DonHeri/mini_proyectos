# Gestor de Notas — Proyecto en Tkinter

Aplicación de escritorio sencilla creada en **Python** usando **Tkinter**, para gestionar notas rápidas con posibilidad de guardarlas, editarlas y cambiar el tema visual.

## Funcionalidades principales

* Crear, editar y eliminar notas desde una interfaz gráfica.
* Guardado automático en un archivo `data/notas.txt`.
* Recuperación de notas guardadas al iniciar.
* Cambio de tema visual con distintos estilos predefinidos.
* Recordatorio de la posición de ventana entre sesiones.

## Estructura del proyecto

```
GestorNotas/
│
├─ main.py           # Punto de entrada de la aplicación
├─ ui.py             # Interfaz principal (clase GestorNotasApp)
├─ funciones.py      # Funciones de utilidad (rutas, temas, notas)
├─ temas.py          # Paleta de temas visuales
├─ icono.ico         # Icono de la aplicación
└─ data/             # Carpeta creada automáticamente al ejecutar
```

## Requisitos

* Python 3.10 o superior
* Librería estándar **tkinter** (incluida en Python)

## Clonar y ejecutar el proyecto

Si quieres probar el código fuente en tu propio equipo:

```bash
# Clonar el repositorio
git clone https://github.com/DonHeri/Gestor-de-notas.git

# Entrar a la carpeta del proyecto
cd Gestor-de-notas

# Ejecutar la aplicación
python main.py
```

No se necesitan dependencias externas.

## Crear el ejecutable (.exe)

Para generar el archivo ejecutable con PyInstaller:

```bash
pyinstaller --noconsole --onefile main.py --icon=icono.ico
```

El ejecutable se generará dentro de la carpeta `dist/`.

## Notas

* Al iniciar por primera vez se crea automáticamente la carpeta `data/` en el mismo directorio.
* Los datos se guardan en texto plano (`notas.txt`) dentro de esa carpeta.

---

**Autor:** Heriberto Rojas