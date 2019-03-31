import cv2
import numpy as np 

def nothing():
    pass

cap = cv2.VideoCapture(0)

panel = np.zeros([30, 700], np.uint8)
cv2.namedWindow('Slider')
cv2.createTrackbar('Hue', 'Slider', 128, 255, nothing)
cv2.createTrackbar('Sat', 'Slider', 128, 255, nothing)
cv2.createTrackbar('Val', 'Slider', 128, 255, nothing)
cv2.createTrackbar('Sen', 'Slider', 100, 255, nothing)

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)

    

    hue = cv2.getTrackbarPos('Hue', 'Slider')
    sat = cv2.getTrackbarPos('Sat', 'Slider')
    val = cv2.getTrackbarPos('Val', 'Slider')
    sen = cv2.getTrackbarPos('Sen', 'Slider')

    l_color = np.array([hue - sen, sat - sen, val - sen])
    u_color = np.array([hue + sen, sat + sen, val + sen])
    

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, l_color, u_color)
    mask_inv = cv2.bitwise_not(mask)

    coloured = cv2.bitwise_and(frame, frame, mask = mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cv2.imshow('Cam Feed', frame)
    cv2.imshow('Colored', coloured)
    cv2.imshow('Slider', panel)
    cv2.imshow('Mask', mask)

cap.release()
cv2.destroyAllWindows()