import io
import json
import threading
import time

from glob import glob
from termcolor import colored
from os import system as terminal
from rembg.bg import remove
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

settings = json.load(open("settings.json", "r"))
EXTENSIONS = settings["extensions"]
THREADS = settings["threads"]
IMAGE_SIZE = 320

class BackgroundRemover:
    def __init__(self, object):
        self.image_paths = []
        self.object_path = object["path"]
        self.object_name = object["name"]
        self.image_count = 0
        self.image_idx = 0

    def CheckImagePath(self):
        for extension in EXTENSIONS:
            self.image_paths += glob(self.object_path + "/*" + extension)

        if len(self.image_paths) == 0:
            print(f"[ERROR] Invalid directory path '{self.object_path}', or no images with a valid extension in the given directory.\n")
            print(f"    Available extensions: {EXTENSIONS}\n")
            exit()
        self.image_count = len(self.image_paths)

    def _RemoveBackground(self, image_idx):
        if self.image_idx >= self.image_count:
            exit()
        for idx in range(image_idx, self.image_count, THREADS):
            image_path = self.image_paths[idx]
            image = Image.open(image_path)
            image_ratio = image.size[0] / image.size[1]
            image = image.resize((int(image_ratio*IMAGE_SIZE), IMAGE_SIZE))
            img_file = io.BytesIO()
            image.save(img_file, "PNG")
            result = remove(img_file.getbuffer(), alpha_matting=True)

            image = Image.open(io.BytesIO(result)).convert("RGBA")
            image.save(f'{self.object_path}/out/{image_idx}.png')

            image_idx += THREADS
            self.image_idx += 1

    def RemoveBackground(self):
        self.CheckImagePath()
        print("Current object:", colored(self.object_name, "green"))

        if len(glob(self.object_path + "/out/")) == 0:
            terminal(f"mkdir {self.object_path}/out")

        loading = threading.Thread(target=self.PrintLoading)
        loading.start()
        for i in range(0, THREADS):
            threading.Thread(target=self._RemoveBackground, args=[i]).start()
            time.sleep(0.3)
        loading.join()

    def PrintLoading(self):
        while self.image_idx < self.image_count:
            print(f"Converting images from '{self.object_path}'... [{self.image_idx+1}/{self.image_count}]", end="\r")
        print("")

def RemoveBackground(object):
    BackgroundRemover(object).RemoveBackground()