import RPi.GPIO as GPIO #Libreria que permite usar los pines
import time #Libreria que permite manejar el tiempo
import signal
total = 0 #Definimos una variable que contendrá el valor total de los pasajeros

#Definir el tipo de numerado de los pides
GPIO.setmode(GPIO.BOARD)
subir = 11 #Definimos el pin de la raspberry para el sensor de subida
bajar = 13 #Definimos el pin de la raspberry para el sensor de bajada

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