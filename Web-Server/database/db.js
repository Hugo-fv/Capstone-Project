const res = require('express/lib/response');
const mysql = require('mysql');

const conexion = mysql.createConnection({
    host:'localhost',
    user:'root',
    password: 'password',
    database:'RegistroAutobuses'
})

conexion.connect((error)=>{
    if (error){
        console.error ('Error en la base de datos ' + error);
        return
    }
    console.log('Conexión a la base de datos exitosa')
})

module.exports = conexion;