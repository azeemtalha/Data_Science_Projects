import cv2
import numpy as np
import time
import hand_tracking_module1 as htm
import pyautogui

screen_width, screen_height = pyautogui.size()


wCam, hCam = 640, 480
framneRed = 100
smoothening = 5
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
detector = htm.handDetector(maxHands=1)

while True:
    # 1. Find hand Landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    # 2. Get the tip of index and middle fingers
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        # 3. Check which fingers are up
        fingers = detector.fingersUp()
        #print(fingers)
        cv2.rectangle(img, (framneRed, framneRed),
                           (wCam - framneRed, hCam - framneRed), (255, 0, 255), 2)

        # 4. Only index finger : Moving Mode
        if fingers[1] == 1 and fingers[2] == 0:
            # 5. Convert Coordinates
            x3 = np.interp(x1, (framneRed, wCam - framneRed), (0, screen_width))
            y3 = np.interp(y1, (framneRed, wCam - framneRed), (0, screen_height))
            # 6. Smoothen Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            # 7. Move Mouse 
            pyautogui.moveTo(wCam- clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

        # 8. Both index and middle finger are up : Clicking Mode
        if fingers[1] == 1 and fingers[2] == 1:
             # 9. Find Distance Between Fingers
            length, img, lineInfo = detector.findDistance(8, 12, img)
            print(length)
             # 10. Click mouse if distance is short
            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                pyautogui.click()

    # 11. Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)


    # 12. Display
    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()