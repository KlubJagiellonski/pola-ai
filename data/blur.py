import os
import cv2
import numpy as np
import math

photo_dir = 'Pola_scaled'
output_dir = 'Pola_blur'

def images_in_dir(photo_dir):
    for subdir in os.listdir(photo_dir):
        if subdir.startswith('.'):
            continue
        for photo in os.listdir(os.path.join(photo_dir, subdir)):
            if photo.startswith('.') or not photo.endswith('.jpg'):
                continue
            yield os.path.join(subdir, photo)

#https://github.com/xinario/defocus_segmentation/blob/master/lbpSharpness.py

def im2double(im):
	min_val = np.min(im.ravel())
	max_val = np.max(im.ravel())
	out = (im.astype('float') - min_val) / (max_val - min_val)
	return out



def s(x):
	temp = x>0
	return temp.astype(float)


def lbpCode(im_gray, threshold):
	width, height = im_gray.shape
	interpOff = math.sqrt(2)/2
	I = im2double(im_gray)
	pt = cv2.copyMakeBorder(I,1,1,1,1,cv2.BORDER_REPLICATE)
	right = pt[1:-1, 2:]
	left = pt[1:-1, :-2]
	above = pt[:-2, 1:-1]
	below = pt[2:, 1:-1]
	aboveRight = pt[:-2, 2:]
	aboveLeft = pt[:-2, :-2]
	belowRight = pt[2:, 2:]
	belowLeft = pt[2:, :-2]
	interp0 = right
	interp1 = (1-interpOff)*((1-interpOff) * I + interpOff * right) + interpOff *((1-interpOff) * above + interpOff * aboveRight)

	interp2 = above
	interp3 = (1-interpOff)*((1-interpOff) * I + interpOff * left ) + interpOff *((1-interpOff) * above + interpOff * aboveLeft)

	interp4 = left
	interp5 = (1-interpOff)*((1-interpOff) * I + interpOff * left ) + interpOff *((1-interpOff) * below + interpOff * belowLeft)

	interp6 = below
	interp7 = (1-interpOff)*((1-interpOff) * I + interpOff * right ) + interpOff *((1-interpOff) * below + interpOff * belowRight) 

	s0 = s(interp0 - I-threshold)
	s1 = s(interp1 - I-threshold)
	s2 = s(interp2 - I-threshold)
	s3 = s(interp3 - I-threshold)
	s4 = s(interp4 - I-threshold)
	s5 = s(interp5 - I-threshold)
	s6 = s(interp6 - I-threshold)
	s7 = s(interp7 - I-threshold)
	LBP81 = s0 * 1 + s1 * 2+s2 * 4   + s3 * 8+ s4 * 16  + s5 * 32  + s6 * 64  + s7 * 128
	LBP81.astype(int)

	U = np.abs(s0 - s7) + np.abs(s1 - s0) + np.abs(s2 - s1) + np.abs(s3 - s2) + np.abs(s4 - s3) + np.abs(s5 - s4) + np.abs(s6 - s5) + np.abs(s7 - s6)
	LBP81riu2 = s0 + s1 + s2 + s3 + s4 + s5 + s6 + s7
	LBP81riu2[U > 2] = 9

	return LBP81riu2




def lbpSharpness(im_gray, s, threshold):
	lbpmap  = lbpCode(im_gray, threshold)
	window_r = (s-1)//2
	h, w = im_gray.shape[:2]
	map =  np.zeros((h, w), dtype=float)
	lbpmap_pad = cv2.copyMakeBorder(lbpmap, window_r, window_r, window_r, window_r, cv2.BORDER_REPLICATE)

	lbpmap_sum = (lbpmap_pad==6).astype(float) + (lbpmap_pad==7).astype(float) + (lbpmap_pad==8).astype(float) + (lbpmap_pad==9).astype(float)
	integral = cv2.integral(lbpmap_sum)
	integral = integral.astype(float)

	map = (integral[s-1:-1, s-1:-1]-integral[0:h, s-1:-1]-integral[s-1:-1, 0:w]+integral[0:h, 0:w])/math.pow(s,2);

	return map

if __name__ == "__main__":
    for filename in images_in_dir(photo_dir):
        image = cv2.imread(os.path.join(photo_dir, filename))

        # Variation of the Laplacian
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        varLap = cv2.Laplacian(gray, cv2.CV_64F).var()

        sharpness_map = lbpSharpness(gray, 21, 0.016)
        sharpness_map = (sharpness_map - np.min(sharpness_map))/(np.max(sharpness_map - np.min(sharpness_map)))

        sharpness_map = (sharpness_map*255).astype('uint8')
        sharpness = 100 * sharpness_map.sum() / (image.shape[0]*image.shape[1]*256)
        concat = np.concatenate((image, np.stack((sharpness_map,)*3, -1)), axis=1)

        text = "varLap: {:.2f}\nsharp: {:.2f}%".format(varLap, sharpness)

        cv2.putText(concat, text, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0))

        cv2.imwrite(os.path.join(output_dir, os.path.basename(filename)), concat)
        