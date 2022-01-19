from rembg.bg import remove
import numpy as np
import io
from PIL import Image, ImageFile
import os
ImageFile.LOAD_TRUNCATED_IMAGES = True

input_path = '/home/tidy/workspace/pyOLO/objects/toycar/'
img_list = os.listdir(input_path)


f = np.fromfile(input_path+img_list[1])
result = remove(f, alpha_matting=True,
                alpha_matting_foreground_threshold=254,
                alpha_matting_background_threshold=253)
img = Image.open(io.BytesIO(result)).convert("RGBA")
img.save(input_path+'test.png')