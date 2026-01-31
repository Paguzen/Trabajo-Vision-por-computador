# PROGRAMA QUE SIMULA EL JUEGO DE LA BRISCA

from enum import Enum
import CardDetector as card

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

# Variables globales
meToca = False
puntosYo = 0
puntosRival = 0


misCartas = []
# TUPLA: (id, nombre, palo, puntos)
# Explicación: Vamos a usar una matriz que contendrá todas las cartas, donde cada fila será un palo distinto (para mayor facilidad y rapidez a la hora de buscar una carta)
quedan = [[(0, "AsOro", Palo.Oro, 11), (1, "TresOro", Palo.Oro, 10), (2, "ReyOro", Palo.Oro, 4), (3, "CaballoOro", Palo.Oro, 3), (4, "SotaOro", Palo.Oro, 2), (5, "SieteOro", Palo.Oro, 0), (6, "SeisOro", Palo.Oro, 0), (7, "CincoOro", Palo.Oro, 0), (8, "CuatroOro", Palo.Oro, 0), (9, "DosOro", Palo.Oro, 0)],
          [(10, "AsCopa", Palo.Copa, 11), (11, "TresCopa", Palo.Copa, 10), (12, "ReyCopa", Palo.Copa, 4), (13, "CaballoCopa", Palo.Copa, 3), (14, "SotaCopa", Palo.Copa, 2), (15, "SieteCopa", Palo.Copa, 0), (16, "SeisCopa", Palo.Copa, 0), (17, "CincoCopa", Palo.Copa, 0), (18, "CuatroCopa", Palo.Copa, 0), (19, "DosCopa", Palo.Copa, 0)],
          [(20, "AsEspada", Palo.Espada, 11), (21, "TresEspada", Palo.Espada, 10), (22, "ReyEspada", Palo.Espada, 4), (23, "CaballoEspada", Palo.Espada, 3), (24, "SotaEspada", Palo.Espada, 2), (25, "SieteEspada", Palo.Espada, 0), (26, "SeisEspada", Palo.Espada, 0), (27, "CincoEspada", Palo.Espada, 0), (28, "CuatroEspada", Palo.Espada, 0), (29, "DosEspada", Palo.Espada, 0)],
          [(30, "AsBasto", Palo.Basto, 11), (31, "TresBasto", Palo.Basto, 10), (32, "ReyBasto", Palo.Basto, 4), (33, "CaballoBasto", Palo.Basto, 3), (34, "SotaBasto", Palo.Basto, 2), (35, "SieteBasto", Palo.Basto, 0), (36, "SeisBasto", Palo.Basto, 0), (37, "CincoBasto", Palo.Basto, 0), (38, "CuatroBasto", Palo.Basto, 0), (39, "DosBasto", Palo.Basto, 0)]]
jugadas = []


def leerCarta():

    num = -1
    numero, palo = card.main()
    if palo != "Desconocido" and  numero != "Desconocido":
        for p in Palo:
            if palo == p.name:
                num = p.value * 10
        for n in Numero:
            if numero == n.name:
                num += n.value  
    return num

# Función que comprueba si carta está en quedan. Si es así devuelve la carta, sino devuelve vacío []. Además, si está, la elimina de quedan y la introduce en jugadas.
def existeCarta(carta):

    esta = []
    if (carta >= 0 and carta < 40):
        esta = [item for item in quedan[int (carta/10)] if item[0] == carta]      # Busca en quedan[fila] si está ese id (= item[0] que es tupla en posicion 0)
        if (esta != []):
            print("Carta: ", esta)
            quedan[int (carta/10)].remove(esta[0])
            jugadas.append(esta[0])

    return esta[0] if esta != [] else []

def imprimeCartas():

    print("Mis Cartas:", end="")
    for x in misCartas:
        print(" ", x, end="")
    print()

    #print("Quedan:")
    #for x in quedan:
    #    print(x)
    #print()

    #print("Jugadas:", end="")
    #for x in jugadas:
    #    print(" ", x, end="")
    #print()

# Función que reparte las 3 cartas iniciales y vira
def repartirInicio():

    # Vira
    global vira     # Vira va a ser variable global
    salir = False
    while (not salir):
        print("Introduzca vira: ")
        carta = leerCarta()
        if (carta >= 0 and carta < 40):
            esta = quedan[int (carta/10)][int (carta%10)]    # Posicion carta viene dada por fila = carta/10, columna = carta%10
            vira = esta
            print("Carta añadida es: ", esta)
            quedan[int (carta/10)].remove(esta)
            salir = True

    # Mis cartas
    i = 0
    while (i < 3):
        print("Introduzca carta " + str(i + 1) + ": ")
        carta = leerCarta()
        esta = existeCarta(carta)
        if (esta != []):
            misCartas.append(esta)
            i += 1


