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


    for object_name in settings["objects"]:
        object = {}
        name_end = object_name.split(" ")[-1]
        if name_end in ["q", "qm", "s"]:
            object["name"] = object_name.replace(f" {name_end}", "")
            object["mode"] =  object_name.split(" ")[-1]
        else:
            object["name"] = object_name
            object["mode"] = "q"
        object["path"] = f"objects/{object['name']}"
        objects.append(object)
        
    # get image paths
    for extension in settings["extensions"]:
        background_paths += glob("backgrounds/*." + extension)

    if len(sys.argv) == 1:
        step = 0
    else:
        try:
            step = int(sys.argv[1])
            if step < 1 or step > 4:
                raise ValueError
        except ValueError:
            print("Usage 1: python pyOLO.py              <= Run whole process")
            print("Usage 2: python pyOLO.py <step(1-4)>  <= Run single step\n")
            print("    [Step 1] Trimming images")
            print("    [Step 2] Generating Dataset")
            print("    [Step 3] Setup YOLO Environment")
            print("    [Step 4] Run YOLO training\n")
            exit()
        
    if step in [0,1]:
        print("[Step 1] Trimming images")

        # remove all previous data
        terminal("rm -rf objects/*/out/*.png")

        CheckRequirements()
        for object in objects:
            Trim(object)
        print("[Step 1] Done.")

    if step in [0,2]:
        print("[Step 2] Generating Dataset")

        # remove all previous data
        terminal("rm -rf data/*/*.png data/*/*.txt")

        GenerateDB(background_paths, objects, settings["bg_size"], settings["dataset_size"])
        print("[Step 2] Done.")

    if step in [0,3]:
        print("[Step 3] Setup YOLO Environment")
        SetupYOLO()
        print("[Step 3] Done.")

    if step in [0,4]:
        print("[Step 4] Run YOLO training")
        weights = glob("darknet/backup/*.weights")
        if len(weights) > 0:
            terminal(f"darknet/darknet detector train data/obj.data data/obj.cfg {weights[0]}")
        else:
            terminal("darknet/darknet detector train data/obj.data data/obj.cfg darknet/darknet19_448.conv.23")
        print("[Step 4] Done.")
