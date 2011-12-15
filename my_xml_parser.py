from xml.dom.minidom import parseString
import sys

__author__ = "Alessandro Pischedda "
__date__ = "14-Dec-2011"

class MyXmlParser():
	""" This class is used to retrieve information from an xml file """

	def __init__(self,filename):
		self.filename = filename
		self.refresh_data()

	def __get_text(self,nodelist):
		for node in nodelist:
			if node.nodeType == node.TEXT_NODE:
				return node.data 

	def get_field(self, tag_name, del_chars = []):
		"""This method return the value between tags. 
		   You can clean it by specifying a list of characters to be replaced by ''.	
		"""
		try:
			tag_value = self.__get_text(self.dom.getElementsByTagName(tag_name)[0].childNodes)
		except:
			print "ERROR!!! xml tag "+str(tag_name)+" in "+str(self.filename)
			sys.exit(2)

		# clean it
		for char in del_chars:
			tag_value = tag_value.replace(char,'')
		return tag_value

	def get_list(self, n_entries,fields=[], del_chars = []):
		""" Return a list where each entry is a dictionary of fields name - value """
		lista = []
		for i in range(0, n_entries):
			entry = {}
			for tag_name in fields:
				#entry[tag_name] = str(self.__get_text(self.dom.getElementsByTagName(tag_name)[i].childNodes))
				tag_value = str(self.__get_text(self.dom.getElementsByTagName(tag_name)[i].childNodes))
				for char in del_chars: 
					tag_value = tag_value.replace(char,'')
				entry[tag_name] = tag_value
			lista.append(entry)

		return lista

	def refresh_data(self):
		""" open the xml file and read it """
		try:
			# open the xml file for reading:
			file = open(self.filename,'r')
			data = file.read()
			# close file cause we dont need it anymore
			file.close()
		except IOError:
			print "Some error is occured trying to open "+str(self.filename)
		        sys.exit(2)

		# parse the xml
		self.dom = parseString(data)

	def number_entries(self, tag_name):
		""" Return how many tag there are with that tag_name """
		n_entries = len( self.dom.getElementsByTagName(tag_name) )
		return n_entries
