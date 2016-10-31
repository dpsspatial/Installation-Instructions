Below are instructions for installing osm2pgRouting and its dependencies on a Linux Debian machine. (Note this assumes PostGIS and pgRouting are already installed)

#Install Dependencies

#cmake
	sudo apt-get install build-essential -y //perhaps not necessary

	sudo apt-get install cmake

#boost
	sudo apt-get install libboost-all-dev

or:
	sudo apt-get install boost

#expat
	sudo apt-get install expat libexpat1-dev

#libpq
This installs the Postgresql binaries for non pgSQL server machines

	sudo apt-get update && sudo apt-get install libpq-dev

#Install osm2pgrouting


first navigate to the downloads folder:

	cd ~/Downloads

download from github

	wget https://github.com/pgRouting/osm2pgrouting/archive/master.zip
							
unzip the file

	unzip master.zip

	cd osm2pgrouting-master

	cmake -H. -Bbuild

	cd build/

	make

	sudo make install


#Get latest OSM file for Denver/Boulder

go to downloads

	cd ~/Downloads

get the file from mapzen

	wget https://s3.amazonaws.com/metro-extracts.mapzen.com/denver-boulder_colorado.osm.bz2

unzip the file

	bzip2 -d denver-boulder_colorado.osm.bz2

#Load OSM Data into pgRouting

While in \Downloads, go to location of osm2pgrouting  

	cd \osm2pgrouting-master/build

Run osm2pgRouting - this will take your .OSM file and load it into the server you're specified, including the new flag for *--schema*, which in this case will load the data into a schema on the database called *osm*:

	./osm2pgrouting -f ~/Downloads/denver-boulder_colorado.osm -c ~/Downloads/osm2pgrouting-master/mapconfig.xml --schema osm --prefix osm_ -h pghostname -d pgdatabasename -U pgusername -W pgpassword --clean

Note: the paramters above and more instructions can be found here: [https://github.com/pgRouting/osm2pgrouting#how-to-use](https://github.com/pgRouting/osm2pgrouting#how-to-use)