# Función que se encarga de la elección de que carta tiramos en la segunda tirada. Devuelve carta tirada.
def segundaTirada(cartaRival):

    cartaLanzada = ()

    # Carta menor que tenemos (tienen preferencia cartas que no son del mismo palo que vira)
    # Si tenemos carta(s) del mismo palo que la vira, guardaremos la de mayor valor.
    menor = misCartas[0]
    hayNormal = False
    triunfo = (any, any, any, -1)
    for x in misCartas:
        # Si la carta es normal la guardaremos como menor.
        if (x[2] != vira[2]):
            if (hayNormal):     # Hay más de 1 normal
                if (x[3] < menor[3]):
                    menor = x
            else:               # Preferencia sobre cartas que son triunfo
                menor = x
                hayNormal = True
        else:   # Si la carta es triunfo
            if (not hayNormal):
                if (x[3] < menor[3]):
                    menor = x
            if (x[3] > triunfo[3]):     # Escogemos triunfo de mayor valor
                triunfo = x

    # Lógica a seguir: si tira palo de la vira lanzaremos la carta más baja. Si tira otra intentaremos superarla.
    if (vira[2] == cartaRival[2]):       
        cartaLanzada = menor
    else:
        hayCarta = False
        # Vamos a ver si tengo una carta del mismo palo superior. Si tenemos varias, lanzamos la mayor.
        aux = cartaRival
        for x in misCartas:
            if ( (x[2] == cartaRival[2]) and (x[3] > aux[3]) ):
                cartaLanzada = x
                aux = x
                hayCarta = True
            # Caso en el que sean mismo valor (= 0) pero tengamos número superior (id menor). Tiene preferencia las cartas que tienen valor (por eso not hayCarta)
            elif ( not hayCarta and (x[2] == cartaRival[2]) and (x[3] == aux[3]) and (x[0] < aux[0]) ):
                cartaLanzada = x
                aux = x


        # Si no tenemos superior, lanzamos triunfo si la cartaRival tiene valor > 0, sino, lanzamos menor
        if (cartaLanzada == ()):
            if ( (triunfo[3] != -1) and (cartaRival[3] > 0) ):
                cartaLanzada = triunfo
            else:
                cartaLanzada = menor
    
    print("Lanzamos: ", cartaLanzada)
    # La introduzco en jugadas y la elimino de mi baza
    jugadas.append(cartaLanzada)
    misCartas.remove(cartaLanzada)

    # Esperar a que se lance carta
    # esperar = True
    # while (esperar):
    #     consola = input("La has tirado ya? (introduce y para seguir): ")
    #     if (consola == 'y' or consola == 'Y'): esperar = False

    return cartaLanzada


