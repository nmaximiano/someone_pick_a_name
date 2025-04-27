import cv2
import numpy as np
import mediapipe as mp
from picamera2 import Picamera2

size_x = 640
size_y = 480

previous_color = None
color_tolerance = 30

person_data = {}

def person_enter():
    with open("./sms/people.txt", "r+") as file:
        people = file.read()
        try:
            people = int(people)
        except:
            people = 0
        people += 1
        file.truncate(0)
        file.seek(0)
        file.write(str(people)) 

def person_exit():
    with open("./sms/people.txt", "r+") as file:
        people = file.read()
        try:
            people = int(people)
        except:
            people = 0
        people -= 1
        file.truncate(0)
        file.seek(0)
        file.write(str(people)) 

def handle_person_exit():
    delta = person_data["entry"]["x"] - person_data["exit"]["x"]
    if delta > 0:
        person_enter()
    elif delta < 0:
        person_exit()

def coord_in_bounds(x, y):
    return (x >= 0 and x < size_x) and (y >= 0 and y < size_y)

def get_average_color(frame, center, radius):
    total = frame[center[1]][center[0]].astype(np.float64).copy()
    steps = 1
    for x in range(-radius, radius):
        for y in range(-radius, radius):
            if coord_in_bounds(center[0] + x, center[1] + y):
                total += frame[center[1] + y][center[0] + x]
                steps += 1
    return total / steps

display_image = True

# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cv2.startWindowThread()

# open webcam video stream
#cap = cv2.VideoCapture(0)

picam2 = Picamera2()
picam2.preview_configuration.main.size = (size_x, size_y)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

while(True):
    # Capture frame-by-frame
    #ret, frame = cap.read()
    frame = picam2.capture_array()
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # resizing for faster detection
    if frame is None:
        continue
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

        if coord_in_bounds(center_x, center_y):
            color = get_average_color(rgb, [center_x, center_y], 50)

             # Draw a dot (a filled circle) at the center
            if abs(center_x - size_x / 2) < 50:
                cv2.circle(frame, (center_x, center_y), radius=5, color=(0, 0, 255), thickness=-1)
            else:
                cv2.circle(frame, (center_x, center_y), radius=50, color=(color[2], color[1], color[0]), thickness=-1)

            if abs(center_x - size_x / 2) < 50:
                if previous_color is not None:
                    difference = abs(previous_color - color)
                    norm = np.sqrt(difference[0]**2 + difference[1]**2 + difference[2]**2)
                    if norm > color_tolerance:
                        print("New Person! ", color)
                        person_data["entry"] = {
                            "color" : color,
                            "x" : center_x
                        }
                else:
                    print("Person Entered! ", color)
                    person_data["entry"] = {
                        "color" : color,
                        "x" : center_x
                    }

                previous_color = color
            else:
                if previous_color is not None:
                    previous_color = None
                    print("Person Exited! ", color)
                    person_data["exit"] = {
                        "color" : color,
                        "x" : center_x
                    }
                    handle_person_exit()
                    
    
    # Display the resulting frame
    if display_image:
        cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

pose.close()
# When everything done, release the capture
cap.release()
picam2.stop()
# finally, close the window
cv2.destroyAllWindows()
cv2.waitKey(1)

