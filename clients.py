#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import string
from xml.dom.minidom import parseString

""" This file contain the functions about the bittorrent clients. """

def read_clients():
	""" Retrieve from clients.xml file the list of the supported clients """

	try :
		# open the xml file for reading:
		file = open('clients.xml','r')
		# convert to string:
		data = file.read()
		# close file cause we dont need it anymore
		file.close()
		# parse the xml
		dom = parseString(data)	
		n_entries = len( dom.getElementsByTagName('client') )
		clients = {}
		for i in range(0, n_entries):
			# retrieve the first xml tag (<tag>data</tag>) that the parser finds with name tagName:
			xmlTag = dom.getElementsByTagName('name')[i].toxml()
			# strip off the tag (<tag>data</tag>  --->   data):
			client_name = xmlTag.replace('<name>','').replace('</name>','')
			xmlTag = dom.getElementsByTagName('command')[i].toxml()
			client_command = xmlTag.replace('<command>','').replace('</command>','')
			clients[client_name] = client_command

		return clients

	except IOError:
		print "Some error is occured trying to open clients.xml"
	        sys.exit(2)
			
	

def find_clients(client_list):
	""" Check which clients in the list are installed """

	for client in client_list.keys():
		check = "/usr/bin/"+client
		if not os.path.exists(check):
			del client_list[client]

def choose_client(client_list):
	""" Return the default client choosen by the user """

	while(True):
		print "Found the following bittorrent client/s on your system :"
		index = 0
		for name in client_list:
			print str(index)+" - "+str(name)
			index = index + 1

		print "Choose which client use to default"

		try :
			option = int( raw_input("Please enter your option [0-"+str(index-1)+"] : ") )
			n_options = len(client_list)
			

			if option in range(0,n_options):
				# insert the client in configuration file
				return client_list[option]
			else :
				print "Option not supported, please insert again"
				print ""
		except :
			print "Option not supported, please insert again"
			print ""


def download_torrent(client_name, torrent_url):
	""" Teorically each bittorrent client need a particoular method """
	

