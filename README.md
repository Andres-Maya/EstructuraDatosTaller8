# 🎬 CineVault — Personal Film Collection Manager

Gestor de colección personal de películas con interfaz gráfica Tkinter y estructura de datos de lista doblemente enlazada.

## 📁 Estructura del Proyecto

```
EstructuraDatosTaller8/
├── main.py                      # Punto de entrada de la aplicación
├── models/                      # Capa de dominio
│   ├── __init__.py
│   ├── media_item.py           # Clase abstracta base
│   └── movie.py                # Entidad Movie con validaciones
├── data_structures/             # Estructuras de datos
│   ├── __init__.py
│   ├── film_bead.py            # Nodo de lista doblemente enlazada
│   └── film_reel.py            # Lista doblemente enlazada
├── services/                    # Lógica de negocio
│   ├── __init__.py
│   └── catalog_manager.py      # CRUD y búsquedas
└── ui/                          # Capa de presentación
    ├── __init__.py
    ├── config.py                # Paleta de colores y configuración
    ├── form_dialog.py           # Diálogo para agregar/editar
    ├── stats_panel.py           # Panel de estadísticas
    └── cinevault_app.py         # Aplicación principal Tkinter
```

## 🚀 Instalación y Ejecución

### Prerrequisitos
- Python 3.10 o superior
- Tkinter (incluido con Python en la mayoría de instalaciones)

### Ejecutar la aplicación

```bash
cd EstructuraDatosTaller8
python main.py
```

## 🎯 Características

- ✅ **Lista doblemente enlazada** personalizada (FilmReel/FilmBead)
- ✅ **Encapsulación completa** en la clase Movie
- ✅ **Validaciones robustas** en tiempo de construcción
- ✅ **CRUD completo** (Crear, Leer, Actualizar, Eliminar)
- ✅ **Búsqueda y filtrado** en tiempo real
- ✅ **Ordenamiento** por título, año, puntuación, director
- ✅ **Estadísticas** de la colección con gráficos de texto
- ✅ **Interfaz oscura** estilo cinematográfico
- ✅ **Datos de demostración** precargados

## 🧩 Arquitectura

### Capas

1. **Domain (models/)**: Entidades de negocio con validaciones
2. **Data Structures (data_structures/)**: Implementación de lista doblemente enlazada
3. **Business Logic (services/)**: Operaciones CRUD y consultas
4. **Presentation (ui/)**: Interfaz gráfica Tkinter

### Principios SOLID

- **SRP**: Cada clase tiene una única responsabilidad
- **OCP**: Extensible sin modificar código existente
- **LSP**: MediaItem es sustituible por Movie
- **ISP**: Interfaces específicas y pequeñas
- **DIP**: Dependencias sobre abstracciones

## 📝 Uso

1. **Agregar película**: Click en "＋ Agregar"
2. **Editar película**: Doble click en una fila o botón "✎ Editar"
3. **Eliminar película**: Seleccionar y click en "✕ Eliminar"
4. **Ver estadísticas**: Click en "📊 Stats"
5. **Buscar**: Escribir en el campo de búsqueda
6. **Ordenar**: Usar los radio buttons o click en encabezados de columna

## 🔧 Posibles Mejoras

- Persistencia en JSON/SQLite
- Importación/exportación CSV
- Integración con API de TheMovieDB
- Imágenes de carteles
- Múltiples listas (Visto, Pendiente, Favoritas)
- Tests unitarios con pytest

## 📄 Licencia

Proyecto educacional - Taller de Estructuras de Datos