def primeraTirada():

    # 1ª PARTE: ANÁLISIS DE LAS CARTAS

    # Lógica que seguiremos: Vamos a ver la probabilidad de que el rival tenga algún triunfo.
    # Si la probabilidad es >50% tiraremos cartas más bajas y si es <50% nos arriesgaremos más.

    # Cálculo probabilidad

    total = len(quedan[0]) + len(quedan[1]) + len(quedan[2]) + len(quedan[3])       # Total de cartas que quedan

    # Cálculo probabilidad NINGUNA carta del rival sea triunfo: (noTriunfo/total) * ( (noTriunfo-1)/(total-1) ) * ( (noTriunfo-2)/(total-2) )
    noTriunfo = 0
    for i in range(len(quedan)):
        if (i != vira[2].value):
            noTriunfo += len(quedan[i])    

    prob = 1
    totalAux = total
    for i in range(len(misCartas)):
        prob = prob * (noTriunfo/totalAux)
        noTriunfo -= 1
        totalAux -= 1

    # Cálculo probabilidad que ALGUNA carta del rival sea triunfo: 1 - prob
    prob = 1 - prob

    # Vamos a analizar las cartas contenidas de cada palo.
    # Lógica a seguir: Vamos a calcular el valor medio de cada palo y el valor medio total para compararlo con los valores de nuestras cartas.
    # Si nuestro valor es mayor, hay mayor posibilidad de que "encartemos". (Ej: Tenemos valor 4 y media = 0.58, lo más normal es que el rival tenga una carta inferior a 4)

    medias = []         # Array con las medias de cada palo
    mediaTotal = 0      # Media total de todas las cartas
    suma = 0
    for i in range(len(quedan)):
        for x in quedan[i]:
            suma += x[3] 
        if (len(quedan[i]) > 0): 
            medias.append(suma/len(quedan[i]))  # Media de ese palo se une a todas las medias de los demás
        else:
            medias.append(0)    # Si no hay cartas añadimos un 0
        mediaTotal += suma
        suma = 0    # Reiniciamos suma
    mediaTotal = mediaTotal/total

    # 2ª PARTE: DECISIÓN DEL ALGORITMO

    # Carta menor que tenemos (tienen preferencia cartas que no son triunfo)
    # Tenemos triunfo?: Sí -> cogemos el de menor valor para no arriesgar mucho
    menor = misCartas[0]
    hayNormal = False
    triunfo = (any, any, any, 12)   # No hay carta con valor 12 -> lo usaremos como inicio de comparación (si hay triunfo, siempre tendrá un menor valor)
    for x in misCartas:
        # Si la carta es normal la guardaremos como menor.
        if (x[2] != vira[2]):
            if (hayNormal):     # Hay más de 1 normal
                if (x[3] < menor[3]):
                    menor = x
            else:               # Preferencia sobre cartas que son triunfo
                menor = x
                hayNormal = True
        else:   # Si la carta es triunfo
            if (not hayNormal):
                if (x[3] < menor[3]):
                    menor = x
            if (x[3] < triunfo[3]):     # Escogemos triunfo de menor valor
                triunfo = x

    candidata = ()
    hayCandidata = False
    # Si la media es alta y tenemos triunfo lo lanzamos
    # Todas las cartas que quedan tienen valor > 0 -> Tomamos 6 como threshold porque (11*4 + 10*4 + 4*4 + 3*4 + 2*4)/20 = 6
    if ( (mediaTotal >= 6) and triunfo[3] != 12):
        candidata = triunfo
    # Si prob > 0.5 -> No tiraremos las cartas con mayor valor
    elif (prob > 0.5):
        # Queremos que cartas bajas (valores 4, 3, 2) tengan prioridad sobre las altas. Así que vamos a ordenar nuestras cartas de menor valor a mayor.
        ordenada = sorted(misCartas, key=lambda a: a[3]) # A key le pasamos función lambda que se aplica a 3ª posición de la tupla
        for x in ordenada:
            if ( (x[2] != vira[2]) and (x[3] < 10) and (x[3] >= medias[x[2].value]) ): # Valores 0, 2, 3 y 4 que son mayores que la media de ese palo. Como están ordenadas hay preferencia (Ej: valor 4 sobre 3) (De entre las menores se escoge la mayor).
                candidata = x
                hayCandidata = True

        if (not hayCandidata): # Si no tenemos carta menor superior a media, echamos la menor
            # Vamos a tener en cuenta que si menor que no es triunfo tiene valor 10 o 11 es preferible echar la menor de las cartas ordenadas.
            # Ej: entre As no triunfo y siete triunfo es mejor echar el siete
            if (menor[3] >= 10):
                candidata = ordenada[0]
            else:
                candidata = menor    
    # Si prob < 0.5 -> Tiraremos cartas con mayor valor
    else:
        ordenada = sorted(misCartas, key=lambda a: a[3], reverse=True) # Ordenamos ahora de mayor a menor
        for x in ordenada:
            if ( not hayCandidata and (x[2] != vira[2]) and (x[3] >= medias[x[2].value]) ): # Prefiero tirar As antes que menores -> por eso not hayCandidata
                candidata = x
                hayCandidata = True

        if (not hayCandidata): # Si no tengo ninguna que supere media, echo carta con menor número de compañeras (para que si no tiene ese palo me eche de otro y yo gane) y con menor media (para que no rival no encarte).
            menorLongitud = 11 # 11 es para comparar, el máximo de cada palo es 10
            for x in misCartas:
                if ( (x[2] != vira[2]) and (len(quedan[x[2].value]) < menorLongitud) ): # Intento evitar echar triunfo
                    menorLongitud = len(quedan[x[2].value])
                    candidata = x
                    hayCandidata = True
            
            # Si todas son triunfo, echo el menor:
            if (not hayCandidata):
                candidata = triunfo
    
    print("Lanzamos: ", candidata)
    # La introduzco en jugadas y la elimino de mi baza
    jugadas.append(candidata)
    misCartas.remove(candidata)

    # Esperar a que se lance carta
    # esperar = True
    # while (esperar):
    #     consola = input("La has tirado ya? (introduce y para seguir): ")
    #     if (consola == 'y' or consola == 'Y'): esperar = False


    return candidata

