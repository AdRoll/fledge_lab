FROM debian:buster-20211201-slim as builder
SHELL ["/bin/bash", "-c"]

# Install required tools or dependencies for mkcert
RUN apt-get update && \
    apt-get install --no-install-recommends -y libnss3-tools wget ca-certificates

# Install local certificate creator for HTTPS (mkcert)
RUN wget https://github.com/FiloSottile/mkcert/releases/download/v1.4.3/mkcert-v1.4.3-linux-amd64 -O /usr/local/bin/mkcert && \
    chmod +x /usr/local/bin/mkcert

ENV CAROOT=/certs
RUN rm -f ${CAROOT}/*.pem && \
    mkcert -install && \
    mkcert -key-file ${CAROOT}/key.pem -cert-file ${CAROOT}/cert.pem localhost 127.0.0.1 ::1 advertiser ssp publisher dsp dsp{0..255} && \
    rm ${CAROOT}/rootCA-key.pem

FROM scratch
COPY --from=builder /certs /
