from aiohttp import web
import os
import logging

logging.basicConfig(level=logging.DEBUG)

app = web.Application()

# app = web.Application(
#     middlewares=[
#         cors_middleware(
#             allow_all=True,
#             origins='*',
#             # urls=[re.compile(r"^\/api")],
#             allow_credentials=True,
#             expose_headers="*",
#             allow_headers='*',
#             allow_methods=["POST", "PATCH", 'GET','OPTION'],
#         ),
#     ]
# )



async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)

async def store_images_handler(request):
    images_store_path = "./uploaded_images"
    reader = await request.multipart()
    # /!\ Don't forget to validate your inputs /!\
    field = await reader.next()
    filename = field.filename
    # You cannot rely on Content-Length if transfer is chunked.
    size = 0
    with open(os.path.join(images_store_path, filename), 'wb') as f:
        while True:
            chunk = await field.read_chunk()  # 8192 bytes by default.
            if not chunk:
                break
            size += len(chunk)
            f.write(chunk)

    return web.Response(text='{} sized of {} successfully stored'
                             ''.format(filename, size))

app.add_routes(
    [
    web.get('/path/{name}', handle),
    web.post('/imgs', store_images_handler)
    ]
)

if __name__ == '__main__':
    web.run_app(app)