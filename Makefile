OS=$(shell uname)

create-certs:
	mkdir -p certificates
	docker build -t cert_creator cert_creator/. && docker run --rm -v ${PWD}/certificates:/certs cert_creator
	cp -a certificates/{cert.pem,key.pem} dsp/
	cp certificates/rootCA.pem client/

build:
	docker compose build

run:
	docker compose up

browser:
	docker exec fledge_lab-client-1 /bin/bash -c 'chrome $${CHROME_ARGS} $${FLEDGE_FLAGS} $${ARAPI_FLAGS}'

vnc:
ifeq ($(OS),Darwin)
	open vnc://:nextroll@localhost:5920
else
	echo "Unupported for ${OS}. You must connect to vnc://:nextroll@localhost:5920 manually."
endif

connect: vnc browser

experiments:
	docker exec -it fledge_lab-client-1  /opt/experiments.sh

enter-client:
	docker exec -it fledge_lab-client-1  /bin/bash

clear-certs:
	find . -name "*.pem" -type f -delete

clear-output:
	rm -rf output/*

install-hooks:
	pip install --user pre-commit
	pre-commit install
