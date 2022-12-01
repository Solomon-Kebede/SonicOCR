#!/usr/bin/python3

import base64
from urllib.parse import quote as urlencoder
from utils.randomizer import Randomizer

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

def f_sid():
	'''Generates a 19 digit signed f.sid'''
	r = Randomizer()
	return int("".join([r.keygen('+-',1), r.keygen(r.digits[1:9], 1), r.keygen(r.digits, 18)]))

def reqid():
	'''Generate a 6 digit unsigned _reqid'''
	r = Randomizer()
	return int(r.keygen(r.digits[1:8], 6))

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

def data4batchexecute(gp_url):
	'''
	Prepares data to be sent to the
	'batchexecute' endpoint
	'''
	r = Randomizer()
	VALUE_X = int("".join([r.keygen(r.digits[1:9], 1), r.keygen(r.digits, 14)]))
	key = uuid4like()
	VALUE_Y = base64.b64encode(key.encode('utf-8')).decode('utf-8')
	data = f"f.req=%5B%5B%5B%22B7fdke%22%2C%22%5B%5B%5C%22{VALUE_X}%5C%22%2C1%2C1%5D%2C%5Bnull%2Cnull%2Cnull%2Cnull%2C%5Bnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5C%22{urlencoder(gp_url, safe='')}%5C%22%5D%5D%2C%5Bnull%2Cnull%2Cnull%2Cnull%2C3%2C%5B%5C%22en%5C%22%2Cnull%2C%5C%22US%5C%22%2C%5C%22Africa%2FCasablanca%5C%22%5D%2Cnull%2Cnull%2C%5Bnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Ctrue%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Ctrue%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Ctrue%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Ctrue%2Cnull%2Cnull%2Cnull%2Ctrue%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Ctrue%2Ctrue%5D%2C%5B%5Bnull%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Cnull%2Cnull%2Cnull%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Cnull%2Cnull%2Cnull%2Ctrue%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Ctrue%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Ctrue%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Ctrue%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Ctrue%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Ctrue%2Cnull%2Cnull%2Cnull%2Ctrue%2Cnull%2Cnull%2Cnull%2Ctrue%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Ctrue%2Ctrue%2Ctrue%2Cnull%2Ctrue%2Ctrue%2Cnull%2Cnull%2Cnull%2Cnull%2Cfalse%2Cfalse%2Cnull%2Cnull%2Cnull%2C%5B4%2C5%2C6%2C7%2C2%5D%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cfalse%2Cnull%2Cfalse%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Ctrue%2Cnull%2Cfalse%2Cnull%2Cfalse%5D%5D%2C%5B%5B%5B7%5D%5D%5D%2Cnull%2Cnull%2Cnull%2C26%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5Bnull%2C5%5D%2Cnull%2C%5B5%5D%5D%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%5D%2Cnull%2Cnull%2Cnull%2C%5Bnull%2Ctrue%5D%2Cnull%2Cnull%2C%5B%5D%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%5Bnull%2C%5Bnull%5D%5D%5D%2Cnull%2C%5C%22{VALUE_Y}%5C%22%5D%22%2Cnull%2C%22generic%22%5D%5D%5D&"
	return data

def url4batchexecute():
	'''
	Returns the prepared url to the
	'batchexecute' endpoint where the
	results are retreived
	'''
	return f"https://lens.google.com/_/LensWebStandaloneUi/data/batchexecute?rpcids=B7fdke&source-path=%2Fsearch&f.sid={f_sid()}=boq_lens-web-standalone-ui_20220518.02_p0&hl=en-US&soc-app=1&soc-platform=1&soc-device=1&_reqid={reqid()}&rt=c"
