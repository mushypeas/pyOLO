import random
import cv2
import numpy as np
import pyrealsense2 as rs

from . import darknet

def image_detection(color_image, network, class_names, class_colors, thresh):
    # Darknet doesn't accept numpy images.
    # Create one with image we reuse for each detect
    width = darknet.network_width(network)
    height = darknet.network_height(network)
    darknet_image = darknet.make_image(width, height, 3)

    image = color_image
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_resized = cv2.resize(image_rgb, (width, height),
                               interpolation=cv2.INTER_LINEAR)

    darknet.copy_image_from_bytes(darknet_image, image_resized.tobytes())
    detections = darknet.detect_image(network, class_names, darknet_image, thresh=thresh)
    darknet.free_image(darknet_image)
    image = darknet.draw_boxes(detections, image_resized, class_colors)
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB), detections

# yolo testing using images in a given path
def test_yolo_ii():
    pass

# yolo testing using images in data/test
def test_yolo_it():
    pass

# yolo testing using realsense
def test_yolo_rs():
    random.seed(3)  # deterministic bbox colors
    network, class_names, class_colors = darknet.load_network(
        "data/obj.cfg",
        "data/obj.data",
        "backup/obj_last.weights",
        batch_size=1
    )
    
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

        # loop asking for new image paths if no list is given

        image, detections = image_detection(
            color_image, network, class_names, class_colors, .25
        )

        cv2.imshow('Inference', image)
        cv2.waitKey(3)

def test_yolo(mode):
    if mode == "rs":
        test_yolo_rs()
    elif mode == "it":
        test_yolo_it()
    elif mode == "ii":
        test_yolo_ii()
