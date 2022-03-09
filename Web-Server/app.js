/*
Servidor Web para el sistema de autobuses.
Por: Victor Hugo Flores Vargas
Fecha de creacion: 25 de febrero.

El proyecto esta organizado de la siguiente forma.

1. app.js: Contiene los metodos necesarios para iniciar un servidor con Express
    y EJS (motor de plantillas de Javascript)
2. router.js: Maneja todas las peticiones GET para el correcto funcionamiento de la
    pagina web.
3. Carpeta 'views': contiene las plantillas EJS que permiten visualizar cada pagina
    que conforma la pagina web.
4. Carpeta 'controllers': contiene el archivo 'crud.js', el cual maneja la creacion y 
    edición del CRUD
5. Carpeta 'database': contiene la conexión con la base de datos 'RegistroAutobuses'

El proyecto utiliza las siguientes herramientas

1. Framework: Bootstrap 5
2. Uso de iconos: BoxIcons
3. Manejo de la tabla de registro de tiempos: Datatables
4. Manejo de graficos: ChartJS
5. Extras: Jquery y Poppet
6. Servidor: NodeJS con Express

*/


const express = require('express');
const app = express();


app.set('view engine', 'ejs');

app.use(express.urlencoded({extended:false}));
app.use(express.json());

app.use('/', require('./router'));



app.listen(5000, ()=>{
    console.log ('Servidor iniciado en http://localhost:5000')
});
