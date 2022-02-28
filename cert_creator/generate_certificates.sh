#!/bin/bash

mkcert -install
mkcert -key-file /certs/key.pem -cert-file /certs/cert.pem \
    localhost 127.0.0.1 ::1 advertiser ssp publisher dsp dsp{0..255}
rm certs/rootCA-key.pem  #  delete the CA's private key
