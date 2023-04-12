import json
import paho.mqtt.client as mqtt_client
import psycopg2
import random
import time
from config import *

client_mqtt = 'aviso' + deviceId + f'-{random.randint(0, 991000)}'
client = mqtt_client.Client(client_mqtt)
intervalo = 60

print("Conectando ao banco de dados")
connection = psycopg2.connect(
    host=DatabaseHostName,
    user=DatabaseUserName,
    password=DatabasePassword,
    database='MQTTbee',
    port=DatabasePort
)

def consultaBd():
    with connection.cursor() as cursor:
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
        print('dados: ')
        print(dados)
        print('apresentador/valores/' + json.dumps(informac))
        if client.is_connected():
            client.publish(topic + '1/apresentador/valores', json.dumps(informac), qos=1, retain=1)
            print('Publicado')
        else:
            client.connect(brokerAdd, brokerPort, keepalive=intervalo+10)
            print('conectando mqtt novamente')

if __name__ == '__main__':
    client.connect(brokerAdd, brokerPort, keepalive=intervalo+10)
    client.loop_start()
    while True:
        consultaBd()
        time.sleep(intervalo)
