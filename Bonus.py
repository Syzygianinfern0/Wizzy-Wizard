import time
import cv2
import imutils
import numpy as np
import pyautogui


def main():
    flag = 0
    cap = cv2.VideoCapture(0)
    
    while True:
        # Reading the video

        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        


        blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)
        hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

        sensitivity = 100
        lower_white = np.array([0,0,255-sensitivity])
        upper_white = np.array([255,sensitivity,255])

        mask = cv2.inRange(hsv, lower_white, upper_white)
        cv2.imshow('whites', mask)

        # Noise Removal

        kernel = np.ones((5, 5), np.uint8)
        no_noise = cv2.erode(mask, kernel, iterations = 1)           # Noise Removal

        perfect = cv2.morphologyEx(no_noise, cv2.MORPH_OPEN, kernel)       # Morphing to enhance
        
        contours, _ = cv2.findContours(perfect, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
 
        for contour in contours:
            # area = cv2.contourArea(contour)
    
            # if area > 20000:
            #     cv2.drawContours(frame, contour, -1, (0, 255, 0), 3)
            box = cv2.boundingRect(contour)
            x, y, w, h = box

            if w<200 or h<200:
                continue

            # cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 10, 16)

            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
            cv2.circle(frame, (x+w, y), 5, (0, 255, 0), -1)
            cv2.circle(frame, (x, y+h), 5, (0, 255, 0), -1)
            cv2.circle(frame, (x+w, y+h), 5, (0, 255, 0), -1)

            # cv2.drawContours(frame, contour, -1, (0, 255, 0), 3)
            
        cv2.imshow('ORIGINAL', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):                               # The quit line
            break

    cap.release()
    cv2.destroyAllWindows()

main()
