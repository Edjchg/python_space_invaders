# Referencias:
# Las imágenes que en este proyecto se utilizan son de autoría propia, elaboradas en Piskel: https://www.piskelapp.com/
# Los audios utilizados en este proyecto son obtenidos de: http://www.sonidosmp3gratis.com/

# Este archivo posee el código necesario para la correcta ejecución del juego Space Invaders.
# Como archivos adjuntos se debe tener la carpeta de imagenes y la de sonido para que el juego se ejecute correctamente

# --------------------------------------------- Uso de bibliotecas -----------------------------------------------------

# - Pygame: se utiliza para lo relacionado a la interacción entre los eventos del teclado y mouse, animaciones,
# manipulacion de imágenes y sonidos con el fin de implementar un juego agradable y fácil de usar.
# Random: con esta biblioteca se genereran numeros random de modo tal que el comportamiento de los enemigos sean de
# forma probabilística, como por ejemplo determinar cuando deben disparar hacia los jugadores.
# Time: se utiliza para hacer uso de sus funciones referentes a la toma del tiempo y frecuencias de uso.

import pygame
import random
import time

# ---------------------------------- Inicialización de algunos módulos de pygame ---------------------------------------
pygame.mixer.init()
pygame.init()

# --------------------------------------------- Variables globales -----------------------------------------------------
# Estas variables se ponen de manera global dado que muchas clases y funciones las ocupan para saber el estado actual
# del juego.

ancho_pantalla = 800
alto_pantalla = 600
marcos_por_segundo = 30  # FPS
negro = (0, 0, 0)
blanco = (255, 255, 255)
imagen_jugador_1 = pygame.image.load('imagenes/jugador1.gif')
imagen_jugador_1 = pygame.transform.scale(imagen_jugador_1, (60, 60))
imagen_jugador_2 = pygame.image.load('imagenes/jugador2.gif')
imagen_jugador_2 = pygame.transform.scale(imagen_jugador_2, (60, 60))
imagen_enemigo_1 = pygame.image.load('imagenes/enemigo1.gif')
imagen_enemigo_1 = pygame.transform.scale(imagen_enemigo_1, (40, 40))
imagen_enemigo_2 = pygame.image.load('imagenes/enemigo2.gif')
imagen_enemigo_2 = pygame.transform.scale(imagen_enemigo_2, (40, 40))
imagen_enemigo_3 = pygame.image.load('imagenes/enemigo3.gif')
imagen_enemigo_3 = pygame.transform.scale(imagen_enemigo_3, (40, 40))
lista_imagenes_enemigos = [imagen_enemigo_1, imagen_enemigo_2, imagen_enemigo_3]
ayuda = pygame.image.load('imagenes/ayuda.gif')
teclas_jugador1 = pygame.image.load('imagenes/flechas_barra.gif')
teclas_jugador2 = pygame.image.load('imagenes/adw.gif')
boton_regresar = pygame.image.load('imagenes/regresar.gif')
boton_puntuaciones = pygame.image.load('imagenes/puntuaciones.gif')
bala = pygame.image.load('imagenes/bala.gif')
bala = pygame.transform.scale(bala, (60, 60))
bala_enemigo = pygame.image.load('imagenes/bala_enemigo.gif')
bala_enemigo = pygame.transform.scale(bala_enemigo, (60, 60))
gano = pygame.image.load('imagenes/gano.gif')
perdio = pygame.image.load('imagenes/perdio.gif')
sonido_disparo = pygame.mixer.Sound('sonidos/disparo.ogg')
sonido_enemigo_eliminado = pygame.mixer.Sound('sonidos/personaje_eliminado.ogg')
sonido_perdio = pygame.mixer.Sound('sonidos/perdio.ogg')
sonido_gano = pygame.mixer.Sound('sonidos/gano.ogg')
posicion_x_jugador_1 = 700
posicion_y_jugador_1 = 550
posicion_x_jugador_2 = 0
posicion_y_jugador_2 = 550
delta_posicion_x_jugador_1 = 0
delta_posicion_x_jugador_2 = 0
delta_posicion_y_jugador_2 = 0
juego = None
matriz_enemigos = [[0] * 6] * 3
cantidad_jugadores = 1
dificultad = 1
ventana_ayuda_activada = 0
ventana_puntuaciones_activada = 0
empezar = 0
lista_de_enemigos = []
lista_de_jugadores = []
nivel = 1


# --------------------------------------------- Declaración de clases --------------------------------------------------
# - Clase Jugador: esta clase maneja la información referente a un jugador, como su posición, puntaje, vidas, cantidad
# de proyectiles disparados, tamaño del jugador, imagen correspondiente y su respectiva máscara.

