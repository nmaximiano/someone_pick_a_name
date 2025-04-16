import cv2
import numpy as np
import mediapipe as mp

size_x = 640
size_y = 480

def coord_in_bounds(x, y):
    return (x >= 0 and x < size_x) and (y >= 0 and y < size_y)

def get_average_color(frame, center, radius):
    total = [0, 0, 0]
    for x in range(-radius, radius):
        for y in range(-radius, radius):
            total += frame[center[1] + y][center[0] + x]

    return total / (radius * radius * 4)

display_image = True

# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cv2.startWindowThread()

# open webcam video stream
cap = cv2.VideoCapture(0)

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # resizing for faster detection
    frame = cv2.resize(frame, (size_x, size_y))

    # using a greyscale picture, also for faster detection
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    image = frame
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)

    if results.pose_landmarks:
        h, w, _ = image.shape
        landmarks = results.pose_landmarks.landmark

        # Get shoulder and hip coordinates
        l_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        r_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        l_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
        r_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]

        x1 = int(min(l_shoulder.x, r_shoulder.x) * w)
        x2 = int(max(l_shoulder.x, r_shoulder.x) * w)
        y1 = int(min(l_shoulder.y, r_shoulder.y) * h)
        y2 = int(max(l_hip.y, r_hip.y) * h)

        center_x = int((x1 + x2) / 2)
        center_y = int((y1 + y2) / 2)

        print(get_average_color(frame, [center_x, center_y], 25))

        # Draw a dot (a filled circle) at the center
        cv2.circle(frame, (center_x, center_y), radius=5, color=(0, 0, 255), thickness=-1)
    
    # Display the resulting frame
    if display_image:
        cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

pose.close()
# When everything done, release the capture
cap.release()
# finally, close the window
cv2.destroyAllWindows()
cv2.waitKey(1)