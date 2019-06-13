from big_fiubrother_core.messages import CameraMessage, FaceEmbeddingMessage, MessageClientFactory
from big_fiubrother_detection.face_detector_factory import FaceDetectorFactory
from big_fiubrother_core.async_task import AsyncTask
import sys
import cv2
import yaml
import numpy as np
import collections


class FaceDetectionWorker:

    def __init__(self, config_file_path):

        # Load settings
        with open(config_file_path) as config_file:
            settings = yaml.load(config_file)

        # Create Message publisher
        self.message_publisher = MessageClientFactory.buildPublisher(settings['message_publisher'])

        # Create Message consumer
        self.message_consumer = MessageClientFactory.buildConsumer(settings['message_consumer'], self._detect_faces)

        # Create Face Detector
        self.face_detector = FaceDetectorFactory.build(config_file_path)

        # Crate Face Detector Thread
        self.face_detector_thread = AsyncTask(self.face_detector.detect_face_image)

        # Create face embedding messages buffer
        self.face_embedding_buffer = collections.deque()

    def start(self):

        self.message_publisher.start()
        self.message_consumer.start()
        self.face_detector_thread.start()

    def stop(self):

        self.message_publisher.stop()
        self.message_consumer.stop()
        self.face_detector.close()
        self.face_detector_thread.stop()

    def _detect_faces(self, message_bytes):

        #print(" [x] Received a frame. Detecting faces.")

        # Get message
        face_detection_message = CameraMessage.decode(message_bytes)
        frame_id = face_detection_message.camera_id + "_" + face_detection_message.timestamp
        frame_bytes = face_detection_message.frame_bytes

        # Convert to cv2 img
        frame = cv2.imdecode(np.fromstring(frame_bytes, np.uint8), cv2.IMREAD_COLOR)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Push embedding messages buffer into pipeline
        if self.face_detector_thread.output_ready():
            rects = self.face_detector_thread.get_output()

            for i in range(len(self.face_embedding_buffer)):
                face_embedding_message = self.face_embedding_buffer.popleft()
                face_embedding_message.face_boxes = rects
                self.message_publisher.publish(face_embedding_message.encode())

        # Queue up face detection
        self.face_detector_thread.set_input(frame)

        # Insert face embedding job request into buffer
        face_embedding_message = FaceEmbeddingMessage(face_detection_message.camera_id, face_detection_message.timestamp, frame_id, frame, [])
        self.face_embedding_buffer.append(face_embedding_message)


if __name__ == "__main__":

    if len(sys.argv) < 2:

        print("--------------------------------")
        print("CAMBIAR DESCRIPCION")
        print("")
        print("Usage: ")
        print("python face_detection_worker.py 'config_file.yaml'")
        print("--------------------------------")

    else:

        config_file = sys.argv[1]
        worker = FaceDetectionWorker(config_file)

        print(" [x] Running FaceDetectionWorker. Press any key + enter to exit.")
        worker.start()
        input()

        worker.stop()
        print(" [x] Exiting.")