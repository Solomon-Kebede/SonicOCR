import json
import requests
import base64
import random
import logging
import pprint

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

image_paths = [
"./test_images/everything-has-beauty-confucius-quote.jpg",
"./test_images/maya-angelou-famous-quote.webp",
"./test_images/download2.jpg",
"./test_images/download.jpg",
"./test_images/d760e79a7997acefb79c917b7771d75f.jpg",
"./test_images/03ab9fbff391a8a3de0569050745a555.jpg",
"./test_images/download.png",
"./test_images/2101793258-amharic-poem.jpg"
]

base_url = "https://lens.google.com"
endpoint_1 = f"{base_url}/_/upload/"

def read_image(file_path):
	with open(file_path, 'rb') as f:
		return f.read()

def get_path(file_path_list):
	index = 0
	while index < len(file_path_list):
		yield file_path_list[index]
		index += 1


async def post(session, url, _headers, _data=None, request_type = None):
	async with session.post(url, headers=_headers, data=_data) as response:
		if request_type == "headers-only":
			# print(f'Status OK: {response.ok}')
			# return response.status, response.headers
			if response.ok:
				return response.headers
			else:
				logging.error(f'Status Code: {response.status}')
				return None
		elif request_type == "text-only":
			if response.ok:
				return await response.text()
			else:
				logging.error(f'Status Code: {response.status}')
				return None

async def main():
	async with aiohttp.ClientSession() as session:
		results_endpoint1 = (
			await asyncio.gather(
			*[
			post(session, endpoint_1,
				header('upload_url'),
				request_type="headers-only") for image_path in image_paths]
		)
			)
		filepath = get_path(image_paths)
		endpoint_2_awaitables = []
		endpoint_3_awaitables = []
		for r in results_endpoint1:
			upload_location = r.get('X-Goog-Upload-URL')
			logging.info(f"[1.0] {upload_location}\n")
			# Read Image
			image_data = read_image(next(filepath))
			# Upload Image
			# res_2 = requests.post(upload_location, headers = header('upload_image'), data = image_data)
			'''[TODO]
			All the images have to be loaded into
			memory [Improve design]
			'''
			endpoint_2_awaitables.append(
			post(session, upload_location,
				header('upload_image'),
				_data=image_data,
				request_type="text-only")
			)
			
		results_endpoint2 =	await asyncio.gather(*endpoint_2_awaitables)
		# print(results_endpoint2)
		for r in results_endpoint2:
			res_2_json = json.loads(r.split('\n')[1])
			# print('=' * 30)
			logging.info(f"[2.0] {res_2_json}\n")
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
			endpoint_3_awaitables.append(
				post(session, results_url,
					header(),
					_data=data,
					request_type="text-only")
				)
		results_endpoint3 =	await asyncio.gather(*endpoint_3_awaitables)
		# print(results_endpoint3)
		for r in results_endpoint3:
			# Parsing for the result
			result_1 = r.split('\n')[3]
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
	asyncio.run(main())