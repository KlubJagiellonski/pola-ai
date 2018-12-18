import argparse
import os
import shutil

import cv2


def blur_ratio(filename):
    # Positive blur ratio - the lower the more blurred the photo is
    image = cv2.imread(filename)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var()


def blur_distribution(photo_dir):
    # Returns blurs of all photos in a directory
    blur_ratios = []
    for subdir in os.listdir(photo_dir):
        print(subdir)
        for photo in os.listdir(os.path.join(photo_dir, subdir)):
            photo_path = os.path.join(photo_dir, subdir, photo)
            blur_ratios.append(blur_ratio(photo_path))
    return sorted(blur_ratios)


def remove_blured(src, dest, threshold=25, ratio=None):
    # Copies src into dest and removes blurred photos from dest based on threshold or ratio
    if ratio:
        blurs = blur_distribution(src)
        threshold = blurs[int(len(blurs) * ratio)]
        print('Blur threshold: {}'.format(threshold))
    shutil.copytree(src, dest)
    for subdir in os.listdir(dest):
        for photo in os.listdir(os.path.join(dest, subdir)):
            photo_path = os.path.join(dest, subdir, photo)
            blur = blur_ratio(photo_path)
            if blur < threshold:
                print('Remove photo {} with a blur score {}'.format(photo_path, blur))
                os.remove(photo_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_dir", type=str)
    parser.add_argument("dest_dir", type=str)
    args = parser.parse_args()
    remove_blured(args.source_dir, args.dest_dir, ratio=0.05)
