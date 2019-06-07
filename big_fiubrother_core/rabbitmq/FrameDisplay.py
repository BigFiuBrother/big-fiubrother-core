from big_fiubrother_core.messages import DisplayFrameMessage
import pika
import threading
import yaml
import cv2
import sys


class FrameDisplay:

    def __init__(self, config_file_path):

        # Load settings
        with open(config_file_path) as config_file:
            settings = yaml.load(config_file)

        rabbitmqhost = settings['rabbitmqhost']
        frame_display_queue = settings['frame_display_queue']

        # Create connection and channel
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=rabbitmqhost))
        self.channel = self.connection.channel()

        # Set frame display queue name
        self.frame_display_queue = frame_display_queue

        # Consume from queue
        self.channel.basic_consume(self._display_frame, queue=self.frame_display_queue, no_ack=True)

        # Create thread
        self.thread = threading.Thread(target=self._start_consuming)

    def start(self):
        self.thread.start()

    def _start_consuming(self):
        self.channel.start_consuming()

    def stop(self):

        self.channel.stop_consuming()
        self.thread.join()

    def _display_frame(self, ch, method, props, body):

        display_frame_message = DisplayFrameMessage.decode(body)
        face_boxes = display_frame_message.face_boxes
        face_ids = display_frame_message.face_ids
        face_id_probs = display_frame_message.face_id_probs

        # Display frame
        frame = display_frame_message.frame_bytes
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        for i in range(len(face_boxes)):
            face_box = face_boxes[i]
            face_id = face_ids[i]
            face_id_prob = face_id_probs[i]
            cv2.rectangle(frame, (int(face_box[0]), int(face_box[1])), (int(face_box[2]), int(face_box[3])),
                          (0, 0, 255), 2)
            self._write_text(frame, (int(face_box[0]), int(face_box[1])), face_id + ", " + face_id_prob)
        cv2.imshow('img', frame)
        cv2.waitKey(1)

    def _write_text(self, img, botleft, text="test text"):

        font = cv2.FONT_HERSHEY_SIMPLEX
        #botleft = (10, 500)
        font_scale = 1
        font_color = (255, 255, 255)
        line_type = 2

        cv2.putText(img, text,
                    botleft,
                    font,
                    font_scale,
                    font_color,
                    line_type)


if __name__ == "__main__":

    if len(sys.argv) < 2:

        print("--------------------------------")
        print("CAMBIAR DESCRIPCION")
        print("")
        print("Usage: ")
        print("python FrameDisplay.py 'config_file.yaml'")
        print("--------------------------------")

    else:

        config_file = sys.argv[1]
        worker = FrameDisplay(config_file)

        print(" [x] Running FrameDisplay. Press any key + enter to exit.")
        worker.start()
        input()

        worker.stop()
        print(" [x] Exiting.")