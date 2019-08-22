import cv2
import numpy as np
import time

WINDOW_NAME = 'LemonTracker'

c=1
def track(image,y):
    global c
    wait = 0

    gausBlur = cv2.GaussianBlur(image, (5, 5), 0)

    hsv = cv2.cvtColor(gausBlur, cv2.COLOR_BGR2HSV)

    lowergreen_value = np.array([20, 100, 100])
    uppergreen_value = np.array([30, 255, 255])

    mask = cv2.inRange(hsv, lowergreen_value, uppergreen_value)
    
    blurmask = cv2.GaussianBlur(mask, (5, 5), 0)
    
    
    moments = cv2.moments(blurmask)

    m00 = moments['m00']
    centroid_x, centroid_y = None, None
    if m00 != 0:
        centroid_x = int(moments['m10'] / m00)
        centroid_y = int(moments['m01'] / m00)

    centr = (-1, -1)

    if centroid_x != None and centroid_y != None:
        centr = (centroid_x, centroid_y)
        if(c!=1):
            if(y[-1]-centroid_y>32 or y[-1]-centroid_y<-32):

                wait = 1
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(image, 'Lemon Falls', (10, 50), font, 1, (0, 0, 139), 2, cv2.LINE_AA)

            else:

                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(image, 'Did Not Fall ', (10, 50), font, 1, (0, 0, 0), 2, cv2.LINE_AA)

        y.append(centroid_y)
        c=c+1
        cv2.circle(image, centr,4, (0,0,0))
        cv2.imshow(WINDOW_NAME, image)
    if wait == 1:
        time.sleep(1)

    if cv2.waitKey(1) & 0xFF == 27:
        centr = None

    return centr

if __name__ == '__main__':

    capture = cv2.VideoCapture('s.mp4')
    y = [-1]
    while True:

        okay, image = capture.read()

        if okay:

            if not track(image,y):
                break

            cv2.waitKey(1)
        else:
            break
        
    capture.release()
    cv2.destroyAllWindows()

