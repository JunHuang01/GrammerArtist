# Scraper.py
# Date created: 5/10/14
# trevor.prater@gmail.com (Trevor Prater)
# jun.huang.cs@gmail.com (Jun Huang)

import os
import re
import sys
import pytumblr
import json
from datetime import datetime, timedelta 
from PIL import Image

class Scraper: 
	
	#Constructors
	def cleanupImageFolder(self):
		os.system('rm -r ./images')
		os.system('mkdir images')
	
	def __init__(self):
		__init__(self,searchTerms)
	
	def __init__(self,searchTerms):
		print "No image count given. Defaulting to 1000 images."
		__init__(self,searchTerms,1000)	
	
	def __init__(self,searchTerms,imgsNeeded):
		if searchTerms == []:
			print 'No search terms given!'
			sys.exit()
		if not len(searchTerms) == len(imgsNeeded):
			print 'Number of images needed was not correctly specified! Ex:( ["rabbit","bieber","kentucky"][1000,100,400] )'
			print 'Defaulting to 1000 for all search terms!'
			imgsNeeded = []
			for i in range(len(searchTerms)):
				imgsNeeded.append(1000)
		else:
			self.consumerKey        = '' #Put in your consumerKey
			self.consumerSecret     = '' #Put in your consumerSecret
			self.oauthToken         = '' #Put in your auth Token
			self.oauthSecret        = '' #Put in your auth Secret
			self.client             = pytumblr.TumblrRestClient(self.consumerKey, self.consumerSecret, self.oauthToken, self.oauthSecret)
			self.timestampList      = []
			self.imageList          = []
			self.searchTerms        = searchTerms
			self.imgsDownloadedMap  = {} #This is a map that keeps track of the number of images downloaded for each search term.
			self.imgsNeededMap      = {}
			self.unixTimestamp      = ''
			self.imgsDownloaded     = 0
			self.imgsNeeded         = imgsNeeded

			self.buildMaps()			
			self.cleanupImageFolder()
			self.delegateSearches(self.searchTerms)
		
	def buildMaps(self):
		i = 0
		for searchTerm in self.searchTerms:
			self.imgsNeededMap[searchTerm] = self.imgsNeeded[i]
			self.imgsDownloadedMap[searchTerm] = 0
			i = i + 1
			
	
	def delegateSearches(self,searchTerms):
		if searchTerms == []:
			print 'No search terms given!'
			sys.exit()
		else:
			for searchTerm in searchTerms:
				self.imgsDownloadedMap[searchTerm] = 0
				self.scrapeImages(searchTerm)
	def downloadImage(self,link):
		os.system('wget -P ./images %s'%link)	
	def scrapeImages(self,searchTerm):
		#As of 5/12/2014, the tumblr API only returns 20 results for each call.
		#(We have a workaround for that!) :)
		#We take the timestamp of the 20th result and tell tumblr to only return results older than that in the next call.
		#We do this until imgsDownloaded and imgsNeeded are equivalent.

		responses = self.client.tagged(searchTerm)
		jsonResponses = json.dumps(responses)
		lastTimestamp = responses[(len(responses)-1)]['timestamp']

		while self.imgsDownloadedMap[searchTerm] < self.imgsNeededMap[searchTerm]:
			for resp in responses:
				if 'photos' in resp:
					photos = resp['photos']
					for photo in photos:
						if self.imgsDownloadedMap[searchTerm] < self.imgsNeededMap[searchTerm]:
							if 'alt_sizes' in photo:
								alt_sizes = photo['alt_sizes']
								#The only guaranteed common image size on tumblr is 75x75 px (the smallest they offer).
								smallest_size_img = alt_sizes[len(alt_sizes)-1]
								link = smallest_size_img['url']
								if '.jpg' in link:
									self.downloadImage(link)
									self.imgsDownloadedMap[searchTerm] = self.imgsDownloadedMap[searchTerm] + 1
									self.imageList.append(link)
						else:
							break	

			responses = self.client.tagged(searchTerm, before=lastTimestamp)
			jsonResponses = json.dumps(responses)
			lastTimestamp = responses[(len(responses)-1)]['timestamp']

