from big_fiubrother_core.messages import FaceEmbeddingMessage
from big_fiubrother_core.messages import FaceClassificationMessage
from big_fiubrother_classification.face_embedder_factory import FaceEmbedderFactory
import pika
import sys
import threading
import importlib
import cv2
import yaml
import os


class FaceEmbeddingWorker:

    def __init__(self, config_file_path):

        # Load settings
        with open(config_file_path) as config_file:
            settings = yaml.load(config_file)

        rabbitmqhost = settings['rabbitmqhost']
        face_embedding_job_queue = settings['face_embedding_queue']
        face_classification_job_queue = settings['face_classification_queue']

        # Create connection and channel
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=rabbitmqhost))
        self.channel = self.connection.channel()

        # Set face classification job queue name
        self.face_embedding_job_queue = face_embedding_job_queue

        # Consume from queue
        self.channel.basic_consume(self._process_face, queue=self.face_embedding_job_queue, no_ack=True)

        # Create thread
        self.thread = threading.Thread(target=self._start_consuming)

        # Set face classification job queue name
        self.face_classification_job_queue = face_classification_job_queue

        # Create Face Embedder
        self.face_embedder = FaceEmbedderFactory.build(config_file_path)

        # Create temp dir
        if not os.path.exists("face_embedding_worker_dump"):
            os.mkdir("face_embedding_worker_dump")

    def start(self):

        self.thread.start()

    def _start_consuming(self):
        self.channel.start_consuming()

    def stop(self):

        self.channel.stop_consuming()
        self.face_embedder.close()
        self.thread.join()

    def _process_face(self, ch, method, props, body):

        print(" [x] Received a message with faces. Analyzing")

        # Get message
        face_embedding_message = FaceEmbeddingMessage.decode(body)

        face_embeddings = []
        for face_box in face_embedding_message.face_boxes:

            # Get face from frame
            frame = face_embedding_message.frame_bytes
            face = frame[face_box[1]:face_box[3], face_box[0]:face_box[2]]

            # Perform face classification
            embedding = self.face_embedder.get_embedding_mem(face)
            face_embeddings.append(embedding)
            #embedding_string = ','.join(['%.8f' % num for num in embedding])
            #print(" [x] Face embedding: " + embedding_string)

        # Post face classification job request
        face_classification_message = FaceClassificationMessage(face_embedding_message.frame_id,
                                                                face_embedding_message.frame_bytes,
                                                                face_embedding_message.face_boxes,
                                                                face_embeddings)
        self.channel.basic_publish("", self.face_classification_job_queue, face_classification_message.encode())


if __name__ == "__main__":

    if len(sys.argv) < 2:

        print("--------------------------------")
        print("CAMBIAR DESCRIPCION")
        print("")
        print("Usage: ")
        print("python FaceEmbeddingWorker.py 'config_file.yaml'")
        print("--------------------------------")

    else:

        config_file = sys.argv[1]
        worker = FaceEmbeddingWorker(config_file)

        print(" [x] Running FaceEmbeddingWorker. Press any key + enter to exit.")
        worker.start()
        input()

        worker.stop()
        print(" [x] Exiting.")