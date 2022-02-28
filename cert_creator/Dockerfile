FROM debian:buster-20211201-slim

# Install required tools or dependencies for mkcert
RUN apt update && \
    apt install --no-install-recommends -y libnss3-tools wget ca-certificates

# Install local certificate creator for HTTPS (mkcert)
RUN wget https://github.com/FiloSottile/mkcert/releases/download/v1.4.3/mkcert-v1.4.3-linux-amd64 && \
    mv mkcert-v1.4.3-linux-amd64 /usr/local/bin/mkcert && \
    chmod +x /usr/local/bin/mkcert

COPY generate_certificates.sh .
RUN chmod +x generate_certificates.sh
ENV CAROOT=/certs
CMD ["./generate_certificates.sh"]
