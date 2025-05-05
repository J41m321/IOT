import socket
import select
import threading
from packet_parser import pack_conf, unpack_header, parse_body
from modelos import add_data_to_database, get_conf

# For data races
db_lock = threading.Lock()


# Función para manejar la conexión TCP con el cliente
def handle_client_tcp(client_tcp, addr):
    print(f"Conexión TCP establecida desde {addr}")
    # Receive packet
    while True:
        values_db = handle_packet(client_tcp)
        if not values_db or values_db == "Config sent":
            break
        with db_lock:
            add_data_to_database(values_db[0], values_db[1], values_db[2])
        break
    client_tcp.close()
    print(f"Conexión TCP cerrada desde {addr}")


# Función para manejar la conexión UDP con el cliente
def handle_client_udp(udp_socket):
    print(f"Paquete UDP recibido desde {addr}")
    while True:
        values_db, addr = handle_packet(udp_socket)
        if not values_db or values_db == "Config sent":
            break
        with db_lock:
            add_data_to_database(values_db[0], values_db[1], values_db[2])
        break


def handle_packet(client_socket):
    # Check request for config
    CONF = 4
    addr = None
    data = b""
    # Recibe datos del cliente
    if client_socket.type == socket.SOCK_STREAM:
        data = client_socket.recv(CONF)
    elif client_socket.type == socket.SOCK_DGRAM:
        data, addr = client_socket.recvfrom(CONF)

    # Maneja el mensaje de solicitud inicial
    if data == b"CONF":
        # Envía la configuración inicial al cliente
        if addr:  # UDP
            initial_config = send_conf(client_socket, addr)
        else:  # TCP
            initial_config = send_conf(client_socket)
        return "Config sent"

    # Header
    N = 6 - CONF
    if client_socket.type == socket.SOCK_STREAM:
        header = client_socket.recv(N)
    elif client_socket.type == socket.SOCK_DGRAM:
        header, addr = client_socket.recvfrom(N)
    if not header:
        packet_loss += 1
        print("Not header data")
        return

    data += header
    print(data)
    header_dict = unpack_header(data)
    print(header_dict)
    length = header_dict["length"]
    print("largo header+body", length)

    data = None
    # Body
    if client_socket.type == socket.SOCK_STREAM:
        data = client_socket.recv(length - 6)
    elif client_socket.type == socket.SOCK_DGRAM:
        data = client_socket.recvfrom(length - 6)
    if not data:
        return
    print("body: ", data, len(data))
    values_db = parse_body(header_dict, data)
    if addr:
        return values_db, addr
    return values_db


def send_conf(client_socket, addr=None):
    id_protocol, transport_layer = get_conf()
    print(id_protocol, transport_layer)
    conf_packet = pack_conf(id_protocol, transport_layer)
    if client_socket.type == socket.SOCK_STREAM:
        client_socket.send(conf_packet)
    elif client_socket.type == socket.SOCK_DGRAM:
        client_socket.sendto(conf_packet, addr)
    else:
        print("Unknown socket type")


def main():
    host = "0.0.0.0"
    port = 1234

    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    tcp_socket.bind((host, port))
    udp_socket.bind((host, port))

    tcp_socket.listen(5)
    print("Servidor esperando conexiones...")

    while True:
        sockets_list = [tcp_socket, udp_socket]

        read_sockets, _, _ = select.select(sockets_list, [], [])

        for sock in read_sockets:
            if sock == tcp_socket:
                client_tcp, addr = tcp_socket.accept()
                client_handler_tcp = threading.Thread(
                    target=handle_client_tcp, args=(client_tcp, addr)
                )
                client_handler_tcp.start()
            elif sock == udp_socket:
                client_handler_udp = threading.Thread(
                    target=handle_client_udp, args=(udp_socket)
                )
                client_handler_udp.start()


if __name__ == "__main__":
    main()