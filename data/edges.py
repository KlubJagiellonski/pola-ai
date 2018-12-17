import os
import cv2
import numpy as np

IMAGES_FOLDER = 'Pola_ai'
OUTPUT_FOLDER = 'Pola_edges'
OUTPUT_SIZE = 224
SKIP_EDGSS_RATIO = 0.10

if __name__ == "__main__":

    images = []
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
            edges = cv2.Canny(img,100,200)

            height, width = img.shape[:2]
            total_edges = 0
            for x in range(width):
                for y in range(height):
                    total_edges += edges[y,x]

            left, top, right, bottom = (0, 0, width-1, height-1)
            skipped_edges = 0
            while right-left > 100 and bottom - top > 100  and \
                  (skipped_edges < SKIP_EDGSS_RATIO * total_edges or (right-left) != (bottom-top)):
                if right - left > bottom - top:
                    left_edge = sum(edges[y, left] for y in range(top, bottom))
                    right_edge= sum(edges[y, right] for y in range(top, bottom))
                    if left_edge < right_edge:
                        left += 1
                        skipped_edges += left_edge
                    else:
                        right -= 1
                        skipped_edges += right_edge
                else:
                    top_edge = sum(edges[top, x] for x in range(left, right))
                    bottom_edge = sum(edges[bottom, x] for x in range(left, right))
                    if top_edge < bottom_edge:
                        top += 1
                        skipped_edges += top_edge
                    else:
                        bottom -= 1
                        skipped_edges += bottom_edge
                
#            img = cv2.rectangle(img, (left, top), (right, bottom), (255,255,255), 2)
#            bgr_edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
#            both = np.hstack((img, bgr_edges))

            cropped = img[top:bottom, left:right]
            resized = cv2.resize(cropped, (OUTPUT_SIZE, OUTPUT_SIZE))

            cv2.imwrite(output_filename, resized)
