const res = require('express/lib/response');
const conexion = require('../database/db');
const mysql = require('../database/db');

exports.save = (req,res) =>{
    const user = req.body.user;
    const nombre = req.body.nombre;
    const unidad = req.body.unidad;

    conexion.query('INSERT INTO users SET ?', {uid:user, nombre:nombre, n_camion:unidad}, (err, results)=>{
        if (err){
            console.log(err);
        }else{
            res.redirect('/crud');
        }
    })
}

exports.update = (req,res)=>{
    const id = req.body.id;
    const uid = req.body.user;
    const nombre = req.body.nombre;
    const unidad = req.body.unidad;

    conexion.query('UPDATE users SET ? WHERE id = ?',[{uid:uid, nombre:nombre, n_camion:unidad}, id], (error, results)=>{
        if (error){
            throw error;
        }else{
            res.redirect('/crud');
        }
    })
}



