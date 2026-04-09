# Estructura de Archivos - CineVault

## Organización del Código

### Punto de Entrada
- **`main.py`** - Archivo principal para ejecutar la aplicación

### Modelos (models/)
- **`__init__.py`** - Exporta MediaItem y Movie
- **`media_item.py`** - Clase abstracta MediaItem (ABC)
- **`movie.py`** - Clase Movie con validaciones y propiedades

### Estructuras de Datos (data_structures/)
- **`__init__.py`** - Exporta FilmBead y FilmReel
- **`film_bead.py`** - Nodo de la lista doblemente enlazada
- **`film_reel.py`** - Lista doblemente enlazada completa

### Servicios (services/)
- **`__init__.py`** - Exporta CatalogManager
- **`catalog_manager.py`** - Lógica de negocio (CRUD, búsquedas, estadísticas)

### Interfaz de Usuario (ui/)
- **`__init__.py`** - Exporta todos los componentes UI
- **`config.py`** - Paleta de colores PALETTE
- **`form_dialog.py`** - Diálogo modal para agregar/editar películas
- **`stats_panel.py`** - Panel de estadísticas
- **`cinevault_app.py`** - Aplicación principal Tkinter

## Flujo de Dependencias

```
main.py
  └─> ui.CineVaultApp
       ├─> services.CatalogManager
       │    ├─> data_structures.FilmReel
       │    │    └─> data_structures.FilmBead
       │    │         └─> models.Movie
       │    └─> models.Movie
       ├─> ui.FormDialog
       │    └─> models.Movie (VALID_GENRES, VALID_RATINGS)
       ├─> ui.StatsPanel
       └─> ui.config.PALETTE
```

## Clases por Archivo

| Archivo | Clases | Líneas Aprox |
|---------|--------|--------------|
| `models/media_item.py` | MediaItem | 15 |
| `models/movie.py` | Movie | 180 |
| `data_structures/film_bead.py` | FilmBead | 20 |
| `data_structures/film_reel.py` | FilmReel | 130 |
| `services/catalog_manager.py` | CatalogManager | 90 |
| `ui/config.py` | PALETTE (dict) | 15 |
| `ui/form_dialog.py` | FormDialog | 130 |
| `ui/stats_panel.py` | StatsPanel | 110 |
| `ui/cinevault_app.py` | CineVaultApp | 380 |
| `main.py` | main() | 15 |

## Ventajas de esta Organización

1. **Separación de responsabilidades** - Cada archivo tiene un propósito claro
2. **Fácil mantenimiento** - Cambios localizados en archivos específicos
3. **Reutilización** - Los módulos pueden importarse independientemente
4. **Testing** - Cada clase puede probarse de forma aislada
5. **Escalabilidad** - Fácil agregar nuevas funcionalidades
6. **Legibilidad** - Archivos más pequeños y enfocados

## Cómo Ejecutar

```bash
python main.py
```

## Notas

- Todos los `__init__.py` exportan las clases principales de cada módulo
- Las importaciones usan rutas relativas desde la raíz del proyecto
- La configuración de colores está centralizada en `ui/config.py`
- El archivo original `cinevault.py` puede mantenerse como referencia o eliminarse