class Jugador:
    def __init__(self):
        self.imagen_nave_jugador = None
        self.puntaje = 0
        self.vidas = 0
        self.posicion_x = 0
        self.posicion_y = 0
        self.frecuencia_disparo = 0
        self.mascara = None
        self.ancho_jugador = 0
        self.largo_jugador = 0
        self.proyectiles = []

    # El método definir_imagen define desde fuera de este objeto la imagen correspondiente a un jugador.
    def definir_imagen(self, imagen):
        self.imagen_nave_jugador = imagen

    # El método definir_puntaje_inicial define desde fuera de este objeto el puntaje inicial de un jugador.
    def definir_puntaje_inicial(self, puntaje):
        self.puntaje = puntaje

    # El método obtener_puntaje permite obtener el puntaje de un jugador.
    def obtener_puntaje(self):
        return self.puntaje

    # El método aumentar_puntaje aumenta el puntaje de un jugador cuando este impacta un enemigo dependiendo del nivel
    # en el que se juega.
    def aumentar_puntaje(self, puntaje):
        self.puntaje += puntaje

    # El método definir_vidas ayuda a establecer desde fuera de este objeto la cantidad de vidas al inicio de una
    # partida
    def definir_vidas(self, vidas):
        self.vidas = vidas

    # El método disminuir_vidas permite disminuir en 1 la cantidad de vidas si algun enemigo consigue impactar a un
    # jugador.
    def disminuir_vidas(self):
        self.vidas -= 1

    # El método obtener_vidas permite conocer la cantidad de vidas que al jugador le restan durante una partida.
    def obtener_vidas(self):
        return self.vidas

    # El método definir_posicion define y actualiza en el canvas de pygame la nueva posición del jugador.
    def definir_posicion(self, posicion_x, posicion_y):
        self.posicion_x = posicion_x
        self.posicion_y = posicion_y
        juego.blit(self.imagen_nave_jugador, (posicion_x, posicion_y))

    # El método definir_mascara establece la máscara que un personaje debe tener para poder manejar las colisiones.
    def definir_mascara(self):
        self.mascara = pygame.mask.from_surface(self.imagen_nave_jugador)

    # El método obtener_mascara permite obtener desde fuera cual es la máscara de un jugador en particular.
    def obtener_mascara(self):
        return self.mascara

    # El método obtener_ancho_jugador retorna el valor del ancho de la imagen del jugador.
    def obtener_ancho_jugador(self):
        return self.imagen_nave_jugador.get_width()

    # El método obtener_largo_jugador retorna el valor del largo de la imagen del jugador.
    def obtener_largo_jugador(self):
        return self.imagen_nave_jugador.get_height()

    # El método disparar permite generar un proyectil y su posición inicial y de esta forma ponerlo en el canvas de
    # pygame ademas de almacenarlo en la lista de proyectiles disparados.
    def disparar(self):
        disparo = Proyectil()
        disparo.definir_imagen(bala)
        disparo.definir_posicion_inicial(self.posicion_x, self.posicion_y)
        disparo.definir_mascara()
        self.proyectiles.append(disparo)

    # El método redibujar_proyectiles permite volver a dibujar la nueva posición del proyectil.
    def redibujar_proyectiles(self):
        for proyectil in self.proyectiles:
            proyectil.definir_posicion(proyectil.posicion_x, proyectil.posicion_y - proyectil.velocidad)
            if not proyectil.proyectil_dentro_pantalla():
                if len(self.proyectiles) > 0:
                    self.proyectiles.remove(proyectil)
        self.revisar_colision()

    # el método revisar_colision permite observar si el proyectil lanzado o alguno de los proyectiles lanzados han
    # alcanzado a algun enemigo y de esta forma eliminarlo de la lista de enemigos.
    def revisar_colision(self):
        for proyectil in self.proyectiles:
            for enemigo in lista_de_enemigos:
                if proyectil.choque(enemigo, 1):
                    lista_de_enemigos.remove(enemigo)
                    # pygame.mixer.Sound.play(sonido_enemigo_eliminado)
                    if len(self.proyectiles) > 0:
                        self.proyectiles.remove(proyectil)
                    self.aumentar_puntaje(nivel + 1)


# - Clase Enemigo: esta clase posee la información necesaria de un enemigo en particular, como la posición dentro del
# canvas de pygame, la imagen, las dimensiones de la imagen, máscara, la lista de los proyectiles que se han lanzado,
# la velocidad con la que el enemigo se va a desplazar dentro del canvas.

