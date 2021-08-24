import os
import json
from glob import glob

from os import system as terminal

def setup_yolo(objects):
    settings = json.load(open("settings.json","r")) 
    cmp_options = settings['compile_options']

    # write data/obj.names
    obj_names = open("data/obj.names", "w")
    for object in objects:
        obj_names.write(f"{object['name']}\n")
    obj_names.close()

    # write data/obj.data
    obj_data = open("data/obj.data", "w")
    class_num = len(objects)
    obj_data.write(f"classes= {class_num}\n")
    train_path = os.path.abspath("data/train.txt")
    test_path = os.path.abspath("data/test.txt")
    names_path = os.path.abspath("data/obj.names")
    backup_path = os.path.abspath("backup")
    obj_data.write(f"train  = {train_path}\nvalid  = {test_path}\nnames  = {names_path}\nbackup = {backup_path}\n")
    obj_data.close()

    # write data/test.txt
    test_txt = open("data/test.txt", "w")
    test_images = glob("data/test/*.png")
    for test_image in test_images:
        test_txt.write(test_image + "\n")
    test_txt.close()

    # write data/train.txt
    train_txt = open("data/train.txt", "w")
    train_images = glob("data/train/*.png")
    for train_image in train_images:
        train_txt.write(train_image + "\n")
    train_txt.close()

    # write darknet/Makefile
    makefile_lines = open("darknet/_Makefile", "r").readlines()
    makefile = open("darknet/Makefile", "w")
    makefile_lines[0] = f"GPU={cmp_options['GPU']}\n"
    makefile_lines[1] = f"CUDNN={cmp_options['CUDNN']}\n"
    makefile_lines[2] = f"CUDNN_HALF={cmp_options['CUDNN_HALF']}\n"
    makefile_lines[3] = f"OPENCV={cmp_options['OPENCV']}\n"
    makefile.writelines(makefile_lines)
    makefile.close()

    # write data/yolov3.cfg

    cfg_lines = open("data/yolov3.cfg", "r").readlines()
    obj_cfg = open("data/obj.cfg", "w")
    filter_num = (class_num+5)*5
    cfg_lines[3]   = f"height={settings['bg_size'][1]}\n"
    cfg_lines[4]   = f"width={settings['bg_size'][0]}\n"
    cfg_lines[223] = f"filters={filter_num}\n"
    cfg_lines[229] = f"classes={class_num}\n"
    obj_cfg.writelines(cfg_lines)
    obj_cfg.close()

    is_changed = False
    try:
        cache_file = open("cache.json","r+")
        cache = json.load(cache_file)
        for option in dict(cmp_options):
            if cmp_options[option] != cache[option]:
                is_changed = True
    except FileNotFoundError:
        if terminal("wget http://pjreddie.com/media/files/darknet19_448.conv.23 -P darknet/") == 0:
            is_changed = True
            cache_file = open("cache.json","w")
        else:
            print("[ERROR] Failed to fetch training weights. Check for network issues.")
            exit()
    if is_changed:
        cache_file.seek(0)
        if terminal("make -C darknet") == 0:
            json.dump(cmp_options, cache_file, indent=4)
        else:
            print("[ERROR] Failed to compile darknet. Check the log for details.")
            exit()
