from big_fiubrother_core.messages import FaceEmbeddingMessage, FaceClassificationMessage, MessageClientFactory
from big_fiubrother_classification.face_embedder_factory import FaceEmbedderFactory
import sys
import cv2
import yaml
import numpy as np


class FaceEmbeddingWorker:

    def __init__(self, config_file_path):

        # Load settings
        with open(config_file_path) as config_file:
            settings = yaml.load(config_file)

        # Create Message publisher
        self.message_publisher = MessageClientFactory.buildPublisher(settings['message_publisher'])

        # Create Message consumer
        self.message_consumer = MessageClientFactory.buildConsumer(settings['message_consumer'], self._do_face_embeddings)

        # Create Face Embedder
        self.face_embedder = FaceEmbedderFactory.build(config_file_path)

    def start(self):

        self.message_publisher.start()
        self.message_consumer.start()

    def stop(self):

        self.message_publisher.stop()
        self.message_consumer.stop()
        self.face_embedder.close()

    def _do_face_embeddings(self, message_bytes):

        #print(" [x] Received a message. Doing face embedding.")

        # Get message
        face_embedding_message = FaceEmbeddingMessage.decode(message_bytes)

        face_embeddings = []
        for face_box in face_embedding_message.face_boxes:
            # Get face from frame
            frame = face_embedding_message.frame_bytes
            face = frame[face_box[1]:face_box[3], face_box[0]:face_box[2]]

            # Perform face classification
            embedding = self.face_embedder.get_embedding_mem(face)
            face_embeddings.append(embedding)

        # Post face embedding job request
        face_classification_message = FaceClassificationMessage(face_embedding_message.frame_id,
                                                                face_embedding_message.frame_bytes,
                                                                face_embedding_message.face_boxes,
                                                                face_embeddings)
        self.message_publisher.publish(face_classification_message.encode())


if __name__ == "__main__":

    if len(sys.argv) < 2:

        print("--------------------------------")
        print("CAMBIAR DESCRIPCION")
        print("")
        print("Usage: ")
        print("python face_embedding_worker.py 'config_file.yaml'")
        print("--------------------------------")

    else:

        config_file = sys.argv[1]
        worker = FaceEmbeddingWorker(config_file)

        print(" [x] Running FaceEmbeddingWorker. Press any key + enter to exit.")
        worker.start()
        input()

        worker.stop()
        print(" [x] Exiting.")