class Enemigo:
    def __init__(self):
        self.imagen = None
        self.vida = 1
        self.posicion_x = 0
        self.posicion_y = 0
        self.frecuencia_disparo = 300
        self.contador_secuencia_disparo = 0
        self.velocidad = 0
        self.ancho_enemigo = 0
        self.largo_enemigo = 0
        self.mascara = None
        self.proyectiles = []

    # El método definir_imagen permite establecer la imagen que le corresponde a un determinado enemigo.
    def definir_imagen(self, imagen):
        self.imagen = imagen

    # El método disminuir_vida permite quitar la vida que posee cada enemigo cuando es impactado por un proyectil,
    # para de esta forma eliminarlo de la lista de enemigos.
    def disminuir_vida(self):
        self.vida -= 1

    # El método definir_posicion establece la posición del enemigo durante un partida.
    def definir_posicion(self, posicion_x, posicion_y):
        self.posicion_x = posicion_x
        self.posicion_y = posicion_y
        juego.blit(self.imagen, (posicion_x, posicion_y))

    # El método posicion_inicial establece la posición aleatoria-inicial del enemigo.
    def posicion_inicial(self, x, y):
        self.posicion_x = x
        self.posicion_y = y

    # El método definir_velocidad establece la velcidad con la que el enemigo se va a mover en el canvas de pygame.
    def definir_velocidad(self, velocidad):
        self.velocidad = velocidad

    # El método obtener_ancho_enemigo retorna el ancho de la imagen que corresponde a un enemigo determinado.
    def obtener_ancho_enemigo(self):
        return self.imagen.get_width()

    # El método obtener_largo_enemigo retorna el largo de la imagen que corresponde a un enemigo determinado.
    def obtener_largo_enemigo(self):
        return self.imagen.get_height()

    # El método definir_mascara establece la máscara de pygame al enemigo para poder manejar las calisiones.
    def definir_mascara(self):
        self.mascara = pygame.mask.from_surface(self.imagen)

    # El método disparar permite hacer que un enemigo genere un proyectil y este se vea reflejado en el canvas de
    # pygame.
    def disparar(self):
        if self.contador_secuencia_disparo == 0:
            disparo = Proyectil()
            disparo.definir_imagen(bala_enemigo)
            disparo.definir_posicion_inicial(self.posicion_x - 10, self.posicion_y)
            disparo.definir_mascara()
            self.proyectiles.append(disparo)
            self.contador_secuencia_disparo = 1

    # El método redibujar_proyectiles permite establecer la nueva posición de un determinado proyectil.
    def redibujar_proyectiles(self):
        self.manejo_frecuencia_disparo()
        for proyectil in self.proyectiles:
            proyectil.definir_posicion(proyectil.posicion_x, proyectil.posicion_y + proyectil.velocidad)
            if not proyectil.proyectil_dentro_pantalla():
                if len(self.proyectiles) > 0:
                    self.proyectiles.remove(proyectil)
        self.revisar_colision()

    # El método revisar_colision revisa si alguno de los proyectiles lanzados por un enemigo impacto con un jugador
    # para disminuirle la vida.
    def revisar_colision(self):
        for proyectil in self.proyectiles:
            for jugador in lista_de_jugadores:
                if proyectil.choque(jugador, 0):
                    jugador.disminuir_vidas()
                    pygame.mixer.Sound.play(sonido_enemigo_eliminado)
                    if len(self.proyectiles) > 0:
                        self.proyectiles.remove(proyectil)

    # El método manejo_frecuencia_disparo ayuda a contener la frecuencia con la que los enemigos disparan.
    def manejo_frecuencia_disparo(self):
        if self.contador_secuencia_disparo >= self.frecuencia_disparo:
            self.contador_secuencia_disparo = 0
        elif self.contador_secuencia_disparo > 0:
            self.contador_secuencia_disparo += 1


# Clase Proyectil: esta clase maneja la información relacionada con un proyectil, como su posicion, la imagen, la
# velocidad con la que se mueve, la máscara y si hubo una colision.
class Proyectil:
    def __init__(self):
        self.posicion_x = 0
        self.posicion_y = 0
        self.imagen = None
        self.velocidad = 2
        self.mascara = None

    # El método definir_imagen permite definir establecer la imagen correspondiente a un proyectil.
    def definir_imagen(self, imagen):
        self.imagen = imagen

    # El método definir_posicion_inicial permite establcer la posicion inicial del proyectil que va depender de la
    # posición actual del enemigo o del jugador.
    def definir_posicion_inicial(self, x, y):
        self.posicion_x = x
        self.posicion_y = y

    # El método definir_posicion permite actualizar la posicón de un proyectil en el canvas de pygame.
    def definir_posicion(self, x, y):
        self.posicion_x = x
        self.posicion_y = y
        juego.blit(self.imagen, (x, y))

    # El método definir_mascara permite establecer la máscara correspondiente a un proyectil con el cual se puede
    # manejar las colisiones.
    def definir_mascara(self):
        self.mascara = pygame.mask.from_surface(self.imagen)

    # El método proyectil_dentro_pantalla evalúa si un determinado proyectil se encuentra dentro de la pantalla, de lo
    # contrario entonces este proyectil se elimina de la lista de proyectiles disparados.
    def proyectil_dentro_pantalla(self):
        if 0 <= self.posicion_y <= alto_pantalla:
            return True
        else:
            return False

    # El método choque evlúa si dos objetos están traslapdos lo que indicaría que han colisionado.
    def choque(self, objeto_cualquiera, origen):
        return revisar_colision(self, objeto_cualquiera, origen)


