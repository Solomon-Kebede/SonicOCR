import json
import requests
import base64
import random
import urllib.parse as uq
import pprint

base_url = "https://lens.google.com"

headers_1 = {
	"accept": "*/*",
	"accept-language": "en-US,en;q=0.9",
	"cache-control": "no-cache",
	"content-type": "application/x-www-form-urlencoded;charset=UTF-8",
	"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
	"x-client-side-image-upload": "true",
	"x-goog-upload-command": "start",
	"x-goog-upload-protocol": "resumable"
}
# headers_1["x-goog-upload-header-content-length"] = "73355"

# Get Upload Location
upload_url = f"{base_url}/_/upload/"

res_1 = requests.post(upload_url, headers = headers_1)
if res_1.status_code == requests.codes.ok:
	upload_location = res_1.headers['X-Goog-Upload-URL']
	print(upload_location)
else:
	print(res_1.status_code)

# Upload Image
# file_path = "../test_images/bible-quote-4-4166309870.jpg"
# file_path = "../test_images/bible-quotes35-1599062854.jpg"
#file_path = "../test_images/test501.jpg"
# file_path = "../test_images/0735211299.01.S003.JUMBOXXX.jpg"
# file_path = "../test_images/download.jpg"
# file_path = "../test_images/mrsd.jpg"
# ======== #
'''
##  - implies ocr engine worked almost to perfection (nothing is really perfect)
#*  - implies ocr engine problem (google problem)
#** - implies parser problem (fixed as far as the test goes)
'''
##file_path = "../test_images/everything-has-beauty-confucius-quote.jpg"
##file_path = "../test_images/maya-angelou-famous-quote.webp"

#*file_path = "../test_images/download2.jpg"
##file_path = "../test_images/download.jpg"
#*file_path = "../test_images/d760e79a7997acefb79c917b7771d75f.jpg"
#*file_path = "../test_images/03ab9fbff391a8a3de0569050745a555.jpg"
#*file_path = "../test_images/download.png"
##file_path = "../test_images/2101793258-amharic-poem.jpg"

'''
#file_path = "../test_images/test.txt"
file_path = ""
file_path = ""
'''
file_path = "../test_images/download.png"
# ======== #
with open(file_path, 'rb') as f:
	image_data = f.read()

headers_2 = {
	"accept": "*/*",
	"accept-language": "en-US,en;q=0.9",
	"cache-control": "no-cache",
	"content-type": "application/x-www-form-urlencoded;charset=UTF-8",
	"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
	"x-client-side-image-upload": "true",
	"x-goog-upload-command": "upload, finalize",
	"x-goog-upload-offset": "0"
}
print("\n" * 2)
res_2 = requests.post(upload_location, headers = headers_2, data = image_data)
if res_2.status_code == requests.codes.ok:
	# for k, v in res_2.headers.items():
	# 	print(f"{k}: {v}")
	# print("\n" * 2)
	res_2_json = json.loads(res_2.text.split('\n')[1])
	print(res_2_json)
else:
	print(res_2.status_code)


# Get Google Lens Location
gl_url = f'{base_url}{res_2_json["url"]}'


# Get Google Photo Link
gp_url_encoded = res_2_json["payload"]
gp_url_decoded = base64.b64decode(gp_url_encoded)
gp_url = f"https://{gp_url_decoded.split(b'https://')[1].split(b'(')[0].decode('utf-8')}"

print("\n" * 2)
print(gp_url)


# Get OCR data

s = 'abcdefghijklmnopqrstuvwxyz'			# STRING
d = '0123456789'							# DIGIT
an = 'abcdefghijklmnopqrstuvwxyz0123456789'	# ALPHANUMERIC

def kg(chars, length):
	'''keygen(length)'''
	key = ''
	for key_len in range(length):
		index = random.randint(0,len(chars)-1)
		key = (key + str(chars[index])).upper()
	return key

