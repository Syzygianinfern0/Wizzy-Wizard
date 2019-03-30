import cv2
import imutils
import numpy as np

def main():
    cap = cv2.VideoCapture(0)
    screenCnt = []
    while True:
        # Reading the video

        _, frame = cap.read()
        frame = cv2.flip(frame, 1)                                  # Flip for mirror
        
        blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)          # Blurrd
        hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

        # Finding Whites

        sensitivity = 120
        lower_white = np.array([0,0,255-sensitivity])
        upper_white = np.array([255,sensitivity,255])

        mask = cv2.inRange(hsv, lower_white, upper_white)           # Whites mask
        cv2.imshow('whites', mask)

        # Noise Removal

        kernel = np.ones((5, 5), np.uint8)
        no_noise = cv2.erode(mask, kernel, iterations = 1)           # Noise Removal

        perfect = cv2.morphologyEx(no_noise, cv2.MORPH_OPEN, kernel)                            # Morphing to enhance
        
        # Getting Contours

        cnts = cv2.findContours(perfect.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)     # find contours in the thresholded image
        cnts = imutils.grab_contours(cnts)

        cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:2]                          # Taking the 3 largest contours

        # Finding Rectangles

        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.1 * peri, True)          # Applying DP algo to make a rectangle

            if len(approx) == 4:                                    # Checking for rectangle
                screenCnt = approx
                break
                
        cv2.drawContours(frame, [screenCnt], -1, (0, 255, 0), 2)[0]
        cv2.imshow('ORIGINAL', frame)

        # Get the image

        img = cv2.imread('Pic.jpg')
        rows, cols, _ = img.shape

        top_left_x, top_left_y = screenCnt[1][0][0], screenCnt[1][0][1]
        top_right_x, top_right_y = screenCnt[0][0][0], screenCnt[0][0][1]
        bottom_left_x, bottom_left_y = screenCnt[2][0][0], screenCnt[2][0][1]
        bottom_right_x, bottom_right_y = screenCnt[3][0][0], screenCnt[3][0][1]


        # pts1 = np.float32([[640, 0], [0, 0], [640, 480], [0, 480]])             #  4 points of the image Note the mirror flip in the beginning
        # pts2 = np.float32([[top_left_x, top_left_y], [top_right_x, top_right_y], [bottom_left_x, bottom_left_y], [bottom_right_x, bottom_right_y]])    # To map to corr coordintes of cam feed
        pts1 = np.float32([[640, 480], [640, 0], [0, 480], [0, 0]])             #  4 points of the image Note the mirror flip in the beginning
        pts2 = np.float32([[top_left_x, top_left_y], [top_right_x, top_right_y], [bottom_left_x, bottom_left_y], [bottom_right_x, bottom_right_y]])    # To map to corr coordintes of cam feed        
        
        M, _ = cv2.findHomography(pts1, pts2)
        dst = cv2.warpPerspective(img, M, (cols, rows))                     # Rectangular to Trapezoidal

        cv2.imshow('dst', dst)

        # white_rem_mask = cv2.bitwise_not(mask)
        # mask_rem_feed = cv2.bitwise_and(frame, white_rem_mask)

        # cv2.polylines(frame, screenCnt, True, (0, 0, 0))
        cv2.fillPoly(frame, [screenCnt], (0, 0, 0))

        cv2.imshow('ORIGINAL', frame)

        


        finished = cv2.bitwise_or(frame, dst)

        cv2. imshow('Finished', finished)
        if cv2.waitKey(1) & 0xFF == ord('q'):                               # The quit line
            break

    cap.release()
    cv2.destroyAllWindows()

main()
