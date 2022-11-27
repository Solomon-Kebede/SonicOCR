import json
import requests
import base64
import random
import logging

from engine.google import headers as header
from engine.google import uuid4like
from engine.randomizer import Randomizer
from engine.google import data4batchexecute
from engine.google import url4batchexecute

import asyncio
import aiohttp

logging.basicConfig(
	level=logging.ERROR,
	format=' %(asctime)s -%(levelname)s - %(message)s'
)

base_url = "https://lens.google.com"
'''
async def post(session, url, headers, data, request_type = None):
	async with session.post(url, headers, data) as response:
		if request_type == "header-only":
			return response.status, response.headers
		elif request_type == "text-only":
			return await response.text()
		elif request_type == "text-and-header":
			response_data = await response.text()
			return response.status, response.headers, response_data

async def main():
    async with aiohttp.ClientSession() as session:
        await post(session, url, headers)
        await session.post(url, data=payload, headers=headers)
'''

image_paths = [
"../test_images/everything-has-beauty-confucius-quote.jpg",
"../test_images/maya-angelou-famous-quote.webp",
"../test_images/download2.jpg",
"../test_images/download.jpg",
"../test_images/d760e79a7997acefb79c917b7771d75f.jpg",
"../test_images/03ab9fbff391a8a3de0569050745a555.jpg",
"../test_images/download.png",
"../test_images/2101793258-amharic-poem.jpg"
]


'''
Endpoint-1: Used to retreive an endpoint from Google
Lens, where we have been authorized to upload our image
to.

POST: /_/upload/
'''
endpoint_1 = f"{base_url}/_/upload/"

# Get Upload Location
res_1 = requests.post(endpoint_1, headers = header('upload_url'))
if res_1.status_code == requests.codes.ok:
	upload_location = res_1.headers['X-Goog-Upload-URL']
	logging.info(f"[1.0] {upload_location}\n")
else:
	logging.error(f"[1.1] {res_1.status_code}\n")

# Read Image
file_path = "./test_images/download.png"
def read_image(file_path):
	with open(file_path, 'rb') as f:
		return f.read()

image_data = read_image(file_path)

# Upload Image
res_2 = requests.post(upload_location, headers = header('upload_image'), data = image_data)
if res_2.status_code == requests.codes.ok:
	res_2_json = json.loads(res_2.text.split('\n')[1])
	logging.info(f"[2.0] {res_2_json}\n")
else:
	logging.error(f"[2.1] {res_2.status_code}\n")


# Get Google Lens Location
gl_url = f'{base_url}{res_2_json["url"]}'

# Get Google Photo Link
gp_url_encoded = res_2_json["payload"]
gp_url_decoded = base64.b64decode(gp_url_encoded)
gp_url = f"https://{gp_url_decoded.split(b'https://')[1].split(b'(')[0].decode('utf-8')}"

logging.info(f"[3.0] {gp_url}\n")

# Get OCR data
results_url = url4batchexecute()
data = data4batchexecute(gp_url)
res = requests.post(results_url, headers = header(), data = data)

# Parsing for the result
result_1 = res.text.split('\n')[3]
result_2 = json.loads(result_1)[0][2]
result_3 = repr(result_2)

c = 0
all_lists = []

for i in result_2.split("["):
	for j in i.split("]"):
		if j != '':
			potential_list = (f"{j}")
			all_lists.append(potential_list)
			c+=1

ocr_result = all_lists[-45]

ocr_results = json.loads(f"[{ocr_result}]")
logging.info(f"[4.0] {ocr_results}\n")

print("Final Result:")
for ocr_item in ocr_results:
	print(f"{ocr_item}")
print()


if __name__ == '__main__':
	'''[old async run code]
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())
	loop.close()
	'''
	'''[new async run code]
	asyncio.run(main())
	'''
	pass