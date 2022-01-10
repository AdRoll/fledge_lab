const fs = require('fs');
const express = require('express');
const https = require('https');

const app = express();
const port = process.env.PORT;
const key = process.env.KEY;
const cert = process.env.CERT;

const server = https.createServer({
    key: fs.readFileSync(key, 'utf8'),
    cert: fs.readFileSync(cert, 'utf8')
  }, app);

// routes
app.get('/:name', (req, res) => {
  res.header('X-Allow-FLEDGE', 'true');
  res.header('supports-loading-mode', 'fenced-frame');

  let ext =  req.params.name.split('.').pop();

  if (req.params.name == ext) {  // no extension
    res.sendFile(__dirname + '/public/' + req.params.name + '.html');
  } else {
    res.sendFile(__dirname + '/public/' + req.params.name);
  }
});

// launch server
server.listen(port, () => console.log('Server listening @ ' + port));
