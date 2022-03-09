import RPi.GPIO as GPIO
import time
import signal
import json
import jsonpickle
import paho.mqtt.client as mqtt
total = 0

GPIO.setmode(GPIO.BOARD)
subir = 11
bajar = 13

client = mqtt.Client()
BufferJson = ''
BrokerMQTT = "18.197.171.34"

GPIO.setup(subir,GPIO.IN)
GPIO.setup(bajar,GPIO.IN)

client.connect(BrokerMQTT, 1883, 60)
while 1:
   lec_bajar = GPIO.input(bajar)
   lec_subir = GPIO.input(subir)
   if lec_subir == 0:
      total = total + 1
 #     print("Subio una persona")
   if lec_bajar == 0:
  #    print("Bajo una persona")
      total = total - 1
   print(total)
   time.sleep(1)
   Bufferjson = jsonpickle.encode(total, unpicklable=False)
   print(BufferJson)
   client.publish('raspb/registro', Bufferjson)
