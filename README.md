## DESCRIPCIÓN

El programa está diseñado para detectar cartas de la brisca española y, posteriormente, aplicar un algoritmo que predice las mejores jugadas para maximizar las probabilidades de victoria. Se ha realizado usando la librería OpenCV.

## PARTES DE LA QUE CONSTA

Tendremos 4 ficheros .py diferentes:
- TrainImages: 	Fichero con el cual se puede tomar capturas para hacer las imágenes de training.

- juegoBrisca:	Algoritmo que simula el juego de la brisca, tomando las mejores decisiones posibles para ganar la partida.

- cardDetector:	Fichero desde el cual se identifican las cartas (se pueden identificar varias cartas a la vez).

- funciones: Será invocada desde cardDetector para llamar todas las funciones necesarias en cada momento.


## INSTRUCCIONES DE USO

1º) Descargar en el móvil la aplicación DroidCam.

2º) Abrir la carpeta completa donde se almacenan los 4 ficheros en el editor de código.

3º) En el fichero cardDetector, cambiar la dirección del VideoCapture por la que se muestra en la aplicación de DroidCam al abrirla.

4º) Ejecutar el algortimo de la brisca desde el editor de código.

5º) Cuando tengamos una carta identificada presionamos espacio para que juegoBrisca la obtenga y prosigamos con nuestro juego.

6º) Continuamos con el juego.

## IMPORTANTE

- La detección de cartas solo funciona con unas específicas parecidas a las del póker, las cuales tienen los números y palos en las esquinas superior izquierda 
e inferior derecha.

## POSIBLES MEJORAS EN EL FUTURO

- Permitir que el módulo juegaBrisca procese más de una carta simultáneamente, para lo cual podría implementarse un sistema de almacenamiento intermedio (buffer).

- Ampliar las funcionalidades de cardDetector para que no solo identifique las cartas, sino que también distinga entre la vira, las cartas en mano del jugador y la carta jugada por el oponente.

- Mejorar la precisión del sistema, de modo que la identificación de las cartas sea robusta frente a distintos fondos, evitando que el entorno visual afecte de forma significativa al reconocimiento.

- Habilitar la detección de las cartas clásicas Fournier.
  


