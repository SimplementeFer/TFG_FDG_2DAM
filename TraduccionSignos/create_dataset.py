import os
import mediapipe as mp
import cv2
import pickle





DATA_DIR = './data'

# Arrays para coordenadas
# data para info en bruto
# labels para categorias
data = []
labels = []

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

# Entrar en cada carpeta del directorio especificado
for dir_ in os.listdir(DATA_DIR):

    dir_path = os.path.join(DATA_DIR, dir_)
    if os.path.isdir(dir_path):

        #Para ir accediendo a cada imagen de cada carpeta
        for img_path in os.listdir(dir_path):
            # ------------Array para cada img---------------
            data_aux = []

            #-------------- Para pillar solo la primera imagen
            #
            # for img_path in os.listdir(dir_path)[:1]:

            # ------------- Para hacer el proceso con todas ---------------
            # for img_path in os.listdir(dir_path):

            img = cv2.imread(os.path.join(dir_path, img_path))
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            results = hands.process(img_rgb)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:

                    # DIBUJAR IMÁGENES PARA EXPLICAR PUNTOS Y TRAZADO
                    #
                    # mp_drawing.draw_landmarks(
                    #     img_rgb,  # Imagen sobre la cual dibujar
                    #     hand_landmarks,  # Salida del modelo
                    #     mp_hands.HAND_CONNECTIONS,  # Conexiones de la mano
                    #     mp_drawing_styles.get_default_hand_landmarks_style(),  # Estilo de puntos de referencia
                    #     mp_drawing_styles.get_default_hand_connections_style())  # Estilo de conexiones

                    # COORDEANADAS DE LOS PUNTOS DE REFERENCIA PARA METER LUEGO EN UN ARRAY
                    for i in range(len(hand_landmarks.landmark)):
                        # Imprimir todas las coords
                        print(hand_landmarks.landmark[i])

                        # Coordenadas de altura y anchura X e Y
                        x = hand_landmarks.landmark[i].x
                        y = hand_landmarks.landmark[i].y
                        # guardar cada coordenada en un conjunto
                        data_aux.append(x)
                        data_aux.append(y)

                # guardar conjuntos de coords en el array de cada img
                data.append((data_aux))
                # guardar en cada categoria (nuestras carpetas de img representan categorias)
                labels.append(dir_)

# abrir el conjunto de datos 'wb' w -> escritura  b -> bytes
f = open('data.pickle', 'wb')

# El objeto a guardar es un diccionario de los datos en bruto y las categorias
pickle.dump({'data': data, 'labels': labels}, f)

f.close()

# ---------------------Mostrar resultado para explicaciones----------------------------------------
#
#             plt.figure()
#             plt.imshow(img_rgb)
#
# plt.show()
