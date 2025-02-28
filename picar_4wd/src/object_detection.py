import cv2
import numpy as np
import os
import picar_4wd.helpers.navigation as car
import tflite_runtime.interpreter as tflite
import time

BASE_PATH = os.path.expanduser('~/picar-4wd/picar_4wd/models')
MODEL_PATH = os.path.join(BASE_PATH, 'detect.tflite')
LABELS_PATH = os.path.join(BASE_PATH, 'labelmap.txt')

class Detect:
    def __init__(self):
        self.boxes, self.classes, self.scores, self.detections = None, None, None, None
        self.stop_sign = None
        with open(LABELS_PATH, "r") as f:
            self.labels = [line.strip() for line in f.readlines()]

        self.camera = cv2.VideoCapture(0)
        self.ret, self.frame = self.camera.read()

    def detect(self):
        interpreter = tflite.Interpreter(model_path=MODEL_PATH)
        interpreter.allocate_tensors()

        input_details, output_details = interpreter.get_input_details(), interpreter.get_output_details()
        images = input_details[0]
        input_shape = images['shape']
        height, width = input_shape[1], input_shape[2]
        image = cv2.resize(self.frame, (width, height))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = np.expand_dims(image, axis=0).astype(np.uint8)
        interpreter.set_tensor(images['index'], image)
        interpreter.invoke()


        self.boxes, self.classes, self.scores, self.detections = (
            interpreter.get_tensor(output_details[i]['index']) for i in range(4)
        )
        self.stop_sign = any(
            'stop sign' in
            self.labels[int(self.classes[0][i])].lower()
            for i in range(len(self.scores[0])) if self.scores[0][i] > 0.5
        )


    def detected_stop_sign(self):
        found_stop = self.stop_sign
        if found_stop:
            print('Stopping for stop sign.')
            car.stop()
            time.sleep(10)

        return found_stop
