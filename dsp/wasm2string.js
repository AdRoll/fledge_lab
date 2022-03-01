// this file converts a binary file into an array of its bytes in text format
// usage: node wasm2string.js input_bin.wasm output_uint8array.js
const fs = require("fs");

const myArgs = process.argv.slice(2);

const data = fs.readFileSync(myArgs[0]);
const newContent = Uint8Array.from(data).toString();
const output = `const wasmBin = Uint8Array.from([${newContent}]);\n`;
fs.writeFileSync(myArgs[1], output);
