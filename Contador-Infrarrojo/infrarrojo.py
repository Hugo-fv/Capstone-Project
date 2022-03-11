# Medicion del sensor infrarrojo TCRT5000 y envio
# de datos por MQTT
# Por: Rogelio Emmanuel Lopez Garcia
# Fecha: 22 de Febrero del 2022
# Proyecto Capstone - CodigoIoT

# El siguiente codigo tiene la funcion de contar personas
# y enviar datos por MQTT destinado al transporte publico
# como parte del proyecto de Capstone de parte de Codigo
# IOT 2021-2022.

# El sistema se compone de una raspberry pi 4, dos sensores
# infrarrojos TCR5000 conectadas a la misma, un sensor esta
# destinado a posicionarse en la puerta de subida del autobus
# y el otro esta destinado a estar en la puerta de bajada y en
# la raspberry se hace el procesamiento y el envio de datos.

# El sensor infrarrojo TCRT5000 tiene la facilidad de tener 
# cuatro pines, el primero es el VCC el cual esta en el rango
# de 3.3V-5V, en el segundo se encuentra GND (tierra), el 
# siguiente es un pin digital (D0) y el pin analogico (A0), en 
# este caso solo utilizamos VCC y GND para alimentar el sensor
# y el pin digital el cual nos ayuda mucho por que unicamente 
# tiene dos estados "0" que significa que hay un objeto enfrente
# y "1" donde no hay nada enfrente aparte de tener un led integrado
# el sensor que se prende cada que detecta un objeto todo esto va 
# conectado a la raspberry pi por medio de jumpers hembra-macho.

# Diagrama de conexion

# Sensores infrarrojo TCRT5000 -> Rasberry Pi 4
#   
#   Primer sensor -> Rasberry Pi 4
#
#             VCC -> Pin 1
#             GND -> Pin 9
#              D0 -> Pin 11
#
#
#   Segundo sensor -> Rasberry Pi 4
#
#             VCC -> Pin 17
#             GND -> Pin 25
#              D0 -> Pin 13


# Se incluyen las librerias necesarias para el proyecto

import RPi.GPIO as GPIO #Libreria que permite usar los pines
import time #Libreria que permite manejar el tiempo
import signal
import json #Libreria que permite leer y transformar JSON
import jsonpickle #Libreria que nos permite transformar objetos a JSON
import paho.mqtt.client as mqtt #Libreria para el uso de MQTT
total = 0 #Definimos una variable que contendra el valor total de los pasajeros

#Definir el tipo de numerado de los pides
GPIO.setmode(GPIO.BOARD)
subir = 11 #Definimos el pin de la raspberry para el sensor de subida
bajar = 13 #Definimos el pin de la raspberry para el sensor de bajada

#Clases
class Sensor (): #Clase vacia que se puede serializar como JSON
   pass


ContaSensor = Sensor() #Definimos una variable y le asignamos la clase
ContaSensor.total = 0 #Variable para el total de personas 
ContaSensor.id_contador= 1914229 #Variable estatica con la id del camion

client = mqtt.Client() #Objeto que maneja la mensajeria por MQTT
BufferJson = '' #Buffer para guardar temporalmente el total de pasajeros
BrokerMQTT = "18.197.171.34" #Colocamos la direccion del broker

#Conectamos con el broker MQTT (HiveMQ)
client.connect(BrokerMQTT, 1883, 60) #
# Nota: si se usa un broker publico, se debe actualizar la direccion
# constantemente

#Definimos los pines de la Raspberry Pi como entrada
GPIO.setup(subir,GPIO.IN)
GPIO.setup(bajar,GPIO.IN)
hora_anterior = time.time() #Definimos una variable que guarde el tiempo antes del loop 


while 1: #Loop principal
   hora_actual =time.time() #Definimos una variable que guarde el tiempo empezado el loop
   lec_bajar = GPIO.input(bajar) #Definimos una variable que lea el sensor de bajada
   lec_subir = GPIO.input(subir) #Definimos una variable que lea el sensor de de subida
   if lec_subir == 0: #Si la lectura es igual a cero sumamos uno a la variable total
      total = total + 1
   if lec_bajar == 0: #Si la lectura es igual a cero restamos uno a la variable total
      if total > 0:
         total = total - 1
   print(total) #Imprimimos el total para verificar que este contando de manera correcta
   time.sleep(1) #Esperamos un segundo porque la velocidad del loop puede ser muy rapida

   if hora_actual - hora_anterior > 30: #Si ya pasaron 30 segundos entramos al if
      hora_anterior = hora_actual #Restablecemos la hora anterior
      ContaSensor.total = total #Asignamos el valor de total
      ContaSensor.hora = hora_actual #Asignamos la hora que vamos a mandar
      Bufferjson = jsonpickle.encode(ContaSensor, unpicklable=False) #Guarmos en al buffer el JSON generado
      print(Bufferjson) #Verificamos por terminal el JSON
      client.publish('raspb/registro', Bufferjson) #Publicamos el JSON en un tema de MQTT
