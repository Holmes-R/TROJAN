from ctypes import byref, c_uint, c_ulong, sizeof, Structure, windll
import random
import sys
import time
import win32api

class LASTINPUTINFO(Structure):
    _fields_ = [
        ('cbSize', c_uint),
        ('dwTime', c_ulong)]

def get_last_input():
    struct_lastinputinfo = LASTINPUTINFO()
    struct_lastinputinfo.cbSize = sizeof(LASTINPUTINFO)
    windll.user32.GetLastInputInfo(byref(struct_lastinputinfo))
    run_time = windll.kernel32.GetTickCount64()
    elapsed = run_time - struct_lastinputinfo.dwTime
    return elapsed

class Detector:
    def __init__(self):
        self.double_clicks = 0
        self.keystrokes = 0
        self.mouse_clicks = 0

    def get_key_press(self):
        for i in range(0, 0xff):
            state = win32api.GetAsyncKeyState(i)
            if state & 0x8000:
                if i == 0x1:  # Left mouse button click
                    self.mouse_clicks += 1
                    return time.time()
                elif 32 < i < 127:  # Printable ASCII characters
                    self.keystrokes += 1
                    return time.time()
        return None

    def detect(self):
        previous_timestamp = None
        first_double_click = None
        double_click_threshold = 0.35  # Seconds

        max_double_clicks = 10
        max_keystrokes = random.randint(10, 25)
        max_mouse_clicks = random.randint(5, 25)
        max_input_threshold = 3000  # Milliseconds

        detection_complete = False
        while not detection_complete:
            last_input = get_last_input()
            print(f"[*] It's been {last_input} milliseconds since the last event.")
            if last_input >= max_input_threshold:
                sys.exit(0)

            keypress_time = self.get_key_press()
            if keypress_time is not None and previous_timestamp is not None:
                elapsed = keypress_time - previous_timestamp

                if elapsed <= double_click_threshold:
                    self.mouse_clicks -= 2
                    self.double_clicks += 1
                    if first_double_click is None:
                        first_double_click = time.time()
                    else:
                        if self.double_clicks >= max_double_clicks:
                            if keypress_time - first_double_click <= (max_double_clicks * double_click_threshold):
                                sys.exit(0)

                if self.keystrokes >= max_keystrokes and self.double_clicks >= max_double_clicks and self.mouse_clicks >= max_mouse_clicks:
                    detection_complete = True

                previous_timestamp = keypress_time

            elif keypress_time is not None:
                previous_timestamp = keypress_time

            time.sleep(1)  # Add a small delay to prevent excessive CPU usage

if __name__ == '__main__':
    d = Detector()
    d.detect()
    print('Detection complete')
