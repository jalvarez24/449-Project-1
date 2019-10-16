init : 
	flask init
	foreman start

seedapi :
	chmod +x seedapi.sh
	./seedapi.sh