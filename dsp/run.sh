#!/bin/bash

set -e

# Create the bidding logic (JS with embedded WASM) file. This is because the worklets
# do not support the typical method of WASM consumption (async loading), see:
# https://github.com/WICG/turtledove/issues/224#issuecomment-926043640
# it takes the WASM binary, converts it into a JS Uint8Array and then prepends
# this file to the actual JS bidding file that will use it
# TODO: explore a better way of doing this, one possible way can be found here
# https://github.com/WICG/turtledove/pull/250
node wasm2string.js bidding_logic_wasm_bg.wasm bidding_logic_wasm.bytes && \
    cat bidding_logic_wasm.bytes public/bidding_logic_wasm_template.js > combined.js && \
    mv combined.js public/bidding_logic_wasm.js

node server.js