# MAIN
def main():

    # global porque vamos a modificar
    global meToca       
    global puntosYo
    global puntosRival

    # Reparto 3 cartas al inicio
    repartirInicio()
    imprimeCartas()

    while (misCartas != []): # Procedimiento menos últimas 3 rondas que no hay que robar

        # Primera tirada
        print("--------PRIMERA TIRADA: ", end="")
        if meToca:
            print("Me toca")
            primera = primeraTirada()
            meToca = False  # Cedemos turno a rival
        else:
            print("Le toca al rival")
            primera = []
            while(primera == []):
                print("Introduzca carta lanzada por rival: ")
                carta = leerCarta()
                primera = existeCarta(carta)
            meToca = True       # Cedemos turno a nosotros

        # Segunda tirada
        print("--------SEGUNDA TIRADA: ", end="")
        if meToca:
            print("Me toca")
            segunda = segundaTirada(primera)     # Le paso carta rival
        else:
            print("Le toca al rival")
            esta = []
            while(esta == []):
                print("Introduzca carta lanzada por rival: ")
                carta = leerCarta()
                esta = existeCarta(carta)
            segunda = esta

        # Comprobamos ganador
        ganamos = False
        if (primera[2] == segunda[2]):  # Cartas lanzadas son del mismo palo

            if (not meToca): # Hicimos primera tirada y nuestra carta es mayor
                if (primera[3] > segunda[3]): # Mayor por valor
                    ganamos = True
                elif( (primera[3] == segunda[3]) and (primera[0] < segunda[0]) ): # Si tienen el mismo valor (=0), mayor por número (id menores son las cartas más grandes)
                    ganamos = True

            elif (meToca): # Hicimos segunda tirada y nuestra carta es mayor
                if (primera[3] < segunda[3]): # Mayor por valor
                    ganamos = True
                elif ( (primera[3] == segunda[3]) and (primera[0] > segunda[0]) ): # Mismo valor, pero nuestro id es mayor (= menor id)
                    ganamos = True

        else:   # Cartas lanzadas son distinto palo
            if (not meToca and (segunda[2] != vira[2]) ): # Hicimos primera tirada y rival no lanza triunfo
                ganamos = True
            elif (meToca and (segunda[2] == vira[2]) ): # Hicimos segunda tirada y nuestra carta es triunfo
                ganamos = True

        print("--------RESULTADOS RONDA:")
        # Sumamos puntos
        if (ganamos):
            puntosYo += primera[3] + segunda[3]
            meToca = True
            print("HEMOS GANADO LA RONDA")
        else:
            puntosRival += primera[3] + segunda[3]
            meToca = False
            print("RIVAL GANA LA RONDA")

        print("Puntos Yo: ", puntosYo)
        print("Puntos Rival: ", puntosRival)

        # Robamos carta. En las 3 últimas rondas no hay que robar -> len(quedan) = 6
        longitudQuedan = len(quedan[0]) + len(quedan[1]) + len(quedan[2]) + len(quedan[3])
        if (longitudQuedan > 3):
            esta = []
            while (esta == []):
                print("Introduzca carta robada: ")
                carta = leerCarta()
                esta = existeCarta(carta)
            misCartas.append(esta)

        elif (longitudQuedan == 3): # Último robo
            if (not ganamos):
                print("Robamos la vira porque hemos perdido")
                misCartas.append(vira)
            else:
                quedan[vira[2].value].append(vira)  # La añado a quedan, que coincide con las cartas del rival
                esta = []
                # Robo última carta
                while (esta == []):
                    print("Introduzca carta robada: ")
                    carta = leerCarta()
                    esta = existeCarta(carta)
                misCartas.append(esta)


        imprimeCartas()
    
    # Puntuaciones finales
    print("------------------PUNTUACION FINAL:")
    print("Yo:", puntosYo, "    ", "Rival: ", puntosRival)
    if (puntosYo > puntosRival):
        print("HAS GANADO!!")
    elif (puntosRival > puntosYo):
        print("BIEN JUGADO!! RIVAL GANA")
    else:
        print("UN EMPATE... LA PRÓXIMA VEZ TE VENCERÉ VAQUERO")


#Para empezar por función main
if __name__ == "__main__":
    main()
