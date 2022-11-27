import time

import asyncio

start = time.time()
async def test(s):
	print(time.time() - start)
	print(s)
	await asyncio.sleep(5)
	print(time.time() - start)
	print(f'{s}-done-sleeping')

async def test2():
	print('s1')
	await asyncio.sleep(5)
	print('s1-done-sleeping')
	print('s2')
	await asyncio.sleep(5)
	print('s2-done-sleeping')


async def main():
	await asyncio.gather(test("hello"), test("help"), test("hello1"), test("help1"))


# asyncio.run(test2())
asyncio.run(main())