# -------------------------------------- Métodos de revisión de condiciones --------------------------------------------
# La función revisar_colision usa la función de pygame "overlap" para determinar si dos objetos han colisionado, basado
# en la distancia entre los dos objetos.
def revisar_colision(objeto_cualquiera1, objeto_cualquiera2, origen):
    if origen == 1:  # Si dispara el jugador
        diferencia_distancia_entre_objetos_x = objeto_cualquiera1.posicion_x - objeto_cualquiera2.posicion_x + 20
        diferencia_distancia_entre_objetos_Y = objeto_cualquiera1.posicion_y - objeto_cualquiera2.posicion_y
        return objeto_cualquiera1.mascara.overlap(objeto_cualquiera2.mascara, (
            diferencia_distancia_entre_objetos_x, diferencia_distancia_entre_objetos_Y)) is not None
    else:
        diferencia_distancia_entre_objetos_x = objeto_cualquiera1.posicion_x - objeto_cualquiera2.posicion_x
        diferencia_distancia_entre_objetos_Y = objeto_cualquiera1.posicion_y - objeto_cualquiera2.posicion_y
        return objeto_cualquiera1.mascara.overlap(objeto_cualquiera2.mascara, (
            diferencia_distancia_entre_objetos_x, diferencia_distancia_entre_objetos_Y)) is not None


# La función revisar_bordes determina si el jugador tomo un valor más grande o mas pequeño que el tamaño de la ventana.
def revisar_bordes():
    if (posicion_x_jugador_1 + delta_posicion_x_jugador_1) > ancho_pantalla - 100 or (
            posicion_x_jugador_1 + delta_posicion_x_jugador_1) < 0 or (
            posicion_x_jugador_2 + delta_posicion_x_jugador_2) > ancho_pantalla - 100 or (
            posicion_x_jugador_2 + delta_posicion_x_jugador_2) < 0:
        return True
    else:
        return False


# La función leer_puntuacion lee un .txt, el cual contiene la última puntuación más alta.
def leer_puntuacion():
    archivo = open("puntuaciones/puntuacion_alta.txt", "r")
    linea = archivo.readlines()
    largo = len(linea)
    archivo.close()
    if largo != 0:
        return linea[0]
    else:
        return "0"


# La función escribir_puntuacion escribe la ultima puntuación más alta en el archivo .txt
def escribir_puntuacion(puntuacion):
    archivo = open("puntuaciones/puntuacion_alta.txt", "w")
    archivo.write(str(puntuacion))
    archivo.close()


# La función objetos_texto retorna un objeto texto renderizado y listo para ser mostrado en el canvas de pygame,
# además calcula el margen de ese texto.
def objetos_texto(texto, fuente):
    superficie = fuente.render(texto, True, blanco)
    return superficie, superficie.get_rect()


# La función mostrar_mensaje es una función que despliega las pantallas correspondientes al gane o pierde del jugador.
def mostrar_mensaje(mensaje, resultado):
    juego.fill(negro)
    if resultado == 1:
        ganar = Jugador()
        ganar.definir_imagen(gano)
        ganar.definir_posicion(ancho_pantalla / 2 - 130, 100)
    else:
        perder = Jugador()
        perder.definir_imagen(perdio)
        perder.definir_posicion(ancho_pantalla / 2 - 130, 100)
    fuente_mensaje = pygame.font.SysFont("comicsans", 70)
    superficie_texto, rectangulo_texto = objetos_texto(mensaje, fuente_mensaje)
    rectangulo_texto.center = (ancho_pantalla / 2, 50)
    juego.blit(superficie_texto, rectangulo_texto)

    pygame.display.update()
    time.sleep(5)


# La función juego_terminado_perdido ejecuta el sonido preestablecido para el pierde de un jugador, y muestra el
# mensaje de que el jugador ha perdido.
def juego_terminado_perdido():
    pygame.mixer.Sound.play(sonido_perdio)
    mostrar_mensaje("Perdió", 0)


# La función juego_terminado_ganado ejecuta el sonido preestablecido para el gane de un jugador, y muestra el
# mensaje de que el jugador ha ganado.
def juego_terminado_ganado():
    pygame.mixer.Sound.play(sonido_gano)
    puntuacion_anterior = leer_puntuacion()
    puntuacion_anterior = int(puntuacion_anterior)
    if cantidad_jugadores == 1:
        if lista_de_jugadores[0].obtener_puntaje() > puntuacion_anterior:
            escribir_puntuacion(lista_de_jugadores[0].obtener_puntaje())
        else:
            pass
    elif cantidad_jugadores == 2:
        if lista_de_jugadores[0].obtener_puntaje() + lista_de_jugadores[1].obtener_puntaje() > puntuacion_anterior:
            escribir_puntuacion(lista_de_jugadores[0].obtener_puntaje() + lista_de_jugadores[1].obtener_puntaje())
        else:
            pass
    mostrar_mensaje("Ganó", 1)


