# 449 Project 2: Music Microservices
## Database Sharding, XSPF Playlists and Load Balancing Proxy with Kong
### Group/Roles:
1. Dev1: Brendan Albert
2. Dev2: Ian Alvarez
3. Ops:  Jayro Alvarez

# To Start Using Our Microservices:
1. Open a terminal in Project Directory
	- Run command: `make init`. This will:
		- Run `ulimit -n 4096 && sudo kong start` and start kong
		- Run `./kong_configuring.sh`, a script to configure all microservices and
			set them up with kong's services, routes, upstreams, and target.
		- Run `flask init` and set up the database schema
		- Run `foreman start` to spin up our four microservices

2. Open another terminal in Project Directory
	- Run command `make startminio`. This will:
		- Run MinIO server to give access to physical mp3 files.

3. Open another terminal in Project Directory
	- Run command `make seedapi`. This will:
		- Fill database with various data

4. The servers are now running! Go to http://localhost:8000 to see full user manual



==================================================================================
## Phase 1
==================================================================================
### 449 Project 1: Music Microservices
#### Group/Roles:
1. Dev1: Ian Alvarez
2. Dev2: JayroAlvarez
3. Ops:  Brendan Albert
