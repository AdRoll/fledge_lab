const fs = require("fs");
const express = require("express");
const https = require("https");

const app = express();
app.set('view engine', 'ejs');
const port = process.env.PORT;
const key = process.env.KEY;
const cert = process.env.CERT;
const dsp_name = process.env.DSP_NAME;

const server = https.createServer(
  {
    key: fs.readFileSync(key, "utf8"),
    cert: fs.readFileSync(cert, "utf8"),
  },
  app
);

// routes
app.get("/ads/:name", (req, res) => {
  // required header to allow fenced frames, see:
  // https://github.com/WICG/nav-speculation/blob/main/opt-in.md#declaration
  res.header("supports-loading-mode", "fenced-frame");
  res.render(__dirname + "/public/ads/" + req.params.name, { dsp_name: dsp_name });
});

app.get("/:name", (req, res) => {
  res.render(__dirname + "/public/" + req.params.name, { dsp_name: dsp_name });
});

app.get("/", (_req, res) => {
  res.render(__dirname + "/public/index", { dsp_name: dsp_name });
});

// launch server
server.listen(port, () => console.log("Server listening @ " + port));
