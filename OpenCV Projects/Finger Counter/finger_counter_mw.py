import cv2
import time
import os
import hand_tracking_module1 as htm #made use  of the previously built hand tracking module

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.75)

folderPath = "fingerImgs"
myList = os.listdir(folderPath)
print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    #print(f'{folderPath}/{imPath}')
    overlayList.append(image)
print(len(overlayList))

#overlayWidth, overlayHeight = 250, 250

# Load and resize each image to the desired size
'''for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    if image is not None:
        resized_image = cv2.resize(image, (overlayWidth, overlayHeight))
        overlayList.append(resized_image)
    else:
        print(f'Failed to load image: {folderPath}/{imPath}')'''

print(len(overlayList))
tipIds = [4, 8, 12, 16, 20]


while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        #print(lmList)
        fingers = []
        # for thumb, can be improved further be checking hands or a different logic
        if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # for fingers
        for id in range(1,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        #print(fingers)
        totalFingers = fingers.count(1)
        print(totalFingers)

        #img[0:overlayHeight, 0:overlayWidth] = overlayList[0]
        h, w, c = overlayList[totalFingers-1].shape
        img[0: h, 0: w] = overlayList[totalFingers-1]

        cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN, 
                    10, (255, 0, 0), 25)

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_COMPLEX, 1,
                ( 255, 0, 0), 3)

    cv2.imshow("Image", img)
    #cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
