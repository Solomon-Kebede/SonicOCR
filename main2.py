import json
from sys import argv
import requests
import base64
import logging
import pprint

from engine.google import headers as header
from engine.google import uuid4like
from engine.google import data4batchexecute
from engine.google import url4batchexecute

import asyncio
import aiohttp
from os import path, system
from sys import argv

import hashlib

import time

logging.basicConfig(
    level=logging.ERROR,
    format=' %(asctime)s -%(levelname)s - %(message)s'
    )
'''# To take input from the terminal.
image_paths = []
user_inputs = [str(x) for x in input("Please enter image path(s): ").split(", ")]

for user_input in user_inputs:
    if path.isfile(user_input) and path.exists(user_input):
        if user_inputs.index(user_input) == 0:
            print("Image(s) being processed...")
        image_path = image_paths.append(user_input)
    else:
        print("Path not found, please enter another path")'''    

image_paths = [
"./test_images/everything-has-beauty-confucius-quote.jpg",
"./test_images/maya-angelou-famous-quote.webp",
"./test_images/download2.jpg",
"./test_images/download.jpg",
"./test_images/d760e79a7997acefb79c917b7771d75f.jpg",
"./test_images/03ab9fbff391a8a3de0569050745a555.jpg",
"./test_images/download.png",
"./test_images/2101793258-amharic-poem.jpg",
"./images_test_2/download.jpeg",
'./images_test_2/my-family-i-love-them-cinderheart-lionblaze-you-only-stepped-on-a-thorn-lionblaze-help-im-dyinblaze.jpeg',
'./images_test_2/Variations-in-handwriting-style-random-sample-of-handwriting-taken-from-IRONOFF-database.png',
'./images_test_2/random-text-to-wrap-around-picture.jpg',
'./images_test_2/preview-image-onlinefiletools.png',
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
                logging.error(f'Status Code_1: {response.status}')
                return None
        elif request_type == "text-only":
            if response.ok:
                return await response.text()
            else:
                logging.error(f'Status Code_2: {response.status}')
                return None

def parse_results(response):
    c = 0
    all_lists = []
    result_1 = response.split('\n')[3]
    result_2 = json.loads(result_1)[0][2]
    for i in result_2.split("["):
        for j in i.split("]"):
            if j != '' and j not in all_lists:
                potential_list = (f"{j}")
                all_lists.append(potential_list)
                c += 1
    for x in all_lists:
        if x[0] == ',' and 'Acna4G' in x:
            ocr_result_index = all_lists.index(x) - 1
            ocr_result = all_lists[ocr_result_index]
            logging.info(f"[{ocr_result_index}] => {ocr_result}")
    ocr_results = json.loads(f"[{ocr_result}]")
    return ocr_results
    

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
            
        results_endpoint2 =    await asyncio.gather(*endpoint_2_awaitables)
        # print(results_endpoint2)
        for r in results_endpoint2:
            #print(f"raw-> {r}")
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
        results_endpoint3 =    await asyncio.gather(*endpoint_3_awaitables)
        # print(results_endpoint3)
        for r in results_endpoint3:
            # Parsing for the result
            ocr_results = parse_results(r)
            logging.info(f"[4.0] {ocr_results}\n")

            print("Final Result:")
            for ocr_item in ocr_results:
                print(f"{ocr_item}")
            print()

if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main())
    print(f'{time.time() - start_time}s')
