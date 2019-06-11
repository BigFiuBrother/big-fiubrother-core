from big_fiubrother_core.messages import DisplayFrameMessage, MessageClientFactory
import sys
import cv2
import yaml


class FrameDisplayMock:

    def __init__(self, config_file_path):

        # Load settings
        with open(config_file_path) as config_file:
            settings = yaml.load(config_file)

        # Create Message consumer
        self.message_consumer = MessageClientFactory.buildConsumer(settings['message_consumer'], self._display_frame)

    def start(self):

        self.message_consumer.start()

    def stop(self):

        self.message_consumer.stop()

    def _display_frame(self, message_bytes):

        display_frame_message = DisplayFrameMessage.decode(message_bytes)
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
        print("python frame_display_mock.py 'config_file.yaml'")
        print("--------------------------------")

    else:

        config_file = sys.argv[1]
        worker = FrameDisplayMock(config_file)

        print(" [x] Running FrameDisplayMock. Press any key + enter to exit.")
        worker.start()
        input()

        worker.stop()
        print(" [x] Exiting.")