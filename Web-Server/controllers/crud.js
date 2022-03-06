const conexion = require('../database/db');
const mysql = require('../database/db');

exports.save = (req,res) =>{
    const user = req.body.user;
    const nombre = req.body.nombre;
    const unidad = req.body.unidad;

    conexion.query('INSERT INTO DatosGenerales SET ?', {uid:user, nombre:nombre, n_camion:unidad}, (err, results)=>{
        if (err){
            console.log(err);
        }else{
            res.redirect('/crud');
        }
    })

}

