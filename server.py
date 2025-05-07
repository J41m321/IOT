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
    print("Esperando datos UDP")
    while True:
        values_db, addr= handle_packet(udp_socket)
        print(f"se cae despues de handlepacket")
        if not values_db or values_db == "Config sent":
            print("no values")
            break
        else:
            add_data_to_database(values_db[0], values_db[1], values_db[2])
            print("added")
    print(f"Conexión UDP cerrada desde {addr}")


def handle_packet(client_socket):
    CONF = 4  # Tamaño del mensaje inicial "CONF"
    addr = None
    data = b""
    
    # 1. Recibir datos iniciales
    try:
        if client_socket.type == socket.SOCK_STREAM:  # TCP
            data = client_socket.recv(CONF)
            if not data:
                return None
        elif client_socket.type == socket.SOCK_DGRAM:  # UDP
            data, addr = client_socket.recvfrom(65535)
    except Exception as e:
        print(f"Error receiving initial data: {e}")
        return None if not addr else (None, addr)
    
    # 2. Manejar solicitud de configuración
    if data == b"CONF":
        send_conf(client_socket, addr)
        return "Config sent" if not addr else ("Config sent", addr)
    
    # 3. Manejo para UDP (paquete completo)
    if client_socket.type == socket.SOCK_DGRAM:
        try:
            if len(data) < 6:
                print(f"UDP packet too small ({len(data)} bytes)")
                return None, addr
                
            header_dict = unpack_header(data[:6])
            expected_length = header_dict["length"]
            
            # Verificar que el tamaño del paquete coincida con el header
            if len(data) != expected_length:
                print(f"Invalid UDP packet length. Header says {expected_length}, got {len(data)}")
                return None, addr
                
            body = data[6:expected_length]
            print(f"[UDP] Received: Header={header_dict}, Body={len(body)} bytes")
            
            values_db = parse_body(header_dict, body)
            if not values_db or values_db[0] is None:
                return None, addr
                
            return values_db, addr
            
        except Exception as e:
            print(f"Error processing UDP packet: {e}")
            return None, addr
    
    # 4. Manejo para TCP (flujo de datos)
    if client_socket.type == socket.SOCK_STREAM:
        try:
            # Completar el header (ya tenemos 4 bytes, faltan 2)
            remaining_header = client_socket.recv(2)
            if not remaining_header or len(remaining_header) < 2:
                print("Incomplete TCP header")
                return None
                
            full_header = data + remaining_header
            header_dict = unpack_header(full_header)
            total_length = header_dict["length"]
            body_length = total_length - 6  # Restamos el tamaño del header
            
            print(f"[TCP] Expecting {body_length} bytes of body data")
            
            # Recibir el cuerpo en bloques si es necesario
            body = b""
            remaining = body_length
            while remaining > 0:
                chunk = client_socket.recv(min(remaining, 4096))  # Leer en bloques de 4KB
                if not chunk:
                    break
                body += chunk
                remaining -= len(chunk)
            
            if len(body) != body_length:
                print(f"Incomplete TCP body. Expected {body_length}, got {len(body)}")
                return None
                
            print(f"[TCP] Full message received: {total_length} bytes")
            values_db = parse_body(header_dict, body)
            return values_db
            
        except Exception as e:
            print(f"Error processing TCP packet: {e}")
            return None


def send_conf(client_socket, addr=None):
    id_protocol, transport_layer = get_conf()
    print(id_protocol, transport_layer)
    conf_packet = pack_conf(id_protocol, transport_layer)
    print(conf_packet.hex())
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
                    target=handle_client_udp, args=(udp_socket,)
                )
                client_handler_udp.start()


if __name__ == "__main__":
    main()
