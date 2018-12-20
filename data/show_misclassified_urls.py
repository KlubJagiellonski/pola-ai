import os
import re

photo_dir = 'Pola_ai'

if __name__ == "__main__":
    company_id2count = {}
    for subdir in os.listdir(photo_dir):
        if subdir.startswith('.'):
            continue
        m = re.search(r'.*#(\d*)', subdir)
        company_id = m[1]
        company_id2count[company_id] = len([name for name in os.listdir(os.path.join(photo_dir, subdir)) if name.endswith('.jpg')])

    aipics = dict()
    with open('misclassified_images.txt') as f:
        for line in f.readlines():
            line = line.strip()
            m = re.search(r'.*#(\d*)\/(\d*)_(\d*)[\w\-]*.jpg\s*(.*) (\d*)',line)
            company_id = m.group(1)
            aipic_id = m.group(2)
            idx = m.group(3)
            label = m.group(4)
            wrong_company_id = m.group(5)

            if company_id == wrong_company_id:
                continue

            aipic = aipics.get(aipic_id, {'indexes':set(), 'labels':set()})
            aipic['indexes'].add(idx)
            aipic['labels'].add(label)
            aipic['count']=company_id2count[wrong_company_id]
            aipics[aipic_id] = aipic
    
    with open("misclassified_images.html", "w") as f:
        for aipic_id, aipic in aipics.items():
            f.write(
                '<br>'\
                '<div><strong>{}</strong> {} ({})</div>'\
                '<iframe width="100%" height="500" src="https://www.pola-app.pl/cms/ai_pics/{}"></iframe>'.format(
                    ','.join(aipic['labels']), ','.join(aipic['indexes']), aipic['count'], aipic_id
                )
            )
    
    print(len(aipics))
