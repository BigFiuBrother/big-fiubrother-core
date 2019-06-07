from big_fiubrother_core.messages import FaceClassificationMessage
from big_fiubrother_core.messages import DisplayFrameMessage
from big_fiubrother_classification.classifier_support_vector import SVClassifier
import pika
import sys
import threading
import cv2
import yaml
import numpy as np


class FaceClassificationWorker:

    def __init__(self, config_file_path):

        # Load settings
        with open(config_file_path) as config_file:
            settings = yaml.load(config_file)

        rabbitmqhost = settings['rabbitmqhost']
        face_classification_job_queue = settings['face_classification_queue']
        frame_display_queue = settings['frame_display_queue']

        # Create connection and channel
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=rabbitmqhost))
        self.channel = self.connection.channel()

        # Set frame display queue name
        self.frame_display_queue = frame_display_queue

        # Set face classification job queue name
        self.face_classification_job_queue = face_classification_job_queue

        # Consume from queue
        self.channel.basic_consume(self._process_face_classification, queue=self.face_classification_job_queue, no_ack=True)

        # Create thread
        self.thread = threading.Thread(target=self._start_consuming)

        # Create Face Classifier
        classifier_pkl = settings['classifier_pkl']
        self.face_classifier = SVClassifier.load(classifier_pkl)

    def start(self):

        self.thread.start()

    def _start_consuming(self):
        self.channel.start_consuming()

    def stop(self):

        self.channel.stop_consuming()
        self.thread.join()

    def _process_face_classification(self, ch, method, props, body):

        print(" [x] Received a message with faces. Analyzing")

        # Get message
        face_classification_message = FaceClassificationMessage.decode(body)
        frame_id = face_classification_message.frame_id
        frame = face_classification_message.frame_bytes
        face_embeddings = face_classification_message.face_embeddings

        # Perform face classification
        face_ids = []
        face_id_probs = []
        for embedding in face_embeddings:
            pred_class, pred_prob = self.face_classifier.predict(embedding)
            face_ids.append(pred_class)
            face_id_probs.append(str(pred_prob))

        # Post frame display message
        frame_display_message = DisplayFrameMessage(frame_id, frame, face_classification_message.face_boxes ,face_ids, face_id_probs)
        self.channel.basic_publish("", self.frame_display_queue, frame_display_message.encode())


if __name__ == "__main__":

    if len(sys.argv) < 2:

        print("--------------------------------")
        print("CAMBIAR DESCRIPCION")
        print("")
        print("Usage: ")
        print("python FaceClassificationWorker.py 'config_file.yaml'")
        print("--------------------------------")

    else:

        config_file = sys.argv[1]
        worker = FaceClassificationWorker(config_file)

        print(" [x] Running FaceClassificationWorker. Press any key + enter to exit.")
        worker.start()
        input()

        worker.stop()
        print(" [x] Exiting.")