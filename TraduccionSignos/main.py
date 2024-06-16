import cv2
import mediapipe as mp
import pickle
import numpy as np

# Cargar el modelo
model_dict = pickle.load(open('model.p', 'rb'))
model = model_dict['model']

# Inicializar la captura de video
cap = cv2.VideoCapture(0)

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.8)

# Diccionario de etiquetas
labels_dict = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5:'F', 6:'G', 7:'H', 8:'I', 9:'J', 10:'K', 11:'L', 12:'M', 13:'N', 14:'O', 15:'P', 16:'Q', 17:'R', 18:'S', 19:'T', 20:'U', 21:'V', 22:'W', 23:'X', 24:'Y', 25:'Z'}

# Variables para contar los resultados
current_result = None
result_count = 0
threshold = 30  # Umbral para agregar la letra al array
word = []  # Lista para almacenar las letras detectadas

while True:
    data_aux = []
    ret, frame = cap.read()
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        if len(results.multi_hand_landmarks) > 1:
            cv2.putText(frame, 'Too many hands detected', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        else:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame,  # Imagen sobre la cual dibujar
                    hand_landmarks,  # Salida del modelo
                    mp_hands.HAND_CONNECTIONS,  # Conexiones de la mano
                    mp_drawing_styles.get_default_hand_landmarks_style(),  # Estilo de puntos de referencia
                    mp_drawing_styles.get_default_hand_connections_style()  # Estilo de conexiones
                )

                # Coordenadas de los puntos de referencia para meter luego en un array
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    data_aux.append(x)
                    data_aux.append(y)

            # Predicción
            prediction = model.predict([np.asarray(data_aux)])[0]
            result = labels_dict[int(prediction)]

            if current_result == result:
                result_count += 1
            else:
                current_result = result
                result_count = 1


            print(f"Resultado: {result}, Nº de detecciones"
                  f": {result_count}")

            if result_count >= threshold:
                # Añadir la letra detectada a la palabra
                word.append(current_result)
                result_count = 0  # Reiniciar el contador
                print(f"Letra añadida: {result}, Palabra: {''.join(word)}")

    # Dibujar la palabra construida en la pantalla
    cv2.putText(frame, ''.join(word), (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 5, cv2.LINE_AA)

    cv2.imshow('frame', frame)

    key = cv2.waitKey(50)
    if key == 8:  # Presionar tecla de borrar (Backspace) para borrar la última letra
        if word:
            word.pop()

    if key == 27:  # Presionar 'ESC' para salir
        break

cap.release()
cv2.destroyAllWindows()
