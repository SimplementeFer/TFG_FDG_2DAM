import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from math import sin, cos, radians
import subprocess
import threading
import queue
import sys
# De dónde leemos los gestos
archivo = "HandRecognition.py"

# Ruta completa al ejecutable de Python
python_executable = sys.executable

# Queue para la comunicación entre threads
data_queue = queue.Queue()


# Definimos nuestros controles
keys = {pygame.K_a: False, pygame.K_d: False, pygame.K_s: False, pygame.K_SPACE: False}


# Función para leer desde el subprocesso y poner datos a la cola
def leer_movimientos():
    try:
        with subprocess.Popen([python_executable, archivo], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1, universal_newlines=True) as proceso:

            for linea in proceso.stdout:
                    dato = linea.strip()
                    data_queue.put(dato)

    except Exception as e:
        print(f"Error al ejecutar el proceso: {e}")


# Función para actuar en consecuencia a los datos que encontramos en la cola
def procesar_datos():
    while True:
        if not data_queue.empty():
            dato = data_queue.get()
            print(dato)
            # Si leemos R
            if dato == ('R'):
                # Enviar señal de movimiento hacia la derecha
                keys[pygame.K_d] = True

            #Si leemos L
            elif dato == ('L'):
                # Enviar señal de movimiento hacia la izquierda
                keys[pygame.K_a] = True

            #Si leemos PALM
            elif dato == ('PALM'):
                # Detener movimiento
                keys[pygame.K_s] = keys[pygame.K_a] = keys[pygame.K_d] = False

            elif dato == ('FIST'):
                # Enviar señal de movimiento hacia adelante
                keys[pygame.K_a] = keys[pygame.K_d] = True

            elif dato == ('ROCK'):
                # Enviar señal de movimiento hacia atrás
                keys[pygame.K_s] = True
                # Detener movimiento
                keys[pygame.K_a] = keys[pygame.K_d] = False




# Función para dibujar el cubo
def draw_cube(x, y, rotation):
    # Guardar la matriz de transformación actual
    glPushMatrix()

    # Traducir a la posición especificada (x, y)
    glTranslatef(x, y, 0)

    # Rotar el cubo alrededor del eje z por el ángulo especificado (rotation)
    glRotatef(rotation, 0, 0, 1)

    # Comenzar a dibujar el cubo usando quads (GL_QUADS) de color blanco
    glBegin(GL_QUADS)
    glColor3f(1.0, 1.0, 1.0)  # Color blanco
    glVertex3f(-0.5, -0.5, 0)
    glVertex3f(0.5, -0.5, 0)
    glVertex3f(0.5, 0.5, 0)
    glVertex3f(-0.5, 0.5, 0)
    glEnd()

    # Dibujar el rectángulo rojo que parte del centro y se extiende hacia el eje Y
    glBegin(GL_QUADS)
    glColor3f(1.0, 0.0, 0.0)  # Color rojo
    glVertex3f(-0.1, 0.0, 0)
    glVertex3f(0.1, 0.0, 0)
    glVertex3f(0.1, -1.0, 0)
    glVertex3f(-0.1, -1.0, 0)
    glEnd()

    # Restaurar la matriz de transformación anterior
    glPopMatrix()


# Función principal del juego
def game():

    # Inicializar Pygame y OpenGL
    pygame.init()
    width, height = 800, 600
    pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)

    # Establecer la posición inicial de la cámara
    gluPerspective(100, (width / height), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    # Posición inicial del jugador (en el centro de la pantalla)
    player_pos = [0, 0]
    player_speed = 0.09  # Velocidad de movimiento
    player_rotation = 0.0  # Ángulo de rotación



    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                keys[event.key] = True
                if event.key == pygame.K_SPACE:
                    shoot = True

            if event.type == pygame.KEYUP:
                keys[event.key] = False
                if event.key == pygame.K_SPACE:
                    shoot = False

        # Actualizar la posición y rotación del jugador según las teclas presionadas
        rotation_speed = 3  # Velocidad de rotación
        player_rotation += rotation_speed * (keys[pygame.K_d] - keys[pygame.K_a])

        movement_direction = keys[pygame.K_s] - keys[pygame.K_a] - keys[pygame.K_d]
        player_pos[0] += player_speed * movement_direction * -sin(radians(player_rotation))
        player_pos[1] += player_speed * movement_direction * cos(radians(player_rotation))

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_cube(player_pos[0], player_pos[1], player_rotation)


        pygame.display.flip()
        clock.tick(60)

# Iniciar los threads
thread_movimientos = threading.Thread(target=leer_movimientos)
thread_proceso = threading.Thread(target=procesar_datos)

# Configurar los threads como daemon para que se detengan al salir del programa principal
thread_movimientos.daemon = True
thread_proceso.daemon = True

# Iniciar los threads
thread_movimientos.start()
thread_proceso.start()

# Ejecutar el juego en el hilo principal
game()

# Esperar a que los threads terminen (si es necesario)
thread_movimientos.join()
thread_proceso.join()
