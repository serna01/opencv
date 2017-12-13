# importamos la libreria
import cv2
import numpy as np

def cartoonifyImg(frame):
    #Mascara
    gris = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    filtro_ruido = 5
    filtro_bordes = 10
    #eliminar ruidos
    filtro1 = cv2.medianBlur(gris, filtro_ruido)
    #buscar bordes
    filtro2 = cv2.Laplacian(filtro1,cv2.CV_8U, filtro_bordes)
    #aplicar filtro binario
    limit = 4
    th, filtro3 = cv2.threshold(filtro2, limit,255, cv2.THRESH_BINARY_INV)

    #Original
    width, height, dim = frame.shape

    smallWidth = width/4
    smallHeight = height/4
    smallImg = cv2.resize(frame, (smallHeight, smallWidth), cv2.INTER_LINEAR)

    reps= 7
    filtro_cartoon = 5
    for i in range(0,reps):
        smallImg = cv2.bilateralFilter(smallImg,filtro_cartoon, sigmaColor=9, sigmaSpace=7)

    big = cv2.resize(smallImg, (height, width), cv2.INTER_LINEAR)

    filtro = cv2.cvtColor(filtro3, cv2.COLOR_GRAY2BGR)

    return cv2.addWeighted(big,0.99,filtro,0.13,0.5)

def evilImg(frame):
    # Mascara
    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    filtro_ruido = 7
    # eliminar ruidos
    filtro1 = cv2.medianBlur(gris, filtro_ruido)

    #Filtro Scharr
    edges = cv2.Scharr(filtro1,cv2.CV_8U,1,0)
    print type(edges)
    print edges.shape
    edges2 = cv2.Scharr(filtro1,cv2.CV_8U,0,1)
    edges3 = cv2.add(edges, edges2)
    print type(edges)
    print edges.shape
    print edges
    filtro_evil = 6
    edges4 = cv2.threshold(edges3, filtro_evil, 255, cv2.THRESH_BINARY_INV)[1]
    edges5 = cv2.medianBlur(edges4, 7)

    # Original
    width, height, dim = frame.shape

    smallWidth = width / 4
    smallHeight = height / 4
    smallImg = cv2.resize(frame, (smallHeight, smallWidth), cv2.INTER_LINEAR)

    reps = 7
    filtro_cartoon = 5
    for i in range(0, reps):
        smallImg = cv2.bilateralFilter(smallImg, filtro_cartoon, sigmaColor=9, sigmaSpace=7)

    big = cv2.resize(smallImg, (height, width), cv2.INTER_LINEAR)

    filtro = cv2.cvtColor(edges5, cv2.COLOR_GRAY2BGR)

    return cv2.addWeighted(big, 0.99, filtro, 0.5, 0)

def PosicionCara(frame):
    img = np.copy(frame)
    #img = np.zeros((512, 512, 3), np.uint8)
    color = (0, 255, 255)
    grosor = 4
    # usar 70% de pantalla como altura de la cara
    width, height, dim = frame.shape
    sw = width
    sh = height

    caraH = sh/2 * 50/100 #radio de la elipse
    caraW = caraH * 62/100
    #dibujar "cara"de ayuda para detectar mas facil el color de piel
    cv2.ellipse(img, (sh/2, sw/2), (caraW, caraH), 0, 0, 360, color,grosor)
    ojoW = caraW * 23/100
    ojoH = caraH * 11/100
    ojoX = caraW * 40/100
    ojoY = caraH * 70/100

    #angulo y desfase ojo
    ojoA = 15 #en grados
    ojoYdesfase = 11
    #ojo derecho
    cv2.ellipse(img, (sw/2+ojoX, sh/2-ojoY), (ojoW, ojoH), 0, 180+ojoA, 360-ojoA, color,grosor)
    cv2.ellipse(img, (sw/2+ojoX, sh/2-ojoY-ojoYdesfase), (ojoW, ojoH), 0, 0+ojoA, 180-ojoA, color,grosor)
    #ojo izquierdo
    cv2.ellipse(img, (sw/2+3*ojoX, sh/2-ojoY), (ojoW, ojoH), 0, 180+ojoA, 360-ojoA, color,grosor)
    cv2.ellipse(img, (sw/2+3*ojoX, sh/2-ojoY-ojoYdesfase), (ojoW, ojoH), 0, 0+ojoA, 180-ojoA, color,grosor)



    return img

cap = cv2.VideoCapture(0)


while True:
    # Ret --> Verdadero o falso si fue capaz de leer la informacion de la camara
    # frame --> lee el siguiente frame del video
    ret, frame = cap.read()
    #cartoon = cartoonifyImg(frame)
    #evil = evilImg(frame)
    pos_cara = PosicionCara(frame)

    cv2.imshow('Original', frame)
    #cv2.imshow('Cartoonifier', cartoon)
    #cv2.imshow('Evil', evil)
    cv2.imshow('Alien', pos_cara)


    # filtro para convertir la imagen a blanco y negro
    # gris = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    # cv2.imshow('Cartoonifier',gris)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
