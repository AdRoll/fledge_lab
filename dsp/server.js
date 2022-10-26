const fs = require("fs");
const express = require("express");
const https = require("https");

const app = express();
app.set('view engine', 'ejs');
app.use(express.json()); // for POST request (ARAPI report)
const port = process.env.PORT;
const key = process.env.KEY;
const cert = process.env.CERT;
const dsp_name = process.env.DSP_NAME;
const ARAPI_REPORTS_REPO = '/opt/output/arapi_reports_repo';

const arapiEvents = {
  "add-to-cart": 0,
  checkout: 1,
  signup: 2,
  donation: 3,
  default: 4,
  // ... we have up to 3 bits
};
let arapiReportCounter = 0;


const server = https.createServer(
  {
    key: fs.readFileSync(key, "utf8"),
    cert: fs.readFileSync(cert, "utf8"),
  },
  app
);


// arapi: register source event (e.g. ad view)
app.get('/register-source', (req, res) => {
  res.set(
    'Attribution-Reporting-Register-Source',
    JSON.stringify({
      source_event_id: '123456789123456',  // u64 as string
      destination: 'https://advertiser',
      expiry: '36000'  // in seconds [1 day, 30 days]
      // can also add priority (i64 as string) and debug key (i64 as string)
    })
  )
  res.status(200).send('OK')
 });


 // arapi: register trigger - attribution/conversion event
 app.get('/arapi-trigger', (req, res) => {
  const triggerData = arapiEvents[req.query["type"]];
  res.set(
    'Attribution-Reporting-Register-Trigger',
    JSON.stringify(
      {
        event_trigger_data: [{
          trigger_data: `${triggerData}`
        }]
      }
    )
  )
  res.sendStatus(200);
 });

 // arapi: reports reception endpoint
app.post(
  "/.well-known/attribution-reporting/report-event-attribution",
  (req, res) => {
    let reportFilename = `/opt/output/arapi_reports_repo/${arapiReportCounter++}.json`;
    if (!fs.existsSync(ARAPI_REPORTS_REPO)) {
      fs.mkdirSync(ARAPI_REPORTS_REPO, { recursive: true });
    }
    fs.writeFile(reportFilename, JSON.stringify(req.body), (err) => {
      if (err) {
        console.error(err);
        return;
      }
    });
  }
);


app.get("/:name", (req, res) => {
  res.header("X-Allow-FLEDGE", "true");
  res.header("supports-loading-mode", "fenced-frame");

  let ext = req.params.name.split(".").pop();

  if (ext == 'js') {
    res.sendFile(__dirname + "/public/" + req.params.name);
  } else {
    res.render(__dirname + "/public/" + req.params.name, { dsp_name: dsp_name });
  }
});

// launch server
server.listen(port, () => console.log("Server listening @ " + port));
