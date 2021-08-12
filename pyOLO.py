import sys
import json
from glob import glob
from os import system as terminal

from src.generate_db import GenerateDB
from src.image_trimmer import Trim, CheckRequirements

if __name__ == "__main__":
    background_paths = []
    objects = []

    settings = json.load(open("settings.json","r"))

    extensions = open("extensions.txt", "r").read().splitlines()
    settings_list = open("settings.txt", "r").read().splitlines()

    for settings in settings_list:
        object = {}
        object["name"] = settings.split(" ")[0]
        object["path"] = f"objects/{object['name']}"
        object["mode"] =  settings.split(" ")[1]
        objects.append(object)
        
    # get image paths
    for extension in extensions:
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