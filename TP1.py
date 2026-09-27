#Importacion de librerias
import cv2
import numpy as np
import matplotlib.pyplot as plt

#Carga de la imagen
img = cv2.imread('Imagen_con_detalles_escondidos.tif',cv2.IMREAD_GRAYSCALE)
plt.imshow(img, cmap='gray')
plt.show()



#Creamos la funcion de ecualizacion
def equalizacion_local(imagen, M, N):


    for fila in range(imagen.shape[0] - M + 1):
        for columna in range(imagen.shape[1] - N + 1):
            recorte = imagen[fila:fila + M, columna:columna + N].copy() #Creamos un recorte particular de la imagen

            fila_central = M // 2
            columna_central = N // 2
            valor = recorte[fila_central, columna_central]

            hist, bins = np.histogram(recorte.flatten(),256,[0,256]) #aplicamos el histograma sobre el recorte 
            histn = hist.astype(np.double) / recorte.size
            cdf = histn.cumsum() #funcion de distribucion acumulada
    print(cdf[valor]) 
    nueva_intensidad = round(255 * cdf[valor]) #devolvemos la nueva intensidad de los pixeles
    print(nueva_intensidad)

    resultado = imagen.copy() #creamos la imagen de salida
    resultado[fila + fila_central, columna + columna_central] = nueva_intensidad
    print(resultado)


equalizacion_local(img, 71, 51)
