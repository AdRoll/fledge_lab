create-certs:
	mkdir -p certificates
	docker build -t cert_creator cert_creator/. && docker run --rm -v ${PWD}/certificates:/certs cert_creator
	cp -a certificates/{cert.pem,key.pem} dsp/
	cp certificates/rootCA.pem selenium/

build:
	docker compose build

run:
	docker compose up

clear-certs:
	find . -name "*.pem" -type f -delete

clear-output:
	rm -rf output/*
