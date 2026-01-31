# Import necessary packages
import cv2
import numpy as np
import time
import os
import funciones

 # Código para conectar la cámara
videostream = cv2.VideoCapture('http://192.168.1.12:4747/video')
time.sleep(1)

def main():     

    # Cargar las imágenes con números y palos
    path = os.path.dirname(os.path.abspath(__file__))
    imgTraining = funciones.imagenesTraining( path + '/train_images/')


    # Vamos a hacer un bucle que coja frames del video. Con estas imagenes 
    # reconoceremos las cartas.
    cam_quit = 0    # variable para salir del bucle

    while cam_quit == 0:

        # Cojo frame del video
        _, imageOrig = videostream.read()
        image = imageOrig.copy()

        # Procesado de imagen: pasarla a escala grises, Gaussian smooth y binarización
        pre_proc = funciones.procesadoImagen(image)
        
        # Encontrar los contorno de palos y números
        parejas = funciones.buscaCartas(pre_proc)

        # Dibujar rectángulo mínimo alrededor de palos y números. 
        # Devolvemos imagen con puntos y rectángulo; los puntos de cada pareja donde pondremos el texto; 
        # y números y palos recortados y binarizados.
        copy, pts, cartasRecortada = funciones.dibujarRectangulo(imageOrig, parejas)
        
        k = 0 # Índice para coger el centro que corresponde a cada pareja (para poner texto)
        # Para cada pareja de contornos detectado
        for i in range(0, len(cartasRecortada), 2): # Voy de 0 a len(cartasRecortada), con salto de 2 en 2

            # Buscamos el mejor emparejamiento para la carta.
            numero, palo = funciones.identificar(cartasRecortada[i], cartasRecortada[i+1], imgTraining)

            # Dibujamos el nombre del resultado del match si es diferente de desconocido.
            if numero != "Desconocido" and palo != "Desconocido":
                image = funciones.dibujar(copy, numero, palo, pts[k])
                k += 1

            # Enseñamos el frame resultante
            cv2.imshow("Card Detector", image)
        
        # Pulsamos espacio para salir del bucle
        key = cv2.waitKey(1) & 0xFF
        if key == ord(" "):
            cam_quit = 1

    cv2.destroyAllWindows()
    
    # Devolvemos el valor obtenido en la identificación de las cartas
    return numero, palo