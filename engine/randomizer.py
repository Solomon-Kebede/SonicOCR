#!/usr/bin/python3

class Randomizer:
	def __init__(self):
		import random
		alpha = 'abcdefghijklmnopqrstuvwxyz'		# ALPHA
		digits = '0123456789'							# DIGIT
		alphanum = 'abcdefghijklmnopqrstuvwxyz0123456789'	# ALPHANUMERIC


	def keygen(self, chars, length):
		'''Generates a key with length `length`
		and with a string of passed characters
		`chars`'''
		key = ''
		for key_len in range(length):
			index = random.randint(0,len(chars)-1)
			key = (key + str(chars[index])).upper()
		return key


	def uuid4like(self):
		'''Generates a uuid4 like string'''
		part1 = self.keygen(alphanum, 8)
		part2 = self.keygen(alphanum, 4)
		part3 = "".join(
			['4', self.keygen(alphanum, 2), self.keygen(digits, 1)])

		part4 = self.keygen(alphanum, 4)
		part5 = "".join([
			self.keygen(alphanum, 2),
			self.keygen(digits, 1),
			self.keygen(alphanum, 9)
			])
		key = "-".join([p1, p2, p3, p4, p5])
		return key
