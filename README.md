TSRAD - TV-Show RSS Auto Downloader
===================================

Date : 2011
Version : 0.2
Require : Python 2.6 - 2.7

DESCRIPTION
-----------

This software is born in order to automatize the download of tv-shows using torrent file. It uses rss feeds from eztv ( http://www.ezrss.it/ ) to know if a certain tv-show is available to be downloaded.
More precisely it act like a Unix daemon and it's still an alpha version so it hasn't much features and his use isn't much user-friendly yet.
This software is released with GPLv2 License. For now it's compatible only with Linux OS.


BITTORRENT CLIENT SUPPORTED
---------------------------

To download torrent file you need one of this client bittorrent:

* Transmission
* Deluge
* Ktorrent
* QBittorrent


SETUP CLIENT
------------

Usually when you add a torrent the client will ask you if you want download the torrent and where you want to put it. If you want disable this option take a look at the following istructions.


TRANSMISSION
		Edit -> Preferences -> Panel Torrents -> Uncheck "Show options dialog"

DELUGE
		Edit -> Preferences -> Interface -> Uncheck "Show always" in "Add torrent"

Qbittorrent
		Tools -> Options -> Download Uncheck "Display torrent content and some options"

I suggest to check this option, apply the change and uncheck the option and re-apply the change because sometimes it doesn't work.


HOW TO USE
----------

As a daemon it perform start and stop actions.

To start the daemon open the shell, go where you've copied this directory and type :

		python tsrad.py start

to stop it 
	
		python tsrad.py stop

At the first start probably (the configuration file should be "empty") it'll ask which client bittorrent you want to use. Obviously it check if any of them are installed in your system. To make sure it happens you can delete configuration.xml, the daemon create one and ask you which client you want to use.

[NOTE]
For KDE users, there's some problem with initialization. I don't know why but KDE returns false negative about the bittorrent clients so I invite you to write down in configuration.xml the client-name and the command  as following example :

  ...
  <client_bt>
	ktorrent
  </client_bt>
  <client_cmd>
	ktorrent
  </client_cmd>
  ...
 
I'll try to fix this bug.

Add/Remove/modify a tv-show
For now the only way is to modify telefilm.xml that you can find in this direcory. This file is an XML file composed with entry like the following :

	<serie>
		<title>TITLE</title>
		<quality>QUALITY</quality>
	</serie>

So if you want add a tv-show you must add an entry like this. The quality field is used to know which version (Normal - 720p or 1080p ) of releases you want to download. 
When you do it stop the daemon and when you've done restart it. This procedure is necessary to avoid inconsisten data.

NOTE
With the second version you can write the tv-show's title in any format except l33t. For who doesn't know the l33t please go to :
	http://en.wikipedia.org/wiki/Leet .


CONFIGURATION FILE
------------------

The configuration file is configuration.xml, it contains the following informations
	- check time 	 : this time indicate how often check the rss
	- client	 : client name
	- client command : command to execute the client bittorrent.
	- last feed 	 : date about last feed read, it's necessary to not re-scan older feeds.

Because it's an alpha if you want to change client or change the check time you must change the configuration.xml


ADD UNSUPPORTED CLIENT
----------------------

If you use a client that isn't supported yet you can modify the clients.xml file adding an entry like 

	<client>
		<name>CLIENT_NAME</name>
		<command>SHELL_COMMAND_TO_EXECUTE_CLIENT</command>
	</client>

it should works.


CHANGELOG
---------

VERSION 0.1

+ Act like an Unix Daemon
+ Compatible only with Linux OS
+ Only start and stop actions
+ Use XML file to store configuration, tv-shows list and client specifications

VERSION 0.2
+ Active waiting removed
+ Improved xml data retrieval
+ improved title match, now you can write a tv_show's title in any format ( NOT l33t )


VERSION 0.3

- Abbandoned XML
+ Use of SQLite 3

THANKS
------
Sander Marechal
The part about "daemonize" is taken from a work of Sander Marechal, more precisely from one of his articles that you can find at the following url
http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/


LICENSE GPLv2


CONTACT 
-------

alessandro.pischedda@gmail.com
Alessandro Pischedda
