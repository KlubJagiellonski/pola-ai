# -*- coding: utf-8 -*-
import requests
import argparse
import operator
import os
from urlparse import urlparse
from PIL import Image

POLISH_LETTERS = [u'ąćęłóźżĄĆĘŁÓŹŻ',u'acelozzACELOZZ']

def normalize_name(name):
    name = name[:30].strip()
    for i in range(len(POLISH_LETTERS[0])):
        name = name.replace(POLISH_LETTERS[0][i], POLISH_LETTERS[1][i])
    name = ''.join([c if ord(c) < 128 and ord(c) > 47 else " " for c in name])
    return name

if __name__ == "__main__":
    parser = argparse.ArgumentParser("get_ai_pics")
    parser.add_argument("shared_secret", type=str)
    parser.add_argument("data_dir", type=str)
    args = parser.parse_args()

    r = requests.post('https://www.pola-app.pl/a/v3/get_ai_pics',
            data = {'shared_secret': args.shared_secret})

    aipics = r.json()['aipics']

    no_per_code = {}
    code_to_name = {}
    for aipic in aipics:
        no_per_code[aipic['code']] = no_per_code.get(aipic['code'],0) +1
        code_to_name[aipic['code']] = aipic['product_name']

    sorted_no_pics = sorted(no_per_code.items(), key=operator.itemgetter(1), reverse=True)

    top_codes = set()
    i = 0
    while sorted_no_pics[i][1] >= 20:
        print sorted_no_pics[i][1],':',code_to_name[sorted_no_pics[i][0]]
        top_codes.add(sorted_no_pics[i][0])
        i += 1

    data_dir = args.data_dir

    existing_dirs = set()
    existing_files = set()
    for dir in os.listdir(data_dir):
        if dir.startswith('.'):
            continue
        existing_dirs.add(dir)
        for file in os.listdir(os.path.join(data_dir, dir)):
            if file.endswith('.jpg') or file.endswith('.png'):
                s = os.path.join(dir, file)
                existing_files.add(s)

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
                print 'Downloading: '+filename
                r = requests.get(aipic['url'], stream=True)
                if r.status_code == 200:
                    with open(os.path.join(data_dir, filename), 'wb') as f:
                        for chunk in r:
                            f.write(chunk)

                    if filename.endswith('.png'):
                        im = Image.open(os.path.join(data_dir, filename))
                        if im.mode != 'RGB':
                            im = im.convert('RGB')
                        im.save(os.path.join(data_dir, filename_jpg), quality=100)
                        os.remove(os.path.join(data_dir, filename))

            existing_files.discard(filename_jpg)

    for filename in existing_files:
        print 'Deleting: '+os.path.join(data_dir, filename)
        os.remove(os.path.join(data_dir, filename))

    for dir in existing_dirs:
        print 'Deleting: '+os.path.join(data_dir, dir)
        ds_store = os.path.join(data_dir, dir, '.DS_Store')
        if os.path.exists(ds_store):
            os.remove(ds_store)
        os.rmdir(os.path.join(data_dir, dir))