# ------------------------------------- Métodos correspondientes a la interfaz -----------------------------------------
# La función generar_enemigos genera enemigos aleatoriamente, en cuanto a su imagen y en cuanto a la posición en la que
# se generan en el canvas de pygame.
def generar_enemigos():
    global nivel
    indice = 0
    while indice < nivel * 10 + 10:
        enemigo = Enemigo()
        enemigo.definir_imagen(lista_imagenes_enemigos[random.randrange(0, 3)])
        enemigo.definir_velocidad(1)
        enemigo.definir_mascara()
        enemigo.posicion_inicial(random.randrange(50, ancho_pantalla - 100), random.randrange(-1500, -100))
        lista_de_enemigos.append(enemigo)
        indice += 1


# La función redibujar_proyectiles_enemigos toma la lista de enemgios y por cada enemigo redibuja sus proyectiles
# lanzados.
def redibujar_proyectiles_enemigos():
    for enemigo in lista_de_enemigos:
        enemigo.redibujar_proyectiles()


# La función redibujar_enemigos toma la lista de enemigos y actualiza la posición de cada enemigo y además determina si
# alguno de estos ha superado la linea en la que se encuentran los jugadores, para quitarles una vida a los jugadores.
def redibujar_enemigos(jugadores):
    for enemigo in lista_de_enemigos[:]:
        enemigo.definir_posicion(enemigo.posicion_x, enemigo.posicion_y + enemigo.velocidad)

        if enemigo.posicion_y + enemigo.obtener_largo_enemigo() > alto_pantalla:
            lista_de_enemigos.remove(enemigo)
            for jugador in range(len(jugadores)):
                if jugadores[jugador].obtener_vidas() > 0:
                    jugadores[jugador].disminuir_vidas()
    redibujar_proyectiles_enemigos()


# La función ventana_puntuacion_mas_alta permite visualizar la ultima puntuación más alta alcanzada por el jugador, con
# la posibilidad de devolverse al menú principal.
def ventana_puntuacion_mas_alta():
    bandera_ventana_puntuaciones = True
    puntuacion_alta = leer_puntuacion()
    while bandera_ventana_puntuaciones:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
        juego.fill(negro)
        fuente_mensaje = pygame.font.SysFont("comicsans", 40)
        superficie_texto, rectangulo_texto = objetos_texto("Última puntuación más alta:", fuente_mensaje)
        rectangulo_texto.center = (ancho_pantalla / 2, alto_pantalla / 2 - 100)
        juego.blit(superficie_texto, rectangulo_texto)

        fuente_mensaje1 = pygame.font.SysFont("comicsans", 70)
        superficie_texto1, rectangulo_texto1 = objetos_texto(puntuacion_alta, fuente_mensaje1)
        rectangulo_texto1.center = (ancho_pantalla / 2, alto_pantalla / 2)
        juego.blit(superficie_texto1, rectangulo_texto1)

        regresar = Jugador()
        regresar.definir_imagen(boton_regresar)
        regresar.definir_posicion(ancho_pantalla / 2 - 20, alto_pantalla / 2 + 200)
        pygame.display.update()
        reloj.tick(15)

        # print(pygame.mouse.get_pos())
        if 379 <= pygame.mouse.get_pos()[0] <= 404 and 499 <= pygame.mouse.get_pos()[1] <= 531 and \
                pygame.mouse.get_pressed()[0] == 1:
            print("Regresar")
            break


