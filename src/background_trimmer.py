import sys
from glob import glob
from os import system as terminal

# TODO: give more flexibility to arguments

class BackgroundTrimmer:
    def __init__(self, args):
        self.args = args
        self.extensions = ["png", "jpg", "jpeg", "bmp"]
        self.image_list = []
        self.save_path = "~"
        self.trim_fuzz = 50
        self.transparent_fuzz = 10
        self.bg_color = ""
        self.color_names = open("colors.txt").read().splitlines()

    def Run(self):
        print("Python Image Background Trimmer\n")

        self.CheckRequirements()
        self.AssignArgs(self.args)
        self.CheckArgs()

        print("{} images found in '{}'.\n".format(len(self.image_list), self.save_path))

        if len(glob(self.save_path + "/out/")) == 0:
            terminal("mkdir {}/out".format(self.save_path))

        i = 0
        for image in self.image_list:
            print("converting '{}'...".format(image))
            terminal("convert {} -resize 256 -fuzz {}% -trim -fuzz {}%% -transparent '{}' -trim {}/out/{}.png".format(image, self.trim_fuzz, self.transparent_fuzz, self.bg_color, self.save_path, i))
            i += 1

        print("\nDone! Converted images are saved in '{}out'.".format(self.save_path))

    def CheckRequirements(self):
        if terminal("type convert") & 0xFF00 != 0:
            print("[ERROR] ImageMagick is not properly installed in your system. Try running:\n")
            print("        sudo apt install imagemagick\n")
            self.ExitByError()

        print("ImageMagick properly installed...\n")

    def AssignArgs(self, args):
        if len(args) not in range(2, 6):
            print("[ERROR] Wrong number of arguments: requires 1 ~ 4, given {}.\n".format(len(args)-1))
            self.ExitByError()

        if len(args) == 2:
            self.bg_color = args[1]

        elif len(args) == 3:
            self.save_path = args[1]
            self.bg_color = args[2]

        elif len(args) == 4:
            self.bg_color = args[1]
            self.trim_fuzz = int(args[2])
            self.transparent_fuzz = int(args[3])

        elif len(args) == 5:
            self.save_path = args[1]
            self.bg_color = args[2]
            self.trim_fuzz = int(args[3])
            self.transparent_fuzz = int(args[4])

        if self.save_path[-1] != "/":
            self.save_path += "/"

    def CheckArgs(self):
        self.CheckSavePath(self.save_path, self.extensions)
        self.CheckColor(self.bg_color, self.color_names)
        self.CheckFuzz(self.trim_fuzz, self.transparent_fuzz)

    def CheckSavePath(self, save_path, extensions):
        for extension in extensions:
            self.image_list += glob(save_path + "/*" + extension)

        if len(self.image_list) == 0:
            print("[ERROR] Invalid directory path '{}', or no images with a valid extension in the given directory.\n".format(save_path))
            print("    Available extensions: {}\n".format(extensions))
            self.ExitByError()

    def CheckColor(self, bg_color, color_names):
        # hex colors
        if bg_color[0] == "#":
            if len(bg_color[1:]) != 6 or int(bg_color[1:], 16) not in range(0, 0x1000000):
                print("[ERROR] Invalid RGB hex value '{}'.\n".format(bg_color))
                self.ExitByError()
        # named colors
        else:
            if bg_color not in color_names:
                print("[ERROR] Invalid color name '{}'. Check the valid colors list at: https://imagemagick.org/script/color.php \n".format(bg_color))
                self.ExitByError()
    
    def CheckFuzz(self, trim_fuzz, transparent_fuzz):
        if int(trim_fuzz) not in range(0, 101) or int(transparent_fuzz) not in range(0, 101):
            print("[ERROR] Wrong fuzz value, must be an integer between 0 and 100.\n")
            self.ExitByError()

    def ExitByError(self):
        print("======================= BackgroundTrimmer Usage ==================================\n")
        print("    [usage 1] python process_images.py <background_color>")
        print("    [usage 2] python process_images.py <img_dir_path> <background_color>")
        print("    [usage 3] python process_images.py <background_color> <trim_fuzz> <transparent_fuzz>")
        print("    [usage 4] python process_images.py <img_dir_path> <background_color> <trim_fuzz> <transparent_fuzz>")
        print("          ex) python process_images.py ~/Downloads '#FFFFFF' 50 20\n")
        exit()

if __name__ == "__main__":
    BackgroundTrimmer(sys.argv).Run()