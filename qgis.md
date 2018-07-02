# Install QGIS on Ubuntu or Linux Mint

## Check Version and Codename

First, what version of Debian Linux (Ubuntu / Mint) are you running?

The codename of your APT repository will depend on the version of the OS and which version of QGIS you can run.

QGIS 3.x will run on Ubuntu 18.04 (bionic) and Linux Mint 19 (bionic) and *above*.

QGIS 2.18.x will run on Ubuntu 16.04 (xenial) and Linux Mint 18.x (xenial) and *below*.

## Add links to QGIS repositories

Open Terminal by typing `Ctrl+Alt+T`

Add links to the QGIS software repositories to your sources.list file:


	sudo sh -c 'echo "deb http://qgis.org/debian codename main" >> /etc/apt/sources.list'

and...

	sudo sh -c 'echo "deb-src http://qgis.org/debian codename main " >> /etc/apt/sources.list'

Then add the QGIS  keyservers:

	wget -O - https://qgis.org/downloads/qgis-2017.gpg.key | gpg --import

Then...

	gpg --fingerprint CAEB3DC3BDF7FB45

Now add the public key to APT (don't miss that dash at the end...):

	gpg --export --armor CAEB3DC3BDF7FB45 | sudo apt-key add -

## Install QGIS

	sudo apt-get update && sudo apt-get install qgis python-qgis

And if you want the GRASS plugin, use this install command:

	sudo apt-get update && sudo apt-get install qgis python-qgis qgis-plugin-grass

You now have QGIS Installed!