# La función ventana_ayuda muestra las instrucciones de uso del juego en el cual se puede ver cuales son las teclas que
# se deben utilizar y como se puede configurara los diferentes modos que posee el juego. Además, esta la posibilidad de
# devolverse al menú principal.
def ventana_ayuda():
    bnadera_ventana_ayuda = True
    while bnadera_ventana_ayuda:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
        juego.fill(negro)
        fuente_mensaje = pygame.font.SysFont("comicsans", 70)
        superficie_texto, rectangulo_texto = objetos_texto("Instrucciones de juego", fuente_mensaje)
        rectangulo_texto.center = (ancho_pantalla / 2, 40)
        juego.blit(superficie_texto, rectangulo_texto)

        fuente_mensaje1 = pygame.font.SysFont("comicsans", 20)
        superficie_texto1, rectangulo_texto1 = objetos_texto("Se puede elegir modo individual o multijugador con dos "
                                                             "jugadores.", fuente_mensaje1)
        rectangulo_texto1.center = (ancho_pantalla / 2, 100)
        juego.blit(superficie_texto1, rectangulo_texto1)

        superficie_texto2, rectangulo_texto2 = objetos_texto(
            "El jugador 1 podrá moverse con las flechas y disparar con la barra espaciadora:", fuente_mensaje1)
        rectangulo_texto2.center = (ancho_pantalla / 2, 120)
        juego.blit(superficie_texto2, rectangulo_texto2)

        teclas_de_jugador1 = Jugador()
        teclas_de_jugador1.definir_imagen(teclas_jugador1)
        teclas_de_jugador1.definir_posicion(ancho_pantalla / 2 - 100, 120)

        superficie_texto3, rectangulo_texto3 = objetos_texto(
            "El jugador 2 podrá moverse con las teclas A y D, y disparar con la tecla W:", fuente_mensaje1)
        rectangulo_texto3.center = (ancho_pantalla / 2, 300)
        juego.blit(superficie_texto3, rectangulo_texto3)

        teclas_de_jugador2 = Jugador()
        teclas_de_jugador2.definir_imagen(teclas_jugador2)
        teclas_de_jugador2.definir_posicion(ancho_pantalla / 2 - 100, 300)

        superficie_texto4, rectangulo_texto4 = objetos_texto(
            "El nivel de dificultad puede ser elegido con los aliens enemigos, el de morado es nivel 1, "
            "el verde es nivel 2 y el rojo nivel 3.",
            fuente_mensaje1)
        rectangulo_texto4.center = (ancho_pantalla / 2, 500)
        juego.blit(superficie_texto4, rectangulo_texto4)

        regresar = Jugador()
        regresar.definir_imagen(boton_regresar)
        regresar.definir_posicion(ancho_pantalla / 2, 550)

        pygame.display.update()
        reloj.tick(15)

        # print(pygame.mouse.get_pos())
        if 400 <= pygame.mouse.get_pos()[0] <= 434 and 551 <= pygame.mouse.get_pos()[1] <= 579 and \
                pygame.mouse.get_pressed()[0] == 1:
            print("Regresar")
            break


# La función menu_principal muestra todas las opciones que en el menú se pueden configurar, como la cantidad de
# jugadores, el nivel de dificultad de la partida y algunas ayudas e información.
def menu_principal():
    global cantidad_jugadores, ventana_ayuda_activada, ventana_puntuaciones_activada, nivel, lista_de_enemigos, \
        posicion_x_jugador_1, posicion_x_jugador_2, empezar
    lista_de_enemigos = []
    posicion_x_jugador_1 = 700
    posicion_x_jugador_2 = 0
    bandera_menu = True
    while bandera_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        juego.fill(negro)
        fuente_mensaje = pygame.font.SysFont("comicsans", 70)
        superficie_texto, rectangulo_texto = objetos_texto("Menú Principal", fuente_mensaje)
        rectangulo_texto.center = (ancho_pantalla / 2, 40)
        juego.blit(superficie_texto, rectangulo_texto)

        superficie_texto2, rectangulo_texto2 = objetos_texto("Un jugador", fuente_mensaje)
        rectangulo_texto2.center = (ancho_pantalla / 2, 150)
        juego.blit(superficie_texto2, rectangulo_texto2)

        superficie_texto2, rectangulo_texto2 = objetos_texto("Dos jugadores", fuente_mensaje)
        rectangulo_texto2.center = (ancho_pantalla / 2, 260)
        juego.blit(superficie_texto2, rectangulo_texto2)

        superficie_texto3, rectangulo_texto3 = objetos_texto("Dificultad", fuente_mensaje)
        rectangulo_texto3.center = (ancho_pantalla / 2, 370)
        juego.blit(superficie_texto3, rectangulo_texto3)

        superficie_texto4, rectangulo_texto4 = objetos_texto("Empezar", fuente_mensaje)
        rectangulo_texto4.center = (ancho_pantalla / 2, 550)
        juego.blit(superficie_texto4, rectangulo_texto4)

        jugador1_menu = Jugador()
        jugador1_menu.definir_imagen(imagen_jugador_1)
        jugador1_menu.definir_posicion(ancho_pantalla / 2 - 190, 120)

        jugador1_1_menu = Jugador()
        jugador1_1_menu.definir_imagen(imagen_jugador_1)
        jugador1_1_menu.definir_posicion(ancho_pantalla / 2 - 270, 230)

        jugador2_menu = Jugador()
        jugador2_menu.definir_imagen(imagen_jugador_2)
        jugador2_menu.definir_posicion(ancho_pantalla / 2 - 230, 230)

        enemigo1_menu = Enemigo()
        enemigo1_menu.definir_imagen(imagen_enemigo_1)
        enemigo1_menu.definir_posicion(ancho_pantalla / 2 - 50, 400)

        enemigo2_menu = Enemigo()
        enemigo2_menu.definir_imagen(imagen_enemigo_2)
        enemigo2_menu.definir_posicion(ancho_pantalla / 2 - 200, 400)

        enemigo3_menu = Enemigo()
        enemigo3_menu.definir_imagen(imagen_enemigo_3)
        enemigo3_menu.definir_posicion(ancho_pantalla / 2 + 100, 400)

        ayuda_menu = Jugador()
        ayuda_menu.definir_imagen(ayuda)
        ayuda_menu.definir_posicion(ancho_pantalla - 40, 10)

        puntuaciones = Jugador()
        puntuaciones.definir_imagen(boton_puntuaciones)
        puntuaciones.definir_posicion(ancho_pantalla - 60, 40)

        pygame.display.update()
        reloj.tick(15)
        # print(pygame.mouse.get_pos())
        if 197 <= pygame.mouse.get_pos()[0] <= 539 and 121 <= pygame.mouse.get_pos()[1] <= 170 and \
                pygame.mouse.get_pressed()[0] == 1:
            print("1 jugador")
            cantidad_jugadores = 1
        elif 100 <= pygame.mouse.get_pos()[0] <= 576 and 229 <= pygame.mouse.get_pos()[1] <= 283 and \
                pygame.mouse.get_pressed()[0] == 1:
            print("2 jugadores")
            cantidad_jugadores = 2
        elif 207 <= pygame.mouse.get_pos()[0] <= 240 and 401 <= pygame.mouse.get_pos()[1] <= 430 and \
                pygame.mouse.get_pressed()[0] == 1:
            nivel = 1
            print("Nivel 1")
        elif 332 <= pygame.mouse.get_pos()[0] <= 396 and 395 <= pygame.mouse.get_pos()[1] <= 430 and \
                pygame.mouse.get_pressed()[0] == 1:
            nivel = 2
            print("Nivel 2")
        elif 496 <= pygame.mouse.get_pos()[0] <= 541 and 399 <= pygame.mouse.get_pos()[1] <= 432 and \
                pygame.mouse.get_pressed()[0] == 1:
            print("Nivel 3")
            nivel = 3
        elif 755 <= pygame.mouse.get_pos()[0] <= 798 and 3 <= pygame.mouse.get_pos()[1] <= 47 and \
                pygame.mouse.get_pressed()[0] == 1:
            ventana_ayuda_activada = 1
            print("Ayuda")
            break

        elif 292 <= pygame.mouse.get_pos()[0] <= 513 and 522 <= pygame.mouse.get_pos()[1] <= 567 and \
                pygame.mouse.get_pressed()[0] == 1:
            print("Empezar")
            empezar = 1
            break
        elif 745 <= pygame.mouse.get_pos()[0] <= 797 and 49 <= pygame.mouse.get_pos()[1] <= 94 and \
                pygame.mouse.get_pressed()[0] == 1:
            print("Puntuaciones")
            ventana_puntuaciones_activada = 1
            break
    generar_enemigos()
    if ventana_ayuda_activada == 1:
        ventana_ayuda()
        ventana_ayuda_activada = 0
    elif ventana_puntuaciones_activada == 1:
        ventana_puntuacion_mas_alta()
        ventana_puntuaciones_activada = 0
    else:
        if cantidad_jugadores == 1 and empezar == 1:
            juego_un_jugador()
            empezar = 0
        elif cantidad_jugadores == 2 and empezar == 1:
            juego_dos_jugadores()
            empezar = 0
        else:
            menu_principal()
    menu_principal()


