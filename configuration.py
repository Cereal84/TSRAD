#!/usr/bin/python
# -*- coding: utf-8 -*-
try:
	import os, sys
	import string
	from xml.dom.minidom import parseString, Document
	from clients import *
	from my_xml_parser import MyXmlParser
except ImportError, e:
	print "ERROR!!! Missing module : ",format(e.message[16:])
	sys.exit(1)

""" Class to store and manage the configuration """

class Setup(MyXmlParser):
	""" This class is used to store the configuration parameters 
		time -> it's how much it must sleep until it can scan again the feeds
		default-client -> the bittorrent client 
		last_feed 
	"""

	def __init__(self):
		" Automatically retrieve the information about the configuration in configuration.xml"
		MyXmlParser.__init__(self,"configuration.xml")
		self.time = 0
		self.default_client = ""
		self.client_command = ""
		self.last_feed = ""
		self.read_conf()
		self.__check_configuration()

	def __add_entry(self, xml, tag_name, tag_value):
		""" Add a entry in configuration.xml. This is a private method. """
		tag = Document().createElement(tag_name)
		xml.appendChild(tag)
		value = Document().createTextNode(tag_value)
		tag.appendChild(value)


	def __client(self):
		clients_list = read_clients()
		clients_supported = clients_list.keys()
		find_clients(clients_list)
		if len(clients_list.keys()) > 1:
			client = choose_client(clients_list.keys())
			self.set_client(client,clients_list[client])
			self.save()
		else:
			print "There isn't bittorrent client supported installed on your system."
			print "Install one of these clients:"
			for name in clients_supported:
				print name
			sys.exit(2)

	def __check_configuration(self):
		# if there isn't the default client try to have one
		if self.default_client == "":
			print "Default client not found"
			self.__client()
	
		# check inf the default client is still installed
		if not os.path.isfile("/usr/bin/"+self.get_client()):
			print self.get_client()+" was set as default but isn't installed."
			print "Please install it or choose another one"
			self.__client()
			sys.exit(2)

	def __getText(nodelist):
		for node in nodelist:
		        if node.nodeType == node.TEXT_NODE:
		            return node.data

	def set_time(self, time):
		self.time = time

	def set_client(self,client, command):
		self.default_client = client
		self.client_command = command
		

	def set_last_feed(self, last_feed):
		self.last_feed = str(last_feed)

	def get_time(self):
		""" the variable time is used in the function sleep() so it will be an int """
		return int(self.time)
	
	def get_client(self):
		return str(self.default_client)

	def get_cl_command(self):
		return str(self.client_command)

	def get_last_feed(self):
		return str(self.last_feed)

	def read_conf(self):
		""" Retrieve configuration parameters from configuration.xml """
		
		# if the file doesn't exsist create it with default value
		if not os.path.isfile("configuration.xml"):
			print "Configuration file - CREATE"
			self.set_default()
		else:
			self.refresh_data()
	
		# non so perché ma mi mette anche i \n, \t and white space
		self.time = self.get_field("check_time",['\n','\t',' '])
		self.default_client = self.get_field("client_bt",['\n','\t',' '])
		self.client_command = self.get_field("client_cmd",['\n','\t',' '])
		self.last_feed = self.get_field("last_feed",['\n','\t',' '])
				


	def save(self):
		""" Save in the configuration.xml the new values.
		    This function rewrite all the configuration file. 		
		"""	

		# Create the minidom document
		doc = Document()

		# Create the <configuration> base element
		xml = doc.createElement("configuration")
		doc.appendChild(xml)

		self.__add_entry(xml, "check_time", str(self.time) )
		self.__add_entry(xml, "client_bt", self.default_client)
		self.__add_entry(xml, "client_cmd", self.client_command)
		self.__add_entry(xml, "last_feed", str(self.last_feed))

		try:
			file = open('configuration.xml','w')
			file.write(str(doc.toprettyxml(indent="  ")))
			file.close()	
			
		except IOError:
			print "Some error is occured trying to save data in configuration.xml"
		        sys.exit(2)



	def set_default(self):
		""" Set the default values for configuration """
		self.time = 60
		self.default_client = ""
		self.client_command = ""
		self.save()

	def show(self):
		print "Check time [minute/s]: "+str(self.time)
		print "Default client: "+self.default_client
	


