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

Ejecutar los scripts desde la carpeta raíz del repositorio, porque las imágenes se leen con rutas relativas. Los archivos de salida del Problema 2 se generan en esa misma carpeta al correr el script.

### Problema 1

```bash
python TP1.py
```

El script muestra tres figuras (hay que cerrar cada ventana para que siga):

1. La imagen original.
2. La imagen original, la ecualización global y la ecualización local con una ventana de 15×15. En la local se ven los detalles ocultos: un cuadrado, una línea diagonal, la letra "a", líneas horizontales y un círculo.
3. La ecualización local con ventanas de 3×3, 15×15, 31×31, 71×71, 215×215, 7×45 y 45×7.

La función principal es `ecualizacion_local(imagen, M, N)`. M y N deben ser enteros positivos. La ventana de 215×215 tarda unos segundos.

### Problema 2

```bash
python TP1b.py
```

Primero muestra, para `grade_sheet_1.png`, los pasos intermedios (imagen umbralada, proyecciones por fila y columna, celdas del registro 1 y huecos entre letras). Hay que cerrar cada ventana para que siga.

Después procesa en un ciclo `grade_sheet_1.png` a `grade_sheet_4.png` y para cada planilla hace lo siguiente:

- **a)** Imprime por terminal el resultado (OK / MAL) de cada campo de cada registro:
  ```
  > Registro 1:
  > Legajo: OK
  > Nombre y apellido: OK
  ...
  ```
- **b)** Genera `no_aprobados_<id>.png`: los recortes del campo *Nombre y apellido* de los alumnos con Condición Final **L** (etiqueta "LIBRE") o **R** (etiqueta "RECUPERA"). Sólo incluye registros con todos los campos OK. Si no hay ninguno, la imagen dice "Sin alumnos L o R para informar".
- **c)** Genera `resultados_<id>.csv` con las columnas `ID, Legajo, Nombre y Apellido, Parcial 1, Parcial 2, Parcial 3, Condición Final` y los valores OK / MAL.

Para procesar una sola planilla:

```python
from TP1b import procesar_planilla
procesar_planilla("grade_sheet_2.png", "resultados_2.csv", "no_aprobados_2.png")
```

## Reglas de validación

| Campo | Regla |
|---|---|
| Legajo | 8 caracteres, una sola palabra |
| Nombre y apellido | Al menos 2 palabras y hasta 12 caracteres (sin contar espacios) |
| Parcial 1, 2 y 3 | 1 o 2 caracteres consecutivos |
| Condición Final | Un único carácter |

## Parámetros principales (`TP1b.py`)

| Constante | Valor | Uso |
|---|---|---|
| `UMBRAL_BINARIO` | 150 | Un píxel con valor menor se considera tinta |
| `UMBRAL_ESPACIO` | 6 px | Un hueco horizontal mayor separa dos palabras |
| `UMBRAL_AREA` | 2 px | Se descartan las componentes conectadas de área menor o igual (ruido o restos de líneas) |
