


import asyncio
import aiohttp

import json

async def post(session, url, headers=None, data=None, request_type = None):
	# async with session.post(url, headers=headers, data=data) as response:
	async with session.get(url, headers=headers, data=data) as response:
		if request_type == "header-only":
			return response.status, response.headers
		elif request_type == "text-only":
			return await response.text()
		elif request_type == "text-and-header":
			response_data = await response.text()
			print(response_data)
			# return response.status, response.headers, response_data

async def main1():
	url = 'https://httpbin.org/uuid'
	# url = 'https://httpbin.org/anything'
	headers = {'a': 'b'}
	data = {'c': 'd'}
	request_type = 'text-and-header'
	async with aiohttp.ClientSession() as session:
		responses = await post(session, url,
			headers=headers,
			data=data,
			request_type = request_type
		)
		# print(responses[0])
		# print(responses[1])
		print(responses[2])
			

async def main():
	async with aiohttp.ClientSession() as session:
		url = 'https://httpbin.org/uuid'
		# url = 'https://httpbin.org/anything'
		headers = {'a': 'b'}
		data = {'c': 'd'}
		request_type = 'text-and-header'
		tasks = [
		post(
			session, url,
			headers=headers,
			data=data,
			request_type = request_type) for _ in range(100)
		]
		await asyncio.gather(*tasks)

if __name__ == '__main__':
	'''
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())
	loop.close()
	'''
	asyncio.run(main())