const express = require('express');
const router = express.Router();
const conexion = require('./database/db');

router.get('/', (req, res)=>{
    res.render('principal')
});

router.get('/CRUD', (req,res)=>{
    conexion.query('SELECT * FROM users', (error, results)=>{
        if (error){
            throw error;
        }else{
            res.render('index', {results:results});
        }
    });

});

router.get('/create', (req,res)=>{
    res.render('create');
});

router.get('/edit/:id', (req,res)=>{
    const id = req.params.id;
    conexion.query('SELECT * FROM users WHERE id = ?', [id], (error,results)=>{
        if (error){
            throw error;
        }else{
            res.render('edit', {user:results[0]});
        }
    })
})

router.get('/delete/:id', (req, res)=>{
    const id = req.params.id;
    conexion.query('DELETE FROM users WHERE id= ? ', [id], (error, results)=>{
        if (error){
            throw error;
        }else{
            res.redirect('/crud')
        }
    });
})



router.get('/prueba', (req,res)=>{
    conexion.query('SELECT DG.uid, nombre, n_camion, id_estacion, DATE_FORMAT(FROM_UNIXTIME(h_entrada), "%H:%i") AS Entrada, DATE_FORMAT(FROM_UNIXTIME(h_salida), "%H:%i") AS Salida, DATE_FORMAT(FROM_UNIXTIME(h_entrada), "%d-%m-%Y") AS Fecha FROM users DG JOIN estacion HR ON DG.uid = HR.uid', (error, results)=>{
        if (error){
            throw error;
        }else{
            res.send(results);
        }
    });
});

router.get('/registro', (req,res)=>{
    res.render('registro');
})



const crud = require('./controllers/crud');
const res = require('express/lib/response');
module.exports = router;

router.post('/save', crud.save);
router.post('/update', crud.update);

