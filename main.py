import socket
from src.port_definitions import PORT_RANGES, PortRange


SOCK_TIMEOUT_MS = 1
OPEN_PORTS: list[int] = []


def cache_port(port: int, cache: list[int] = OPEN_PORTS) -> None:
    assert isinstance(port, int)
    cache.append(port)
    
    
def check_port(tartget_ip: str, port: int) -> int | None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(SOCK_TIMEOUT_MS)
    
    result = sock.connect_ex((tartget_ip, port))
    if result == 0:
        return port 
    
    return None


def scan_port_range(port_range: PortRange, target: str, cache: function) -> None:
    for port in range(port_range):
        result = check_port(target, port)
        
        if (result):
            cache(port)
        

def main():
    target_ip = input('Enter target IP: ')
    
    for item in PORT_RANGES:
        scan_port_range(item, target_ip, cache_port)
        
    print(f"Open ports: {OPEN_PORTS}", end="")
    

if __name__ == "__main__":
    main()
