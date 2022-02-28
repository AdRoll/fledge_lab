const fs = require("fs");
const express = require("express");
const https = require("https");

const app = express();
const port = process.env.PORT;
const key = process.env.KEY;
const cert = process.env.CERT;

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
  res.sendFile(__dirname + "/public/ads/" + req.params.name + ".html");
});

app.get("/:name", (req, res) => {
  res.sendFile(__dirname + "/public/" + req.params.name + ".html");
});

app.get("/", (_req, res) => {
  res.sendFile(__dirname + "/public/index.html");
});

// launch server
server.listen(port, () => console.log("Server listening @ " + port));
