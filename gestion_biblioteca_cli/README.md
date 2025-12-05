# 📚 Gestor de Biblioteca CLI

Aplicación simple para gestionar libros y usuarios en una biblioteca. Permite registrar usuarios, agregar libros, hacer préstamos y devoluciones con persistencia en JSON.

## 🎯 Características

- Gestión de libros (agregar, listar, prestar)
- Gestión de usuarios (registrar, ver préstamos)
- Préstamos y devoluciones automáticos
- Persistencia de datos en JSON
- Validaciones de datos

## 📋 Requisitos

- Python 3.10+

## 🚀 Instalación

```bash
git clone https://github.com/DonHeri/gestion-biblioteca.git
cd gestion-biblioteca
python main.py
```

## 💻 Uso

```
[1] 📖 Añadir libro
[2] 👤 Registrar usuario  
[3] 📤 Prestar libro
[4] 📥 Devolver libro
[5] 📋 Ver libros
[6] 👥 Ver usuarios
[7] 🚪 Salir
```

## 📁 Estructura

```
├── main.py          # Interfaz de usuario
├── gestor.py        # Lógica de negocio
├── modelos.py       # Clases de datos
├── persistencia.py  # Serialización JSON
└── data/            # Base de datos (generada automáticamente)
```

## 📝 Detalles

- Sin dependencias externas
- Datos se guardan automáticamente
- Máximo 3 libros por usuario
- IDs automáticos: LBR-XXXX, USR-XXXX


## 👤 Autor

**Heri** - GitHub: [@DonHeri](https://github.com/DonHeri)
