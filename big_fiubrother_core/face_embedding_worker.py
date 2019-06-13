from big_fiubrother_core.messages import FaceEmbeddingMessage, FaceClassificationMessage, MessageClientFactory
from big_fiubrother_classification.face_embedder_factory import FaceEmbedderFactory
from big_fiubrother_core.async_task import AsyncTask
import sys
import yaml


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

        # Save last result for centroid comparison
        self.previous_message = None
        self.centroid_use_counter = 0

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
        if len(face_embedding_message.face_boxes) != 0:
            if self.centroid_use_counter % 100 == 0 or \
                    len(face_embedding_message.face_boxes) != len(self.previous_message.face_boxes):

                print("Embedding")
                self.centroid_use_counter = 1
                for face_box in face_embedding_message.face_boxes:
                    # Get face from frame
                    frame = face_embedding_message.frame_bytes
                    face = frame[face_box[1]:face_box[3], face_box[0]:face_box[2]]

                    # Perform face classification
                    embedding = self.face_embedder.get_embedding_mem(face)
                    face_embeddings.append(embedding)

            else:
                #print("Centroid")
                face_box_min_distances = []

                for i in range(len(face_embedding_message.face_boxes)):
                    face_embeddings.append(0)
                    face_box_min_distances.append(999)

                    face_box = face_embedding_message.face_boxes[i]
                    face_box_x = (face_box[0] + face_box[2]) / 2
                    face_box_y = (face_box[1] + face_box[3]) / 2

                    for j in range(len(self.previous_message.face_boxes)):
                        prev_face_box = self.previous_message.face_boxes[j]
                        prev_face_box_x = (prev_face_box[0] + prev_face_box[2]) / 2
                        prev_face_box_y = (prev_face_box[1] + prev_face_box[3]) / 2

                        dist = ((face_box_x - prev_face_box_x)**2 + (face_box_y - prev_face_box_y)**2)**0.5

                        if dist < face_box_min_distances[i]:
                            face_box_min_distances[i] = dist
                            face_embeddings[i] = self.previous_message.face_embeddings[j]

        # Post face embedding job request
        face_classification_message = FaceClassificationMessage(face_embedding_message.camera_id,
                                                                face_embedding_message.timestamp,
                                                                face_embedding_message.frame_id,
                                                                face_embedding_message.frame_bytes,
                                                                face_embedding_message.face_boxes,
                                                                face_embeddings)
        self.message_publisher.publish(face_classification_message.encode())
        self.previous_message = face_classification_message


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