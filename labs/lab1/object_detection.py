import os
import tflite_runtime.interpreter as tflite

BASE_PATH = os.path.expanduser('~/picar-4wd/labs/lab1/models')
MODEL_PATH = os.path.join(BASE_PATH, 'detect.tflite')
LABELS_PATH = os.path.join(BASE_PATH, 'labelmap.txt')


interpreter = tflite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
images = input_details[0]
input_shape = images['shape']
height, width = input_shape[1], input_shape[2]

output_details = interpreter.get_output_details()
# boxes, classes, scores, detections = (interpreter.get_tensor(output_details[i]['index']) for i in range(4))

with open(LABELS_PATH, "r") as f:
    labels = [line.strip() for line in f.readlines()]