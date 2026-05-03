import cv2
import face_recognition
import numpy as np
import os

def enroll_face(name):

    cap = cv2.VideoCapture(0)

    print("Press S to capture face")
    print("Press Q to quit")

    while True:

        ret, frame = cap.read()

        if not ret:
            print("Camera error")
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        faces = face_recognition.face_locations(rgb)

        # Draw rectangle around detected face
        for (top, right, bottom, left) in faces:

            cv2.rectangle(
                frame,
                (left, top),
                (right, bottom),
                (0, 255, 0),
                2
            )

        cv2.imshow("Face Enrollment", frame)

        key = cv2.waitKey(1)

        if key == ord("s"):

            if len(faces) == 0:
                print("No face detected")
                continue

            encoding = face_recognition.face_encodings(
                rgb,
                faces
            )[0]

            os.makedirs("faces", exist_ok=True)

            file_path = f"faces/{name}.npy"

            np.save(
                file_path,
                encoding
            )

            print(f"{name} enrolled successfully")

            break

        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()