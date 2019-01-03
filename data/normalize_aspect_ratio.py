import os
import cv2
import numpy as np

IMAGES_FOLDER = 'Pola_ai'
OUTPUT_FOLDER = 'Pola_scaled'
TARGET_ASPECT_RATIO = 480 / 640 # = 0.75

if __name__ == "__main__":

    for dir in os.listdir(IMAGES_FOLDER):
        if dir.startswith('.'):
            continue
        output_dir = os.path.join(OUTPUT_FOLDER, dir)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for file in os.listdir(os.path.join(IMAGES_FOLDER, dir)):
            if not file.endswith('.jpg'):
                continue
            
            filename = os.path.join(IMAGES_FOLDER, dir, file)
            output_filename = os.path.join(OUTPUT_FOLDER, dir, file)

            if os.path.exists(output_filename):
                continue

            img = cv2.imread(filename)

            height, width = img.shape[:2]
            ratio = width / height

            if ratio == TARGET_ASPECT_RATIO:
                scaled = img
            elif ratio > TARGET_ASPECT_RATIO:
                new_width = int(height * TARGET_ASPECT_RATIO)
                scaled = img[0:height, width//2-new_width//2:width//2+new_width//2] 
            else:
                new_height = int(width / TARGET_ASPECT_RATIO)
                scaled = img[height//2-new_height//2:height//2+new_height//2, 0:width]
            
            height, width = scaled.shape[:2]
            ratio = width / height

            cv2.imwrite(output_filename, scaled)
            
