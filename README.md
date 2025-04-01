# Dual Raspberry Pi Camera Controller
## Overview
This Python script provides a user interface to control two Raspberry Pi cameras at the same time. It allows you to view the live feed from both cameras, switch between them, capture images, adjust resolution, exposure, and brightness. The captured images are saved with timestamps in a designated directory.

## Features
+ Dual Camera Support: Controls two Raspberry Pi cameras connected to the device.
+ Live Preview: Displays a combined live preview from both cameras.
+ Camera Selection: Allows switching the active camera for individual control.
+ Image Capture: Captures and saves images from the selected camera or both.
+ Resolution Control: Cycles through predefined resolution options for both cameras.
+ Exposure Adjustment: Increases or decreases the exposure compensation for the active camera.
+ Brightness Adjustment: Increases or decreases the brightness for the active camera.
+ Information Overlay: Displays timestamp, resolution, exposure, and brightness on the preview.
+ Preview Toggle: Allows pausing and resuming the live preview.
+ User-Friendly Controls: Utilizes keyboard input for easy control of camera functions.
## Prerequisites
### Hardware:
+ Raspberry Pi (tested with versions supporting Picamera2)
+ Two Raspberry Pi cameras connected to the Raspberry Pi.
### Software:
+ Raspberry Pi OS (with necessary camera drivers enabled)
+ Python 3
+ picamera2 library: Install using `sudo apt install python3-picamera2`
+ opencv-python library: Install using `sudo apt install python3-opencv`
+ numpy library: Install using `sudo apt install python3-numpy`
## Installation
### Clone the repository:
```shell
git clone https://github.com/Dion4cen/Dual_Cam_Controller.git
```
## Usage
1. Navigate to the project directory:
```shell
cd Dual_Cam_Controller
```
2. Run the script:
```shell
python dual_cam_capture.py
```
3. Control the application using the following keyboard inputs:
```
Controls:
 1, 2     - Select Camera 1 or 2
 s         - Save image from active camera
 d         - Save images from both cameras
 r         - Change resolution
 e/c       - Increase/decrease exposure of active camera
 b/v       - Increase/decrease brightness of active camera
 p         - Pause/resume preview
 q         - Quit application
```
4. Captured images will be saved in the `camera_captures` directory within the project.

