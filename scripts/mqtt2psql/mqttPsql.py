import paho.mqtt.client as mqtt_client
import traceback
import psycopg2
import random
from config import * 
client_mqtt = deviceId + f'-{random.randint(0, 1000)}'

print("Connecting to database")
connection = psycopg2.connect(
	host = DatabaseHostName,
	user = DatabaseUserName,
	password = DatabasePassword,
	database = DatabaseName,
	port = DatabasePort
)

## setup mqtt
#client_source = mqtt.Client(deviceId)

def insertIntoDatabase(message):
	"Inserts the mqtt data into the database"
	with connection.cursor() as cursor:
		print("Inserting data: " + str(message.topic) + ";" + str(message.payload)[2:][:-1] + ";" + str(message.qos))
		cursor.callproc('InsertIntoMQTTTable', [str(message.topic), str(message.payload)[2:][:-1], int(message.qos)])
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

    client.subscribe(topic + '/#')
    client.on_message = on_message
	


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()



if __name__ == '__main__':
    run()
