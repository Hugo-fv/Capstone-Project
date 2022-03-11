# Administración de transporte público.
## Capstone-Project. Diplomado de Internet de las cosas. Samsung Innovation Campus.

Este proyecto contiene los códigos y programas necesarios para la implementación de un sistema de monitoreo y recolección de datos en una terminal de autobuses y un conteo de pasajeros dentro de un autobús. Así mismo, presentamos una página web que permite visualizar los datos recolectados de una forma fácil y entendible.
## Primeros pasos.
Los requisitos de **hardware** mínimos para hacer funcionar este proyecto son los siguientes.

 1. Raspberry Pi Model B3+
 2. Sensor de ultrasonido HC-SR04.
 3. Antena RFID modulo RC522.
 4. Al menos, 2 etiquetas RFID.
 5. Dos sensores de presencia infrarrojos modulo TCRT5000 

Debes tener instalado previamente el siguiente **software**.

 - Librerías para Raspberry:
	 - [jsonpickle](https://jsonpickle.github.io/) para facilitar la gestión de JSON.
	 - [paho-mqtt](https://pypi.org/project/paho-mqtt/) para gestionar el envío de datos por MQTT.
	 - [MFRC522-python](https://github.com/mxgxw/MFRC522-python) para facilitar la lectura de la antena RFID RC522 (librería incluida en este repositorio).

Puedes instalar estas librerías con el gestión de librerías de Python. 

- Software para la máquina virtual.
	- MySQL
	- NodeJS con Express.
	- Node-RED.

## Organización del proyecto.
La organización de carpetas se divide en los elementos que están programados para ejecutarse en Raspberry Pi, y los que están programados para ejecutarse en la máquina virtual.

 - Carpetas para la Raspberry Pi.
	 - **Estacion-RFID**: El script "Estacion .py" coordina el sensor HC-RS04 con la antena RFID RC522  para el monitoreo y envío de datos por medio de internet de la estación (entrada y salida de autobuses). Se incluyen también dos scripts de ejemplo para la lectura de dichos sensores (lectura offline).
	 - **Contador-Infrarrojo**: El script "infrarrojo. py" permite monitorizar el numero de pasajeros que ingresa al autobus, para enviar esta información por internet.

-	Carpetas para la máquina virtual.
	-	**Databases**: Contiene una base de datos tipo SQL con tablas que contienen datos de ejemplo. 
	-	**Flows**: Contiene los *flows* de Node-RED que permiten una recepción de la información enviada por las estaciones y los autobuses. Además, incluye una simulación de entrada de datos.
	-	**Web-Server**: Contiene los archivos necesarios para visualizar una página web que permite una mejor visualización de los datos. Hace uso de *NodeJS y Express* para realizar una API-RESTful, y el gestor de plantillas *EJS*.

## Transito de la información.
El siguiente diagrama representa el transito de la información que realiza el sistema para almacenarse en la BD.
![Transito de la información](https://github.com/Hugo-fv/Capstone-Project/blob/main/Imagenes/transito-info.png)
