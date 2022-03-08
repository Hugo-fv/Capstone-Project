
"""
# Lectura del sensor RFID, sensor Ultrasonico y envio
# de datos por MQTT
# Por: Victor Hugo Flores Vargas
# Fecha: 22 de febrero del 2022

# El siguiente codigo se utiliza en la Raspberry Pi para la estacion
# de autobuses que se desee supervisar. Se coordinan dos sensores 
# que permiten el correcto funcionamiento del sistema: el sensor
# de distancia Ultrasonico y la antena RFID. 

# La logica de programacion es sencilla. Primero, se comprueba que 
# haya un objeto delante (simulando la presencia de un autobus);
# posteriormente, se comprueba que haya un identificador RFID
# valido cerca de la antena RFID, para despues almacenar los datos 
# mas relevantes en un objeto. Por ultimo, se comprueba que el objeto 
# se haya retirado, para posteriormente enviar el objeto en forma de JSON
# por MQTT.

# Diagrama de conexion

##  RC522 -> Raspberry Pi B3+

    SDA  ->  Pin 24
    SCK  ->  Pin 23
    MOSI ->  Pin 19
    MISO ->  Pin 21
    GND  ->  GND
    RST  ->  Pin 22
    3.3V ->  3.3V

##  HC-SR04 -> Raspberry Pi B3+

    Vcc  ->  5V
    TRIG ->  Pin 29 
    ECHO ->  Pin 31 # IMPORTANTE: Se debe realizar un divisor de voltaje
    GND  ->  GND

Nota: Para mas informacion sobre el divisor de voltaje, consultar el contenido
del curso pertinentes.
"""
#Librerias 
import RPi.GPIO as GPIO #Libreria que permite usar los pines
import MFRC522  #Libreria que nos facilita el manejo del lector RC522
import signal
import time #LIbreria que nos permite manejar el tiempo
import json #Liberia que permite leer y transformar JSON
import jsonpickle #Libreria que nos permite transformar objetos a JSON 
import paho.mqtt.client as mqtt #Libreria para el uso de MQTT

#Definir el tipo numerado de los pines
GPIO.setmode(GPIO.BOARD)

#Objetos

RFID = MFRC522.MFRC522() #Objeto que contiene los metodos para leer el RC522
client = mqtt.Client() #Objeto que maneja la mensajeria por MQTT

#Clases

class Autobus (): #Clase vacia que se puede serializar como JSON
    pass

InfoAutobus = Autobus() #Variable de tipo Autobus
InfoAutobus.id_estacion = 10 #La estacion es constante

#Variables

BufferID = '' #Buffer para guardar temporalmente la id de la RFID. Comienza vacio
BanderaRegistro = False #Bandera que indica si ya se verifico la tarjeta
KeepGoing = True #Variable que controla el bucle principal
BufferJson = '' #Buffer que almacena el JSON antes de mandarlo por MQTT
BrokerMQTT = "18.197.171.34"
UmbralDistancia = 17.0 #Distancia maxima (cm) para decir si hay un objeto delante del sensor

##Variables del sensor Ultrasonico

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

#Definimos a la funcion end_read como el final del programa


# Conectamos con el broker MQTT (HiveMQ)
client.connect(BrokerMQTT, 1883, 60)
## NOTA: si se usa un broker publico, se debe actualizar la direccion
## constantemente

#Programa Principal

print ('Programa iniciado. Esperando tarjetas.')
try:
    while KeepGoing: #Loop principal
	client.loop_start() #Reconecta el cliente MQTT si se ha desconectado
        if MedirDistancia() < UmbralDistancia : #Si hay un objeto, entonces
            (status,TagType) = RFID.MFRC522_Request(RFID.PICC_REQIDL) # Comprobamos si hay una tarjeta
        
            if status == RFID.MI_OK: #Si hay una tarjeta valida, entonces
                print('TARJETA VALIDA ENCONTRADA') 
                (status,uid) = RFID.MFRC522_Anticoll() #Tratamos de obtener el UID de la tarjeta
            
                if status == RFID.MI_OK: #Si pudimos obtener el UID de la tarjeta, entonces
                    id = str(uid[0]) + str(uid[1]) + str(uid[2])# + str(uid[3]) #Guardamos el UID en una variable
                
                    if BufferID != id: # Si la UID que guardamos es diferente a la registrada anteriormente, entonces
                        print('NUEVA TARJETA. Guardando informacion')
                        BanderaRegistro = True # Activamos la bandera que indica que ya se registro esa UID
                        BufferID = id # Guardamos en el buffer la nueva ID
                        InfoAutobus.h_entrada= time.time() # Obtenemos la hora de entrada y la guardamos
                        InfoAutobus.id_autobus = id # Guardamos la UID en el objeto
                
                    else: # Si la UID es igual a la del buffer...
                        print('MISMA TARJETA. Reintentando...')
                        time.sleep(2) # Pausa bloqueante necesaria (2 segundos)
    
        elif MedirDistancia() > UmbralDistancia and BanderaRegistro == True : #Si no hay objeto y ya se ha registrado una tarjeta
            BanderaRegistro = False # No se ha registrado una UID
            InfoAutobus.h_salida = time.time() # Guardamos la hora de salida del autobus
            BufferJson = jsonpickle.encode(InfoAutobus, unpicklable=False) # Guardamos en un Buffer el JSON generado
            print(BufferJson) # Verificamos por terminal el JSON generado
            client.publish('raspb/autobuses', BufferJson) # Publicamos el JSON en un tema de MQTT.

#Fin del programa principal.

#Ctrl+C para detener la ejecucion
except KeyboardInterrupt:
    print('Programa detenido')

#Deja libre el GPIO
finally:
    client.loop_stop() #Detiene la conexión con el Broker
    GPIO.cleanup() #Limpia el GPIO







