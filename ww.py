import numpy as np
import cv2

cap = cv2.VideoCapture(0)
 
while(True):
    # Reading the video

    ret, frame = cap.read()
    cv2.imshow('ORIGINAL', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):                               # The quit line
        break
    
    # Mask to find the colour

    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)                  # The convertion 
    cv2.imshow('HSV', frame_hsv)

    l_green = np.array([40, 40, 40])
    u_green = np.array([70, 255, 255])
    green_mask = cv2.inRange(frame_hsv, l_green, u_green)               # The mask
    cv2.imshow('Green Mask', green_mask)

    # Noise Removal

    kernel = np.ones((5, 5), np.uint8)
    no_noise = cv2.erode(green_mask, kernel, iterations = 1)           # Noise Removal
    cv2. imshow('No Noise', no_noise)

    opening = cv2.morphologyEx(no_noise, cv2.MORPH_OPEN, kernel)       # Morphing to enhance it
    cv2. imshow('opening', opening)

cap.release()
cv2.destroyAllWindows()