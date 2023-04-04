#!/usr/bin/env python3
## script temporário para a mudança de tópico e hora

import paho.mqtt.client as mqtt
def on_connect(client, userdata, flags, rc):
    # This will be called once the client connects
    print(f"Connected with result code {rc}")
    # Subscribe here!
    client.subscribe("testando/sensores/")
def on_message(client, userdata, msg):
#    print(f"Message received [{msg.topic}]: {msg.payload}")
    characters = [chr(ascii) for ascii in msg.payload] # Convert ASCII to char
    chars_joined = ''.join(characters) # Join chars to a string
    mensagemMQTT = chars_joined.split(";")     # Split string by comma
    novamsg=mensagemMQTT[0]+";"+str((int(mensagemMQTT[1])+10800))+";"+mensagemMQTT[2]+";"+mensagemMQTT[3]+";"+mensagemMQTT[4]+";"+mensagemMQTT[5]
#    print (novamsg)
    client.publish('reual/sensores', novamsg)
    



client = mqtt.Client("mqttTemp") # client ID "mqtt-test"
client.on_connect = on_connect
client.on_message = on_message
#client.username_pw_set("myusername", "aeNg8aibai0oiloo7xiad1iaju1uch")
client.connect('192.168.31.250', 1883)
client.loop_forever()  # Start networking daemon



#####
"""
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
    #client.subscribe(topic + '/leituras/#')
    client.subscribe(topic + '/#')
    client.on_message = on_message
    """
