# Trojan
### KeyLogger
####  Overview
This is a simple keylogger written in Python that captures keystrokes and mouse clicks. It records the currently active window and logs all keypresses and mouse clicks within that window. This script uses the pynput library to listen to keyboard and mouse events and the ctypes library to interact with the Windows API

#### Requirements
- Python 3.x
- pynput library
- pywin32 library (for clipboard interaction)


### Anti-Analysis Detector
#### Overview
This script is designed to detect suspicious user activity patterns, potentially indicating the presence of an analysis environment. It monitors keyboard and mouse events, tracking keystrokes, mouse clicks, and double-clicks. If the activity exceeds certain thresholds, the script can terminate itself to prevent further analysis.
#### Requirements
- Python 3.x
- pywin32 library



### Screenshot Capture and Encoding Script
### Overview
This Python script captures a screenshot of the entire virtual screen and encodes the image to a base64 string. The script utilizes the pywin32 library to interact with the Windows API for capturing the screen.
### Requirements
- Python 3.x
- pywin32 library

### Shellcode Execution Script
### Overview
This Python script is designed to download, decode, and execute shellcode from a specified URL. It leverages the ctypes library to interact with the Windows API, allocating memory and executing the shellcode.

### Requirements
Python 3.x
