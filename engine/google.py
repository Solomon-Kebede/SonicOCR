#!/usr/bin/python3

from engine.randomizer import Randomizer

def headers(header_type='base'):
	"""Returns different headers for various endpoints"""
	base = {
		"accept": "*/*",
		"accept-language": "en-US,en;q=0.9",
		"cache-control": "no-cache",
		"content-type": "application/x-www-form-urlencoded;charset=UTF-8",
		"user-agent": "Mozilla/5.0 (X11; Linux x86_64) \
		AppleWebKit/537.36 (KHTML, like Gecko) \
		Chrome/99.0.4844.51 Safari/537.36"
	}
	if header_type == 'base':
		'''No special headers required'''
		return base
	elif header_type == 'upload_url':
		'''Headers to retrieve upload url for image'''
		base["x-client-side-image-upload"] = "true"
		base["x-goog-upload-command"] = "start"
		base["x-goog-upload-protocol"] = "resumable"
		return base
	elif header_type == 'upload_image':
		'''Headers to initiate image upload'''
		base["x-client-side-image-upload"] = "true"
		base["x-goog-upload-command"] = "upload, finalize"
		base["x-goog-upload-offset"] = "0"
		return base

def uuid4like():
	'''Generates a uuid4 like string'''
	r = Randomizer()
	part1 = r.keygen(r.alphanum, 8)
	part2 = r.keygen(r.alphanum, 4)
	part3 = "".join(
		['4', r.keygen(r.alphanum, 2), r.keygen(r.digits, 1)])

	part4 = r.keygen(r.alphanum, 4)
	part5 = "".join([
		r.keygen(r.alphanum, 2),
		r.keygen(r.digits, 1),
		r.keygen(r.alphanum, 9)
		])
	key = "-".join([part1, part2, part3, part4, part5])
	return key
