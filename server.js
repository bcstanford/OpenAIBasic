const express = require('express');
const WebSocket = require('ws');
const path = require('path');
const { spawn } = require('child_process');

// Create a new express application
const app = express();

// Serve static files from the 'public' directory
app.use(express.static('public'));

// Start the web server
const server = app.listen(3000, 'localhost', function () {
  console.log('Listening on http://localhost:3000');
});

// Create a WebSocket server
const wss = new WebSocket.Server({ server });

wss.on('connection', function connection(ws) {
  ws.on('message', function incoming(message) {
    console.log('received: %s', message);

    // Call the Python script
    const python = spawn('python', ['main.py']);
    python.stdin.write(message + '\n');
    python.stdin.end();

    python.stdout.on('data', function (data) {
      console.log('Pipe data from python script ...');
      ws.send(data.toString());
    });

    python.stderr.on('data', (data) => {
      console.error(`stderr: ${data}`);
    });
  });
});