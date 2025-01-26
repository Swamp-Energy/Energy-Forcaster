const express = require('express');
const dotenv = require('dotenv');
const cors = require('cors');
const bodyParser = require('body-parser');
const forecastRoutes = require('./routes/forecastRoutes');
const weatherRoutes = require('./routes/weatherRoutes');

dotenv.config(); // Load environment variables

const app = express();

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Routes
app.use('/api/forecast', forecastRoutes);
app.use('/api/weather', weatherRoutes);

module.exports = app;
