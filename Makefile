init : 
	flask init
	foreman start

addusers :
	chmod +x users.sh
	./users.sh

addtracks :
	chmod +x addtracks.sh
	./addtracks.sh

seedapi :
	chmod +x seedapi.sh
	./seedapi.sh