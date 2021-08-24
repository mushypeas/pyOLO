import random
import cv2
import os
import numpy as np
from numpy.lib.type_check import imag
import pyrealsense2 as rs

from glob import glob
from PIL import Image

from . import darknet

# yolo image detection threshold vlaue
THRESHOLD = 0.25

def image_detection(color_image, darknet_network, thresh, is_realsense):
    # Darknet doesn't accept numpy images.
    # Create one with image we reuse for each detect
    network, class_names, class_colors = darknet_network
    width = darknet.network_width(network)
    height = darknet.network_height(network)
    darknet_image = darknet.make_image(width, height, 3)

    image = color_image
    # change RGB values for realsense
    if is_realsense:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_resized = cv2.resize(image, (width, height),
                               interpolation=cv2.INTER_LINEAR)

    darknet.copy_image_from_bytes(darknet_image, image_resized.tobytes())
    detections = darknet.detect_image(network, class_names, darknet_image, thresh=thresh)
    darknet.free_image(darknet_image)
    image = darknet.draw_boxes(detections, image_resized, class_colors)
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB), detections

# yolo testing using images in a given path
def test_yolo_ii(network):
    while True:
        image_path = input("\nInput image path, or q to exit.\n>> ")
        if image_path.lower() == "q":
            exit()
        elif os.path.isfile(image_path):
            color_image = np.asarray(Image.open(image_path))
            image, detections = image_detection(
                color_image, network, THRESHOLD, False
            )

            cv2.imshow(os.path.basename(image_path), image)
            cv2.waitKey()
        else:
            print(f"Invalid image path \"{image_path}\".")

# yolo testing using images in data/test
def test_yolo_it(network):
    test_images = glob("data/test/*.png")
    for test_image in test_images:
        color_image = np.asarray(Image.open(test_image))
        image, detections = image_detection(
            color_image, network, THRESHOLD, False
        )

        cv2.imshow(os.path.basename(test_image), image)
        print("Press Enter/Space to continue, ESC to exit.")
        input_key = cv2.waitKeyEx()
        if input_key == 27:
            exit()

# yolo testing using realsense
def test_yolo_rs(network):
    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    # Start streaming
    pipeline.start(config)

    while True:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())

        image, detections = image_detection(
            color_image, network, THRESHOLD, True
        )

        cv2.imshow('Inference', image)
        cv2.waitKey(3)

def test_yolo(mode):
    random.seed(3)  # deterministic bbox colors
    network = darknet.load_network(
        "data/obj.cfg",
        "data/obj.data",
        "backup/obj_last.weights",
        batch_size=1
    )
    if mode == "rs":
        test_yolo_rs(network)
    elif mode == "it":
        test_yolo_it(network)
    elif mode == "ii":
        test_yolo_ii(network)
