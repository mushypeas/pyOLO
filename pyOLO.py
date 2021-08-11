import sys
from glob import glob

from src.generate_db import GenerateDB
from src.background_trimmer import Trim, CheckRequirements

EXTENSIONS = ["png", "jpg", "jpeg", "bmp"]
BACKGROUND_SIZE = 608
OBJECT_SIZE = 96
DATASET_SIZE = 20

if __name__ == "__main__":
    background_paths = []
    object_paths = []

    # get image paths
    for extension in EXTENSIONS:
        background_paths += glob("backgrounds/*." + extension)
    object_paths += glob("objects/*/")
if int(sys.argv[1]) <= 1:
    print("[Step 1] Trimming images")
    CheckRequirements()
    for object_path in object_paths:
        Trim(object_path, "white", 50, 10, EXTENSIONS) # TODO: should automate?
if int(sys.argv[1]) <= 2:
    print("[Step 2] Generating Dataset")
    GenerateDB(background_paths, object_paths, BACKGROUND_SIZE, OBJECT_SIZE, DATASET_SIZE)