import re

if __name__ == "__main__":
    aipics = dict()
    with open('misclassified_images.txt') as f:
        for line in f.readlines():
            m = re.search(r'.*#(\d*)\/(\d*)_(\d*)[\w\-]*.jpg\s*(.*)',line)
            company_id = m.group(1)
            aipic_id = m.group(2)
            idx = m.group(3)
            label = m.group(4)

            aipic = aipics.get(aipic_id, {'indexes':set(), 'labels':set()})
            aipic['indexes'].add(idx)
            aipic['labels'].add(label)
            aipics[aipic_id] = aipic
    
    for aipic_id, aipic in aipics.items():
        print(','.join(aipic['indexes']))
        print(','.join(aipic['labels']))
        print('https://www.pola-app.pl/cms/ai_pics/{}'.format(aipic_id))
        print()
    
    print(len(aipics))
