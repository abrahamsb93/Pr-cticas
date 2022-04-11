import cv2
import pytesseract  # Librería para utilizar el reconocimiento óptico de caracteres.
# Falta una línea (línea 4) para buscar el programa pytesseract en el equipo, no se si es ncesario
# ya que instalas la libreria, si hace falta miras el otro vídeo y añades la línea.
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\abrah\OneDrive\Escritorio\Aprendiendo Python\curso python\Miniproyectomatriculas\Tesseract-OCR\tesseract"


placa = [] # Aquí se almacena la información de la placa detectada.
image = cv2.imread("chevrolet.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.blur(gray,(3,3))
canny = cv2.Canny(gray,150,200)
canny = cv2.dilate(canny,None,iterations=1)

cnts,_ = cv2.findContours(canny,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
#cv2.drawContours(image,cnts,-1,(0,255,0),2)

for c in cnts:
    area = cv2.contourArea(c)
    x,y,w,h = cv2.boundingRect(c) #Encontrar el rectángulo en la matrícula.
    epsilon = 0.09*cv2.arcLength(c,True)
    approx = cv2.approxPolyDP(c,epsilon,True)

    if len(approx)==4 and area > 9000:
        print("area=",area)
        #cv2.drawContours(image,[c],0,(0,255,0),2)
        aspect_ratio = float(w)/h
        if aspect_ratio>2.4:
            #cv2.drawContours(image, [c], 0, (0, 255, 0), 2)
           #cv2.drawContours(image, cnts, -1, (0, 255, 0), 2)
            placa = gray[y:y+h,x:x+w]
            text = pytesseract.image_to_string(placa, config="--psm 11")
            print("text", text)
            cv2.imshow("placa", placa)
            cv2.moveWindow("placa", 780, 10)
            cv2.rectangle(image,(x, y), (x + w, y + h), (0, 255, 0), 3)
            cv2.putText(image, text, (x - 20, y - 10), 1, 2.2, (0, 255, 0), 3)


cv2.imshow("Image",image) # Visualizar imagen
#cv2.imshow("Canny",canny) # Visualizar imagen # Esta línea se ha anulado porque muestra otra en blanco y negro
# #cv2.imshow("Image",canny)
cv2.moveWindow("Image",45,10)
cv2.waitKey(0)




