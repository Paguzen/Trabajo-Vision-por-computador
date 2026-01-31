import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
import funciones

img_path = os.path.dirname(os.path.abspath(__file__)) + '/images/'
res_path = os.path.dirname(os.path.abspath(__file__)) + '/train_images/'

ANCHO_IMG = 70
ALTO_IMG = 125

# Main
j = -1
for Name in ['As','Dos','Tres','Cuatro', 'Cinco', 'Seis', 'Siete', 'Sota', 'Caballo', 'Rey', 'Oro', 'Basto', 'Copa', 'Espada']:
    filename = Name + '.jpg'
    filenameInv = Name + '_inv.jpg'

    # Preprocesamos la imagen
    image = cv2.imread('./images/' + filename)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    ret, edges = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY)

    # Hierarchy cogemos pares padre-hijo
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

    # Dibuja los contornos
    c = []
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        if area < 45000 and area > 5000 and hierarchy[0][i][3] != -1:
            c.append(contours[i])

    cv2.drawContours(image,c,-1,(255,0,0),5)
    c = sorted(c, key=lambda a: np.sum(a)/len(a))

    plt.imshow(image)
    plt.show()

    j += 1
    for i in range(len(c)):
        # i = 0 -> Número esquina izq
        # i = 1 -> Palo esquina izq
        # i = 2 -> Palo esquina der
        # i = 3 -> Número esquina der

        rect = cv2.minAreaRect(c[i])

        box = cv2.boxPoints(rect)
        box = np.int0(cv2.boxPoints(rect))
        cv2.circle(image, (box[0][0], box[0][1]), radius=8, color=(0, 0, 255), thickness=16) 
        cv2.circle(image, (box[1][0], box[1][1]), radius=8, color=(0, 0, 255), thickness=16) 
        cv2.circle(image, (box[2][0], box[2][1]), radius=8, color=(0, 0, 255), thickness=16) 
        cv2.circle(image, (box[3][0], box[3][1]), radius=8, color=(0, 0, 255), thickness=16)
        cv2.drawContours(image, [box], 0, (0,0,255), 6)

        recortada = funciones.perpectivaYRedimensionar(image, box, rect[1][0], rect[1][1])
        _, image_binarized = cv2.threshold(recortada, 150, 255, cv2.THRESH_BINARY_INV)

        if(j <= 9):     # Obtenemos el número
            if(i == 0): # Número esquina izq
                cv2.imwrite(res_path + filename, image_binarized)
                plt.imshow(image_binarized)
                plt.show()

            if(i == 3): # Número esquina der
                cv2.imwrite(res_path + filenameInv, image_binarized)
                plt.imshow(image_binarized)
                plt.show()
        else:      # Obtenemos el palo
            if(i == 1): # Palo esquina izq
                cv2.imwrite(res_path + filename, image_binarized)
                plt.imshow(image_binarized)
                plt.show()
            if(i == 2): # Palo esquina der
                cv2.imwrite(res_path + filenameInv, image_binarized)
                plt.imshow(image_binarized)
                plt.show()