import subprocess
import queue



archivo = 'HandRecognition.py'
#Queue para la comunicación entre threads
data_queue = queue.Queue()

# Ruta completa al ejecutable de Python
python_executable = r'..\..\pySDK\GameLogic\Scripts\python.exe'


# Establecer una comunicación continua con el archivo indicado
try:
    with subprocess.Popen([python_executable, archivo], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1, universal_newlines=True) as read_process:
        #Leer la salida y los errores en tiempo real
        for linea in read_process.stdout:
            #Obtener la información de cada gesto que nos imprime en consola
            dato = linea.strip()

            #Ponemos a la cola cada dato
            data_queue.put(dato)


            #Aqui lo imprimimos
            print(dato)

except Exception as e:
            print(f"Error al ejecutar el proceso: {e}")



