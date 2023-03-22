import paho.mqtt.client as mqtt_client
import traceback
import psycopg2
import random
from config import * 
client_mqtt = deviceId + f'-{random.randint(0, 1000)}'

print("Conectando ao banco de dados")
connection = psycopg2.connect(
	host = DatabaseHostName,
	user = DatabaseUserName,
	password = DatabasePassword,
	database = 'MQTTbee',
	port = DatabasePort
)

## setup mqtt
#client_source = mqtt.Client(deviceId)

def insertIntoDatabase(message):
	"Inserts the mqtt data into the database"
	with connection.cursor() as cursor:
		characters = [chr(ascii) for ascii in message.payload] # Convert ASCII to char
		chars_joined = ''.join(characters) # Join chars to a string
		mensagemMQTT = chars_joined.split(";")     # Split string by comma
		temperatura="INSERT INTO public.tbl_dado(id_dado, id_sensor, id_unidade, timestamp_dado, valor_dado) VALUES ((SELECT MAX(id_dado)+1 FROM public.tbl_dado), (SELECT id_sensor from tbl_sensor where nome_sensor='"+mensagemMQTT[0]+"'), 1, (to_timestamp("+mensagemMQTT[1]+")), "+mensagemMQTT[3]+");"
		umidade="INSERT INTO public.tbl_dado(id_dado, id_sensor, id_unidade, timestamp_dado, valor_dado) VALUES ((SELECT MAX(id_dado)+1 FROM public.tbl_dado), (SELECT id_sensor from tbl_sensor where nome_sensor='"+mensagemMQTT[0]+"'), 2, (to_timestamp("+mensagemMQTT[1]+")), "+mensagemMQTT[5]+");"
		cursor.execute(temperatura)
		cursor.execute(umidade)
		connection.commit()


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_mqtt)
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(brokerAdd, brokerPort)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        insertIntoDatabase(msg)
    client.subscribe(topic + '/sensores/#')
    #client.subscribe(topic + '/#')
    client.on_message = on_message
	


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()



if __name__ == '__main__':
    run()
