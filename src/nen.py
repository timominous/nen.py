class Artist:
	name = ""
	albums = []

	def __init__(self, newname, newalbums):
		self.name = newname
		self.albums = newalbums

	def addalbum(self, newalbum):
		if not self.containsalbum(newalbum):
			self.albums.append(newalbum)

	def containsalbum(self, calbum):
		for album in self.albums:
			if album.title == calbum:
				return True
		return False

	def getalbum(self, calbum):
		for idx, album in enumerate(self.albums):
			if album.title == calbum:
				return album, idx
		return None, None

class Album:
	title = ""
	songs = []

	def __init__(self, newtitle, newsongs):
		self.title = newtitle
		self.songs = newsongs

	def addsong(self, newsong):
		if not self.songs.__contains__(newsong):
			self.songs.append(newsong)

def containsartist(cartists, cartist):
	for artist in cartists:
		if artist.name == cartist:
			return True
	return False

def getartist(cartists, cartist):
	for idx, artist in enumerate(cartists):
		if artist.name == cartist:
			return artist, idx
	return None, None

import os
import sys
from sys import stdout

try: 
	import eyeD3
except ImportError:
	print "Please install eyeD3. Get the latest copy here: http://eyed3.nicfit.net/"
	sys.exit(1)

artists = []
librarypath = ""
filepath = ""
count = 0

if len(sys.argv) < 3:
	print """Usage: python nen.py [PATH] [FILENAME]
	PATH           path to directory of mp3 files
	FILENAME       filename of destination file"""
	sys.exit(1)

librarypath = sys.argv[1]
filepath = sys.argv[2]

print "Scanning music library..."

for dirname, dirnames, filenames in os.walk(librarypath):
	for filename in filenames:
		if filename.lower().endswith('.mp3'):
			count += 1
			stdout.write("\rFiles scanned: %d" % count)
			stdout.flush()

			tag = eyeD3.Tag()
			path = dirname + '/' + filename
			tag.link(path)

			martist = tag.getArtist().encode("utf8")
			malbum = tag.getAlbum().encode("utf8")
			msong = tag.getTitle().encode("utf8") + ""

			if not containsartist(artists, martist):
				nartist = Artist(martist, [])
				nalbum = Album(malbum, [])
				nalbum.addsong(msong)
				nartist.addalbum(nalbum)
				artists.append(nartist)

			else:
				cartist, idx = getartist(artists, martist)

				if not cartist.containsalbum(malbum):
					nalbum = Album(malbum, [])
					nalbum.addsong(msong)
					cartist.addalbum(nalbum)
					artists[idx] = cartist

				else:
					calbum, aidx = cartist.getalbum(malbum)
					calbum.addsong(msong)
					artists[idx].albums[aidx] = calbum


stdout.write("\n")
stdout.flush()

print "Generating " + filepath + " file..."

try:
	f = open(filepath, "w")
	try:

		for artist in artists:
			f.write("%s\n" % artist.name)
			for album in artist.albums:
				f.write("  %s\n" % album.title)
				for song in album.songs:
					f.write("    %s\n" % song)

	finally:
		f.close()
except IOError:
	print "Error generating " + filepath + " file"