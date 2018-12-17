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
            total_edges = edges.sum()

            left, top, right, bottom = (0, 0, width-1, height-1)
            skipped_edges = 0
            while right-left > OUTPUT_SIZE and bottom - top > OUTPUT_SIZE  and \
                  (skipped_edges < SKIP_EDGSS_RATIO * total_edges or (right-left) != (bottom-top)):
                if right - left > bottom - top:
                    left_edge = np.sum(edges[top:bottom, left])
                    right_edge = np.sum(edges[top:bottom, right])
                    if left_edge < right_edge:
                        left += 1
                        skipped_edges += left_edge
                    else:
                        right -= 1
                        skipped_edges += right_edge
                else:
                    top_edge = np.sum(edges[top, left:right])
                    bottom_edge = np.sum(edges[bottom, left:right])
                    if top_edge < bottom_edge:
                        top += 1
                        skipped_edges += top_edge
                    else:
                        bottom -= 1
                        skipped_edges += bottom_edge
                
#            bgr_edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
#            img = cv2.rectangle(img, (left, top), (right, bottom), (255,255,255), 2)
#            all = np.hstack((img, bgr_edges))
#            output_filename = os.path.join(OUTPUT_FOLDER, file)
#            cv2.imwrite(output_filename, all)
            

            cropped = img[top:bottom, left:right]
#            resized = cv2.resize(cropped, (OUTPUT_SIZE, OUTPUT_SIZE))
            cv2.imwrite(output_filename, cropped)
