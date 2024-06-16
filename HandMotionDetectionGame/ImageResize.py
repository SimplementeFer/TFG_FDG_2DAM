import cv2
def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # Dimensiones de la imagen a redimensionar
    dim = None
    (h, w) = image.shape[:2]

    # Parámetros de anchura y altura son none, devolvemos imagen orighinal
    if width is None and height is None:
        return image

    # Si anchura es none
    if width is None:
        # Calculamos para tener una imagen proporcional a partir de la altura

        r = height / float(h)
        dim = (int(w * r), height)

    # Si la altura es none
    else:
        # Calculamos para tener una imagen proporcional a partir de la anchura

        r = width / float(w)
        dim = (width, int(h * r))

    # Guardar imagen redimensionada en variable resultado
    resized = cv2.resize(image, dim, interpolation = inter)

    # Obtener resultado
    return resized