from big_fiubrother_core.messages import CameraMessage, FaceEmbeddingMessage
from big_fiubrother_detection.face_detector_factory import FaceDetectorFactory
import pika
import sys
import threading
import importlib
import cv2
import yaml
import os
import numpy as np


class FaceDetectionWorker:

    def __init__(self, config_file_path):

        # Load settings
        with open(config_file_path) as config_file:
            settings = yaml.load(config_file)

        rabbitmqhost = settings['rabbitmqhost']
        face_embedding_job_queue = settings['face_embedding_queue']
        face_detection_job_queue = settings['face_detection_queue']

        # Create connection and channel
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=rabbitmqhost))
        self.channel = self.connection.channel()

        # Set face embedding job queue name
        self.face_embedding_job_queue = face_embedding_job_queue

        # Set face detection job queue name
        self.face_detection_job_queue = face_detection_job_queue

        # Create face detection job queue
        #self.channel.queue_declare(queue=self.face_detection_job_queue)

        # Consume from queue
        self.channel.basic_consume(self._process_frame, queue=self.face_detection_job_queue, no_ack=True)

        # Create thread
        self.thread = threading.Thread(target=self._start_consuming)

        self.number = 0

        # Create Face Detector
        self.face_detector = FaceDetectorFactory.build(config_file_path)

        # Create temp dir
        if not os.path.exists("face_detection_worker_dump"):
            os.mkdir("face_detection_worker_dump")

    def start(self):

        self.thread.start()

    def _start_consuming(self):
        self.channel.start_consuming()

    def stop(self):

        self.channel.stop_consuming()
        self.face_detector.close()
        self.thread.join()

    def _process_frame(self, ch, method, props, body):

        print(" [x] Received a frame. Analyzing")

        # Get message
        face_detection_message = CameraMessage.decode(body)
        frame_id = face_detection_message.camera_id + "_" + face_detection_message.timestamp
        frame_bytes = face_detection_message.frame_bytes

        # Convert to cv2 img
        frame = cv2.imdecode(np.fromstring(frame_bytes, np.uint8), cv2.IMREAD_COLOR)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Perform face detection
        rects = self.face_detector.detect_face_image(frame)
        print(" [x] Found " + str(len(rects)) + " faces.")

        # Post face embedding job request
        face_embedding_message = FaceEmbeddingMessage(frame_id, frame, rects)
        self.channel.basic_publish("", self.face_embedding_job_queue, face_embedding_message.encode())


if __name__ == "__main__":

    if len(sys.argv) < 2:

        print("--------------------------------")
        print("CAMBIAR DESCRIPCION")
        print("")
        print("Usage: ")
        print("python FaceDetectionWorker.py 'config_file.yaml'")
        print("--------------------------------")

    else:

        config_file = sys.argv[1]
        worker = FaceDetectionWorker(config_file)

        print(" [x] Running FaceDetectionWorker. Press any key + enter to exit.")
        worker.start()
        input()

        worker.stop()
        print(" [x] Exiting.")