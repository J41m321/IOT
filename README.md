# IOT
Repositorio para el curso CC5326 

## Instalar Docker en la RaspberryPi
* Primero actualizamos el sistema con:
```bash
sudo apt update && sudo apt upgrade -y
```
* Luego instalamos algunas herramientas necesarias:
```bash
sudo apt install ca-certificates curl gnupg -y
```
* El siguiente paso es instalar docker desde el script oficial de docker:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```
* Verificar que docker se instaló correctamente:
```bash
docker --version
```
* Instalar Docker Compose (v2):
```bash
sudo apt install docker-compose-plugin -y
```
* verficar:
```bash
docker compose version
```

## Archivos en el repositorio

- docker-compose.yml : Define el contenedor de PostgreSQL y su configuración.
- init.sql : Script SQL que crea las tablas necesarias al iniciar la base.

## Levantar la base de datos
```bash
docker compose up -d
docker ps
```

## Conectarse a la base de datos
* Instalar el cliente de PostgreSQL:
```bash
sudo apt install postgresql-client -y
```
* Conectarse:
```bash
psql -h localhost -U miusuario -d midatabase
```

* Verificar las tablas:
```sql
\dt
```

## Detener y eliminar contenedores
```bash
docker compose down
docker compose down -v  # (Esto borra los datos)
```


## Avance de la tarea

* Esta tarea entrega bien para protocolos 0-3, para UDP y TCP, cambiando en la base de datos el valor del transport layer entre 0 (tcp) y 1 (udp), esto guardando archivos en Docker en Raspberry y ejecutando en ESP32. 