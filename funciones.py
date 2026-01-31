import random
from scipy import signal
import numpy as np
import cv2
from enum import Enum
import matplotlib.pyplot as plt

### Constantes ###

AREA_CARTA_MIN = 150
AREA_CARTA_MAX = 700

# Dimensiones de los numeros y palos
ANCHO_IMG = 70
ALTO_IMG = 125

# Rango de píxeles diferentes
DIFERENCIA_MAX_NUM = 2500
DIFERENCIA_MAX_PALO = 2500

# Para saber qué contorno es pareja de cual
PAREJA = 500

# Para identificar número de la carta
class Numero(Enum):
    As = 0
    Tres = 1
    Rey = 2
    Caballo = 3
    Sota = 4
    Siete = 5
    Seis = 6
    Cinco = 7
    Cuatro = 8
    Dos = 9

# Para identificar palo
class Palo(Enum):
    Oro = 0
    Copa = 1
    Espada = 2
    Basto = 3


##---- FUNCIONES  ----##
def imagenesTraining(path):
    """Guardamos en un array todas las imagenes del training y lo devolvemos."""

    todo = []

    for num in Numero:
        # Sin invertir
        filename = str(num.name) + '.jpg'
        image = cv2.imread(path + filename, cv2.IMREAD_GRAYSCALE)
        todo.append(image)     # Se guardan por orden establecido en juegoBrisca

        # Inversas
        filename = str(num.name) + '_inv.jpg'
        image = cv2.imread(path + filename, cv2.IMREAD_GRAYSCALE)
        todo.append(image)     # Se guardan por orden establecido en juegoBrisca
    

    for palo in Palo:
        # Sin invertir
        filename = str(palo.name) + '.jpg'
        image = cv2.imread(path + filename, cv2.IMREAD_GRAYSCALE)
        todo.append(image)    # Se guardan por orden establecido en juegoBrisca

        # Inversas
        filename = str(palo.name) + '_inv.jpg'
        image = cv2.imread(path + filename, cv2.IMREAD_GRAYSCALE)
        todo.append(image)    # Se guardan por orden establecido en juegoBrisca        

    return todo

# Implement a function that blurres an input image using a Gaussian filter and then normalizes it. (Cogido de práctica 3.2)
def gaussian_smoothing(image, sigma, w_kernel):
    """ Blur and normalize input image.   
    
        Args:
            image: Input image to be binarized
            sigma: Standard deviation of the Gaussian distribution
            w_kernel: Kernel aperture size
                    
        Returns: 
            smoothed_norm: Blurred image
    """   
    # Write your code here!
    
    # Define 1D kernel
    s=sigma
    w=w_kernel
    # Create 1D Gaussian filter
    kernel_1D = np.array([(1/(np.sqrt(2*np.pi)*s))*np.exp(-(1/2)*(z*z/(s*s))) for z in range(-w,w+1)])
    
    # Apply distributive property of convolution
    vertical_kernel = kernel_1D.reshape(2*w+1,1)
    horizontal_kernel = kernel_1D.reshape(1,2*w+1)   
    gaussian_kernel_2D = signal.convolve2d(vertical_kernel, horizontal_kernel)   
    
    # Blur image
    smoothed_img = cv2.filter2D(image, cv2.CV_8U, gaussian_kernel_2D)
    
    # Normalize to [0 254] values
    smoothed_norm = np.array(image.shape)
    # cv.normalize(src, dst, alpha (=norm value to normalize), beta (=upper range boundary in case of the range normalization), norm_type) 
    smoothed_norm = cv2.normalize(smoothed_img, None, 0, 255, cv2.NORM_MINMAX) # Leave the second argument as None
    
    return smoothed_norm


def procesadoImagen(image):
    """Devuelve la imagen después de pasarla a gris, hacerle suavizado Gaussiano y binarizarla."""

    # La pasamos a gris y le hacemos suavizado gaussiano
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    blurred_img = gaussian_smoothing(gray, 1.40, 3)
    
    # Idea:
    # Queremos que cuando haya mucho brillo, el threshold sea alto. Si hay poco brillo (imagen oscura),
    # el threshold sea bajo. Para ello, vamos a usar lo siguiente:
    # Vamos a cojer 10 pixeles random de la imagen, haremos la media de sus valores (=intensidad media de los 10 piexeles)
    # y a continuación le sumaremos una constante.
    height = image.shape[0] # Eje y
    width = image.shape[1] # Eje x

    cont = 0
    valley = 0
    hist = cv2.calcHist([image],[0],None,[256],[0,256])

    while cont < 7/10 * height * width:        
        cont += hist[valley]
        valley += 1
    
    threshold = valley
    # Binarizamos la imagen con threshold calculado
    _, image_binarized = cv2.threshold(blurred_img, threshold, 255, cv2.THRESH_BINARY)
    
    return image_binarized


