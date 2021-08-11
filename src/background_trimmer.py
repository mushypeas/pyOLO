from glob import glob
from os import system as terminal
# import cv2 as cv


# TODO: give more flexibility to arguments

class BackgroundTrimmer:
    def __init__(self, image_path, bg_color, trim_fuzz, trans_fuzz):
        self.color_names = open("colors.txt").read().splitlines()
        self.image_list = []
        self.image_path = image_path
        self.bg_color = bg_color
        self.trim_fuzz = trim_fuzz
        self.trans_fuzz = trans_fuzz

    def CheckImagePath(self, extensions):
        for extension in extensions:
            self.image_list += glob(self.image_path + "/*" + extension)

        if len(self.image_list) == 0:
            print("[ERROR] Invalid directory path '{}', or no images with a valid extension in the given directory.\n".format(self.image_path))
            print("    Available extensions: {}\n".format(extensions))
            self.ExitByError()
        return len(self.image_list)

    def CheckColor(self):
        # hex colors
        if self.bg_color[0] == "#":
            if len(self.bg_color[1:]) != 6 or int(self.bg_color[1:], 16) not in range(0, 0x1000000):
                print("[ERROR] Invalid RGB hex value '{}'.\n".format(self.bg_color))
                self.ExitByError()
        # named colors
        else:
            if self.bg_color not in self.color_names:
                print("[ERROR] Invalid color name '{}'. Check the valid colors list at: https://imagemagick.org/script/color.php \n".format(bg_color))
                self.ExitByError()
    
    def CheckFuzz(self):
        if self.trim_fuzz not in range(0, 101) or self.trans_fuzz not in range(0, 101):
            print("[ERROR] Wrong fuzz value, must be an integer between 0 and 100.\n")
            self.ExitByError()

    def Trim(self):
        i = 0
        for image in self.image_list:
            # print("converting '{}'...".format(image))
            terminal("convert {} -resize 256 -fuzz {}% -trim -fuzz {}%% -transparent '{}' -trim {}/out/{}.png".format(image, self.trim_fuzz, self.trans_fuzz, self.bg_color, self.image_path, i))
            i += 1

    def ExitByError(self):
        print("======================= BackgroundTrimmer Usage ==================================\n")
        print("    [usage 1] python process_images.py <background_color>")
        print("    [usage 2] python process_images.py <img_dir_path> <background_color>")
        print("    [usage 3] python process_images.py <background_color> <trim_fuzz> <transparent_fuzz>")
        print("    [usage 4] python process_images.py <img_dir_path> <background_color> <trim_fuzz> <transparent_fuzz>")
        print("          ex) python process_images.py ~/Downloads '#FFFFFF' 50 20\n")
        exit()

def CheckRequirements():
    if terminal("type convert") & 0xFF00 != 0:
        print("[ERROR] ImageMagick is not properly installed in your system. Try running:\n")
        print("        sudo apt install imagemagick\n")
        BackgroundTrimmer.ExitByError()

    print("ImageMagick properly installed...\n")

def Trim(image_path, bg_color, trim_fuzz, trans_fuzz, extensions):
    trimmer = BackgroundTrimmer(image_path, bg_color, trim_fuzz, trans_fuzz)

    image_num = trimmer.CheckImagePath(extensions)
    trimmer.CheckColor()
    trimmer.CheckFuzz()

    print("Converting {} images from '{}'...".format(image_num, image_path))

    if len(glob(image_path + "/out/")) == 0:
        terminal("mkdir {}/out".format(image_path))

    trimmer.Trim()