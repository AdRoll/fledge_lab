#!/bin/bash

mkcert -install
mkcert -key-file /certs/key.pem -cert-file /certs/cert.pem localhost 127.0.0.1 ::1 \
    advertiser ssp dsp dsp0 dsp1 dsp2 dsp3 dsp4 dsp5 dsp6 dsp7 dsp8 dsp9 dsp10  \
    dsp11 dsp12 dsp13 dsp14 dsp15 dsp16 dsp17 dsp18 dsp19 dsp20 dsp21 dsp22 dsp23 \
    dsp24 dsp25 dsp26 dsp27 dsp28 dsp29 dsp30 dsp31 dsp32 dsp33 dsp34 dsp35 dsp36 \
    dsp37 dsp38 dsp39 dsp40 dsp41 dsp42 dsp43 dsp44 dsp45 dsp46 dsp47 dsp48 dsp49 \
    dsp50 dsp51 dsp52 dsp53 dsp54 dsp55 dsp56 dsp57 dsp58 dsp59 dsp60 dsp61 dsp62 \
    dsp63 publisher
rm certs/rootCA-key.pem  #  delete the CA's private key