def keygen():
	p1 = kg(an, 8)
	p2 = kg(an, 4)
	p3 = "".join(['4', kg(an, 2), kg(d, 1)])
	p4 = kg(an, 4)
	p5 = "".join([kg(an, 2), kg(d,1), kg(an,9)])
	key = "-".join([p1, p2, p3, p4, p5])
	return key
	# print(f"{key}: {base64.b64encode(key.encode('utf-8')).decode('utf-8')}")

headers = {
	"accept": "*/*",
	"accept-language": "en-US,en;q=0.9",
	"cache-control": "no-cache",
	"content-type": "application/x-www-form-urlencoded;charset=UTF-8",
	"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
}

# /// 6 Values up for for extraction /// #

f_sid = int("".join([kg('+-',1), kg(d[1:9], 1), kg(d, 18)]))
reqid = int(kg(d[1:8], 6))
f_sid_url = f"https://lens.google.com/_/LensWebStandaloneUi/data/batchexecute?rpcids=B7fdke&source-path=%2Fsearch&f.sid={f_sid}=boq_lens-web-standalone-ui_20220518.02_p0&hl=en-US&soc-app=1&soc-platform=1&soc-device=1&_reqid="

"https%3A%2F%2Flh3.googleusercontent.com%2FBPr3LwxOAg-WE7-bbXkeZHE6zyiQHeb0BtqZ9l_W38TZ89GHd0yA3eN6FdAj5917t-KmvrLsWRbWvfgli55_44CZLSQjyMT5XsMwuBMK"

def ocr_results(f_sid_url, _reqid, gp_url):
	### OCR STUFF ###
	url = f"{f_sid_url}{_reqid}&rt=c"
	VALUE_X = int("".join([kg(d[1:9], 1), kg(d, 14)]))
	key = keygen()
	VALUE_Y = base64.b64encode(key.encode('utf-8')).decode('utf-8')
	data = f"f.req=%5B%5B%5B%22B7fdke%22%2C%22%5B%5B%5C%22{VALUE_X}%5C%22%2C1%2C1%5D%2C%5Bnull%2Cnull%2Cnull%2Cnull%2C%5Bnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5C%22{uq.quote(gp_url, safe='')}%5C%22%5D%5D%2C%5Bnull%2Cnull%2Cnull%2Cnull%2C3%2C%5B%5C%22en%5C%22%2Cnull%2C%5C%22US%5C%22%2C%5C%22Africa%2FCasablanca%5C%22%5D%2Cnull%2Cnull%2C%5Bnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Ctrue%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Ctrue%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Ctrue%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Ctrue%2Cnull%2Cnull%2Cnull%2Ctrue%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Ctrue%2Ctrue%5D%2C%5B%5Bnull%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Cnull%2Cnull%2Cnull%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Cnull%2Cnull%2Cnull%2Ctrue%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Ctrue%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Ctrue%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Ctrue%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Ctrue%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Ctrue%2Cnull%2Cnull%2Cnull%2Ctrue%2Cnull%2Cnull%2Cnull%2Ctrue%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Ctrue%2Ctrue%2Ctrue%2Cnull%2Ctrue%2Ctrue%2Cnull%2Cnull%2Cnull%2Cnull%2Cfalse%2Cfalse%2Cnull%2Cnull%2Cnull%2C%5B4%2C5%2C6%2C7%2C2%5D%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cfalse%2Cnull%2Cfalse%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Ctrue%2Cnull%2Cfalse%2Cnull%2Cfalse%5D%5D%2C%5B%5B%5B7%5D%5D%5D%2Cnull%2Cnull%2Cnull%2C26%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5Bnull%2C5%5D%2Cnull%2C%5B5%5D%5D%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%5D%2Cnull%2Cnull%2Cnull%2C%5Bnull%2Ctrue%5D%2Cnull%2Cnull%2C%5B%5D%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%5Bnull%2C%5Bnull%5D%5D%5D%2Cnull%2C%5C%22{VALUE_Y}%5C%22%5D%22%2Cnull%2C%22generic%22%5D%5D%5D&"
	return (url, data)

