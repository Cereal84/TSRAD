
try:
	import os
	from xml.dom.minidom import parseString
	import clients
except ImportError, e:
	print "ERROR!!! Missing module : ",format(e.message[16:])
	sys.exit(1)



def catalogo():
	""" 
	     retrieve all tv-series from telefilm.xml   
	     should build a list of telefilm catalog[<name-serie>].parameters (like quality)
	"""

	try :
		# open the xml file for reading:
		tv_file = open('telefilm.xml','r')
	except IOError:
		print "Some error is occured trying to open the telefilm.xml file"
		sys.exit(2)

	# convert to string:
	data = tv_file.read()
	# close file cause we dont need it anymore
	tv_file.close()
	# parse the xml
	dom = parseString(data)
	n_entries = len( dom.getElementsByTagName('title') )
	catalog = []
	for i in range(0, n_entries):
		# retrieve the first xml tag (<tag>data</tag>) that the parser finds with name tagName:
		xmlTag = dom.getElementsByTagName('title')[i].toxml()
		# strip off the tag (<tag>data</tag>  --->   data):
		xmlData=xmlTag.replace('<title>','').replace('</title>','')
		xmlTag = dom.getElementsByTagName('quality')[i].toxml()
		xmlQuality = xmlTag.replace('<quality>','').replace('</quality>','')
		catalog.append(xmlData+xmlQuality)

	return catalog


