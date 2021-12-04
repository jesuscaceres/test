import os
import cv2 as cv
import numpy as np

# Constants
KNOWN_COLORS: dict = {
    'red': {
        'lower': [3, 30, 30],
        'upper': [8, 250, 250]
    },
    'yellow': {
        'lower': [25, 30, 30],
        'upper': [30, 250, 250]
    },
    'green': {
        'lower': [35, 40, 40],
        'upper': [85, 255, 255]
    },
    'blue': {
        'lower': [100, 40, 40],
        'upper': [125, 255, 255]
    },
    'black': {
        'lower': [0, 0, 0],
        'upper': [180, 255, 50]
    }
}


def create_and_process_blob(net, ln, base_image):
    blob = cv.dnn.blobFromImage(base_image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    outputs = net.forward(ln)
    return np.vstack(outputs)


def get_height_and_width(source):
    return source.shape[:2]


def analize_source(base_image, outputs, conf):
    heigth, width = get_height_and_width(base_image)
    boxes = []
    confidences = []
    class_ids = []
    for output in outputs:
        scores = output[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > conf:
            x, y, w, h = output[:4] * np.array([width, heigth, width, heigth])
            p0 = int(x - w // 2), int(y - h // 2)
            boxes.append([*p0, int(w), int(h)])
            confidences.append(float(confidence))
            class_ids.append(class_id)
    indexes = cv.dnn.NMSBoxes(boxes, confidences, conf, conf - 0.1)
    return class_ids, confidences, indexes


def recognize_object(base_image, classes, net, ln):
    outputs = create_and_process_blob(net, ln, base_image)
    class_ids, confidences, indexes = analize_source(base_image, outputs, 0.3)
    if len(indexes) == 1:
        return classes[class_ids[0]]
    return 'Unknown'


def verify_color(filtered_image, net, ln):
    outputs = create_and_process_blob(net, ln, filtered_image)
    class_ids, confidences, indexes = analize_source(filtered_image, outputs, 0.2)
    if len(indexes) == 1:
        return True
    return False


def initialize_network():
    # Load names of classes and get random colors
    classes = open('TP_Arch_config/coco.names').read().strip().split('\n')

    # Give the configuration and weight files for the model and load the network.
    net = cv.dnn.readNetFromDarknet('TP_Arch_config/yolov3.cfg', 'TP_Arch_config/yolov3.weights')
    net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

    # determine the output layer
    ln = net.getLayerNames()
    ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]

    return classes, net, ln


def load_images():
    folder_path = "TP_Arch_config/Lote0001"
    filenames = [f'{folder_path}/{fn}' for fn in os.listdir(folder_path) if fn.endswith('.jpg')]
    images = []
    for file in filenames:
        img: np.ndarray = cv.imread(file)
        if img is not None:
            images.append((file, img))
    return images


def identify_color(img, ln, net):
    color = None
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    for key in KNOWN_COLORS.keys():
        lower = np.array(KNOWN_COLORS[key]['lower'])
        upper = np.array(KNOWN_COLORS[key]['upper'])
        mask = cv.inRange(hsv, lower, upper)
        image = cv.bitwise_and(img, img, mask=mask)
        if verify_color(image, net, ln):
            color = key
    return color


def process_item(classes, img, ln, net):
    object_name = recognize_object(img, classes, net, ln)
    if object_name not in ['bottle', 'cup']:
        img = cv.GaussianBlur(img, (5, 5), cv.BORDER_DEFAULT)
        object_name = recognize_object(img, classes, net, ln)
    if object_name in ['bottle', 'cup']:
        color = identify_color(img, ln, net)
        print(f"It's a {object_name} of color {color}" if color is not None else "I don't know that color.")
    elif object_name == 'cat':
        print("It's a cat.")
    elif object_name == 'cow':
        print("It's a cow.")
    elif object_name == 'dog':
        print("It's a dog.")
    else:
        print(f"Is this a {object_name}." if object_name != 'Unknown' else "I don't know this object.")


def main():
    classes, net, ln = initialize_network()

    images = load_images()
    for img in images:
        print(img[0], end=' -> ')
        process_item(classes, img[1], ln, net)


main()
