FROM python:3.9.9-slim-buster

# Install required tools or dependencies for mkcert
RUN apt update && \
    apt install -y libnss3-tools wget unzip

# Install local certificate creator for HTTPS (mkcert)
RUN wget https://github.com/FiloSottile/mkcert/releases/download/v1.4.3/mkcert-v1.4.3-linux-amd64 && \
    mv mkcert-v1.4.3-linux-amd64 /usr/local/bin/mkcert && \
    chmod +x /usr/local/bin/mkcert

WORKDIR /opt

# Create local certificate authority using the shared CA
RUN mkdir -p $HOME/.pki/nssdb && certutil -d sql:$HOME/.pki/nssdb -N --empty-password
RUN mkcert -install

# Install TigerVNC to have a display so we can use Chromium in headful mode as headless fails to run auctions
# Set password for VNC to fledgevnc (no real need for security in this context, just need a password)
# .Xauthority is required by VNC to be able to use a display
RUN apt install -y tigervnc-standalone-server xorg && \
    mkdir $HOME/.vnc && echo fledgevnc | vncpasswd -f > $HOME/.vnc/passwd && \
    touch $HOME/.Xauthority
ENV DISPLAY=:0

# Install Chromium dependencies
RUN apt install -y gconf-service libasound2 libatk1.0-0 libatk-bridge2.0-0 libc6 libcairo2 libcups2 \
                    libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 \
                    libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 \
                    libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates \
                    fonts-liberation libappindicator1 lsb-release xdg-utils

# Install Chromium
ARG CHROMIUM_REVISION
RUN wget http://commondatastorage.googleapis.com/chromium-browser-snapshots/Linux_x64/$CHROMIUM_REVISION/chrome-linux.zip && \
    unzip chrome-linux.zip && \
    echo "export PATH=/opt/chrome-linux:$PATH" >> /root/.bashrc && \
    rm chrome-linux.zip

# Install the Chromium driver for selenium
RUN wget http://commondatastorage.googleapis.com/chromium-browser-snapshots/Linux_x64/$CHROMIUM_REVISION/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver_linux64/chromedriver /usr/local/bin && \
    rm chromedriver_linux64.zip

RUN apt install -y tesseract-ocr
RUN pip install selenium==4.1.0 pillow==8.4.0 pytesseract==0.3.8 pandas==1.3.5 seaborn==0.11.2 statsmodels==0.13.1

RUN mkdir output && \
    mkdir scripts

COPY rootCA.pem .
ENV CAROOT=/opt
RUN mkcert -install

COPY scripts/. scripts/
COPY *.sh .
RUN chmod +x run.sh launch_browser.sh
CMD ["./run.sh"]