# La función juego_dos_jugadores muestra la pantalla para que dos jugadores puedan jugar en modo colaborativo al mismo
# tiempo.
def juego_dos_jugadores():
    global posicion_x_jugador_1, posicion_x_jugador_2, delta_posicion_x_jugador_1, delta_posicion_x_jugador_2, juego, \
        ancho_pantalla, lista_de_jugadores, lista_de_enemigos

    jugador1 = Jugador()
    jugador1.definir_imagen(imagen_jugador_1)
    jugador1.definir_vidas(5)
    jugador1.definir_mascara()

    jugador2 = Jugador()
    jugador2.definir_imagen(imagen_jugador_2)
    jugador2.definir_vidas(5)
    jugador2.definir_mascara()

    lista_de_jugadores = [jugador1, jugador2]

    # El ciclo principal del juego:
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    delta_posicion_x_jugador_1 = -10
                if evento.key == pygame.K_RIGHT:
                    delta_posicion_x_jugador_1 = 10
                if evento.key == pygame.K_SPACE:
                    jugador1.disparar()
                    pygame.mixer.Sound.play(sonido_disparo)
                if evento.key == pygame.K_a:
                    delta_posicion_x_jugador_2 = -10
                if evento.key == pygame.K_d:
                    delta_posicion_x_jugador_2 = 10
                if evento.key == pygame.K_w:
                    jugador2.disparar()
                    pygame.mixer.Sound.play(sonido_disparo)

            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT or evento.key == pygame.K_UP or \
                        evento.key == pygame.K_DOWN or evento.key == pygame.K_a or evento.key == pygame.K_s or \
                        evento.key == pygame.K_d or evento.key == pygame.K_w:
                    delta_posicion_x_jugador_1 = 0
                    delta_posicion_x_jugador_2 = 0
        juego.fill(negro)
        if random.randrange(0, 2*30) == 1 and len(lista_de_enemigos) > 0:
            enemigo = random.choice(lista_de_enemigos)
            enemigo.disparar()
        fuente_etiquetas = pygame.font.SysFont("comicsans", 30)
        etiqueta_vidas1 = fuente_etiquetas.render(f"Vidas del jugador_1: {jugador1.obtener_vidas()}", 1, blanco)
        etiqueta_vidas2 = fuente_etiquetas.render(f"Vidas del jugador_2: {jugador2.obtener_vidas()}", 1, blanco)
        etiqueta_puntaje = fuente_etiquetas.render(
            f"Puntaje del equipo: {jugador1.obtener_puntaje() + jugador2.obtener_puntaje()}", 1, blanco)
        etiqueta_enemigos = fuente_etiquetas.render(f"Cantidad de enemigos: {len(lista_de_enemigos)}", 1, blanco)
        juego.blit(etiqueta_vidas1, (10, 10))
        juego.blit(etiqueta_vidas2, (10, 40))
        juego.blit(etiqueta_enemigos, (10, 70))
        juego.blit(etiqueta_puntaje, (10, 100))

        redibujar_enemigos([jugador1, jugador2])
        jugador1.redibujar_proyectiles()
        jugador2.redibujar_proyectiles()

        if revisar_bordes():
            pass
        else:
            posicion_x_jugador_1 += delta_posicion_x_jugador_1
            posicion_x_jugador_2 += delta_posicion_x_jugador_2

        if jugador1.obtener_vidas() <= 0 and jugador2.obtener_vidas() <= 0:
            juego_terminado_perdido()
            menu_principal()
        else:
            jugador1.definir_posicion(posicion_x_jugador_1, posicion_y_jugador_1)
            jugador2.definir_posicion(posicion_x_jugador_2, posicion_y_jugador_2)

        if len(lista_de_enemigos) == 0 and (jugador2.obtener_vidas() > 0 or jugador1.obtener_vidas() > 0):
            juego_terminado_ganado()
            menu_principal()
        else:
            redibujar_enemigos([jugador1, jugador2])
        pygame.display.update()
        reloj.tick(marcos_por_segundo)


