-- init.sql

-- Drop tables if they exist (optional, useful for development/reset)
DROP TABLE IF EXISTS loss CASCADE;
DROP TABLE IF EXISTS logs CASCADE;
DROP TABLE IF EXISTS datos CASCADE;
DROP TABLE IF EXISTS configuracion CASCADE;

-- Create the configuracion table
CREATE TABLE configuracion (
    id SERIAL PRIMARY KEY CHECK (id = 1),
    id_protocol INTEGER CHECK (id_protocol >= 0 AND id_protocol <= 4),
    transport_layer INTEGER CHECK (transport_layer >= 0 AND transport_layer <= 1)
);

-- Create the datos table
CREATE TABLE datos (
    id SERIAL PRIMARY KEY,
    id_device VARCHAR(255) NOT NULL,
    mac CHAR(6) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    batt_level INTEGER CHECK (batt_level >= 1 AND batt_level <= 100),
    temp INTEGER CHECK (temp >= 5 AND temp <= 30),
    press INTEGER CHECK (press >= 1000 AND press <= 1200),
    hum INTEGER CHECK (hum >= 30 AND hum <= 80),
    co FLOAT CHECK (co >= 30.0 AND co <= 200.0),
    rms FLOAT,
    amp_x FLOAT CHECK (amp_x IS NULL OR (amp_x >= 0.0059 AND amp_x <= 0.12)),
    freq_x FLOAT CHECK (freq_x IS NULL OR (freq_x >= 29.0 AND freq_x <= 31.0)),
    amp_y FLOAT CHECK (amp_y IS NULL OR (amp_y >= 0.0041 AND amp_y <= 0.11)),
    freq_y FLOAT CHECK (freq_y IS NULL OR (freq_y >= 59.0 AND freq_y <= 61.0)),
    amp_z FLOAT CHECK (amp_z IS NULL OR (amp_z >= 0.008 AND amp_z <= 0.15)),
    freq_z FLOAT CHECK (freq_z IS NULL OR (freq_z >= 89.0 AND freq_z <= 91.0)),
    acc_x FLOAT[],
    acc_y FLOAT[],
    acc_z FLOAT[],
    rgyr_x FLOAT[],
    rgyr_y FLOAT[],
    rgyr_z FLOAT[]
);

-- Create the logs table
CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
    datos_id INTEGER NOT NULL REFERENCES datos(id),
    id_device VARCHAR(255) NOT NULL,
    id_protocol INTEGER CHECK (id_protocol >= 0 AND id_protocol <= 4),
    transport_layer INTEGER CHECK (transport_layer >= 0 AND transport_layer <= 1),
    timestamp TIMESTAMP NOT NULL
);

-- Create the loss table
CREATE TABLE loss (
    id SERIAL PRIMARY KEY,
    datos_id INTEGER NOT NULL REFERENCES datos(id),
    delay VARCHAR NOT NULL,
    packet_loss INTEGER NOT NULL
);

-- Optionally insert the initial row into configuracion (with id=1)
INSERT INTO configuracion (id, id_protocol, transport_layer) VALUES (1, 0, 0)
ON CONFLICT (id) DO NOTHING;
