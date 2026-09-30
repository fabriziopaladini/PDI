import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('grade_sheet_1.png', cv2.IMREAD_GRAYSCALE)
print(img.shape)
plt.imshow(img, cmap='gray')
plt.show()

img_th = img < 150   # True compara cada pixel con 150 si es menor: True(blanco), si es mayor: False(negro)
plt.imshow(img_th, cmap='gray')
plt.show()

img_rows = np.sum(img_th, 1)   # suma cada fila: cuántos píxeles blancos tiene
plt.plot(img_rows)
plt.title("Píxeles blancos por fila")
plt.xlabel("Número de fila")
plt.show()

'''
De 0 a 200 aprox.: es el encabezado de la planilla, con la imagen de los robots, el título "Procesamiento de Imágenes 1" y el logo. 
Tiene bastantes píxeles oscuros, pero ninguna fila llega a ser una línea completa
Pico en ~210: es la línea de arriba de la tabla, donde empieza el encabezado "Nro., Legajo, Nombre y Apellido...".
Pico más bajo en ~260, que llega a ~380: es la línea que separa "Notas" de "Parcial 1, Parcial 2, Parcial 3". 
Es más corta porque solo cruza esas tres columnas, no todo el ancho.
Desde ~285 hasta ~805: una seguidilla de picos altos, muy parejos y a distancias iguales. Son las líneas que separan los 20 registros.
Entre los picos, valores de ~100: es el texto de cada fila (el número de registro y lo que esté escrito).
Desde ~805 hasta ~900: es la línea que separa "Promedio" de "Final". 
'''
img_rows_th = img_rows > 500   # True en las filas que son línea
filas_linea = np.where(img_rows_th)[0]   # números de esas filas
print(filas_linea)

img_cols = np.sum(img_th, 0)   # suma cada columna
plt.plot(img_cols)
plt.title("Píxeles blancos por columna")
plt.xlabel("Número de columna")
plt.show()

img_cols_th = img_cols > 400
columnas_linea = np.where(img_cols_th)[0]
print(columnas_linea)

campos = ["Legajo", "Nombre y apellido", "Parcial 1", "Parcial 2", "Parcial 3", "Condición Final"]

fila_ini = filas_linea[1] + 1   # registro 1: debajo de la línea 286
fila_fin = filas_linea[2]       # hasta la línea 312 (sin incluirla)

plt.figure(figsize=(15, 3))
for i in range(6):
    col_ini = columnas_linea[i + 1] + 1
    col_fin = columnas_linea[i + 2]
    celda = img_th[fila_ini:fila_fin, col_ini:col_fin]
    plt.subplot(1, 6, i + 1)
    plt.imshow(celda, cmap='gray')
    plt.title(campos[i])
plt.show()

celda = img_th[fila_ini:fila_fin, columnas_linea[1] + 1:columnas_linea[2]]
celda = celda.astype(np.uint8)   # connectedComponents necesita números, no True/False

n, labels, stats, centroids = cv2.connectedComponentsWithStats(celda, 8, cv2.CV_32S)
print("Cantidad de componentes:", n)
print(stats)

caracteres = stats[1:]                            # sacamos el fondo
caracteres = caracteres[np.argsort(caracteres[:, 0])]   # ordenamos por x
for i in range(1, len(caracteres)):
    fin_anterior = caracteres[i - 1, 0] + caracteres[i - 1, 2]   # x + ancho
    hueco = caracteres[i, 0] - fin_anterior
    print("hueco:", hueco)

#No hay ningún hueco grande, así que el Legajo es una sola palabra

celda = img_th[fila_ini:fila_fin, columnas_linea[2] + 1:columnas_linea[3]].astype(np.uint8)
n, labels, stats, centroids = cv2.connectedComponentsWithStats(celda, 8, cv2.CV_32S)
print("Componentes:", n)

caracteres = stats[1:]                            # sacamos el fondo
caracteres = caracteres[np.argsort(caracteres[:, 0])]   # ordenamos por x
for i in range(1, len(caracteres)):
    fin_anterior = caracteres[i - 1, 0] + caracteres[i - 1, 2]   # x + ancho
    hueco = caracteres[i, 0] - fin_anterior
    print("hueco:", hueco)


