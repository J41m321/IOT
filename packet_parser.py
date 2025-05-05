import struct # Libreria muy util para codificar y decodificar datos
from datetime import datetime

"""

--- Packing en C ---



char * pack(int packet_id, float value_float, char * text) {
    char * packet = malloc(12 + strlen(text));
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
    return struct.pack('<ii', id_protocol, transport_layer)

def unpack_header(packet: bytes):
    packet_id, transport_layer, id_protocol, length = struct.unpack('<HBBH', packet) # '<H6sBBH'
    values =  {
        "packet_id": packet_id,
        # "mac": mac,
        "transport_layer": transport_layer,
        "id_protocol": id_protocol,
        "length": length,
    }
    return values

def parse_body(header: list, packet: bytes) -> dict:
    id_protocol = header['id_protocol']
    data = ['batt_level','timestamp','temp','press','hum','co','rms','amp_x','frec_x','amp_y','frec_y','amp_z','frec_z']
    p4 = ['batt_level','timestamp','temp','press','hum','co','acc_x','acc_y','acc_z','rgyr_x','rgyr_y','rgyr_z']
    datos_dict = {}
    logs_dict = {}
    loss_dict = {}

    datos_dict["id_device"] = "123456"#header["mac"] # id_device is commonly mac in Iot
    datos_dict["mac"] = "123456"#header["mac"]

    logs_dict["id_device"]  = "123456"#header["mac"] # id_device is commonly mac in Iot
    logs_dict["id_protocol"] = header["id_protocol"]
    logs_dict["transport_layer"] = header["transport_layer"]
    logs_dict["timestamp"] = datetime.now()

    loss_dict["delay"] = 0
    loss_dict["packet_loss"] = 0

    if id_protocol == 0:
        parsed_data=struct.unpack('<B', packet)
        #Estructura del protocolo 0
        #Batt_level
        pass
    elif id_protocol == 1:
        parsed_data=struct.unpack('<BL', packet)
        #Estructura del protocolo 1
        #Batt_level+Timestamp
        pass
    elif id_protocol == 2:
        parsed_data=struct.unpack('<BLBiBf', packet)
        #Estructura del protocolo 2
        #Batt_level+Timestamp+Temp+Press+Hum+Co
    elif id_protocol == 3:
        parsed_data=struct.unpack('<BLBiBffffffff', packet)
    else:
        parsed_data=struct.unpack('<BLBiBi2000f2000f2000f2000f2000f2000f2000f', packet)
        length = len(parsed_data)
        for i in range(length):
            datos_dict[p4[i]] = parsed_data[i]
        datos_dict["timestamp"] = datetime.now()
        return datos_dict, logs_dict, loss_dict

    length = len(parsed_data)
    for i in range(length):
        datos_dict[data[i]] = parsed_data[i]
    datos_dict["timestamp"] = datetime.now()
    return datos_dict, logs_dict, loss_dict


if __name__ == "__main__":
    mensage = pack(1, 3.20, "Hola mundo")
    print(mensage)
    print(unpack(mensage))