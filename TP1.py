#Importacion de librerias
import cv2
import numpy as np
import matplotlib.pyplot as plt

#Carga de la imagen
img = cv2.imread('Imagen_con_detalles_escondidos.tif',cv2.IMREAD_GRAYSCALE)
plt.imshow(img, cmap='gray')
plt.show()

#Comentar que al principio creia que tenia que hacer un recorte de la imagen que vaya recorriendo sobre la imagen original


#Creamos la funcion de ecualizacion
def equalizacion_local(imagen, M, N):
    copia = imagen.copy()  # creamos la imagen de salida
    fila_central = M // 2
    columna_central = N // 2
    # Genera una imagen con bordes para poder aplicar la ventana centrada en los bordes
    bordes = cv2.copyMakeBorder(copia, fila_central, fila_central, columna_central, columna_central, cv2.BORDER_REPLICATE)
    filas, columnas = copia.shape
    for fila in range(filas):
        for col in range(columnas):
            ventana = bordes[fila:fila + M, col:col + N]
            equalizacion_ventana = cv2.equalizeHist(ventana)
            # por cada fila y columna recorrida, almaceno el valor ecualizado del centro de la ventana
            copia[fila, col] = equalizacion_ventana[fila_central, columna_central]
    return copia

 
imagen_local = equalizacion_local(img, 71, 71)

plt.figure(figsize=(12, 5))
plt.subplot(1,4,1)
plt.imshow(img, cmap="gray")
plt.title("Original")


plt.subplot(1,4,2)
plt.imshow(imagen_local, cmap="gray")
plt.title("Ecualización local 71x71")


#Aplicamos pruebas para corroborar si influye el tamaño de la ventana
imagen_local_2 = equalizacion_local(img, 15, 15)

imagen_local_3 = equalizacion_local(img, 215, 215)

plt.subplot(1,4,3)
plt.imshow(imagen_local_2, cmap="gray") #Mostrar que en vez de poner img local 2 y 3, puse siempre la img local 1
plt.title("Ecualización local 15x15")


plt.subplot(1,4,4)
plt.imshow(imagen_local_3, cmap="gray")
plt.title("Ecualización local 215x215")
plt.show()


#Se cambian los tamaños de la ventana creada, no de la imagen original
