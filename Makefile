SHELL := /bin/bash
init :
	flask init
	foreman start -m all=2

seedapi :
	chmod +x seedapi.sh
	./seedapi.sh
