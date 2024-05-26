import cv2
import mediapipe as mp
import time


cap = cv2.VideoCapture('FaceVideo/10.mp4')
pTime = 0

mpFaceMesh = mp.solutions.face_mesh
mpDraw = mp.solutions.drawing_utils
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=2)
mpDrawingStyles = mp.solutions.drawing_styles
#drawSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=2)
desired_width = 800
desired_height = 600

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = faceMesh.process(imgRGB)

    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks:
            #mpDraw.draw_landmarks(img, faceLms, mpFaceMesh.FACE_CONNECTIONS)
            mpDraw.draw_landmarks(
                img, faceLms, mpFaceMesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mpDrawingStyles.get_default_face_mesh_tesselation_style())
            mpDraw.draw_landmarks(
                img, faceLms, mpFaceMesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=None,
                connection_drawing_spec=mpDrawingStyles.get_default_face_mesh_contours_style())
            for id, lm in enumerate(faceLms.landmark):
                ih, iw, ic = img.shape
                x, y = int(lm.x*iw), int(lm.y*ih)

    img = cv2.resize(img, (desired_width, desired_height))

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_COMPLEX, 3,
                (0, 255, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)