import cv2
import mediapipe as mp
import time

# Initialize video capture
cap = cv2.VideoCapture('FaceVideo/10.mp4')
pTime = 0

# Initialize MediaPipe Face Mesh
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=2)
mpDraw = mp.solutions.drawing_utils

# Define custom drawing specifications
drawSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=2, color=(0, 255, 0))
tesselationSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=1, color=(0, 255, 0))
contourSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=1, color=(0, 255, 0))

desired_width = 800
desired_height = 600

while True:
    success, img = cap.read()
    if not success:
        break

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = faceMesh.process(imgRGB)

    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks:
            mpDraw.draw_landmarks(
                img, faceLms, mpFaceMesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=tesselationSpec,
                connection_drawing_spec=tesselationSpec)
            mpDraw.draw_landmarks(
                img, faceLms, mpFaceMesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=contourSpec,
                connection_drawing_spec=contourSpec)
            for id, lm in enumerate(faceLms.landmark):
                ih, iw, ic = img.shape
                x, y = int(lm.x * iw), int(lm.y * ih)

    # Resize the image
    img = cv2.resize(img, (desired_width, desired_height))

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_COMPLEX, 3,
                (0, 255, 0), 3)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
