
try:
	from my_xml_parser import MyXmlParser
except ImportError, e:
	print "ERROR!!! Missing module : ",format(e.message[16:])
	sys.exit(1)



def catalogo():
	""" 
	     retrieve all tv-series from telefilm.xml   
	     should build a list of telefilm catalog[<name-serie>].parameters (like quality)
	"""

	parser = MyXmlParser('telefilm.xml')
	
	n_series = parser.number_entries('serie')
	# return a list of entry like {title:'value',quality:'value'}
	entries = parser.get_list(n_series,['title','quality'],['\n','\t'])
	catalog = []
	for serie in entries:
		key = ((serie['title']+serie['quality']).replace(' ','')).lower()
		catalog.append(key)
	

	return catalog


