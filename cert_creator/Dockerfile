FROM debian:buster-20211201-slim

# Install required tools or dependencies for mkcert
RUN apt update && \
    apt install -y libnss3-tools wget

# Install local certificate creator for HTTPS (mkcert)
RUN wget https://github.com/FiloSottile/mkcert/releases/download/v1.4.3/mkcert-v1.4.3-linux-amd64 && \
    mv mkcert-v1.4.3-linux-amd64 /usr/local/bin/mkcert && \
    chmod +x /usr/local/bin/mkcert

COPY generate_certificates.sh .
RUN chmod +x generate_certificates.sh
ENV CAROOT=/certs
CMD ["./generate_certificates.sh"]
