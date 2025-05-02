-- Crear tabla Datos
CREATE TABLE IF NOT EXISTS Datos (
    id SERIAL PRIMARY KEY,
    dispositivo VARCHAR(100) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valor FLOAT
);

-- Crear tabla Logs
CREATE TABLE IF NOT EXISTS Logs (
    id SERIAL PRIMARY KEY,
    dispositivo_id INT,
    capa_transporte VARCHAR(50),
    protocolo VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla Configuracion
CREATE TABLE IF NOT EXISTS Configuracion (
    id SERIAL PRIMARY KEY,
    dispositivo_id INT,
    protocolo VARCHAR(50),
    capa_transporte VARCHAR(50)
);

-- Crear tabla Loss
CREATE TABLE IF NOT EXISTS Loss (
    id SERIAL PRIMARY KEY,
    dispositivo_id INT,
    tiempo_retardo_ms FLOAT,
    perdida_paquetes_bytes INT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);