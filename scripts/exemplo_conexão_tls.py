#!/bin/python
from pickle import TRUE
import ssl
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Conectado com sucesso. Código de retorno: " + str(rc))
    client.subscribe("topico/teste")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.tls_set("./certs/ca.crt", "./certs/client.crt", "./certs/client.key")
client.tls_insecure_set(TRUE)
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.31.135", 8880)

client.loop_forever()

