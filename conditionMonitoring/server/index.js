const http = require('http');
const fs = require('fs');
const request = require('request');

const serverIP = '10.0.122.233'; // Replace 'YOUR_SERVER_IP' with your server's IP address
const sendDataPort = 8080;
const clientEventsPort = 5001;

let client = null;
let dataQueue = []; // Queue to store data for POST requests

function sendToClient(data) {
    if (client) {
        console.log(data)
        client.write(`data: ${JSON.stringify(data)}\n\n`);
    }
}

function processQueue() {
    if (dataQueue.length > 0) {
        const data = dataQueue.shift(); // Take data from the queue

        // Send data to connected client immediately
        sendToClient(data);

        // Send data to Flask application asynchronously
        const options = {
            url: `http://10.0.122.233:5000/api/models/nlr/predict`,
            method: 'POST',
            json: data
        };

        request(options, (error, response, body) => {
            if (!error && response.statusCode === 200) {
                // Send the Flask response to connected client as a separate data packet
                sendToClient(body);
            } else {
                console.error('Error sending data to Flask:', error);
            }

            // Process next item in the queue
            processQueue();
        });
    }
}

http.createServer((req, res) => {
    if (req.method === 'POST' && req.url === '/sendData') {
        let body = '';
        req.on('data', (chunk) => {
            body += chunk;
        });
        req.on('end', () => {
            // Process received JSON data
            console.log('Received data from Bash script:', body);
            const parsedData = JSON.parse(body);

            // Add data to the queue for processing
            dataQueue.push(parsedData);

            // If queue was empty before, start processing
            if (dataQueue.length === 1) {
                processQueue();
            }
        });
        res.writeHead(200);
        res.end('Data received by server');
    } else {
        res.writeHead(404);
        res.end();
    }
}).listen(8080, () => {
    console.log(`Server running at http://${serverIP}:${sendDataPort}/`);
});

// Create a separate HTTP server for client events on port 5001
http.createServer((req, res) => {
    res.writeHead(200, {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Access-Control-Allow-Origin': '*'
    });
    res.write('\n');
    // Allow the client to connect to this server for events
    client = res;
    // Remove the client when the connection is closed
    req.on('close', () => {
        client = null;
    });
}).listen(5001, () => {
    console.log(`Client events server running at http://${serverIP}:${clientEventsPort}/`);
});
