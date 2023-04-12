import json
import paho.mqtt.client as mqtt_client
import psycopg2
import random
import time
from config import *

class MqttClient:
    def __init__(self, deviceId):
        self.deviceId = deviceId
        self.client_mqtt = f'aviso{self.deviceId}-{random.randint(0, 991000)}'
        self.client = mqtt_client.Client(self.client_mqtt)
        self.intervalo = 60
        self.topic = 'iotbee/{}'.format(deviceId)

        self.connect()

    def connect(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Conectado ao MQTT Broker")
            else:
                print("Falha ao conectar ao MQTT Broker, código de retorno: ", rc)

        def on_disconnect(client, userdata, rc):
            print("Desconectado do MQTT Broker, código de retorno: ", rc)
            time.sleep(self.intervalo)
            self.connect()

        self.client.on_connect = on_connect
        self.client.on_disconnect = on_disconnect
        self.client.connect(brokerAdd, brokerPort, keepalive=self.intervalo+10)
        self.client.loop_start()

    def publish(self, data):
        if self.client.is_connected():
            self.client.publish(f'{self.topic}/apresentador/valores', json.dumps(data), qos=1, retain=1)
            print('Dados publicados')
        else:
            print('Não é possível publicar os dados, reconectando ao MQTT Broker')
            self.connect()

class Database:
    def __init__(self):
        print("Conectando ao banco de dados")
        self.connection = psycopg2.connect(
            host=DatabaseHostName,
            user=DatabaseUserName,
            password=DatabasePassword,
            database='MQTTbee',
            port=DatabasePort
        )

    def query(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT tbl_sensor.nome_sensor, tbl_unidade.simbolo_unidade, tbl_dado.valor_dado FROM tbl_dado INNER JOIN tbl_sensor ON tbl_sensor.id_sensor = tbl_dado.id_sensor INNER JOIN tbl_unidade ON tbl_unidade.id_unidade = tbl_dado.id_unidade ORDER BY tbl_dado.id_dado DESC LIMIT (SELECT max(id_sensor) FROM tbl_sensor) * (SELECT max(id_unidade) FROM tbl_unidade)")
            dados = cursor.fetchall()
            informac = {}
            for dado in dados:
                nome_sensor = dado[0]
                simbolo_unidade = dado[1]
                valor_dado = dado[2]
                if nome_sensor not in informac:
                    informac[nome_sensor] = {}
                if simbolo_unidade == 'C':
                    informac[nome_sensor]['tmp'] = valor_dado
                else:
                    informac[nome_sensor][simbolo_unidade] = int(valor_dado)
            return informac

if __name__ == '__main__':
    mqtt_client = MqttClient(deviceId)
    db

