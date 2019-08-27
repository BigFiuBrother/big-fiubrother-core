import numpy as np
import cv2


def bytes_to_image(buffer, color):
  np_arr = np.fromstring(buffer, np.uint8)
  return cv2.imdecode(np_arr, color)

def image_to_RGB(image):
  return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

def image_to_bytes(image, extension='.jpg'):
  ret_val, buffer = cv2.imencode(extension, image)
  return buffer

def save_image(filepath, image):
  cv2.imwrite(filepath, image)