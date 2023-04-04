import paho.mqtt.client as mqtt_client
import traceback
import psycopg2
import random
import time
from config import * 
client_mqtt = deviceId + f'-{random.randint(0, 1000)}'
client = mqtt_client.Client(client_mqtt)
client.connect(enderecoNuvem, portaNuvem)

print("Conectando ao banco de dados")
connection = psycopg2.connect(
	host = DatabaseHostName,
	user = DatabaseUserName,
	password = DatabasePassword,
	database = 'MQTTbee',
	port = DatabasePort
)


def consultaBd(message):
    with connection.cursor() as cursor:
        characters = [chr(ascii) for ascii in message.payload]
        chars_joined = ''.join(characters) # Join chars to a string
        cursor.execute("SELECT MAX(id_dado) FROM Public.tbl_dado")
        maxId = cursor.fetchone()
        print('Id Solicitado pela nuvem: '+str(chars_joined))
        print('Maior Id no SGBD________: '+str(maxId[0]))

#        if 'a'=='b':
        if int(chars_joined) < int(maxId[0]):
            cursor.execute("SELECT id_dado, id_sensor, id_unidade, timestamp_dado, valor_dado FROM public.tbl_dado WHERE id_dado = "+chars_joined+"")
            tupla1 = cursor.fetchall()
            tupla = tupla1[0]
            paraInserir = "%s;%s;%s;%s;%s" % (tupla[0],tupla[1],tupla[2],tupla[3],tupla[4])
            print(paraInserir)
            client.publish(topicoNuvem+'/paraInserir',str(paraInserir), qos=2)
        else:
            print("Aguardando:")
            time.sleep(5)
            consultaBd(message)

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        consultaBd(msg)
    #client.subscribe(topic + '/leituras/#')
    client.subscribe(topicoNuvem+'/solicitaID', qos=2)
    client.on_message = on_message
	


def run():
    subscribe(client)
    client.loop_forever()



if __name__ == '__main__':
    run()
