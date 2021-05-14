==========
Installing
==========

7i76e Configuration Tool

.. Note:: Tested on Debian 10, no other OS is supported but it should
	work on other Debian type OS's.

.. Note:: Requires Python 3.6 or newer to work.

I now have a Debian deb for installing 7i76e!!!

Download the `deb <https://github.com/jethornton/7i76e/raw/master/7i76e_0.1.1_all.deb>`_

Or use wget from a terminal
::

	wget https://github.com/jethornton/7i76e/raw/master/7i76e_0.1.1_all.deb

If you get `bash: wget: command not found` you can install it from a terminal with
::

	sudo apt install wget

Check the md5sum of the downloaded deb to be sure you got it all. Open a
terminal in the directory containing the deb and issue the md5sum
::

	md5sum 7i76e_0.1.1_all.deb
	3acd14cbcd8172f3eb0fa3cbf69a76b2  7i76e_0.1.1_all.deb

Open the File Manager and right click on the file and open with Gdebi then install.

If you don't have Gdebi installed you can install it from a terminal
::

	sudo apt install gdebi

If you don't have LinuxCNC installed then the 7i76e Configuration tool
will show up in the Applications > Other menu otherwise it will be in
the CNC menu.

To flash firmware to the 7i76e you need to install 
`mesaflash <https://github.com/LinuxCNC/mesaflash>`_ from the LinuxCNC
repository.

To uninstall the 7i76e Configuration Tool right click on the .deb file
and open with Gdebi and select `Remove Package`.

To upgrade the 7i76e Configuration Tool delete the .deb file and download
a fresh copy then right click on the .deb file and open with Gdebi and
select `Reinstall Package`
