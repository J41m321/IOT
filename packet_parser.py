import struct # Libreria muy util para codificar y decodificar datos
from datetime import datetime

"""

--- Packing en C ---



char * pack(int packet_id, float value_float, char * text) {
    int largo_text = strlen(text);
    char * packet = malloc(12 + largo_text);
    memcpy(packet, &packet_id, 4);
    memcpy(packet + 4, &value_float, 4);
    memcpy(packet + 8, &largo_text, 4);
    memcpy(packet + 12, text, largo_text);
    return packet;
}


//Luego mandan el paquete por el socket


--- Unpacking en C ---


void unpack(char * packet) {
    int packet_id;
    float value_float;
    int largo_text;
    char * text;

    memcpy(&packet_id, packet, 4);
    memcpy(&value_float, packet + 4, 4);
    memcpy(&largo_text, packet + 8, 4);

    text = malloc(largo_text + 1); // +1 for the null-terminator
    if (text == NULL) {
        // Handle memory allocation failure
        return;
    }
    
    memcpy(text, packet + 12, largo_text);
    text[largo_text] = '\0'; // Null-terminate the string

    printf("Packet ID: %d\n", packet_id);
    printf("Float Value: %f\n", value_float);
    printf("Text: %s\n", text);

    free(text); 
}


"""

def pack_conf(id_protocol, transport_layer):
    return struct.pack('<BB', id_protocol, transport_layer)

def unpack_header(packet: bytes):
    packet_id, transport_layer, id_protocol, length= struct.unpack('<HBBH', packet) # '<H6sBBH'
    values =  {
        "packet_id": packet_id,
        "transport_layer": transport_layer,
        "id_protocol": id_protocol,
        "length": length,
    }
    return values

def parse_body(header: list, packet: bytes) -> dict:
    id_protocol = header['id_protocol']
    data = ['batt_level','timestamp','temp','press','hum','co','rms','amp_x','freq_x','amp_y','freq_y','amp_z','freq_z']
    p4 = ['batt_level','timestamp','temp','press','hum','co','acc_x','acc_y','acc_z','rgyr_x','rgyr_y','rgyr_z']
    datos_dict = {}
    logs_dict = {}
    loss_dict = {}

    parsed_data = struct.unpack('<H', packet[:2])
    device_id = parsed_data[0]

    datos_dict["id_device"] = str(device_id)
    logs_dict["id_device"] = str(device_id)


    # datos_dict["id_device"] = "123456"
    # datos_dict["mac"] = "123456"

    logs_dict["id_device"] = "123456"
    logs_dict["id_protocol"] = header["id_protocol"]
    logs_dict["transport_layer"] = header["transport_layer"]
    logs_dict["timestamp"] = datetime.now()

    loss_dict["delay"] = "0ms"
    loss_dict["packet_loss"] = 0

    try:
        if id_protocol == 0:
            parsed_data = struct.unpack('<B', packet)
            datos_dict["batt_level"] = parsed_data[0]
            
        elif id_protocol == 1:
            parsed_data = struct.unpack('<BL', packet)
            datos_dict["batt_level"] = parsed_data[0]
            datos_dict["timestamp"] = datetime.fromtimestamp(parsed_data[1])
            
        elif id_protocol == 2:
            parsed_data = struct.unpack('<BLBiBf', packet)
            datos_dict["batt_level"] = parsed_data[0]
            datos_dict["timestamp"] = datetime.fromtimestamp(parsed_data[1])
            datos_dict["temp"] = parsed_data[2]
            datos_dict["press"] = parsed_data[3]
            datos_dict["hum"] = parsed_data[4]
            datos_dict["co"] = parsed_data[5]
            
        elif id_protocol == 3:
            # Cambiar el formato para coincidir con lo que envía el cliente C
            parsed_data = struct.unpack('<BLBiBfffffff', packet[:39])
            datos_dict["batt_level"] = parsed_data[0]
            datos_dict["timestamp"] = datetime.fromtimestamp(parsed_data[1])
            datos_dict["temp"] = parsed_data[2]
            datos_dict["press"] = parsed_data[3]
            datos_dict["hum"] = parsed_data[4]
            datos_dict["co"] = parsed_data[5]
            datos_dict["rms"] = parsed_data[6]
            datos_dict["amp_x"] = parsed_data[7]
            datos_dict["freq_x"] = parsed_data[8]
            datos_dict["amp_y"] = parsed_data[9]
            datos_dict["freq_y"] = parsed_data[10]
            datos_dict["amp_z"] = parsed_data[11]
            
        elif id_protocol == 4:
            # Protocolo 4 (manejar arrays)
            pass
            
        datos_dict["timestamp"] = datetime.now()
        return datos_dict, logs_dict, loss_dict
        
    except Exception as e:
        print(f"Error parsing packet: {e}")
        return None, None, None

if __name__ == "__main__":
    mensage = pack(1, 3.20, "Hola mundo")
    print(mensage)
    print(unpack(mensage))
