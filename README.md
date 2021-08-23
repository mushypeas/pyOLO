# pyOLO: Automated YOLOv3 training tool using Python

## Introduction
pyOLO is a tool written in Python that helps users train their data with YOLO easily. All you need is some initial setup and your images for training! This project cotains a darknet model cloned from:
`https://github.com/AlexeyAB/darknet.git`

Currently pyOLO mainly consists of 4 steps:
- Step 1: Preparing Object Images
- Step 2: Generating Dataset
- Step 3: Setting Up YOLO Environment
- Step 4: Run YOLO Training
- (TODO, maybe) Step 5: Run YOLO Testing

## Requirements
- **Linux** (Tested on: Ubuntu 18.04)
- **pip, python virtual environment** for basic environment setup
  - Run `sudo apt install python-pip python-venv` on your terminal to install.
  - You might have to install a specific version of venv, depending on your python version. e.g if you are using python3.9, you might have to run `sudo apt install python-pip python3.9-venv` instead.
- **darknet Requirements** check `https://github.com/AlexeyAB/darknet#requirements-for-windows-linux-and-macos`

## How To Use

### 0. Initial Setup
- You only have go get through this step once for each device.
- clone this repository to your workspace, and move to the pyOLO directory.
```
git clone https://github.com/mushypeas/pyOLO.git
cd pyOLO
```
- Make & activate a virtual environment. If you don't know how, just run the following lines:
```
python3 -m venv ~/venv/pyOLO
echo alias pyolo='source ~/venv/pyOLO/bin/activate' >> ~/.bashrc
pyolo
```
Now, simply running `pyolo` on your terminal will activate your virtual environment. If you want to exit the virtual environment, run `deactivate` on your terminal.
- Install the required python libraries by running
```
pip install -r requirements.txt
```
### 1. Preparing Images
- Take Pictures of Background Images
(TODO)
- Take Pictures of Object Images
(TODO)
- Import Background Images to Project
Move the background images to `pyOLO/backgrounds`.
- Import Object Images to Project
Move the images of an object in a **directory named as the object's YOLO class name**, and move those directories into `pyOLO/objects`. The name of the images doesn't matter. For example, if you want to train YOLO to recognize a dog and a tuna can, the hierarchy would be as follows:
```
pyOLO
├── objects
│   ├── dog
│   │   ├── firstdog.png
│   │   ├── second_dog.jpg
│   │   ├── ...
│   │   └── lastdog.png
│   └── tuna can
│       ├── tuna01.png
│       ├── tuunatwo.jpg
│       ├── ...
│       └── finalTunaCan.png
├── ...
```
... And your all set!

### 2. Running pyOLO

*Dont forget to activate the virtual environment!
Before runnung pyOLO, you'll have to edit `pyOLO/settings.json`.
```json
# settings.json
{
    "extensions": ["png", "PNG", "jpg", "JPG", "jpeg", "JPEG", "bmp", "BMP"],
    "bg_size": [640, 480],
    "dataset_size": 10,
    "threads": 2,
    "compile_options": {
        "GPU": 0,
        "CUDNN": 0,
        "CUDNN_HALF": 0,
        "OPENCV": 0
    }
}
```
  - **extensions:** `[ext1, ext2, ...]`The allowed extensions of background/object images. Mostly you would't need to change this.
  - **bg_size:** `[width, height]` Resolution of the background image in pixels. 
  - **dataset_size:** Generated YOLO dataset per background. YOLO would train & test with `<dataset_size> * <number of background images>`.
  - **threads:** Number of threads to run Step 1 and Step 2.
  - **compile_options:** Compilation options for YOLO darknet. Use only if you satisfied the requirements.

  
If it's the first time running pyOLO, just run
```
python pyOLO.py
```
from the project root directory.