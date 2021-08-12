import json
from glob import glob

def SetupYOLO():
    objects = open("objects.txt","r").read().splitlines()
    settings = json.load(open("settings.json","r"))

    # write data/obj.names
    obj_names = open("data/obj.names", "w")
    for object in objects:
        obj_names.write(object.split(" ")[0])
    obj_names.close()

    # write data/obj.data
    obj_data = open("data/obj.data", "w")
    class_num = len(objects)
    obj_data.write(f"classes= {class_num}\n")
    obj_data.write("train  = ../data/train.txt\nvalid  = ../data/test.txt\nnames  = ../data/obj.names\nbackup = backup/\n")
    obj_data.close()

    # write data/test.txt
    test_txt = open("data/test.txt", "w")
    test_images = glob("images/test/*.png")
    for test_image in test_images:
        test_txt.write(test_image + "\n")
    test_txt.close()

    # write data/train.txt
    train_txt = open("data/train.txt", "w")
    train_images = glob("images/train/*.png")
    for train_image in train_images:
        train_txt.write(train_image + "\n")
    train_txt.close()

    # write data/yolov3.cfg
    cfg_lines = open("data/yolov3.cfg", "r").readlines()
    obj_cfg = open("data/obj.cfg", "w")
    filter_num = (class_num+5)*3
    cfg_lines[7]   = f"width={settings['bg_size'][0]}\n"
    cfg_lines[8]   = f"height={settings['bg_size'][1]}\n"
    cfg_lines[19]  = f"max_batches={class_num*4000}\n"
    cfg_lines[21]  = f"steps={class_num*1600},{class_num*1800}\n"
    cfg_lines[602] = f"filters={filter_num}\n"
    cfg_lines[609] = f"classes={class_num}\n"
    cfg_lines[688] = f"filters={filter_num}\n"
    cfg_lines[695] = f"classes={class_num}\n"
    cfg_lines[775] = f"filters={filter_num}\n"
    cfg_lines[782] = f"classes={class_num}\n"
    obj_cfg.writelines(cfg_lines)
    obj_cfg.close()