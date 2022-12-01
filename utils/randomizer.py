#!/usr/bin/python3

import random

class Randomizer:
	def __init__(self):
		self.alpha = 'abcdefghijklmnopqrstuvwxyz'		# ALPHA
		self.digits = '0123456789'							# DIGIT
		self.alphanum = 'abcdefghijklmnopqrstuvwxyz0123456789'	# ALPHANUMERIC


	def keygen(self, chars, length):
		'''Generates a key with length `length`
		and with a string of passed characters
		`chars`'''
		key = ''
		for key_len in range(length):
			index = random.randint(0,len(chars)-1)
			key = (key + str(chars[index])).upper()
		return key
