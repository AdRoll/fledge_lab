create-certs:
	mkdir -p certificates
	docker build -t cert_creator cert_creator/. && docker run --rm -v ${PWD}/certificates:/certs cert_creator
	cp -a certificates/{cert.pem,key.pem} dsp/
	cp certificates/rootCA.pem selenium/
	cp certificates/rootCA.pem client/

build:
	docker compose build

run:
	docker compose up

connect:
	open vnc://:nextroll@localhost

test:
	docker exec -it $(shell docker ps -qf "name=fledge_lab-client") /opt/tests.sh

clear-certs:
	find . -name "*.pem" -type f -delete

clear-output:
	rm -rf output/*

install-hooks:
	pip install --user pre-commit
	pre-commit install
