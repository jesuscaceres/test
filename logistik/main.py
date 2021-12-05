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


def initialize_network(folder_path: dir):
    # Load names of classes and get random colors
    classes = open(f'{folder_path}/coco.names').read().strip().split('\n')

    # Give the configuration and weight files for the model and load the network.
    net = cv.dnn.readNetFromDarknet(f'{folder_path}/yolov3.cfg', f'{folder_path}/yolov3.weights')
    net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

    # determine the output layer
    ln = net.getLayerNames()
    ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]

    return classes, net, ln


def load_images(folder_path: str):
    if os.path.exists(folder_path):
        filenames = [f'{folder_path}/{fn}' for fn in os.listdir(folder_path) if fn.endswith('.jpg')]
    else:
        raise FileNotFoundError

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


def get_object_info(classes, img, ln, net):
    color: str = ''
    object_name = recognize_object(img, classes, net, ln)
    if object_name not in ['bottle', 'cup']:
        img = cv.GaussianBlur(img, (5, 5), cv.BORDER_DEFAULT)
        object_name = recognize_object(img, classes, net, ln)
    if object_name in ['bottle', 'cup']:
        color = identify_color(img, ln, net)
    return object_name, color


def add_item(obj_dict, color):
    if len(color) > 0:
        if color not in obj_dict.keys():
            obj_dict[color] = 1
        else:
            obj_dict[color] += 1


def get_stock():
    config_path = "Config"
    images_path = f"{config_path}/Lote0001"
    bottles: dict = {}
    cups: dict = {}
    try:
        classes, net, ln = initialize_network(config_path)
    except FileNotFoundError:
        print(f"\n\t\tDirectory '{config_path}' not found.")
    else:
        try:
            images = load_images(images_path)
        except FileNotFoundError:
            print(f"\n\t\tDirectory '{images_path}' not found.")
        else:
            print("\n\t\tLoading...\n")
            for img in images:
                print(f"\n\t\tProcessing {img[0]}")
                object_name, color = get_object_info(classes, img[1], ln, net)
                if object_name == 'bottle':
                    add_item(bottles, color)
                elif object_name == 'cup':
                    add_item(cups, color)
                elif object_name == 'cat':
                    print("\n\t\tDANGER! There is a cat on the conveyor belt!!!")
                    input("\n\tPress ENTER to continue...")
    return bottles, cups
