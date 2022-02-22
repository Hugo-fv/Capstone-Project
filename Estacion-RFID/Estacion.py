
"""
# Lectura del sensor RFID, sensor Ultrasonico y envio
# de datos por MQTT
# Por: Victor Hugo Flores Vargas
# Fecha: 22 de febrero del 2022
# 
# El siguiente codigo se utiliza en 
#
#

"""
#Librerias 
import RPi.GPIO as GPIO #Libreria que permite usar los pines
import MFRC522  #Libreria que nos facilita el manejo del lector RC522
import signal
import time #LIbreria que nos permite manejar el tiempo
import json #Liberia que permite leer y transformar JSON
import paho.mqtt.client as mqtt #Libreria para el uso de MQTT

#Definir el tipo numerado de los pines
GPIO.setmode(GPIO.BOARD)

#Objetos

RFID = MFRC522.MFRC522() #Objeto que contiene los metodos para leer el RC522
client = mqtt.Client() #Objeto que maneja la mensajeria por MQTT

#Clases

class Autobus (): #Clase vacia que se puede serializar como JSON
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

InfoAutobus = Autobus() #Variable de tipo Autobus
InfoAutobus.id_estacion = 510 #La estacion es constante

#Variables
BufferID = '' #Buffer para guardar temporalmente la id de la RFID. Comienza vacio
BanderaRegistro = False #Bandera que indica si ya se verifico la tarjeta
KeepGoing = True #Variable que controla el bucle principal
BufferJson = '' #Buffer que almacena el JSON antes de mandarlo por MQTT

##Variables del sensor Ultrasonico
GPIO.setmode(GPIO.BOARD)
GPIO_TRIGGER = 29 #Trigger o disparador
GPIO_ECHO = 31 #Respuesta
GPIO.setup(GPIO_TRIGGER, GPIO.OUT) #El disparador es una salida.
GPIO.setup(GPIO_ECHO, GPIO.IN) #La respuesta es una entrada

#Funciones del usuario
##Funcion que mide la distancia con el sensor Ultrasonico y la devuelve

def MedirDistancia():
    # El pin del disparador en 1 (alto)
    GPIO.output(GPIO_TRIGGER, True)
 
    # Dejamos el pin del disparador en alto por 10 ms y luego lo ponemos en 0
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    
    # Variables para guardar el tiempo
    StartTime = time.time()
    StopTime = time.time()
 
    # Guardamos el tiempo inicial
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # Guardamos el tiempo final
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # La diferencia entre ambos tiempos es el tiempo que ha pasado
    TimeElapsed = StopTime - StartTime
    # Multiplicamos por la velocidad del sonido (34300 cm/s) para obtener cm
    # y dividimos entre 2, pues el tiempo es de ida y vuelta
    distancia = (TimeElapsed * 34300) / 2
 
    return distancia

#Funcion que captura e interpreta Ctrl+C en la consola
def end_read(signal,frame):
    global KeepGoing
    print ('FIN DEL PROGRAMA')
    KeepGoing = False
    GPIO.cleanup() #Deja libre los pines cuando se termina el programa

#Definimos a la funcion end_read como el final del programa
signal.signal(signal.SIGINT, end_read)


client.connect("3.126.191.185", 1883, 60)
#Programa Principal

while KeepGoing: #Loop principal

    if MedirDistancia() < 6 : #Si hay un objeto, entonces
        (status,TagType) = RFID.MFRC522_Request(RFID.PICC_REQIDL) #
        if status == RFID.MI_OK:
            print('Tarjeta encontrada')
            (status,uid) = RFID.MFRC522_Anticoll()
            if status == RFID.MI_OK:
                id = str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3])
                if BufferID != id:
                    BanderaRegistro = True
                    BufferID = id
                    InfoAutobus.h_entrada= time.time()
                    InfoAutobus.id_autobus = id
                else:
                    print('Misma tarjeta. Intente de nuevo')
                    time.sleep(2)
    
    elif MedirDistancia() > 6 and BanderaRegistro == True : #Si no hay objeto y ya se ha registrado una tarjeta
        BanderaRegistro = False
        InfoAutobus.h_salida = time.time()
        BufferJson = json.dumps(InfoAutobus.toJSON())
        print(BufferJson)
        client.publish('raspb/autobuses', BufferJson)





