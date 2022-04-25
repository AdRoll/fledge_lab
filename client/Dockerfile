# syntax=docker/dockerfile:1.3-labs
FROM ubuntu:20.04
ARG TARGETPLATFORM
WORKDIR /opt
SHELL ["/bin/bash", "-c"]


# Install required tools or dependencies for mkcert
RUN apt update && \
    apt install --no-install-recommends -y libnss3-tools wget curl unzip ca-certificates


# Cert stuff (TODO: Don't use arch-specific binaries??)
RUN apt install --no-install-recommends -y libnss3-tools ca-certificates
RUN wget --no-check-certificate https://github.com/FiloSottile/mkcert/releases/download/v1.4.3/mkcert-v1.4.3-linux-arm64 && \
    mv mkcert-v1.4.3-linux-arm64 /usr/local/bin/mkcert && \
    chmod +x /usr/local/bin/mkcert
RUN mkdir -p $HOME/.pki/nssdb && certutil -d sql:$HOME/.pki/nssdb -N --empty-password
RUN mkcert -install
COPY rootCA.pem .
ENV CAROOT=/opt
RUN mkcert -install


# Install VNC
RUN DEBIAN_FRONTEND=noninteractive apt install --no-install-recommends -y x11vnc xvfb libgtk-3-0

# Install Chromium and Chromium Driver (for Selenium)
ARG CHROMIUM_REVISION
RUN <<EOF
  if [ $TARGETPLATFORM == 'linux/arm64' ]
  then
    apt install --no-install-recommends -y chromium-browser chromium-chromedriver
    ln -sfn $(which chromium-browser) /usr/bin/chrome
  else
    apt install --no-install-recommends -y gconf-service libasound2 libatk1.0-0 libatk-bridge2.0-0 libc6 libcairo2 libcups2 \
                    libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 \
                    libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 \
                    libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates \
                    fonts-liberation libappindicator1 lsb-release xdg-utils libgbm-dev

    wget http://commondatastorage.googleapis.com/chromium-browser-snapshots/Linux_x64/$CHROMIUM_REVISION/chrome-linux.zip
    unzip chrome-linux.zip
    ln -sfn /opt/chrome-linux/chrome /usr/bin/chrome
    rm chrome-linux.zip

    wget http://commondatastorage.googleapis.com/chromium-browser-snapshots/Linux_x64/$CHROMIUM_REVISION/chromedriver_linux64.zip
    unzip chromedriver_linux64.zip
    mv chromedriver_linux64/chromedriver /usr/bin/
    rm chromedriver_linux64.zip
  fi
EOF


# Install Python + Selenium
RUN <<EOF
  apt install --no-install-recommends -y software-properties-common tesseract-ocr
  add-apt-repository -y ppa:deadsnakes/ppa
  apt install -y python3.9 python3.9-distutils
  curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
  python3.9 get-pip.py
  ln -sfn /usr/bin/python3.9 /usr/bin/python
  pip install --upgrade pip
  pip install selenium==4.1.0 pillow==8.4.0  # NOTE(Chris): For some reason I needed to install pillow before the rest
  pip install pytesseract==0.3.8 pandas==1.3.5 seaborn==0.11.2 statsmodels==0.13.1
EOF

RUN mkdir output

COPY scripts/. scripts/
COPY entrypoint.sh experiments.sh ./

# necessary for VNC (see entrypoint.sh)
ENV DISPLAY=:20

ENTRYPOINT ["/opt/entrypoint.sh"]