def related_images(f_sid_url, _reqid, gp_url):
	### RELATED PICTURES ###
	# Unparsed: Just as a baseline
	_reqid += 100000
	url = f"{f_sid_url}{_reqid}&rt=c"
	VALUE_M = int("".join([kg(d[1:9], 1), kg(d, 14)]))
	key = keygen()
	VALUE_N = base64.b64encode(key.encode('utf-8')).decode('utf-8')
	data = f"f.req=%5B%5B%5B%22B7fdke%22%2C%22%5B%5B%5C%22{VALUE_M}%5C%22%2C1%2C1%5D%2C%5Bnull%2Cnull%2Cnull%2Cnull%2C%5Bnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5C%22{uq.quote(gp_url, safe='')}%5C%22%5D%5D%2C%5Bnull%2Cnull%2Cnull%2Cnull%2C3%2C%5B%5C%22en%5C%22%2Cnull%2C%5C%22US%5C%22%2C%5C%22Africa%2FCasablanca%5C%22%5D%2Cnull%2Cnull%2C%5Bnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Ctrue%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Ctrue%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Ctrue%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Ctrue%2Cnull%2Cnull%2Cnull%2Ctrue%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Ctrue%2Ctrue%5D%2C%5B%5Bnull%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Cnull%2Cnull%2Cnull%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Cnull%2Cnull%2Cnull%2Ctrue%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Ctrue%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Ctrue%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Ctrue%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Ctrue%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Ctrue%2Cnull%2Cnull%2Cnull%2Ctrue%2Cnull%2Cnull%2Cnull%2Ctrue%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Ctrue%2Ctrue%2Ctrue%2Cnull%2Ctrue%2Ctrue%2Cnull%2Cnull%2Cnull%2Cnull%2Cfalse%2Cfalse%2Cnull%2Cnull%2Cnull%2C%5B4%2C5%2C6%2C7%2C2%5D%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cfalse%2Cnull%2Cfalse%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Ctrue%2Cnull%2Cfalse%2Cnull%2Cfalse%5D%5D%2C%5B%5B%5B7%5D%5D%5D%2Cnull%2Cnull%2Cnull%2C26%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5Bnull%2C5%5D%2Cnull%2C%5B5%5D%5D%2C%5Bnull%2C%5B%5B2%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B0.5%2C0.5%2C1%2C1%2Cnull%2C1%5D%5D%5D%2C%5B%5D%2C%5B%5D%5D%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%5D%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%5D%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%5Bnull%2C%5Bnull%5D%5D%5D%2Cnull%2C%5C%22{VALUE_N}%5C%22%5D%22%2Cnull%2C%22generic%22%5D%5D%5D&"
	pass
	#INCOMPLETE FOR USAGE

url, data = ocr_results(f_sid_url, reqid, gp_url)
res = requests.post(url, headers = headers, data = data)
#print(res.status_code)
#print()
result_1 = res.text.split('\n')[3]
result_2 = json.loads(result_1)[0][2]
#print(result_2)
#print()
result_3 = repr(result_2)
#print(result_3)
print()
# EXTRACTION PROBLEMS (Fixed below)

c = 0
actual_lists = []
all_lists = []
#print(result_2.count("["))
#print(result_2.count("]"))
for i in result_2.split("["):
	for j in i.split("]"):
		if j != '':
			#potential_list = (f"[{j}]")
			potential_list = (f"{j}")
			#print(f"{c} => {potential_list}")
			all_lists.append(potential_list)
			c+=1
			'''
			try:
				actual_list = json.loads(potential_list)
				#print(f"{c} => {actual_list}")
				actual_lists.append(actual_list)
				#c+=1
			except:
				pass
			'''

#print("\n" * 3, c)


#ocr_result = actual_lists[-21] #didn't work for 1/8 tests
ocr_result = all_lists[-45]

ocr_results = json.loads(f"[{ocr_result}]")
print(ocr_results)
print("========================\nFinal Result:")
for ocr_item in ocr_results:
	print(ocr_item)
print()

# Next TODO:
'''
Potential steganography to upload any file ftemporarily to google photos, to utilize fast bandwith of google
'''

# Another TODO:
"""
Another Idea would be doing batch processing
Toenhance the speed maybe replacement or addition of aiohttp for async i/o
"""
