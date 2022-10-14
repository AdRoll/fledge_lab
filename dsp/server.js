const fs = require("fs");
const express = require("express");
const https = require("https");

const app = express();
app.use(express.json()); // for POST request (ARAPI report)
const port = process.env.PORT;
const key = process.env.KEY;
const cert = process.env.CERT;
const ARAPI_REPORTS_REPO = '/opt/output/arapi_reports_repo';
const FLEDGE_REPORTS_REPO = '/opt/output/click_reports_repo';

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


// arapi: click on ad
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


// arapi: attribution/conversion event
 app.get('/arapi-register', (req, res) => {
  const triggerData = arapiEvents[req.query["type"]];
  res.set(
    'Attribution-Reporting-Register-Event-Trigger',
    JSON.stringify([
      {
        trigger_data: `${triggerData}`
      }
    ])
  )
  res.sendStatus(200);
 });


 // arapi: reports
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

// fledge click report
// NB: this currenly creates an empty file, it does not seem to write the actual request body.
// I tried playing around with it but had no luck. I see in the browser console that eventData is
// including in the request payload. That was good enough for me to confirm that we can send
// the ARAPI attribution source event ID through the fledge click report.  
app.post(
  "/click_reports",
  (req, res) => {
    const buyer_event_id = req.query.buyer_event_id;
    let reportFilename = `/opt/output/click_reports_repo/${buyer_event_id}.json`;
    if (!fs.existsSync(FLEDGE_REPORTS_REPO)) {
      fs.mkdirSync(FLEDGE_REPORTS_REPO, { recursive: true });
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

  if (req.params.name == ext) {
    // no extension
    res.sendFile(__dirname + "/public/" + req.params.name + ".html");
  } else {
    res.sendFile(__dirname + "/public/" + req.params.name);
  }
});

// launch server
server.listen(port, () => console.log("Server listening @ " + port));
