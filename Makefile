SHELL := /bin/bash
init :
	flask init
	foreman start -m all=3

seedapi :
	chmod +x seedapi.sh
	./seedapi.sh
