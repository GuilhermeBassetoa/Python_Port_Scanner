import socket


def scan_port(host: str, port: int, timeout: float = 1.0) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        resultado = s.connect_ex((host, port))
        return resultado == 0 

def scan_range(host: str, start: int, end: int, timeout: float = 1.0) -> list[int]:
    ports = []
    for i in range (start, end+1):
        estado = scan_port(host, i, timeout)
        if estado:
            ports.append(i)
    return ports

    