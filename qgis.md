#Install QGIS#

Open Terminal by typing `Ctrl+Alt+T`

Add links to the QGIS software repositories to your sources.list file:


	sudo sh -c 'echo "deb http://qgis.org/debian trusty main" >> /etc/apt/sources.list'

	sudo sh -c 'echo "deb-src http://qgis.org/debian trusty main " >> /etc/apt/sources.list'

Then add the QGIS  keyservers:

	wget -O - http://qgis.org/downloads/qgis-2015.gpg.key | gpg --import

	gpg --fingerprint 3FF5FFCAD71472C4

Now install QGIS:

	sudo apt-get update && sudo apt-get install qgis python-qgis

And if you want the GRASS plugin, use this install command:

	sudo apt-get update && sudo apt-get install qgis python-qgis qgis-plugin-grass

You now have QGIS Installed!