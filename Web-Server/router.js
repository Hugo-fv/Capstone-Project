const express = require('express');
const router = express.Router();


router.get('/hola', (req, res)=>{
    res.send('INICIO');
})

module.exports = router;