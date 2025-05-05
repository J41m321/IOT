from peewee import Model, IntegerField, CharField, DateTimeField, FloatField, Check, ForeignKeyField, AutoField
from playhouse.postgres_ext import PostgresqlExtDatabase, ArrayField
from datetime import datetime

# Configuración de la base de datos
db_config = {
    'host': 'localhost', 
    'port': 5432, 
    'user': 'myuser', 
    'password': 'mypassword', 
    'database': 'mydatabase'
}
db = PostgresqlExtDatabase(**db_config)
db.connect()
db.execute_sql("SET search_path TO public;")
db.close()

# Definición de un modelo
class BaseModel(Model):
    class Meta:
        database = db

class Configuracion(BaseModel):
    class Meta:
        table_name = 'configuracion'

    id = AutoField(primary_key=True, constraints=[Check('id = 1')])
    id_protocol = IntegerField(constraints=[Check('id_protocol >= 0 AND id_protocol <= 4')])
    transport_layer = IntegerField(constraints=[Check("transport_layer >= 0 AND transport_layer <= 1")])

class Datos(BaseModel):
    class Meta:
        table_name = 'datos'

    id = AutoField(primary_key=True)
    id_device = CharField(max_length=255)
    mac = CharField(max_length=6)
    timestamp = DateTimeField()
    batt_level = IntegerField(constraints=[Check('batt_level >= 1 AND batt_level <= 100')])
    temp = IntegerField(constraints=[Check('temp >= 5 AND temp <= 30')], null=True)
    press = IntegerField(constraints=[Check('press >= 1000 AND press <= 1200')], null=True)
    hum = IntegerField(constraints=[Check('hum >= 30 AND hum <= 80')], null=True)
    co = FloatField(constraints=[Check('co >= 30.0 AND co <= 200.0')], null=True)
    rms = FloatField(null=True)
    amp_x = FloatField(constraints=[Check('amp_x IS NULL OR (amp_x >= 0.0059 AND amp_x <= 0.12)')], null=True)
    freq_x = FloatField(constraints=[Check('freq_x IS NULL OR (freq_x >= 29.0 AND freq_x <= 31.0)')], null=True)
    amp_y = FloatField(constraints=[Check('amp_y IS NULL OR (amp_y >= 0.0041 AND amp_y <= 0.11)')], null=True)
    freq_y = FloatField(constraints=[Check('freq_y IS NULL OR (freq_y >= 59.0 AND freq_y <= 61.0)')], null=True)
    amp_z = FloatField(constraints=[Check('amp_z IS NULL OR (amp_z >= 0.008 AND amp_z <= 0.15)')], null=True)
    freq_z = FloatField(constraints=[Check('freq_z IS NULL OR (freq_z >= 89.0 AND freq_z <= 91.0)')], null=True)
    acc_x = ArrayField(FloatField, null=True)
    acc_y = ArrayField(FloatField, null=True)
    acc_z = ArrayField(FloatField, null=True)
    rgyr_x = ArrayField(FloatField, null=True)
    rgyr_y = ArrayField(FloatField, null=True)
    rgyr_z = ArrayField(FloatField, null=True)

class Logs(BaseModel):
    class Meta:
        table_name = 'logs'

    id = AutoField(primary_key=True)
    datos_id = ForeignKeyField(Datos, backref='logs')
    id_device = CharField(max_length=255)
    id_protocol = IntegerField(constraints=[Check('id_protocol >= 0 AND id_protocol <= 4')])
    transport_layer = IntegerField(constraints=[Check("transport_layer >= 0 AND transport_layer <= 1")])
    timestamp = DateTimeField()

class Loss(BaseModel):
    class Meta:
        table_name = 'loss'

    id = AutoField(primary_key=True)
    datos_id = ForeignKeyField(Datos, backref='loss')
    delay = CharField()
    packet_loss = IntegerField()

def add_data_to_database(datos_data: dict, logs_data: dict, loss_data: dict):
    try:
        with db.atomic():
            datos = Datos.create(**datos_data)
            logs_data['datos_id'] = datos.id
            loss_data['datos_id'] = datos.id
            Logs.create(**logs_data)
            Loss.create(**loss_data)
    except Exception as error:
        print("Error al agregar datos a la base de datos:", error)

def get_conf():
    query = Configuracion.select()
    # Must be only one row
    for row in query:
        id_protocol = row.id_protocol
        transport_layer = row.transport_layer
    return id_protocol, transport_layer

def update_conf(id_protocol, transport_layer):
    query = Configuracion.update(
        id_protocol = id_protocol,
        transport_layer = transport_layer).where(Configuracion.id == 1).execute()


if __name__ == "__main__":
    try:
        # # Datos de ejemplo para Datos
        # datos_data = {
        #     'id_device': 'ABC123',
        #     'mac': '123456',
        #     'timestamp': datetime.now(),
        #     'batt_level': 80,
        #     'temp': 25,
        #     'press': 1100,
        #     'hum': 50,
        #     'co': 100.0,
        #     # Agrega más datos según sea necesario
        # }

        # # Datos de ejemplo para Logs
        # logs_data = {
        #     'id_device': 'XYZ789',
        #     'id_protocol': 0,
        #     'transport_layer': 'tcp',
        #     'timestamp': datetime.now(),
        # }

        # # Datos de ejemplo para Loss
        # loss_data = {
        #     'delay': '10ms',
        #     'packet_loss': 5,
        # }
        # with db.atomic():
        #     datos = Datos.create(**datos_data)
        #     logs_data['datos_id'] = datos.id
        #     loss_data['datos_id'] = datos.id
        #     Logs.create(**logs_data)
        #     Loss.create(**loss_data)

        query = Configuracion.select()
        for row in query:
            id_protocol = row.id_protocol
            transport_layer = row.transport_layer
        print(id_protocol, transport_layer)

    except Exception as error:
        print("Error al agregar datos a la base de datos:", error)