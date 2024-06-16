from HandRegognitionModule import handDetector
from ImageResize import image_resize

import cv2

# Esto es para establecer una forma de capturar video
cap = cv2.VideoCapture(0)


# Se inicializa la clase handetector con los parámetros establecidos

detector = handDetector()

detector = handDetector(staticMode=False, maxHands=2, modelComplexity=1, detectionCon=0.9, minTrackCon=0.5)

# Bucle while para capturar frames de forma constante
while True:

    #success tendrá valor true si se captura con éxito un frame e img será el propio frame capturado
    success, img = cap.read()


    #AQUÍ SE REDIMENSIONA LA IMAGEN
    img = image_resize(img, height = 800)



    # 'draw' nos dibuja las lineas que se están empleando para detectar las manos, false para dejar de verlo
    # 'flipType' nos sirve  como espejo, invierte la imagen para facilitar las detecciones
    hands, img = detector.findHands(img, draw=True, flipType=True)


    # Si se detectan manos
    if hands:

        # Información necesaria de la primera mano detectada en cámara
        hand1 = hands[0]  # La mano en la primera posición de la lista
        lmList1 = hand1["lmList"]  # Lista con los 21 puntos de referencia de la mano 1
        bbox1 = hand1["bbox"]  # Recuadro que nos indica la mano 1
        center1 = hand1['center']  # Centra las cordenadas de hand1
        handType1 = hand1["type"]  # El type nos permite diferenciar entre mano izquierda y mano derecha

        # Contamos el numero de dedos que hay subidos
        fingers1 = detector.fingersUp(hand1)




        #Los gestos que tenemos se detectan en función de los dedos que hay o no arriba
        #1 = dedo abierto 0 = dedo cerrado, esto se invierte al mostrar la mano desde el lado contrario
        #Ejemplos más básicos:
        #todos los dedos abajo = puño cerrado
        #todos los dedos arriba = palma


        if detector.fingersUp(hands[0]) == [0, 0, 0, 0, 0] :

            print ("FIST")



        elif detector.fingersUp(hands[0]) == [1, 1, 1, 1, 1] :
            print ("PALM")


        elif detector.fingersUp(hands[0]) == [1, 0, 0, 0, 0] :
            print ("EXTEND_THUMB")


        elif detector.fingersUp(hands[0]) == [0, 1, 0, 0, 1] :
            print ("ROCK")


        elif detector.fingersUp(hands[0]) == [1, 0, 1, 1, 1] :
            print ("OK")


        else:

            print("none")

        #MOSTRAR QUE DEDOS SE ENCUENTRAN
        #print(fingers1)



        #print(f'H1 = {fingers1.count(1)}', end=" ")  # Se imprime la cuenta los dedos que hay subidos

        # Se calcula y dibuja la distancia entre 2 referencias específicas en la imagen
        # Aquí es la distancia entre índice y pulgar de esta mano
        length, info, img = detector.findDistance(lmList1[4][0:2], lmList1[8][0:2], img, color=(255, 0, 255), scale=10)

        # La lista de manos contiene 2 manos
        if len(hands) == 2:
            # Se repite el proceso anterior
            hand2 = hands[1] #2nd posición para hand2
            lmList2 = hand2["lmList"] #puntos de referencia para estra mano
            bbox2 = hand2["bbox"] #recuadro para esta mano
            center2 = hand2['center'] #centrar coordenadas para esta mano
            handType2 = hand2["type"]#identificar si es mano izq. o dch.

            # Contamos el numero de dedos que hay subidos
            fingers2 = detector.fingersUp(hand2)


            #Cuenta de los dedos que hay subidos
            #print(f'H2 = {fingers2.count(1)}', end=" ")


            #Aqui los gestos para esta mano

            if detector.fingersUp(hands[1]) == [0, 0, 0, 0, 0] :
                print ("FIST")


            elif detector.fingersUp(hands[1]) == [1, 1, 1, 1, 1] :
                print ("PALM")


            elif detector.fingersUp(hands[1]) == [1, 0, 0, 0, 0] :
                print ("EXTEND_THUMB")


            elif detector.fingersUp(hands[1]) == [0, 1, 0, 0, 1] :
                print ("ROCK")


            elif detector.fingersUp(hands[1]) == [1, 0, 1, 1, 1] :
                print ("OK")

            else :

                print("none")


            #Mostrar que dedos se detectan
            #print(fingers2)


            # Distancia entre los 2 dedos índices
            length, info, img = detector.findDistance(lmList1[8][0:2], lmList2[8][0:2], img, color=(255, 0, 0), scale=10)

            # Distancia entre índice y pulgar de mano izq.
            length, info, img = detector.findDistance(lmList2[4][0:2], lmList2[8][0:2], img, color=(255, 0, 255),scale=10)


        #Separador
        print("-")







    # Enseñamops la imagen en ventana
    cv2.imshow("Image", img)

    # Mantener ventana abierta y actualizar en milisegundos el timepo especificado
    cv2.waitKey(1)


