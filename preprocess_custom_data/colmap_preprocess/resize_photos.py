import cv2 as cv
import os
import sys
from glob import glob

if __name__ == '__main__':
    work_dir = sys.argv[1]
    out_dir = os.path.join(work_dir, 'images')
    img_paths = sorted(glob(os.path.join(work_dir, 'photos/*')))
    for i, img_name in enumerate(img_paths):
        img = cv.imread(img_name)
        if 442368 < img.shape[0]/img.shape[1]:
            raise ValueError('Image smaller than 442368 pixels is not supported.')
        img_small = cv.resize(img,
                              (0, 0),
                              fx=(442368/img.shape[0]/img.shape[1])**0.5,
                              fy=(442368/img.shape[0]/img.shape[1])**0.5,
                              interpolation=cv.INTER_AREA)
        os.makedirs(out_dir, exist_ok=True)
        cv.imwrite(os.path.join(out_dir, '{:0>3d}.png'.format(i)), img_small)
    print(f'Resized {i+1} images.')
