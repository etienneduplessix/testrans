def myprint(str):
	print ("\033[35m", str,"\033[37m" )

def myprint2(str):
    print("\033[32m",str, "\033[37m")

def myprint3(str):
    print("\033[34m", str, "\033[37m")

import socket

def get_local_ip():
    # Create a UDP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # This doesn't actually connect to the internet
        s.connect(("8.8.8.8", 80))  # Google Public DNS
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'  # Fallback to localhost
    finally:
        s.close()
    return local_ip
