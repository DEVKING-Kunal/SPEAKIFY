import cv2
import numpy as np

# Initialize face detector and recognizer
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Step 1: Capture the authorized user's face and train recognizer
def capture_and_train():
    video_capture = cv2.VideoCapture(0)
    authorized_face_images = []
    sample_count = 0
    max_samples = 20  # Number of samples to capture for training

    print("Capturing the authorized face. Please stay still.")
    while sample_count < max_samples:
        ret, frame = video_capture.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

        for (x, y, w, h) in faces:
            sample_count += 1
            face_image = gray[y:y+h, x:x+w]
            authorized_face_images.append(face_image)
            cv2.imshow('Capturing Face', face_image)
            cv2.waitKey(100)  # Small delay between captures
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

    # Train the recognizer on the captured faces
    if authorized_face_images:
        print("Training recognizer with captured face images...")
        labels = [1] * len(authorized_face_images)  # All images belong to the authorized user (label 1)
        recognizer.train(authorized_face_images, np.array(labels))
        print("Training complete!")
    else:
        print("No face images captured. Please try again.")

# Step 2: Implement Face Recognition
def recognize_face():
    video_capture = cv2.VideoCapture(0)
    print("Face recognition started. Look at the camera...")

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

        for (x, y, w, h) in faces:
            face_image = gray[y:y+h, x:x+w]
            label, confidence = recognizer.predict(face_image)
            
            # If confidence is low, it indicates a closer match (lower is better with LBPH)
            if label == 1 and confidence < 50:  # Adjust confidence threshold as needed
                cv2.putText(frame, "Access Granted", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "Access Denied", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

            # Draw rectangle around the face
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Show the video with detection
        cv2.imshow('Speakify Authorized Face Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

# Run the functions
capture_and_train()
recognize_face()
