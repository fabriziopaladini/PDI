# TP1 – Procesamiento de Imágenes I (TUIA – UNR, 2026 2° semestre)

Resolución del Trabajo Práctico N° 1:

- **Problema 1: Ecualización local de histograma** (`TP1.py`)
- **Problema 2: Validación de planillas de calificaciones** (`TP1b.py`)

El informe completo, con el análisis y los resultados, está en [`informe/Informe_TP1_PDI.pdf`](informe/Informe_TP1_PDI.pdf).

## Integrantes

- Aguirre, Federico
- Gambandé, Sara
- Paladini, Fabrizio

## Requisitos

Versiones con las que se desarrolló y probó el trabajo:

| Software | Versión |
|---|---|
| Python | 3.14.2 |
| opencv-contrib-python | 5.0.0 |
| numpy | 2.5.3 |
| matplotlib | 3.11.2 |

Instalación en un entorno virtual:

```bash
python -m venv venv
# Windows
venv\Scripts\activate

pip install opencv-contrib-python==5.0.0.93 numpy==2.5.3 matplotlib==3.11.2
```

## Estructura

```
.
├── TP1.py                        # Problema 1
├── TP1b.py                       # Problema 2
├── README.md
├── TUIA_PDI_TP1_2026_C2.pdf      # enunciado del TP
└── informe/
    └── Informe_TP1_PDI.pdf       # informe
```

## Imágenes de entrada

Las imágenes de entrada no se incluyen en el repositorio. Son las provistas por la cátedra y, antes de ejecutar los scripts, hay que copiarlas en la carpeta raíz, junto a `TP1.py` y `TP1b.py`, con estos nombres:

- Problema 1: `Imagen_con_detalles_escondidos.tif`
- Problema 2: `grade_sheet_1.png`, `grade_sheet_2.png`, `grade_sheet_3.png` y `grade_sheet_4.png`

## Ejecución

Ejecutar los scripts desde la carpeta raíz del repositorio, porque las imágenes se leen con rutas relativas.

### Problema 1

```bash
python TP1.py
```

Muestra la imagen original, la comparación entre la ecualización global y la local (ventana de 15×15) y los resultados con distintos tamaños de ventana. Hay que cerrar cada ventana para que siga. La de 215×215 tarda unos segundos.

### Problema 2

```bash
python TP1b.py
```

Muestra los pasos intermedios sobre `grade_sheet_1.png` (hay que cerrar cada ventana para que siga). Después procesa las 4 planillas: imprime OK/MAL por campo de cada registro y genera `resultados_<id>.csv` y `no_aprobados_<id>.png` en la misma carpeta.
