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
        cv2.imshow('ORIGINAL', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):                               # The quit line
            break

        blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)
        hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

        lower_book = np.array([310, 20, 40])
        upper_book = np.array([315, 36, 47])

        mask = cv2.inRange(hsv, lower_book, upper_book)
        cv2.imshow('Book', hsv)
    cap.release()
    cv2.destroyAllWindows()

main()
