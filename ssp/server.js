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

app.get("/run_ad_auction.js", (req, res) => {
  res.render(__dirname + "/public/run_ad_auction", { dsp_name: dsp_name });
});

// routes
app.get("/:name", (req, res) => {
  res.header("X-Allow-FLEDGE", "true");
  res.header("supports-loading-mode", "fenced-frame");

  const ext = req.params.name.split(".").pop();
  const has_no_extension = req.params.name == ext;

  if (has_no_extension) {
    // no extension
    res.sendFile(__dirname + "/public/" + req.params.name + ".html");
  } else {
    res.sendFile(__dirname + "/public/" + req.params.name);
  }
});

// launch server
server.listen(port, () => console.log("Server listening @ " + port));
