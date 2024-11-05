import pygame
import random
import math
from pygame import mixer
import io

# Inicializar Pygame
pygame.init()

# crear pantalla
pantalla = pygame.display.set_mode((800, 600))  # tupla es el tamanio de ancho por alto

# Titulo e icono
pygame.display.set_caption("Invasion Espacial")
icono = pygame.image.load('ufo png.png')
pygame.display.set_icon(icono)
fondo = pygame.image.load('Fondo.jpg')

# agregar musica
mixer.music.load('MusicaFondo.mp3')
mixer.music.set_volume(0.3)
mixer.music.play(-1)

# Crear Jugador y variables del jugador
img_jugador = pygame.image.load("rocket-ship.png")
jugador_x = 368  # Posicion en el eje de las x (ancho entre 2 y le restas la mitad de lo que mide la imagen
jugador_y = 500  # posicion en el eje de las y (alto menos lo que mide la imagen para posicionarlo hasta abajo)
jugador_x_cambio = 0

# Crear enemigo y variables del enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8

for e in range(cantidad_enemigos):

    img_enemigo.append(pygame.image.load("enemigo.png"))
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(50, 200))
    enemigo_x_cambio.append(0.5)
    enemigo_y_cambio.append(50)

# Crear bala y variables de la bala
balas = []
img_bala = pygame.image.load("bala.png")
bala_x = 0
bala_y = 500  # posicion en el eje de las y (alto menos lo que mide la imagen para posicionarlo hasta abajo)
bala_x_cambio = 0
bala_y_cambio = 3
bala_visible = False


def fuente_bytes(letrilla):
    # Abre el archivo .ttf en forma binaria
    with open(letrilla, 'rb') as f:
        #  Lee todos los bytes del archivo y los almacena en una variable
        ttf_bytes = f.read()
        #  Crea un objeto BytesIO a partir de los bytes del archivo ttf
        return io.BytesIO(ttf_bytes)


#  Puntaje
puntaje = 0
fuente_como_bytes = fuente_bytes("FreeSansBold.ttf")
fuente = pygame.font.Font(fuente_como_bytes, 32)  # para agregar fuente solo descargas el ttf y lo pones en el name
texto_x = 10
texto_y = 10


# Texto final del juego
fuente_final = pygame.font.Font(fuente_como_bytes, 40)


def texto_final():
    mi_fuente_final = fuente_final.render("GAME OVER", True, (255,255,255))
    pantalla.blit(mi_fuente_final, (60, 200))


# Funcion mostrar puntaje
def mostrar_puntaje(x, y):
    texto = fuente.render(f'Score: {puntaje}', True, (255, 255, 255))
    pantalla.blit(texto, (x, y))


# Funcion Jugador
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))


# Funcion enemigo
def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))


# Funcion para disparar la bala
def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16, y + 16))


# Funcion para detectar colisiones
def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_2 - x_1, 2) + math.pow(y_2 - y_1, 2))
    if distancia < 27:
        return True
    else:
        return False


#  Loop del Juego
se_ejecuta = True
while se_ejecuta:
    # RGB
    # pantalla.fill((205, 144, 228))  # cambiar color de fondo de pantalla en formato RGB en tupla

    # Imagen de fondo
    pantalla.blit(fondo, (0,0))

    # Iterar eventos
    for evento in pygame.event.get():

        # Evento cerrar programa
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        # Evento presionar teclas
        if evento.type == pygame.KEYDOWN:

            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -1
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 1
            if evento.key == pygame.K_SPACE:
                balazo = mixer.Sound('disparo.mp3')
                balazo.play()
                nueva_bala = {
                    "x": jugador_x,
                    "y": jugador_y,
                    "velocidad": -5
                }
                balas.append(nueva_bala)
        # Evento soltar flechas
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0
                jugador_y_cambio = 0
        #  Movimiento Bala
    for bala in balas:
        bala["y"] += bala["velocidad"]
        pantalla.blit(img_bala, (bala["x"] + 16, bala["y"] + 10))
        if bala["y"] < 0:
            balas.remove(bala)

    # Modificar ubicacion del jugador
    jugador_x += jugador_x_cambio

    # Mantener los limites de la pantalla Jugador
    if jugador_x <= 0:
        jugador_x = 0

    elif jugador_x >= 736:
        jugador_x = 736

    # Modificar ubicacion del enemigo
    for e in range(cantidad_enemigos):

        #  Fin del juego
        if enemigo_y[e] > 470:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break
        enemigo_x[e] += enemigo_x_cambio[e]

    # Mantener los limites de la pantalla enemigo
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 1
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -1
            enemigo_y[e] += enemigo_y_cambio[e]

        # colision
        for bala in balas:
            colision_bala_enemigo = hay_colision(enemigo_x[e], enemigo_y[e], bala["x"], bala["y"])
            if colision_bala_enemigo:
                sonido_colision = mixer.Sound("Golpe.mp3")
                sonido_colision.play()
                balas.remove(bala)
                puntaje += 1
                enemigo_x[e] = random.randint(0, 736)
                enemigo_y[e] = random.randint(20, 200)
                break

        enemigo(enemigo_x[e], enemigo_y[e], e)

    #  Movimiento de la bala
    if bala_y <= -64:
        bala_y = 500
        bala_visible = False

    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio

    jugador(jugador_x, jugador_y)

    mostrar_puntaje(texto_x, texto_y)
    # Actualizar pantalla
    pygame.display.update()
