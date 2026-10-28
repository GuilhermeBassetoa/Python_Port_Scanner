import socket
from functools import partial
from concurrent.futures import ThreadPoolExecutor

def scan_port(host: str, port: int, timeout: float = 1.0) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        resultado = s.connect_ex((host, port))
        return resultado == 0 

def get_service(port: int) -> str:
    try:
        return socket.getservbyport(port)
    except OSError:
        return "unknown"

def grab_banner(host: str, port: int, timeout: float = 2.0) -> str:
    try:
        with socket.create_connection((host, port), timeout=timeout) as s:
            s.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
            dados = s.recv(1024)
    except OSError:
        return ""
    if not dados:
        return ""
    return dados.decode(errors="replace").splitlines()[0]

def scan_range(host: str, start: int, end: int, timeout: float = 1.0) -> list[int]:
    portas = range(start, end + 1)
    verificar = partial(scan_port, host, timeout = timeout)
    with ThreadPoolExecutor(max_workers = 50) as executor:
        resultado = list(executor.map(verificar, portas))
    ports = []
    for porta, aberta in zip (portas, resultado):
        if aberta:
            ports.append(porta)
    return ports