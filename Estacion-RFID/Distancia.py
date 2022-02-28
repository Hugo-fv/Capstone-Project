import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BOARD)
distancia = 0
GPIO_TRIGGER = 29 #Trigger o disparador
GPIO_ECHO = 31 #Respuesta
GPIO.setup(GPIO_TRIGGER, GPIO.OUT) #El disparador es una salida.
GPIO.setup(GPIO_ECHO, GPIO.IN) #La respuesta es una entrada

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


while True:

    distancia = MedirDistancia()

    print('Distancia [cm]: %.2f' %distancia)
    time.sleep(5)

