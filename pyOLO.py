import sys
import json
from glob import glob
from os import system as terminal

from src.generate_db import GenerateDB
from src.image_trimmer import Trim, CheckRequirements
from src.yolo_setup import SetupYOLO

if __name__ == "__main__":
    background_paths = []
    objects = []

    settings = json.load(open("settings.json","r"))

    object_list = open("objects.txt", "r").read().splitlines()

    for _object in object_list:
        object = {}
        object["name"] = _object.split(" ")[0]
        object["path"] = f"objects/{object['name']}"
        object["mode"] =  _object.split(" ")[1]
        objects.append(object)
        
    # get image paths
    for extension in settings["extensions"]:
        background_paths += glob("backgrounds/*." + extension)

    if len(sys.argv) == 1:
        step = 1
    else:
        try:
            step = int(sys.argv[1])
        except TypeError:
            print("Usage: python pyOLO.py <step (1 - 4)>\n")
            exit()

    if step <= 1:
        print("[Step 1] Trimming images")

        # remove all previous data
        terminal("rm -rf objects/*/out/*.png")

        CheckRequirements()
        for object in objects:
            Trim(object)
        print("[Step 1] Done.")

    if step <= 2:
        print("[Step 2] Generating Dataset")

        # remove all previous data
        terminal("rm -rf data/*/images/*.png data/*/labels/*.txt")

        GenerateDB(background_paths, objects, settings["bg_size"], settings["object_size"], settings["dataset_size"])
        print("[Step 2] Done.")

    if step <= 3:
        print("[Step 3] Setup YOLO Environment")
        SetupYOLO()
        print("[Step 3] Done.")

    if step <= 4:
        print("[Step 4] Run YOLO training")
        terminal("./setup.sh")
        terminal("darknet/darknet detector train data/obj.data data/obj.cfg darknet/darknet53.conv.74")
        print("[Step 4] Done.")