def buscaCartas(image):
    """Buscamos todas las cartas a partir de su contorno. Devolvemos el número
    de cartas mostradas y una lista de contornos con su correspondiente pareja."""

    # Busco los contornos que aparecen en la imagen
    # contours es la lista con todos los contornos
    # hierarchy es la lista que establece relación padre-hijo entre contornos (un contorno es padre si tiene a otro contorno en su interior)
    # hierarchy = [Next, Previous, First_Child, Parent]
    # Usamos RETR_CCOMP para única relación padre-hijo
    contours, hierarchy = cv2.findContours(image, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    # Recorro los contornos para encontrar las áreas más grandes.
    contornosCartas = []
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        # Que sea de tamaño apropiado y tenga padre (borde carta)
        if area > AREA_CARTA_MIN and area < AREA_CARTA_MAX and hierarchy[0][i][3] != -1:
            contornosCartas.append(contours[i])

    
    # Vamos a quedarnos solo aquellos contornos que tengan una correspondiente pareja
    pareja = []
    for i in range(len(contornosCartas)):
        
        M = cv2.moments(contornosCartas[i])
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        j = i+1     # Comparo con los siguientes contornos
        salir = False
        while j < len(contornosCartas) and not salir:
            
            M = cv2.moments(contornosCartas[j])
            cX2 = int(M["m10"] / M["m00"])
            cY2 = int(M["m01"] / M["m00"])

            if (abs(cX - cX2) < PAREJA) and (abs(cY - cY2) < PAREJA):
                pareja.append([contornosCartas[i], contornosCartas[j]])
                salir = True
            
            j += 1

    
    return pareja
    

def dibujarRectangulo(image, parejas):
    """Dibujamos el rectángulo mínimo que envuelve a los contornos pasados por parámetro.
    Devolvemos la imagen con el rectángulo dibujado, los vértices del rectángulo y la imagen
    con la transformación de perpectiva."""

    copy = image.copy()
    bin = []
    puntosTodos = []

    # Dibujamos menor rectángulo y cogemos los puntos
    for i in range(len(parejas)):
        
        # Dibujo mínimo rectangulo alrededor
        rect = cv2.minAreaRect(parejas[i][0]) # Pareja 1
        rect2 = cv2.minAreaRect(parejas[i][1]) # Pareja 2
        
        # Array con los vértices
        # Pongo np.int para que los vértices no tengan decimales (También se podría haber hecho manualmente (más trabajoso))
        ptos = [np.int0(cv2.boxPoints(rect)), np.int0(cv2.boxPoints(rect2))]
        
        for k in range(len(ptos)):
            for j in range(len(ptos[k])):
                # Dibujo puntos (=vértices)        
                cv2.circle(image, (ptos[k][j][0], ptos[k][j][1]), radius=1, color=(0, 0, 255), thickness=4) 

            # Dibujo líneas rectángulo
            cv2.drawContours(copy, [ptos[k]], 0, (0,0,255), 3)

            # Guardamos un array con las cartas haciendole una transformación de perspectiva
            w = rect[1][0]      # Anchura del rectángulo
            h = rect[1][1]      # Largo del rectángulo
            recortada = perpectivaYRedimensionar(image, ptos[k], w, h)

            # Binarizamos la imagen
            _, image_binarized = cv2.threshold(recortada, 150, 255, cv2.THRESH_BINARY_INV)
            bin.append(image_binarized)

        # Añadimos 1 punto caulquiera para cada pareja (para después poner el texto) (Hemos escogido primer punto de cada pareja)
        x = parejas[i][0][0][0][0]
        y = parejas[i][0][0][0][1]
        puntosTodos.append((x, y))

    return copy, puntosTodos, bin


# Encuentra si coincide con alguna de las imagenes del training, es decir, el palo y el número con la que mejor se identifica.
def identificar(par1, par2, training):
    """Encuentra si coincide con alguna de las imágenes del training, es decir, el palo y el número con el que mejor se identifica.
    Devuelve el número y palo con el que se ha identificado. Si no se ha podido identificar con ninguno, devuelve "Desconocido"."""

    nombreNumero = "Desconocido"
    nombrePalo = "Desconocido"

    # Voy a comparar par1 y par2 con todas las imágenes del training
    # Empecemos con cual encaja par1
    limite = 10000
    nomPalo = "False"
    nomNum = "False"
    for i in range(len(training)):
            
        dif = cv2.absdiff(par1, training[i])
        dif = int(np.sum(dif)/255)

        # Me quedo con limite menor
        if dif < limite and i < 20:  # Si coincide con número (hay 20 numeros (10 normales + 10 inversos))
            nomPalo = "False"
            limite = dif
            if i >= 10:
                k = i - 10
            else:
                k = i
            nomNum = Numero(k).name

        elif dif < limite: # Si coincide con palo (si es >20, entonces son las últimas 4 que son los palos)
            nomNum = "False"
            limite = dif
            k = i - 20
            if k >= 4:
                k = k - 4
            nomPalo = Palo(k).name

    if (limite < DIFERENCIA_MAX_NUM) and (nomNum != "False"):
        nombreNumero = nomNum

    if (limite < DIFERENCIA_MAX_PALO) and (nomPalo != "False"):
        nombrePalo = nomPalo

    # Lo mismo para par2
    limite = 10000
    nomPalo = "False"
    nomNum = "False"
    for i in range(len(training)):
            
        dif = cv2.absdiff(par2, training[i])
        dif = int(np.sum(dif)/255)

        # Me quedo con límite menor
        if dif < limite and i < 20:  # Si coincide con número (hay 20 numeros (10 normales + 10 inversos))
            nomPalo = "False"
            limite = dif
            if i >= 10:
                k = i - 10
            else:
                k = i
            nomNum = Numero(k).name

        elif dif < limite: # Si coincide con palo (si es >20, entonces son las últimas 4 que son los palos)
            nomNum = "False"
            limite = dif
            k = i - 20
            if k >= 4:
                k = k - 4
            nomPalo = Palo(k).name

    if (limite < DIFERENCIA_MAX_NUM) and (nomNum != "False"):
        nombreNumero = nomNum

    if (limite < DIFERENCIA_MAX_PALO) and (nomPalo != "False"):
        nombrePalo = nomPalo

    # En dif, hemos calculado la diferencia de píxeles entre la carta a reconocer y la de entrenamiento.
    # Si el número de píxeles obtenido es menor que el rango máximo, entonces tenemos match. Si es mayor, es decir, 
    # hay muchos fallos, entonces dejamos el contorno como desconocido.

    # Devuelvo el nombre del número y palo que mejor se identifica con la carta/contorno
    return nombreNumero, nombrePalo
    
# Dibujar centro y nombre de la carta    
def dibujar(image, numero, palo, punto):
    """Devuelve la imagen con el texto que identifica a la carta."""

    # Coordenadas del centro
    x = punto[0]
    y = punto[1]

    # Dibujamos texto sobre la carta
    cv2.putText(image,(numero +' de'), (x-60,y-10), cv2.FONT_ITALIC, 1, (255,0,0), 2, cv2.LINE_AA)
    cv2.putText(image, palo, (x-60,y+25), cv2.FONT_ITALIC, 1, (255,0,0), 2, cv2.LINE_AA)

    return image

def perpectivaYRedimensionar(image, pts, w, h):
    """Quita la perpectiva de la imagen y la convierte en una imagen plana de escala de grises.
    Redimensiona a una imagen 70 x 125."""

    # Idea: Los puntos vienen ordenados: el primer vértice es el de menor x, y los siguientes seguirán
    # el sentido horario.

    temp_rect = np.zeros((4,2), dtype = "float32")

    # Si la carta está ladeada, es decir, no está ni horizontal ni vertical
    if pts[0][0] != pts[3][0]:
        # Si la carta está ladeada hacia la izquierda (vértice 0 es el superior izq)
        if pts[0][1] < pts[2][1]: 
            temp_rect[0] = pts[0]
            temp_rect[1] = pts[1]
            temp_rect[2] = pts[2]
            temp_rect[3] = pts[3]

        # Si la carta está ladeada hacia la derecha (vértice 0 es el inferior izq)
        else: 
            temp_rect[0] = pts[1]
            temp_rect[1] = pts[2]
            temp_rect[2] = pts[3]
            temp_rect[3] = pts[0]
    
    else: # Si la carta está vertical u horizontal
        
        if h >= w: # Si la altura > anchura -> está vertical; o si es un cuadrado perfecto (oros)
            temp_rect[0] = pts[0]
            temp_rect[1] = pts[1]
            temp_rect[2] = pts[2]
            temp_rect[3] = pts[3]

        elif w > h: # Si la anchura > altura -> está horizontal
            temp_rect[0] = pts[3]
            temp_rect[1] = pts[0]
            temp_rect[2] = pts[1]
            temp_rect[3] = pts[2]
            
        
    maxWidth = ANCHO_IMG
    maxHeight = ALTO_IMG

    # Creamos la imagen con la transformada, usando getPerspectiveTransform y la "deformamos" con warpPerspective
    dst = np.array([[0,0], [maxWidth-1,0], [maxWidth-1,maxHeight-1], [0, maxHeight-1]], np.float32)
    persp = cv2.getPerspectiveTransform(temp_rect, dst)
    warp = cv2.warpPerspective(image, persp, (maxWidth, maxHeight))
    warp = cv2.cvtColor(warp, cv2.COLOR_BGR2GRAY)

    # Devolvemos la imagen "deformada"
    return warp