# La función juego_un_jugador muestra la pantalla en la cual unicamente un jugador puede jugar en la misma partida.
def juego_un_jugador():
    global posicion_x_jugador_1, delta_posicion_x_jugador_1, juego, ancho_pantalla, lista_de_jugadores

    jugador1 = Jugador()
    jugador1.definir_imagen(imagen_jugador_1)
    jugador1.definir_vidas(5)
    jugador1.definir_mascara()

    lista_de_jugadores = [jugador1]
    # El ciclo principal del juego:
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    delta_posicion_x_jugador_1 = -10
                if evento.key == pygame.K_RIGHT:
                    delta_posicion_x_jugador_1 = 10
                if evento.key == pygame.K_SPACE:
                    jugador1.disparar()
                    pygame.mixer.Sound.play(sonido_disparo)

            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                    delta_posicion_x_jugador_1 = 0
        juego.fill(negro)
        if random.randrange(0, 2*30) == 1 and len(lista_de_enemigos) > 0:
            enemigo = random.choice(lista_de_enemigos)
            enemigo.disparar()
        fuente_etiquetas = pygame.font.SysFont("comicsans", 30)
        etiqueta_vidas = fuente_etiquetas.render(f"Vidas del jugador_1: {jugador1.obtener_vidas()}", True, blanco)
        etiqueta_puntaje = fuente_etiquetas.render(f"Puntaje: {jugador1.obtener_puntaje()}", True, blanco)
        etiqueta_enemigos = fuente_etiquetas.render(f"Cantidad de enemigos: {len(lista_de_enemigos)}", True, blanco)
        juego.blit(etiqueta_vidas, (10, 10))
        juego.blit(etiqueta_puntaje, (10, 40))
        juego.blit(etiqueta_enemigos, (10, 70))

        redibujar_enemigos([jugador1])
        jugador1.redibujar_proyectiles()

        if revisar_bordes():
            pass
        else:
            posicion_x_jugador_1 += delta_posicion_x_jugador_1

        if jugador1.obtener_vidas() == 0:
            juego_terminado_perdido()
            menu_principal()
        else:
            jugador1.definir_posicion(posicion_x_jugador_1, posicion_y_jugador_1)

        if len(lista_de_enemigos) == 0:
            juego_terminado_ganado()
            menu_principal()
        else:
            redibujar_enemigos([jugador1])
        pygame.display.update()
        reloj.tick(marcos_por_segundo)


# ----------------------------------- Algunos parametros iniciales y generales -----------------------------------------
juego = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
pygame.display.set_caption('Mi Space Invaders :)')
reloj = pygame.time.Clock()
menu_principal()
pygame.quit()
quit()