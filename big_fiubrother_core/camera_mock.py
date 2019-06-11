from big_fiubrother_core.messages import CameraMessage
import cv2
import pika
from datetime import datetime
import time

# Start webcam
camera = cv2.VideoCapture(2)
ret, image = camera.read()
cv2.imshow('img', image)

fps = 10
fps_inv = 1.0 / fps
print(fps_inv)

start_time = time.time()
last_frame_time = start_time
frames_sent = 0
while True:

    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    face_detection_job_queue = "FACE_DETECTION"

    # Read frame from Webcam
    ret, image = camera.read()

    # Show image on screen
    cv2.imshow('img', image)


    # Check for exit button 'q'
    ch = cv2.waitKey(1) & 0xFF
    if ch == ord("q"):
        break

    #if ch == ord(" "):
    time_now = time.time()
    elapsed_time = time_now - last_frame_time
    if elapsed_time >= fps_inv:
        #print("Sending frame")
        last_frame_time = time_now
        frames_sent += 1

        cv2.imwrite("temp.jpg", image)
        f = open("temp.jpg", "rb")
        frame_bytes = f.read()
        f.close()

        # Post face classification job request
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        camera_message = CameraMessage("0", frame_bytes, timestamp)
        channel.basic_publish("", face_detection_job_queue, camera_message.encode())

end_time = time.time()
print("FPS: ", frames_sent / (end_time - start_time))