#!/usr/bin/python
# Filename: models.py


class Serie:
	""" This class is used to store the informations about the tv serie who user is interested """

	def __init__(self, title, quality):
		self.title = title
		self.quality = quality

	def set_title(self, name):
		self.title = name

	def set_quality(self,quality):
		self.quality = quality
	

class TvShow(Serie):
	""" This class store the information about an entry in RSS entry """

	def __init__(self, title, episode, quality, link):
		Serie.__init__(self,title, quality)
		self.episode = episode
		self.torrent = self.__clean_link(link)

	def __str__(self):
		return str(self.title)+' '+str(self.episode)+' '+str(self.quality)

	def __clean_link(self, link):
		""" Replaces '(' and ')' with '\(' '\)' because the shell don't like them """
		link = link.replace('(','\(')
		link = link.replace(')','\)')
		return link

	def set_title(self, name):
		self.title = name

	def set_quality(self,quality):
		self.quality = quality

	def set_episode(self, episode):
		self.episode = episode

	def set_torrent(self, torrent):
		self.torrent = self.__clean_link(torrent)

	def get_title(self):
		return self.title
	
	def get_quality(self):
		return self.quality
	
	def get_episode(self):
		return self.episode

	def get_torrent(self):
		return str(self.torrent)



