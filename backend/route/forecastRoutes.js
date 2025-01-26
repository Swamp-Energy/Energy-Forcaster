const express = require('express');
const { getForecast, trainModel } = require('../controllers/forecastController');

const router = express.Router();

// Define Routes
router.get('/', getForecast); // GET /api/forecast
router.post('/train', trainModel); // POST /api/forecast/train

module.exports = router;
