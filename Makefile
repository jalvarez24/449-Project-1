SHELL := /bin/bash
init :
	ulimit -n 4096 && sudo kong start
	chmod +x kong_configuring.sh
	./kong_configuring.sh
	flask init
	foreman start -m all=3

startminio :
	chmod +x minio
	./minio server minio_data/

seedapi :
	chmod +x seedapi.sh
	./seedapi.sh
