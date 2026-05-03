import cv2
import face_recognition
import numpy as np
import os
from datetime import datetime

# Load saved faces
def load_known_faces():

    encodings = []
    names = []

    if not os.path.exists("faces"):
        print("No faces directory found")
        return encodings, names

    for file in os.listdir("faces"):

        path = os.path.join("faces", file)

        encoding = np.load(path)

        encodings.append(encoding)

        name = os.path.splitext(file)[0]

        names.append(name)

    return encodings, names


def mark_attendance(name):

    file_exists = os.path.isfile("attendance.csv")

    now = datetime.now()

    time = now.strftime("%H:%M:%S")
    date = now.strftime("%Y-%m-%d")

    with open("attendance.csv", "a") as f:

        if not file_exists:
            f.write("Name,Time,Date\n")

        f.write(f"{name},{time},{date}\n")


def start_recognition():

    known_encodings, known_names = load_known_faces()

    if len(known_encodings) == 0:
        print("No registered faces found")
        return

    cap = cv2.VideoCapture(0)

    marked_today = set()

    print("Press ESC to stop")

    while True:

        ret, frame = cap.read()

        if not ret:
            print("Camera error")
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        faces = face_recognition.face_locations(rgb)

        encodings = face_recognition.face_encodings(
            rgb,
            faces
        )

        for encoding, location in zip(encodings, faces):

            matches = face_recognition.compare_faces(
                known_encodings,
                encoding
            )

            face_distances = face_recognition.face_distance(
                known_encodings,
                encoding
            )

            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:

                name = known_names[best_match_index]

                if name not in marked_today:

                    mark_attendance(name)

                    marked_today.add(name)

                top, right, bottom, left = location

                cv2.rectangle(
                    frame,
                    (left, top),
                    (right, bottom),
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    name,
                    (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )

        cv2.imshow(
            "Attendance Recognition",
            frame
        )

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()