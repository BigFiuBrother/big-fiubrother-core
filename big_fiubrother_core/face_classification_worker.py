from big_fiubrother_core.messages import FaceClassificationMessage, DisplayFrameMessage, MessageClientFactory
from big_fiubrother_classification.classifier_support_vector import SVClassifier
import sys
import cv2
import yaml
import numpy as np


class FaceClassificationWorker:

    def __init__(self, config_file_path):

        # Load settings
        with open(config_file_path) as config_file:
            settings = yaml.load(config_file)

        # Create Message publisher
        self.message_publisher = MessageClientFactory.buildPublisher(settings['message_publisher'])

        # Create Message consumer
        self.message_consumer = MessageClientFactory.buildConsumer(settings['message_consumer'], self._classify_faces)

        # Create Face Classifier
        classifier_pkl = settings['classifier_pkl']
        self.face_classifier = SVClassifier.load(classifier_pkl)

    def start(self):

        self.message_publisher.start()
        self.message_consumer.start()

    def stop(self):

        self.message_publisher.stop()
        self.message_consumer.stop()

    def _classify_faces(self, message_bytes):

        #print(" [x] Received a message. Doing face classification.")

        # Get message
        face_classification_message = FaceClassificationMessage.decode(message_bytes)
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
        frame_display_message = DisplayFrameMessage(frame_id, frame, face_classification_message.face_boxes, face_ids,
                                                    face_id_probs)
        self.message_publisher.publish(frame_display_message.encode())


if __name__ == "__main__":

    if len(sys.argv) < 2:

        print("--------------------------------")
        print("CAMBIAR DESCRIPCION")
        print("")
        print("Usage: ")
        print("python face_classification_worker.py 'config_file.yaml'")
        print("--------------------------------")

    else:

        config_file = sys.argv[1]
        worker = FaceClassificationWorker(config_file)

        print(" [x] Running FaceClassificationWorker. Press any key + enter to exit.")
        worker.start()
        input()

        worker.stop()
        print(" [x] Exiting.")