const fs = require('fs');
const express = require('express');
const https = require('https');

const app = express();
app.use(express.json());  // for POST request (ARAPI report)
const port = process.env.PORT;
const key = process.env.KEY;
const cert = process.env.CERT;

const arapiEvents = {
  'add-to-cart': 0,
  'checkout': 1,
  'signup': 2,
  'donation': 3,
  'default': 4,
  // ... we have up to 3 bits
};
let arapiReportCounter = 0;
fs.mkdirSync('/opt/output/arapi_reports_repo', { recursive: true });


const server = https.createServer({
    key: fs.readFileSync(key, 'utf8'),
    cert: fs.readFileSync(cert, 'utf8')
  }, app);

// routes
app.get('/arapi-register', (req, res) => {
  const triggerData = arapiEvents[req.query['type']];
  res.redirect(
    302,
    `https://dsp/.well-known/attribution-reporting/trigger-attribution?trigger-data=${triggerData}`
  );
});

app.post('/.well-known/attribution-reporting/report-attribution', (req, res) => {
  let reportFilename = `/opt/output/arapi_reports_repo/${arapiReportCounter++}.json`;
  fs.writeFile(reportFilename, JSON.stringify(req.body), (err) => {
    if (err) {  console.error(err);  return; };
  });
});

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
