import json
import random
from threading import Thread, Lock

from PIL import Image, ImageEnhance
from glob import glob
from copy import copy

idx_lock = Lock()
data_idx = 0
data_count = 0
settings = json.load(open("settings.json", "r"))
THREADS = settings["threads"]

def generate_data(init_idx, backgrounds, object_data_list, dataset_size):
    global data_idx

    for bg_idx in range(init_idx, len(backgrounds), THREADS):
        for i in range(0, dataset_size):
            data_image = copy(backgrounds[bg_idx])
            background_w, background_h = data_image.size
            objects = []
            YOLO_txt = ""

            for object_data in object_data_list:
                object_class = object_data[0]
                object_file = random.choice(object_data[1])
                object_image = Image.open(object_file)
                
                # process chosen object image
                object_image = ImageEnhance.Brightness(object_image).enhance(random.uniform(0.5, 1.5))
                object_image = object_image.rotate(random.uniform(0.0, 360.0), expand=True, resample=Image.BICUBIC)
                object_image = object_image.crop(object_image.getbbox())
                if object_image.size[0] < object_image.size[1]:
                    object_h = int(background_h / random.uniform(5.0, 8.0))
                    object_w = int(object_image.size[0] / object_image.size[1] * object_h)
                else:
                    object_w = int(background_w / random.uniform(5.0, 8.0))
                    object_h = int(object_image.size[1] / object_image.size[0] * object_w)
                object_image = object_image.resize((object_w, object_h)) 

                # make data image
                offset_w = random.randint(0, background_w-object_w)
                offset_h = random.randint(0, background_h-object_h)
                data_image.paste(object_image, (offset_w, offset_h), object_image)

                # make data txt
                x_center = round(((offset_w + int(object_w/2)) / background_w), 4)
                y_center = round(((offset_h + int(object_h/2)) / background_h), 4)
                YOLO_width = round((object_w / background_w), 4)
                YOLO_height = round((object_h / background_h), 4)
                YOLO_txt += f"{object_class} {x_center} {y_center} {YOLO_width} {YOLO_height}\n"

            # ~80% of the data is used for training
            idx_lock.acquire()
            if i / dataset_size < 0.8:
                data_text = open(f"data/train/{data_idx}.txt", "w")
                data_text.write(YOLO_txt)
                data_text.close()
                data_image.save(f"data/train/{data_idx}.png")
            # rest of the data is used for testing
            else:
                data_text = open(f"data/test/{data_idx}.txt", "w")
                data_text.write(YOLO_txt)
                data_text.close()
                data_image.save(f"data/test/{data_idx}.png")
            data_idx += 1
            idx_lock.release()

def print_loading():
    while data_idx < data_count:
        print(f"Generating Data... [{data_idx+1}/{data_count}]", end="\r")
    print("")

def generate_db(background_paths, objects, bg_size, dataset_size):
    global data_count, data_idx

    print("Loading Images...")

    # load resized backgrounds
    backgrounds = []
    for background_path in background_paths:
        background = Image.open(background_path).resize(bg_size)
        backgrounds.append(background)

    data_count = len(backgrounds) * dataset_size

    # load object image paths
    object_classes = {}
    object_data_list = []
    object_id = 0

    for object in objects:
        object_name = object["name"]
        if object_name not in object_classes.keys():
            object_classes[object_name] = object_id
            object_id += 1

        image_paths = glob(f"{object['path']}/out/*.png")
        object_data_list.append((object_classes[object_name], image_paths))

    loading = Thread(target=print_loading)
    loading.start()
    for init_idx in range(0, THREADS):
        Thread(target=generate_data, args=[init_idx, backgrounds, object_data_list, dataset_size]).start()
    loading.join()