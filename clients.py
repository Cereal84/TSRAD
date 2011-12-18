#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import string
from my_xml_parser import MyXmlParser

__author__ = "Alessandro Pischedda"
__date__ = "15-Dec-2011"


""" This file contain the functions about the bittorrent clients. """

def read_clients():
	""" Retrieve from clients.xml file the list of the supported clients """

	parser = MyXmlParser('clients.xml')
	
	n_clients = parser.number_entries('client')
	# return a list of entry like {name:'value',command:'value'}
	entries = parser.get_list(n_clients,['name','command'],['\n','\t'])
	clients = {}
	for client in entries:
		clients[str(client['name'])] = str(client['command'])
		
	return clients
	

def find_clients(client_list):
	""" Check which clients in the list are installed """

	for client in client_list.keys():
		check = "/usr/bin/"+client
		if not os.path.isfile(check):
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

	

