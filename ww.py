# My friend has bought a new laptop which has a touchscreen. He brags
# about it telling that he can draw/write in it easily unlike using a mouse to
# draw. Being a tech enthusiast I decide to draw in My laptop without even
# touching anything. So here's what I have made :Have a colour marker in
# My finger. So I Open any application like MS Paint and draw in it just by moving
# My finger in front of the camera.

import time

import cv2
import imutils
import numpy as np
import pyautogui
import pynput


def main():
    flag = 0
    flag1 = 0                                                               # Start painting
    cap = cv2.VideoCapture(0)
    
    while(True):
        try:

            # Reading the video

            _, frame = cap.read()
            frame = cv2.flip(frame, 1)
            cv2.imshow('ORIGINAL', frame)
            if cv2.waitKey(1) & 0xFF == 27:                               # The quit line
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):                               # The quit line
                flag1 = not flag1
            
            # Mask to find the colour

            frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)                  # The convertion 
            #cv2.imshow('HSV', frame_hsv)

            l_green = np.array([40, 40, 40])
            u_green = np.array([70, 255, 255])
            green_mask = cv2.inRange(frame_hsv, l_green, u_green)               # The mask
            #cv2.imshow('Green Mask', green_mask)

            # Noise Removal

            kernel = np.ones((5, 5), np.uint8)
            no_noise = cv2.erode(green_mask, kernel, iterations = 1)           # Noise Removal
            #cv2. imshow('No Noise', no_noise)

            perfect = cv2.morphologyEx(no_noise, cv2.MORPH_OPEN, kernel)       # Morphing to enhance
            #cv2. imshow('Green', perfect)

        
            cnts = cv2.findContours(perfect.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)   # find contours in the thresholded image
            cnts = imutils.grab_contours(cnts)
            
            for c in cnts:
                M = cv2.moments(c)                                              # compute the center of the contour
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                cv2.circle(perfect, (cX, cY), 7, (0, 255, 0), -1)               # Draw a circle for test
            
            # show the image
            cv2.imshow("Perfect", perfect)
            
            draw_x = int(cX * 1920 / 640)
            draw_y = int(cY * 1080 / 480)
            print(draw_x, draw_y)

            # Draw the Thing For Papa
            # if flag == 0:
            #     time.sleep(5) 
            #     flag = 1
            if flag1:
                pyautogui.dragTo(draw_x, draw_y)
        except UnboundLocalError:
            print('err')
            continue
        

    cap.release()
    cv2.destroyAllWindows()

main()
