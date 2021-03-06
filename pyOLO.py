import sys
import json
from glob import glob
from os import system as terminal

from src.generate_db import generate_db
from src.background_remover import remove_background
from src.yolo_setup import setup_yolo
from src.yolo_test import test_yolo

MAX_STEPS = 5

if __name__ == "__main__":
    background_paths = []
    objects = []

    settings = json.load(open("settings.json","r"))

    object_paths = glob("objects/*")
    for object_path in object_paths:
        object = {}
        object["name"] = object_path.split("/")[1]
        object["path"] = object_path
        objects.append(object)
        
    # get image paths
    for extension in settings["extensions"]:
        background_paths += glob("backgrounds/*." + extension)

    if len(sys.argv) == 1:
        step = 0
    else:
        try:
            step = int(sys.argv[1])
            if step < 1 or step > MAX_STEPS:
                raise ValueError
        except ValueError:
            print("Usage 1: python pyOLO.py              <= Run whole process")
            print(f"Usage 2: python pyOLO.py <step(1-{MAX_STEPS})>  <= Run single step\n")
            print("    [Step 1] Preparing Object Images")
            print("    [Step 2] Generating Dataset")
            print("    [Step 3] Setup YOLO Environment")
            print("    [Step 4] Run YOLO Training\n")
            print("    [Step 5] Run YOLO Testing\n")
            exit()
        
    if step in [0,1]:
        print("[Step 1] Preparing Object Images")

        # remove all previous data
        terminal("rm -rf objects/*/out/*.png")

        for object in objects:
            remove_background(object)
        print("[Step 1] Done.")

    if step in [0,2]:
        print("[Step 2] Generating Dataset")

        # remove all previous data
        terminal('find data/train/ -name "*.png" -delete')
        terminal('find data/train/ -name "*.txt" -delete')
        terminal('find data/test/ -name "*.png" -delete')
        terminal('find data/test/ -name "*.txt" -delete')

        generate_db(background_paths, objects, settings["bg_size"], settings["dataset_size"])
        print("[Step 2] Done.")

    if step in [0,3]:
        print("[Step 3] Setup YOLO Environment")
        setup_yolo(objects)
        print("[Step 3] Done.")

    if step in [0,4]:
        print("[Step 4] Run YOLO Training")

        # start training from the last weights if possible
        weights = glob("backup/obj_last.weights")
        if len(weights) > 0:
            terminal("darknet/darknet detector train data/obj.data data/obj.cfg backup/obj_last.weights")
        else:
            terminal("darknet/darknet detector train data/obj.data data/obj.cfg darknet/darknet19_448.conv.23")
        print("[Step 4] Done.")

    if step in [0,5]:
        print("[Step 5] Run YOLO Testing")
        while True:
            mode = input("Select type of testing(rs/it/ii):\n\n\
    rs: Test realtime videos using realsense\n\
    it: Test images in data/test\n\
    ii: Test image at a given path\n\n>> ").lower()
            if mode in ["rs", "it", "ii"]:
                test_yolo(mode)
                break
            else:
                print("Invalid testing mode.")
