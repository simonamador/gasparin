import cv2
from time import sleep

for i in range(2):
    cap = cv2.VideoCapture(i)
    test, frame = cap.read()
    if test:
        print("i : "+str(i)+" /// result: "+str(test))

cap = cv2.VideoCapture(1)
while True:
    success, img = cap.read()   # Gives us our frame
    cv2.imshow("Image", img)
    cv2.waitKey(1) 