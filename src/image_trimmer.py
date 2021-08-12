import json
import requests
import threading

from glob import glob
from termcolor import colored
from os import system as terminal


API_KEY = '60d841675c6eda8e560aab1bbce1653ccd81f105'
settings = json.load(open("settings.json", "r"))
extensions = settings["extensions"]
COLOR_NAMES = open("data/colors.txt").read().splitlines()

class ImageTrimmer:
    def __init__(self, object):
        self.image_list = []
        self.object_path = object["path"]
        self.mode = object["mode"]
        self.object_name = object["name"]
        self.bg_color = "White"
        self.trim_fuzz = 50
        self.trans_fuzz = 10
        self.image_count = 0
        self.image_idx = 0

    def CheckImagePath(self):
        for extension in extensions:
            self.image_list += glob(self.object_path + "/*" + extension)

        if len(self.image_list) == 0:
            print("[ERROR] Invalid directory path '{}', or no images with a valid extension in the given directory.\n".format(self.object_path))
            print("    Available extensions: {}\n".format(extensions))
            self.ExitByError()
        self.image_count = len(self.image_list)

    def isColorValid(self, bg_color):
        # hex colors
        if bg_color[0] == "#":
            if len(bg_color[1:]) != 6 or int(bg_color[1:], 16) not in range(0, 0x1000000):
                print("Invalid RGB hex value '{}'.\n".format(bg_color))
                return False
        # named colors
        else:
            if bg_color not in COLOR_NAMES:
                print("Invalid color name '{}'. Check the valid colors list at: https://imagemagick.org/script/color.php \n".format(bg_color))
                return False
        return True

    def CheckColor(self):
        # hex colors
        if self.bg_color[0] == "#":
            if len(self.bg_color[1:]) != 6 or int(self.bg_color[1:], 16) not in range(0, 0x1000000):
                print("[ERROR] Invalid RGB hex value '{}'.\n".format(self.bg_color))
                self.ExitByError()
        # named colors
        else:
            if self.bg_color not in COLOR_NAMES:
                print("[ERROR] Invalid color name '{}'. Check the valid colors list at: https://imagemagick.org/script/color.php \n".format(self.bg_color))
                self.ExitByError()
    
    def isFuzzValid(self, trim_fuzz, trans_fuzz):
        try:
            trim_fuzz = int(trim_fuzz)
            trans_fuzz = int(trans_fuzz)
        except ValueError:
            print("Wrong fuzz value, must be an integer between 0 and 100.\n")
            return False
        if trim_fuzz not in range(0, 101) or trans_fuzz not in range(0, 101):
            print("Wrong fuzz value, must be an integer between 0 and 100.\n")
            return False
        return True

    def CheckFuzz(self):
        if self.trim_fuzz not in range(0, 101) or self.trans_fuzz not in range(0, 101):
            print("[ERROR] Wrong fuzz value, must be an integer between 0 and 100.\n")
            self.ExitByError()

    def QuickManualTrim(self):
        while True:
            args = input("Enter 3 arguments: [background_color] [trim_fuzz] [transparent_fuzz] (ex1) #FFFFFF 50 10 (ex2) white 40 15\n>> ").split(" ")
            if len(args) < 3:
                print("Insufficient number of arguments.")
                continue
            bg_color, trim_fuzz, trans_fuzz = args[0:3]
            if (self.isColorValid(bg_color) and self.isFuzzValid(trim_fuzz, trans_fuzz)):
                self.QuickTrim(trim_fuzz, trans_fuzz, bg_color)
                break

    def QuickAutoTrim(self):
        self.CheckColor()
        self.CheckFuzz()
        self.QuickTrim(self.trim_fuzz, self.trans_fuzz, self.bg_color)
        
    def QuickTrim(self, trim_fuzz, trans_fuzz, bg_color):
        threading.Thread(target=self.PrintLoading).start()

        for image in self.image_list:
            terminal("convert {} -resize 256 -fuzz {}% -trim -fuzz {}%% -transparent '{}' -trim {}/out/{}.png".format(
                image,
                trim_fuzz,
                trans_fuzz,
                bg_color,
                self.object_path,
                self.image_idx
            ))
            self.image_idx += 1

    def SlowTrim(self):
        global image_idx

        threading.Thread(target=self.PrintLoading).start()

        for image in self.image_list:
            terminal("convert {} -resize 512x {}/temp/temp0.png".format(
                image,
                self.object_path,
            ))

            response = requests.post(
                'https://api.pixmiller.com/v1/remove',
                files={'image_file': open("{}/temp/temp0.png".format(self.object_path), 'rb')},
                headers={'X-Api-Key': API_KEY},
            )
            if response.status_code == 201:
                with open('{}/temp/temp1.png'.format(self.object_path), 'wb') as out:
                    img_removed_url = response.json()["url"]
                    out.write(requests.get(img_removed_url).content)
            else:
                print("\nError:", response.status_code, response.text, "\n")

            terminal("convert {}temp/temp1.png -gravity South -chop x30 -trim {}/out/{}.png".format(
                self.object_path,
                self.object_path,
                image_idx
            ))

            image_idx += 1
        terminal("rm -rf {}/temp".format(self.object_path))

    def Trim(self):
        self.CheckImagePath()
        print("Current object:", colored(self.object_name, "green"))

        if len(glob(self.object_path + "/out/")) == 0:
            terminal("mkdir {}/out".format(self.object_path))

        if len(glob(self.object_path + "/temp/")) == 0:
            terminal("mkdir {}/temp".format(self.object_path))

        if self.mode == "qa" or self.mode == "q":
            print(" - Quick Auto trimming mode - ")
            self.QuickAutoTrim()
        elif self.mode == "qm":
            print(" - Quick manual trimming mode - ")
            self.QuickManualTrim()
        elif self.mode == "s":
            print(" - Slow API trimming mode - ")
            self.SlowTrim()

    def ExitByError(self):
        print("======================= BackgroundTrimmer Usage ==================================\n")
        print("    [usage 1] python process_images.py <background_color>")
        print("    [usage 2] python process_images.py <img_dir_path> <background_color>")
        print("    [usage 3] python process_images.py <background_color> <trim_fuzz> <transparent_fuzz>")
        print("    [usage 4] python process_images.py <img_dir_path> <background_color> <trim_fuzz> <transparent_fuzz>")
        print("          ex) python process_images.py ~/Downloads '#FFFFFF' 50 20\n")
        exit()

    def PrintLoading(self):
        while self.image_idx < self.image_count:
            print("Converting images from '{}'... [{}/{}]".format(self.object_path, self.image_idx+1, self.image_count), end="\r")
        print("")

def CheckRequirements():
    if terminal("type convert") & 0xFF00 != 0:
        print("[ERROR] ImageMagick is not properly installed in your system. Try running:\n")
        print("        sudo apt install imagemagick\n")
        ImageTrimmer.ExitByError()

    print("ImageMagick properly installed.\n")

def Trim(object):
    ImageTrimmer(object).Trim()

    print("")