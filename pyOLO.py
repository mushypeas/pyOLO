import sys
import json
from glob import glob
from os import system as terminal

from src.generate_db import GenerateDB
from src.image_trimmer import Trim, CheckRequirements

if __name__ == "__main__":
    background_paths = []
    objects = []

    settings = json.load(open("data/settings.json","r"))

    object_list = open("data/objects.txt", "r").read().splitlines()

    for _object in object_list:
        object = {}
        object["name"] = _object.split(" ")[0]
        object["path"] = f"objects/{object['name']}"
        object["mode"] =  _object.split(" ")[1]
        objects.append(object)
        
    # get image paths
    for extension in settings["extensions"]:
        background_paths += glob("backgrounds/*." + extension)
        
    if int(sys.argv[1]) <= 1:
        print("[Step 1] Trimming images")

        # remove all previous data
        terminal("rm -rf objects/*/out/*.png")

        CheckRequirements()
        for object in objects:
            Trim(object)
        print("[Step 1] Done.")

    if int(sys.argv[1]) <= 2:
        print("[Step 2] Generating Dataset")

        # remove all previous data
        terminal("rm -rf images/*/*.png images/*/*.txt")

        GenerateDB(background_paths, objects, settings["bg_size"], settings["object_size"], settings["dataset_size"])
        print("[Step 2] Done.")