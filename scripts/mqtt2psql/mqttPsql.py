import paho.mqtt.client as mqtt_client
import traceback
import psycopg2
from config import * 

#print("Connecting to database")
#connection = psycopg2.connect(
#	host = DatabaseHostName,
#	user = DatabaseUserName,
#	password = DatabasePassword,
#	database = DatabaseName,
#	port = DatabasePort
#)

## setup mqtt
#client_source = mqtt.Client(deviceId)
broker_source = brokerAdd
broker_source_port = brokerPort

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(deviceId)
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(brokerAdd, brokerPort)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic + '/#')
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()