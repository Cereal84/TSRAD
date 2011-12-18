#!/usr/bin/env python
try:
	import sys, os
	# mine
	from daemon import Daemon
	from configuration import Setup
	from rss_seeker import RSS_Daemon
except ImportError, e:
	print "ERROR!!! Missing module : ",format(e.message[16:])
	sys.exit(1)


if __name__ == "__main__":

	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:	
			conf = Setup()
			daemon = RSS_Daemon(conf)
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon = Daemon('daemon-rss.pid')
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			conf = Setup()
			daemon = RSS_Daemon(conf)
			daemon.restart()
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)
