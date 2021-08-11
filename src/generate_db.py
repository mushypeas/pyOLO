from cv2 import data
from PIL import Image
from glob import glob
import random
import copy
data_count = 0

def Resize(image, image_h, is_background):
    image_w = int(image.size[0]/image.size[1] * image_h)
    if is_background:
        image_w -= image_w%32
    return image.resize((image_w, image_h))

def GenerateDataImage(_background, object_lists, object_size, dataset_size):
    global data_count

    objects = []
    for object_list in object_lists:
        object_image = Image.open(random.choice(object_list))
        objects.append(Resize(object_image, object_size, is_background=False))
        # objects.append(object_image)
        
    for i in range(0, dataset_size):
        background = copy.copy(_background)

        for object in objects:
            object_w, object_h = object.size
            background_w, background_h = background.size
            offset_w = int(object_w/2) + random.randint(0, background_w-object_w)
            offset_h = int(object_h/2) + random.randint(0, (background_h-object_h))

            background.paste(object, (offset_w, offset_h), object)

        # ~80% of the data is used for training
        if i / dataset_size < 0.8:
            background.save("images/train/{}.png".format(data_count))
        # rest of the data is used for testing
        else:
            background.save("images/test/{}.png".format(data_count))

        data_count += 1

def GenerateDB(background_paths, object_paths, background_size, object_size, dataset_size):
    backgrounds = []
    object_lists = []
    # store resized images to list
    for background_path in background_paths:
        background = Resize(Image.open(background_path), background_size, is_background=True)
        backgrounds.append(background)

    for object_path in object_paths:
        image_paths = glob("{}/out/*.png".format(object_path))
        object_lists.append(image_paths)

    for background in backgrounds:
        GenerateDataImage(background, object_lists, object_size, dataset_size)