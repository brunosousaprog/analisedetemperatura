from machine import Pin, unique_id 
from time import sleep
import dht
import network
import ubinascii
from umqtt.simple import MQTTClient


SSID = "************"  
PASSWORD = "*******" 
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883  
CLIENT_ID = ubinascii.hexlify(unique_id())
MQTT_TOPIC_TEMPERATURE = "sensor/temperatura"
MQTT_TOPIC_HUMIDITY = "sensor/umidade"

def conecta_wifi():
    wifi = network.WLAN(network.STA_IF)
    if not wifi.isconnected():
        print('Conectando à rede Wi-Fi...')
        wifi.active(True)
        wifi.connect(SSID, PASSWORD)
        while not wifi.isconnected():
            pass
    print('Conectado! Configurações de rede:', wifi.ifconfig())


conecta_wifi()


sensor = dht.DHT11(Pin(23))


client = MQTTClient(CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
client.connect()


while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        umid = sensor.humidity()

       
        print("Temperatura lida:", temp,"°celsius")
        client.publish(MQTT_TOPIC_TEMPERATURE, str(temp))

        print("Umidade lida:", umid,"%")
        client.publish(MQTT_TOPIC_HUMIDITY, str(umid))

        sleep(2)  

    except OSError as err:
        print("Falha na leitura dos dados", err)
