#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

// Al momento de usar las funciones en main(), recordar inicializar la semilla:
// srand(time(NULL)) // Para garantizar que la semilla siempre es diferente

// Acceloremeter_kpi

// Función para generar un número aleatorio en un rango dado
float randomInRange(float min, float max) {
    return min + ((float)rand() / RAND_MAX) * (max - min);
}

// Función para generar Ampx
float generateAmpx() {
    return randomInRange(0.0059, 0.12);
}

// Función para generar Freqx
float generateFreqx() {
    return randomInRange(29.0, 31.0);
}

// Función para generar Ampy
float generateAmpy() {
    return randomInRange(0.0041, 0.11);
}

// Función para generar Freqy
float generateFreqy() {
    return randomInRange(59.0, 61.0);
}

// Función para generar Ampz
float generateAmpz() {
    return randomInRange(0.008, 0.15);
}

// Función para generar Freqz
float generateFreqz() {
    return randomInRange(89.0, 91.0);
}

// Función para generar el RMS
float generateRMS(float Ampx, float Ampy, float Ampz) {
    return sqrtf(powf(Ampx, 2) + powf(Ampy, 2) + powf(Ampz, 2));
}

// Acceloremeter_Sensor

// Función para generar Acc_X, Acc_Y, o Acc_Z
float generateAcc() {
    const int size = 2000;
    // Recordar hacer free()
    float* float_array = malloc(size * sizeof(float));

    if (float_array == NULL) {
        // Manejo de error si malloc falla
        perror("Error al asignar memoria");
        exit(EXIT_FAILURE);
    }

    for (int i = 0; i < size; i++) {
        float_array[i] = randomInRange(-16.0, 16.0);
    }
    return float_array;
}

// Función para generar Rgyr_X, Rgyr_Y, o Rgyr_Z
float* generateRgyr() {
    const int size = 2000;
    // Recordar hacer free()
    float* float_array = malloc(size * sizeof(float));

    if (float_array == NULL) {
        // Manejo de error si malloc falla
        perror("Error al asignar memoria");
        exit(EXIT_FAILURE);
    }

    for (int i = 0; i < size; i++) {
        float_array[i] = randomInRange(-1000, 1000);
    }
    return float_array;
}

// Temperatura-Humedad-Presión-CO

// Función para generar la temperatura (Temp)
int generateTemperature() {
    return rand() % 26 + 5; // Valor aleatorio entre 5 y 30
}

// Función para generar la humedad (Hum)
int generateHumidity() {
    return rand() % 51 + 30; // Valor aleatorio entre 30 y 80
}

// Función para generar la presión (Pres)
int generatePressure() {
    return rand() % 201 + 1000; // Valor aleatorio entre 1000 y 1200
}

// Función para generar el nivel de CO (CO)
float generateCO() {
    return randomInRange(30.0, 200.0);
}

// Batt_Sensor

// Función para generar el nivel de batería
unsigned char generateBatteryLevel() {
    return rand() % 100 + 1; // Valor aleatorio entre 1 y 100
}