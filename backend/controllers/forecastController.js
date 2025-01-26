const { spawn } = require('child_process');

// Fetch forecast data
exports.getForecast = async (req, res) => {
    try {
        // Example placeholder response
        res.status(200).json({ message: 'Forecast fetched successfully', data: [] });
    } catch (err) {
        res.status(500).json({ message: 'Error fetching forecast', error: err.message });
    }
};

// Train ML model
exports.trainModel = async (req, res) => {
    try {
        // Spawn Python process to train the model
        const pythonProcess = spawn('python', ['./ml/train.py']);

        pythonProcess.stdout.on('data', (data) => {
            console.log(`stdout: ${data}`);
        });

        pythonProcess.stderr.on('data', (data) => {
            console.error(`stderr: ${data}`);
        });

        pythonProcess.on('close', (code) => {
            console.log(`Child process exited with code ${code}`);
            res.status(200).json({ message: 'Model trained successfully' });
        });
    } catch (err) {
        res.status(500).json({ message: 'Error training model', error: err.message });
    }
};
