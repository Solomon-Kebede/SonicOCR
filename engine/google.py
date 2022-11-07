#!/usr/bin/python3

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
