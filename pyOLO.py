import sys
from glob import glob
from os import system as terminal

from src.generate_db import GenerateDB
from src.image_trimmer import Trim, CheckRequirements

BACKGROUND_SIZE = 608
OBJECT_SIZE = 96
DATASET_SIZE = 5

if __name__ == "__main__":
    background_paths = []
    objects = []

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

        GenerateDB(background_paths, objects, BACKGROUND_SIZE, OBJECT_SIZE, DATASET_SIZE)
        print("[Step 2] Done.")