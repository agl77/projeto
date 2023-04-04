import paho.mqtt.client as mqtt_client
#import traceback
import psycopg2
import random
import time
from config import * 
client_mqtt = 'aviso' + deviceId + f'-{random.randint(0, 1000)}'
client = mqtt_client.Client(client_mqtt)
intervalo = 60


print("Conectando ao banco de dados")
connection = psycopg2.connect(
	host = DatabaseHostName,
	user = DatabaseUserName,
	password = DatabasePassword,
	database = 'MQTTbee',
	port = DatabasePort
)


def consultaBd():
    with connection.cursor() as cursor:
        cursor.execute("select id_sensor,id_unidade,valor_dado from tbl_dado order by id_dado desc limit 4")
        dados = cursor.fetchall()
        ext_temp = 0
        ext_umi = 0
        cx1_temp = 0
        cx1_umi = 0
        for i in range (0,4):
            if (dados[i][0])==1:
                if ((dados[i][1]))==1:
                    ext_temp=(dados[i][2])
                elif ((dados[i][1]))==2:
                    ext_umi=(dados[i][2])
            if (dados[i][0])==2:
                if ((dados[i][1]))==1:
                    cx1_temp=(dados[i][2])
                    print (cx1_temp)
                elif ((dados[i][1]))==2:
                    cx1_umi=(dados[i][2])
        
        informac=(f"{ext_temp};{ext_umi};{cx1_temp};{cx1_umi}")
        
        print('dados: ')
        print(dados)
        print('apresentador/valores/'+str(informac))
        if client.is_connected():
            client.publish(topic+'/apresentador/valores',str(informac), qos=1, retain=1)
            print('Publicado')
        else:
            client.connect(brokerAdd, brokerPort, keepalive=intervalo+10)
            print('conectando mqtt novamente')
                    

if __name__ == '__main__':
    #client.loop_forever()
    client.connect(brokerAdd, brokerPort, keepalive=intervalo+10)
    client.loop_start()
    while True:
        consultaBd()
        time.sleep(intervalo)
        

