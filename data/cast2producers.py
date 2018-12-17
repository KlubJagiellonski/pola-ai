import argparse
import os
import shutil

parser = argparse.ArgumentParser("get_ai_pics")
parser.add_argument("products_dir", type=str)
parser.add_argument("producers_dir", type=str)
args = parser.parse_args()

DIR = args.products_dir
NEW_DIR = args.producers_dir


def name2producer_code(name):
    return name.split('#')[-1]


# Found here: https://stackoverflow.com/questions/1868714/how-do-i-copy-an-entire-directory-of-files-into-an-existing-directory-using-pyth/31039095
def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


if __name__ == "__main__":
    os.makedirs(NEW_DIR)
    for product in os.listdir(DIR):
        path = os.path.join(DIR, product)
        code = name2producer_code(product)
        new_path = os.path.join(NEW_DIR, code)
        os.makedirs(new_path, exist_ok=True)
        copytree(path, new_path)