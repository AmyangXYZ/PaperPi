const express = require('express');
const path = require('path');
const fs = require('fs').promises;
const crypto = require('crypto');
const multer = require('multer');
const { spawn } = require('child_process');

const app = express();
const port = 3000;

// Configure multer for file upload
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, path.join(__dirname, '..', 'images'))
  },
  filename: function (req, file, cb) {
    const uniqueSuffix = crypto.randomBytes(16).toString('hex');
    cb(null, uniqueSuffix + path.extname(file.originalname))
  }
});

const upload = multer({
  storage: storage,
  fileFilter: (req, file, cb) => {
    if (file.mimetype.startsWith('image/')) {
      cb(null, true);
    } else {
      cb(new Error('Not an image! Please upload an image.'), false);
    }
  }
}).single('image');

app.use(express.static(path.join(__dirname)));

app.post('/api/upload', (req, res) => {
  upload(req, res, async (err) => {
    if (err instanceof multer.MulterError) {
      console.error('Multer error:', err);
      return res.status(400).send(err.message);
    } else if (err) {
      console.error('Unknown error:', err);
      return res.status(500).send('An unknown error occurred');
    }

    if (!req.file) {
      return res.status(400).send('No file uploaded.');
    }

    const filePath = req.file.path;
    const pythonScriptPath = path.join(__dirname, '..', 'display', 'display.py');

    console.log(`Image saved: ${filePath}`);
    console.log(`Python script path: ${pythonScriptPath}`);

    try {
      await fs.access(pythonScriptPath);
    } catch (error) {
      console.error('Python script not found:', error);
      return res.status(500).send('Error: Python script not found');
    }

    const pythonProcess = spawn('python3', [pythonScriptPath, filePath]);

    let stdoutData = '';
    let stderrData = '';

    pythonProcess.stdout.on('data', (data) => {
      stdoutData += data;
      console.log(`Python stdout: ${data}`);
    });

    pythonProcess.stderr.on('data', (data) => {
      stderrData += data;
      console.error(`Python stderr: ${data}`);
    });

    pythonProcess.on('error', (error) => {
      console.error('Error spawning Python process:', error.toString());
      res.status(500).send('Error displaying image: ' + error.toString());
    });

    pythonProcess.on('close', (code) => {
      console.log(`Python process exited with code ${code}`);
      if (code === 0) {
        res.send(`Image uploaded and displayed successfully. Saved as ${req.file.filename}`);
        console.log('Image displayed successfully');
      } else {
        res.status(500).send(`Python script exited with code ${code}. Error: ${stderrData}`);
      }
    });
  });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send('Something broke!');
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});