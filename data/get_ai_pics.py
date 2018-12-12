# -*- coding: utf-8 -*-
import requests
import argparse
import operator
import os
import asyncio
from aiohttp import ClientSession, ClientTimeout, client_exceptions
from urllib.parse import urlparse
from PIL import Image

MAX_NO_REQUESTS = 50
POLISH_LETTERS = [u'ąćęłńóśźżĄĆĘŃŁÓŚŹŻ',u'acelnoszzACENLOSZZ']

def normalize_name(name):
    name = name[:30].strip()
    for i in range(len(POLISH_LETTERS[0])):
        name = name.replace(POLISH_LETTERS[0][i], POLISH_LETTERS[1][i])
    name = ''.join([c if ord(c) < 128 and ord(c) > 47 else " " for c in name])
    return name


async def download_file(session, url, data_dir, filename, filename_jpg):
    print('Downloading: '+filename)
    retry = 3
    while (retry > 0):
        try:
            async with session.get(url) as response:
                with open(os.path.join(data_dir, filename), 'wb') as f:
                    content = await response.read()
                    f.write(content)

                if filename.endswith('.png'):
                    im = Image.open(os.path.join(data_dir, filename))
                    if im.mode != 'RGB':
                        im = im.convert('RGB')
                    im.save(os.path.join(data_dir, filename_jpg), quality=100)
                    os.remove(os.path.join(data_dir, filename))
                break
        except (client_exceptions.ServerDisconnectedError, asyncio.TimeoutError):
            retry -= 1
            pass

async def bound_download_file(sem, session, url, data_dir, filename, filename_jpg):
    # Getter function with semaphore.
    async with sem:
        return await download_file(session, url, data_dir, filename, filename_jpg)

async def download_files(aipics, existing_dirs, existing_files):
    tasks = []
    sem = asyncio.Semaphore(MAX_NO_REQUESTS)  # create instance of Semaphore; limit open requests to MAX_NO_REQUESTS
    async with ClientSession(timeout=ClientTimeout(total=60, connect=60, sock_connect=60, sock_read=60)) as session:
        for aipic in aipics:
            if aipic['code'] in top_codes:

                prod = u'{}#{}'.format(normalize_name(aipic['product_name']), aipic['company_id'])
                dir = os.path.join(data_dir, prod)
                if not os.path.exists(dir):
                    os.makedirs(dir)
                existing_dirs.discard(prod)

                file = aipic['url'].split('/')[-1]
                filename = os.path.join(prod, file)
                filename_jpg = os.path.splitext(filename)[0] + '.jpg'
                if not filename_jpg in existing_files:
                    task = asyncio.ensure_future(
                        bound_download_file(sem, session, aipic['url'], data_dir, filename, filename_jpg))
                    tasks.append(task)

                existing_files.discard(filename_jpg)
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    parser = argparse.ArgumentParser("get_ai_pics")
    parser.add_argument("shared_secret", type=str)
    parser.add_argument("data_dir", type=str)
    args = parser.parse_args()

    aipics = []
    page_no = 0

    while(True):
        r = requests.post('https://www.pola-app.pl/a/v3/get_ai_pics?page={}'.format(page_no),
                data = {'shared_secret': args.shared_secret})
        page_aipics = r.json()['aipics']
        if len(page_aipics) == 0:
            break
        aipics.extend(page_aipics)
        page_no += 1

    no_per_code = {}
    code_to_name = {}
    for aipic in aipics:
        no_per_code[aipic['code']] = no_per_code.get(aipic['code'],0) +1
        code_to_name[aipic['code']] = aipic['product_name']

    sorted_no_pics = sorted(no_per_code.items(), key=operator.itemgetter(1), reverse=True)

    top_codes = set()
    i = 0
    total_no_of_pics = 0
    while sorted_no_pics[i][1] >= 30:
        print(sorted_no_pics[i][1],':',code_to_name[sorted_no_pics[i][0]])
        top_codes.add(sorted_no_pics[i][0])
        total_no_of_pics += sorted_no_pics[i][1]
        i += 1

    print('total pics: ', total_no_of_pics)
    data_dir = args.data_dir

    existing_dirs = set()
    existing_files = set()
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    for dir in os.listdir(data_dir):
        if dir.startswith('.'):
            continue
        existing_dirs.add(dir)
        for file in os.listdir(os.path.join(data_dir, dir)):
            if file.endswith('.jpg') or file.endswith('.png'):
                s = os.path.join(dir, file)
                existing_files.add(s)

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(download_files(aipics, existing_dirs, existing_files))
    loop.run_until_complete(future)

    for filename in existing_files:
        print('Deleting: '+os.path.join(data_dir, filename))
        os.remove(os.path.join(data_dir, filename))

    for dir in existing_dirs:
        print('Deleting: '+os.path.join(data_dir, dir))
        ds_store = os.path.join(data_dir, dir, '.DS_Store')
        if os.path.exists(ds_store):
            os.remove(ds_store)
        os.rmdir(os.path.join(data_dir, dir))
