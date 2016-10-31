Below are instructions for installing osm2pgRouting and its dependencies on a Linux Debian machine.

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

#libpqf
	sudo apt-get install libpq-dev

#Install osm2pgrouting


first navigate to the downloads folder:

	cd ~/Downloads

download from github

	wget https://github.com/pgRouting/osm2pgrouting/archive/master.zip
							
unzip the file

	unzip master.zip //-d destination_folder

(if on a non-postgresql install machine, make sure you install **libpq-dev**)
	
	sudo apt-get install libpq-dev (optional)

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

install osmconvert to clip the OSM file to Denver: 

	sudo apt-get install osmctools

use OSMCONVERT to extract denver (optional): 

	osmconvert denver-boulder_colorado.osm -b=-105.147456690777,39.5853206121359,-104.561947277233,39.9431650145789 -o=denver_DPS.osm


Next, ensure your PostgreSQL search path points to the schema you want to load your OSM data into: 

To see current order, in pgAdmin SQL window:

	show search_path

Change to osm schema (schema must already be created) in SQL:

	set search_path = osm, public

While in Downloads/osm2pgrouting-master/build

	cd \Downloads/osm2pgrouting-master/build




Run osm2pgRouting - this will take your .OSM file and load it into the server you're specified:

	./osm2pgrouting -file ~/Downloads/denver-boulder_colorado.osm -conf ~/Downloads/osm2pgrouting-master/mapconfig.xml -host 860-10d2-data -dbname dps_osm -user postgres -passwd xxx -clean

Make sure you reset your search path in SQL:

	set search_path = public, osm










