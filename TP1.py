# Importación de librerías
import cv2
import matplotlib.pyplot as plt

RUTA_IMAGEN = 'Imagen_con_detalles_escondidos.tif'

# a) Función de ecualización local de histograma
def ecualizacion_local(imagen, M, N):
    """
    Ecualiza localmente el histograma de `imagen` con una ventana de M filas x N columnas.
    Para cada píxel se ecualiza la ventana centrada en él y se conserva solo el valor
    resultante del píxel central.
    """
    if not (isinstance(M, int) and isinstance(N, int)) or M <= 0 or N <= 0:
        raise ValueError("M y N deben ser enteros positivos")
    if M % 2 == 0 or N % 2 == 0:
        raise ValueError("M y N deben ser impares para que la ventana tenga un píxel central")

    salida = imagen.copy()
    fila_central = M // 2
    columna_central = N // 2
    # Se agregan bordes replicados para poder centrar la ventana también en los píxeles del borde
    bordes = cv2.copyMakeBorder(imagen, fila_central, fila_central, columna_central, columna_central,
                                cv2.BORDER_REPLICATE)
    filas, columnas = imagen.shape
    for fila in range(filas):
        for col in range(columnas):
            ventana = bordes[fila:fila + M, col:col + N]
            ventana_ecualizada = cv2.equalizeHist(ventana)
            salida[fila, col] = ventana_ecualizada[fila_central, columna_central]
    return salida


def mostrar(imagenes, titulos, titulo_figura):
    plt.figure(figsize=(4 * len(imagenes), 4))
    for i, (im, titulo) in enumerate(zip(imagenes, titulos)):
        plt.subplot(1, len(imagenes), i + 1)
        plt.imshow(im, cmap='gray', vmin=0, vmax=255)
        plt.title(titulo)
        plt.axis('off')
    plt.suptitle(titulo_figura)
    plt.tight_layout()
    plt.show()


img = cv2.imread(RUTA_IMAGEN, cv2.IMREAD_GRAYSCALE)

if img is None:
    raise FileNotFoundError(f"No se encontró la imagen {RUTA_IMAGEN}")

# Se muestra la imagen original
plt.imshow(img, cmap='gray', vmin=0, vmax=255)
plt.title("Imagen original")
plt.axis('off')
plt.show()

# b) Análisis de la imagen: global vs local
img_global = cv2.equalizeHist(img)
img_local = ecualizacion_local(img, 15, 15)
mostrar([img, img_global, img_local],
        ["Original", "Ecualización global", "Ecualización local 15x15"],
        "Detección de detalles ocultos")

'''
Detalles ocultos encontrados (ventana 15x15):
 - Cuadrado superior izquierdo: un cuadrado más pequeño en su interior.
 - Cuadrado superior derecho: una línea diagonal.
 - Cuadrado central: la letra "a".
 - Cuadrado inferior izquierdo: varias líneas horizontales.
 - Cuadrado inferior derecho: un círculo.
La ecualización global no los revela porque el histograma se calcula sobre toda la imagen,
dominada por el fondo claro; los detalles tienen intensidades muy parecidas a su fondo local
(el cuadrado negro) y la transformación global prácticamente no los separa.
'''

# c) Influencia del tamaño de la ventana
tamanios = [(3, 3), (15, 15), (31, 31), (71, 71), (215, 215), (7, 45), (45, 7)]
resultados = [ecualizacion_local(img, M, N) for M, N in tamanios]
mostrar(resultados, [f"{M}x{N}" for M, N in tamanios], "Influencia del tamaño de ventana")

'''
Conclusiones:
 - Ventanas muy chicas (3x3): se amplifica muchísimo el ruido del fondo y de los objetos quedan
   sobre todo los bordes (el cuadrado y el círculo aparecen como contornos).
 - Ventanas intermedias (15x15 a 31x31), menores que los cuadrados (~62 px): mejor resultado.
   Los cinco detalles aparecen nítidos y completos; el costo es un fondo algo granulado.
 - Ventanas mayores que los cuadrados (71x71): la ventana incluye mucho fondo claro, el
   histograma local ya no representa la zona del detalle y el contraste cae.
 - Ventanas muy grandes (215x215): el resultado se acerca a la ecualización global y los
   detalles vuelven a quedar ocultos.
 - Ventanas rectangulares (7x45 y 45x7): el realce deja de ser uniforme. Con 45x7 (alta y
   angosta) las líneas horizontales casi desaparecen y el círculo queda con un gradiente;
   con 7x45 las líneas se ven, pero con intensidades desiguales. Como los detalles no tienen
   una orientación preferente, conviene una ventana cuadrada.
 - Costo computacional: crece con M*N (215x215 tarda unas 50 veces más que 15x15).
En resumen, el tamaño de ventana debe ser comparable o menor al tamaño de las regiones que
contienen los detalles, pero no tan chico como para que domine el ruido.
'''
