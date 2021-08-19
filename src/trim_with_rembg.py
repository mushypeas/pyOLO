from rembg.bg import remove
import numpy as np
import io
import json
from PIL import Image, ImageFile
from glob import glob
from os import system as terminal
import os
from tqdm import tqdm
ImageFile.LOAD_TRUNCATED_IMAGES = True


input_path = '/home/tidy/workspace/pyOLO/objects/soap'
output_path = '/home/tidy/workspace/pyOLO/objects/soap/out/'

image_list = []
image_list += glob(input_path + "/*" + 'jpg')
for i, image in tqdm(enumerate(image_list)):
    f = np.fromfile(image)
    result = remove(f)
    img = Image.open(io.BytesIO(result)).convert("RGBA")
    img.save(output_path + '{}.png'.format(i))
