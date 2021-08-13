from PIL import Image
from glob import glob
from copy import copy

import random
import threading

data_idx = 0
data_count = 0

def GenerateData(_background, object_data_list, object_size, dataset_size):
    global data_idx

    for i in range(0, dataset_size):
        data_image = copy(_background)
        objects = []
        YOLO_txt = ""

        for object_data in object_data_list:
            object_class = object_data[0]
            object_file = random.choice(object_data[1])
            object_image = Image.open(object_file)
            object_image = object_image.resize((int(object_image.size[0]/object_image.size[1]*object_size), object_size)) 
            objects.append({"class": object_class, "image": object_image})

        for object in objects:
            # make data image
            object_w, object_h = object["image"].size
            background_w, background_h = data_image.size
            offset_w = random.randint(0, background_w-object_w)
            offset_h = random.randint(0, background_h-object_h)
            data_image.paste(object["image"], (offset_w, offset_h), object["image"])

            # make data txt
            x_center = round(((offset_w + int(object_w/2)) / background_w), 4)
            y_center = round(((offset_h + int(object_h/2)) / background_h), 4)
            YOLO_width = round((object_w / background_w), 4)
            YOLO_height = round((object_h / background_h), 4)
            YOLO_txt += "{} {} {} {} {}\n".format(object["class"], x_center, y_center, YOLO_width, YOLO_height)

        # ~80% of the data is used for training
        if i / dataset_size < 0.8:
            data_text = open("data/train/{}.txt".format(data_idx), "w")
            data_text.write(YOLO_txt)
            data_text.close()
            data_image.save("data/train/{}.png".format(data_idx))
        # rest of the data is used for testing
        else:
            data_text = open("data/test/{}.txt".format(data_idx), "w")
            data_text.write(YOLO_txt)
            data_text.close()
            data_image.save("data/test/{}.png".format(data_idx))

        data_idx += 1

def PrintLoading():
    while data_idx < data_count:
        print("Generating Data... [{}/{}]".format(data_idx+1, data_count), end="\r")

def GenerateDB(background_paths, objects, bg_size, object_size, dataset_size):
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

        image_paths = glob("{}/out/*.png".format(object["path"]))
        object_data_list.append((object_classes[object_name], image_paths))

    threading.Thread(target=PrintLoading).start()

    for background in backgrounds:
        GenerateData(background, object_data_list, object_size, dataset_size)
    print("")