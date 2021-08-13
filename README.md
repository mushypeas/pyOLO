# pyOLO: Automated YOLOv3 training tool using Python

## Introduction
pyOLO is a tool written in Python that helps users train their data with YOLO easily. All you need is some initial setup and your images for training! This project cotains a darknet model cloned from:
`https://github.com/AlexeyAB/darknet.git`
Currently pyOLO mainly consists of 4 steps:
- Step 1: Trimming Images
- Step 2: Generating Dataset
- Step 3: Setting Up YOLO Environment
- Step 4: Run YOLO Training
- (TODO, maybe) Step 5: Run YOLO Testing

## Requirements
- **Linux** (Tested on: Ubuntu 18.04)
- **pip, python virtual environment** for basic environment setup
  - Run `sudo apt install python-pip python-venv` on your terminal to install.
  - You might have to install a specific version of venv, depending on your python version. e.g if you are using python3.9, you might have to run `sudo apt install python-pip python3.9-venv` instead.
- **ImageMagick** for image trimming
  - Run `sudo apt install imagemagick` on your terminal to install.
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
(TODO)
### 1. Preparing Images
### 2. Running pyOLO