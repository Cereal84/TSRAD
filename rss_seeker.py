""" 
TSRAD - TV-Show RSS Auto Downloader
Copyright (C) 2011  Alessandro Pischedda

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

disclaims all copyright interest in the program `TSRAD' written by Alessandro Pischedda.
Contact me :
alessandro.pischedda@gmail.com

"""

# standard module
try:
	import os, sys
	import datetime
	import time
	import urllib2
	import pynotify
	import re
	import feedparser

	# mine modules
	from configuration import *
	from clients import *
	from models import *
	from daemon import Daemon
	from tool import *

except ImportError, e:
	print "ERROR!!! Missing module : ",format(e.message[16:])
	sys.exit(1)





class RSS_Daemon(Daemon):
	""" This function read the rss and if find a match in shows download the tv-show """

	def __init__(self,conf):
		Daemon.__init__(self,'daemon-rss.pid')
		self.conf = conf
		self.catalog = catalogo()
		self.locks = {}
		self.rss_urls = ["http://www.ezrss.it/feed","http://eztv.ptain.info/cgi-bin/eztv.pl?id=index&name=Latest%20Releases"]

	def __notify(self, message):
		""" Notify the message through pynotify """
	
		if pynotify.init("Tv-Serie"):
		        Alert = pynotify.Notification("TV RSS", message)
		        Alert.show()
		else:
		        print "Error starting pynotify"



	def __find_match(self,lista):
		""" Looking for some match between catalog and lista """
	
		download_list = []
		for show in self.catalog:
			if show.replace(' ','') in lista:
				download_list.append(show.replace(' ',''))
			
		return download_list


	def set_conf(self, conf):
		self.conf = conf

	def run(self):
		""" This function read the rss and if find a match in shows download the tv-show """
	
		last_feed = self.conf.get_last_feed()

		loop = True
		delay = 0 #used to see in the future :)

		while(loop):

			# DEBUG print "Check RSS: "+str(datetime.datetime.now())
			# 1- Download RSS feeds
			# 1.1 Open it
			
			url_found = False
			# Try until you've found an url rss that works else sleep
			for rss_url in self.rss_urls:

				# Assume that the url is unreachble after 10 seconds	
				try:
					f = urllib2.urlopen(rss_url, timeout=10)
					feeds = feedparser.parse(rss_url)
				except urllib2.URLError:
					continue

				else:
					url_found = True
					break # break only for
			if not url_found:
				self.__notify("RSS unreachble")
				# sleep for one hour
				time.sleep(60*60)
				continue # restart the while


			# 1.2 check if the rss is updated
			#if (last_feed == feeds.entries[0].updated) and (events.get_tv_changes() != 0) :
			#	print "devo controllare nei vecchi feed solo le nuove serie"

			if (str(last_feed) != str(feeds.entries[0].updated).replace(' ','') ):			

				tvs = {}	
				for tv in feeds["entries"]:
					# in this case we have'nt read this feed yet
					if str(tv.update).replace(' ','') != last_feed:
						# parse the rss entry and retrive serie - quality - episode 
						episode = re.findall(r'\d+x\d+',tv.title)
						split = re.split(r'\d+x\d+',tv.title)
						resto = split.pop()
						if len(split)>0:	
							quality = re.match(r'..720P', resto)
							if quality:
								tvshow = TvShow(split[0],episode[0],"720p",tv.link)
								#print str(split[0])+' '+str(episode[0])+' 720p'
							else :
								tvshow = TvShow(split[0],episode[0],"Normal",tv.link)
		
							tvs[split[0].replace(' ', '')+tvshow.get_quality()] = tvshow
					else:
						# old rss_feed so skip it
						break

				# 1.3 update the last_feed
				last_feed = str(feeds.entries[0].updated).replace(' ','')					
	
				self.conf.set_last_feed(last_feed)
				self.conf.save()

				# 2- Check for tv-shows you're interested
				download_list = self.__find_match(tvs.keys())
	
				# 3- Notify it using pynotify
				if len(download_list)>0:
					for serie in download_list:
						tv = tvs[serie.replace(' ','')]				
						message = str(tv)
						# redirect the std output and std error to /dev/null because deluge give some message error
						# which not depend on this script so we ignore the messages
						# the last & is used to put it in background.
						# NOTE it'll be removed, the daemon redirect all stream to null :)
					
						shell_command = self.conf.get_cl_command()+" "+tv.get_torrent()+" >& /dev/null &"
						self.__notify(message)		
						os.system(shell_command)
			
	
			# check time is in minutes
			delay = self.conf.get_time()			
		
			# See in the future :D
			future = datetime.timedelta(minutes = delay) + datetime.datetime.now()
	
			while(1):
				if future <= datetime.datetime.now():
					# time out
					break
				# DEBUG print "Nap Time"
				time.sleep(1)
				# DEBUG print "Wake Up"
	


