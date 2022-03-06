const express = require('express');
const router = express.Router();
const conexion = require('./database/db')

router.get('/', (req, res)=>{
    res.send('INICIO');
})

router.get('/CRUD', (req,res)=>{
    conexion.query('SELECT * FROM DatosGenerales', (error, results)=>{
        if (error){
            throw error;
        }else{
            res.render('index', {results:results});
        }
    })

})

router.get('/create', (req,res)=>{
    res.render('create');
})


const crud = require('./controllers/crud');
module.exports = router;

router.post('/save', crud.save)