'''''
10 huecos (11 letras), todos de entre 1 y 3 píxeles, salvo uno de 12. Ese es el espacio entre el nombre y el apellido, 
 así que el Nombre y Apellido son dos palabras
Un umbral de 6 separa bien los dos casos, con margen de los dos lados:
 Hueco menor o igual a 6: siguiente letra de la misma palabra.
 Hueco mayor a 6: empieza una palabra nueva.
'''''

cant_caracteres = n - 1   # sacamos el fondo
cant_espacios = 0
for i in range(1, len(caracteres)):
    fin_anterior = caracteres[i - 1, 0] + caracteres[i - 1, 2]
    hueco = caracteres[i, 0] - fin_anterior
    if hueco > 6:
        cant_espacios = cant_espacios + 1

cant_palabras = cant_espacios + 1
print("Caracteres:", cant_caracteres, "- Palabras:", cant_palabras)

#La cantidad de palabras es la cantidad de espacios más uno: con un espacio hay dos palabras, con cero espacios hay una.
#Para JUAN CARLINI debería imprimir Caracteres: 11 - Palabras: 2

def contar(celda):
    celda = celda.astype(np.uint8)
    n, labels, stats, centroids = cv2.connectedComponentsWithStats(celda, 8, cv2.CV_32S)
    caracteres = stats[1:]
    caracteres = caracteres[np.argsort(caracteres[:, 0])]
    cant_espacios = 0
    for i in range(1, len(caracteres)):
        fin_anterior = caracteres[i - 1, 0] + caracteres[i - 1, 2]
        hueco = caracteres[i, 0] - fin_anterior
        if hueco > 6:
            cant_espacios = cant_espacios + 1
    cant_letras = n - 1
    if cant_letras == 0:
        return 0, 0
    return cant_letras, cant_espacios + 1

for i in range(6):
    celda = img_th[fila_ini:fila_fin, columnas_linea[i + 1] + 1:columnas_linea[i + 2]]
    print(campos[i], contar(celda))


def validar(campo, cant_caracteres, cant_palabras):
    if campo == "Legajo":
        ok = cant_caracteres == 8 and cant_palabras == 1
    elif campo == "Nombre y apellido":
        ok = cant_palabras >= 2 and cant_caracteres <= 12
    elif campo == "Condición Final":
        ok = cant_caracteres == 1
    else:   # Parcial 1, 2 y 3
        ok = cant_palabras == 1 and 1 <= cant_caracteres <= 2
    if ok:
        return "OK"
    return "MAL"

print("> Registro 1:")
for i in range(6):
    celda = img_th[fila_ini:fila_fin, columnas_linea[i + 1] + 1:columnas_linea[i + 2]]
    cant_caracteres, cant_palabras = contar(celda)
    print(">", campos[i] + ":", validar(campos[i], cant_caracteres, cant_palabras))

resultados = []
for r in range(1, len(filas_linea) - 1):
    fila_ini = filas_linea[r] + 1
    fila_fin = filas_linea[r + 1]
    print("> Registro", str(r) + ":")
    fila_resultado = []
    for i in range(6):
        celda = img_th[fila_ini:fila_fin, columnas_linea[i + 1] + 1:columnas_linea[i + 2]]
        cant_caracteres, cant_palabras = contar(celda)
        estado = validar(campos[i], cant_caracteres, cant_palabras)
        print(">", campos[i] + ":", estado)
        fila_resultado.append(estado)
    resultados.append(fila_resultado)
    print(">")

revisar = [3, 8, 10, 11, 12, 14, 15, 19, 20]
plt.figure(figsize=(10, 8))
for k, r in enumerate(revisar):
    fila_ini = filas_linea[r] + 1
    fila_fin = filas_linea[r + 1]
    celda = img_th[fila_ini:fila_fin, columnas_linea[2] + 1:columnas_linea[3]]
    print("Registro", r, "- Nombre (caracteres, palabras):", contar(celda))
    plt.subplot(len(revisar), 1, k + 1)
    plt.imshow(img[fila_ini:fila_fin, columnas_linea[1]:columnas_linea[7]], cmap='gray')
    plt.ylabel(r, rotation=0)
    plt.xticks([]); plt.yticks([])

plt.show()