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

router.get('/registro', (req,res)=>{
    res.render('registro');
});



const crud = require('./controllers/crud');
const res = require('express/lib/response');
module.exports = router;

router.post('/save', crud.save);
router.post('/update', crud.update);

