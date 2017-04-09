# -*- coding: utf-8 -*-
"""
Created on Sat Apr 08 23:56:59 2017
@author: YH
"""

import spotipy
import webbrowser
import sys
import socket
import subprocess
import time
import threading

spotify = spotipy.Spotify()


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('', 8001))
serversocket.listen(5)
already_playing_flag = 0

class wait_till_song_fin(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		global already_playing_flag
		time.sleep(30)
		already_playing_flag = 0
		print("ready to play again")

while True:
	# accept connections from outside
	print("waiting for incoming connection...")
	(clientsocket, address) = serversocket.accept()
	print("connection received")
	# now do something with the clientsocket
	# in this case, we'll pretend this is a threaded server
	ct = clientsocket
	data = ct.recv(128)
	ct.close()
	while already_playing_flag == 0:
		already_playing_flag = 1
		if int(data.decode("utf-8")) == 1:
			# Megadeath
			track_uri = 'spotify:artist:1Yox196W7bzVNZI7RBaPnf'
			track_result = spotify.artist_top_tracks(track_uri)['tracks'][0]
		elif int(data.decode("utf-8")) == 2:
			# Yo-yo Ma
			track_uri = "spotify:track:17i5jLpzndlQhbS4SrTd0B"
			# track_uri = "spotify:track:2w2lfwoTELQyN940qM7Nfd"
			track_result = spotify.track(track_uri)
		else:
			track_uri = "spotify:track:3FCto7hnn1shUyZL42YgfO"
			track_result = spotify.track(track_uri)
			# Stop

		print(track_result)
		print ('track: ' + track_result['name'])
		webbrowser.open(track_result['preview_url'])
		waiter = wait_till_song_fin()
		waiter.start()
	
	
