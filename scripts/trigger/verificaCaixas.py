from msilib.schema import PublishComponent
import paho.mqtt.client as mqtt_client
import psycopg2
import random
import time
from config import * 
client_mqtt = 'aviso' + deviceId + f'-{random.randint(0, 1000)}'
client = mqtt_client.Client(client_mqtt)

def conectaBd():
    print("Conectando ao banco de dados")
    connection = psycopg2.connect(
	    host = DatabaseHostName,
	    user = DatabaseUserName,
	    password = DatabasePassword,
	    database = 'MQTTbee',
	    port = DatabasePort
    )

def consultaBd():
    conectaBd()
    with connection.cursor() as cursor:
        cursor.execute("select id_sensor,id_unidade,valor_dado from tbl_dado order by id_dado desc LIMIT (SELECT max(id_sensor) FROM tbl_sensor) * (SELECT max(id_unidade) FROM tbl_unidade)")
        dados = cursor.fetchall()
        ext_temp = 0
        ext_umi = 0
        cx1_temp = 0
        cx1_umi = 0
        # Verificação dos dados
        for id_dado, id_sensor, id_unidade, valor_dado in cur.fetchall():
            if id_unidade == 1 and id_sensor > 1 and (valor_dado < 10 or valor_dado > 40):
        # Publica o valor 1 no tópico /local/alarme se o id_unidade for 1 e o valor_dado abaixo de 10 ou acima de 40
            publish.single("/local/alarme", "1", hostname=mqtt_host, port=mqtt_port)
        elif id_unidade == 2 and valor_dado < 50 and id_sensor > 1:
            # Publica o valor 1 no tópico /local/alarme se o id_unidade for 2 e o valor_dado menor que 50
            PublishComponent.single("/local/alarme", "1", hostname=mqtt_host, port=mqtt_port)

        # Publica o valor 0 no tópico /local/topico se os valores estiverem normalizados
        cur.execute("SELECT COUNT(*) FROM tbl_dado WHERE id_unidade = 1 AND valor_dado BETWEEN 10 AND 40")
            count_unidade_1 = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM tbl_dado WHERE id_unidade = 2 AND valor_dado >= 50")
            count_unidade_2 = cur.fetchone()[0]


if __name__ == '__main__':
    #client.loop_forever()
    client.connect(brokerAdd, brokerPort, keepalive=intervalo+10)
    client.loop_start()
    while True:
        consultaBd()
        time.sleep(intervalo)