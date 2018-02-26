#Install QGIS#

**NOTE**: This is geared towards Debian (Ubuntu, Mint) version 16.04 (Xenial). If you're using a different version, please replace the words "Xenial" below with your version's nickname (14.04 is "Trusty")

Open Terminal by typing `Ctrl+Alt+T`

Add links to the QGIS software repositories to your sources.list file:


	sudo sh -c 'echo "deb http://qgis.org/debian xenial main" >> /etc/apt/sources.list'

and...

	sudo sh -c 'echo "deb-src http://qgis.org/debian xenial main " >> /etc/apt/sources.list'

Then add the QGIS  keyservers:

	wget -O - https://qgis.org/downloads/qgis-2017.gpg.key | gpg --import

Then...

	gpg --fingerprint CAEB3DC3BDF7FB45

Now add the public key to APT:

	gpg --export --armor CAEB3DC3BDF7FB45 | sudo apt-key add -

Now install QGIS:

	sudo apt-get update && sudo apt-get install qgis python-qgis

And if you want the GRASS plugin, use this install command:

	sudo apt-get update && sudo apt-get install qgis python-qgis qgis-plugin-grass

You now have QGIS Installed!
