import os
import cv2

#Ruta y nombre del directorio
DATA_DIR = './data'

#Si el directorio no existe se crea
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

#Aquí establecemos el numero de veces que queremos crear una carpeta de imgs y el número de imgs a captar
number_of_classes = 1
dataset_size = 500

# Obtener el una lista del nombre de las carpetas

existing_dirs = [i for i in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, i))]


# Definir una función para convertir nombres de carpetas a enteros
def get_dir_number(dir_name):
    try:
        return int(dir_name)
    except ValueError:
        # Retornamos -1, indicando que el nombre de la carpeta no es un valor válido y no puede ser usado como índice.
        return -1

# Ordenar las carpetas por su nombre numérico
existing_dirs.sort(key=get_dir_number)

#Si ya hay dirs
if existing_dirs:
    #Se mira cuenta cual es el último y se le suma 1
    starting_index = get_dir_number(existing_dirs[-1]) + 1

#Si no hay dirs
else:
    #Se empieza en 0
    starting_index = 0

#Iniciamos la captura de video, si solo tienes una cam el valor es 0, si tienes varias y quieres elegir tu segunda cam pones 1, etc...
cap = cv2.VideoCapture(0)

# Iterar a través de un rango de índices, comenzando en starting_index y terminando en starting_index + number_of_classes
for j in range(starting_index, starting_index + number_of_classes):
    if not os.path.exists(os.path.join(DATA_DIR, str(j))):
        os.makedirs(os.path.join(DATA_DIR, str(j)))

    print('Creando carpeta grupo de frames {}'.format(j))

    # Esperar a que el usuario presione la barra espaciadora
    while True:
        ret, frame = cap.read()
        cv2.putText(frame, 'Espacio para captar una señal', (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.imshow('frame', frame)
        if cv2.waitKey(25) == 32:
            break

    # Capturar las imágenes
    counter = 0
    while counter < dataset_size:
        ret, frame = cap.read()
        cv2.putText(frame, 'Captando frames', (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.imshow('frame', frame)
        cv2.waitKey(25)
        cv2.imwrite(os.path.join(DATA_DIR, str(j), '{}.jpg'.format(counter)), frame)
        counter += 1

cap.release()
cv2.destroyAllWindows()
