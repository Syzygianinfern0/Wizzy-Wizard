import time
import cv2
import imutils
import numpy as np
import pyautogui


def main():
    flag = 0
    cap = cv2.VideoCapture(0)
    screenCnt = []
    while True:
        # Reading the video

        _, frame = cap.read()
        frame = cv2.flip(frame, 1)                                  # Flip for mirror
        
        blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)          # Blurrd
        hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

        sensitivity = 120
        lower_white = np.array([0,0,255-sensitivity])
        upper_white = np.array([255,sensitivity,255])

        mask = cv2.inRange(hsv, lower_white, upper_white)           # Whites mask
        cv2.imshow('whites', mask)

        # Noise Removal

        kernel = np.ones((5, 5), np.uint8)
        no_noise = cv2.erode(mask, kernel, iterations = 1)           # Noise Removal

        perfect = cv2.morphologyEx(no_noise, cv2.MORPH_OPEN, kernel)                            # Morphing to enhance
        
        cnts = cv2.findContours(perfect.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)     # find contours in the thresholded image
        cnts = imutils.grab_contours(cnts)

        cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:2]

        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.1 * peri, True)

            if len(approx) == 4:
                print('something')
                screenCnt = approx
                cv2.drawContours(frame, [screenCnt], -1, (0, 255, 0), 2)    
                break
                

        # cv2.drawContours(frame, screenCnt, -1, (0, 255, 0), 2)    
        # cv2.drawContours(frame, approx, -1, (0, 255, 0), 2)    

        cv2.imshow('ORIGINAL', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):                               # The quit line
            break

    cap.release()
    cv2.destroyAllWindows()

main()
