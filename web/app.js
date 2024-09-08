const express = require('express')
const path = require('path')
const fs = require('fs')
const { spawn } = require('child_process');


const app = express()
const port = 3000

app.use(express.static(path.join(__dirname)));
app.use('/images', express.static(path.join(__dirname, '..', 'images')));

app.get('/api/images', (req, res) => {
  const images = fs.readdirSync(path.join(__dirname, '..', 'images'))
  res.json(images)
})

app.get('/api/display', (req, res) => {
  const { image } = req.query;
  if (!image) return res.status(400).send('Image parameter is required');

  const pythonProcess = spawn('python', ['../display/display.py', '../images/' + image]);


  pythonProcess.on('error', () => {
    console.error('Error:', error.toString());
    res.status(500).send('Error displaying image');
  });

  pythonProcess.on('close', code => {
    if (!errorOccurred) {
      if (code === 0) {
        res.send(image + ' displayed successfully');
        console.log(image + ' displayed successfully')
      } else {
        handleError(`Python script exited with code ${code}`);
      }
    }
  });

});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`)
})