FROM node:17.1.0-buster-slim

# Install required tools or dependencies for mkcert
RUN apt update && \
    apt install -y libnss3-tools wget curl build-essential

# Install local certificate creator for HTTPS (mkcert)
RUN wget https://github.com/FiloSottile/mkcert/releases/download/v1.4.3/mkcert-v1.4.3-linux-amd64 && \
    mv mkcert-v1.4.3-linux-amd64 /usr/local/bin/mkcert && \
    chmod +x /usr/local/bin/mkcert

WORKDIR /opt

COPY *.pem .
ENV CAROOT=/opt
RUN mkcert -install

# Install npm dependencies
RUN npm install express

##### Rust portion for WASM
# TODO: add multi-stage build? Image size is not a concern for this at the moment though
# Install Rust and wasm-pack
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:$PATH"
RUN curl https://rustwasm.github.io/wasm-pack/installer/init.sh -sSf | sh

RUN mkdir -p bidding-logic-wasm/src
COPY bidding-logic-wasm/Cargo.* bidding-logic-wasm/

# caching trickery, is there a better way to do this?
RUN echo "fn dummy() {}" > bidding-logic-wasm/src/lib.rs && \
    cd bidding-logic-wasm && \
    wasm-pack build && \
    rm src/lib.rs

# Compile WASM
COPY bidding-logic-wasm/src/lib.rs bidding-logic-wasm/src/.
RUN cd bidding-logic-wasm && \
    wasm-pack build && \
    mv pkg/bidding_logic_wasm_bg.wasm /opt/.
#####

COPY server.js .
COPY public/ public/.

# Create the bidding logic (JS with embedded WASM) file. This is because the worklets
# do not support the typical method of WASM consumption (async loading), see:
# https://github.com/WICG/turtledove/issues/224#issuecomment-926043640
# it takes the WASM binary, converts it into a JS Uint8Array and then prepends
# this file to the actual JS bidding file that will use it
# TODO: explore less hacky ways of doing this once we actually get WASM to work
COPY wasm2string.js .
RUN node wasm2string.js bidding_logic_wasm_bg.wasm bidding_logic_wasm.bytes && \
    cat bidding_logic_wasm.bytes public/bidding_logic_wasm.js >> combined.js && \
    mv combined.js public/bidding_logic_wasm.js

ENV CERT=./cert.pem
ENV KEY=./key.pem
CMD ["node", "server.js"]
