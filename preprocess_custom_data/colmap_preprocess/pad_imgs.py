import os
import cv2 as cv
from glob import glob
import sys
import numpy as np


def pad(image, size, color=None, centering=(0.5, 0.5)):
    """
    Returns a resized and padded version of the image, expanded to fill the
    requested aspect ratio and size.

    :param image: The image to resize and crop.
    :param size: The requested output size in pixels, given as a
                 (width, height) tuple.
    :param method: Resampling method to use. Default is
                   :py:attr:`PIL.Image.BICUBIC`. See :ref:`concept-filters`.
    :param color: The background color of the padded image.
    :param centering: Control the position of the original image within the
                      padded version.

                          (0.5, 0.5) will keep the image centered
                          (0, 0) will keep the image aligned to the top left
                          (1, 1) will keep the image aligned to the bottom
                          right
    :return: An image.
    """
    if image.shape == size:
        out = image
        mask = np.ones_like(out[:, :, 0]) * 255
    else:
        out = np.zeros((*size, 3))
        out[:image.shape[0], :image.shape[1]] = image
        mask = np.zeros_like(out[:, :, 0])
        mask[:image.shape[0], :image.shape[1]] = 255
    return out, mask


def pad_images(work_dir):
    out_dir = os.path.join(work_dir, 'preprocessed')
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(os.path.join(out_dir, 'image'), exist_ok=True)
    os.makedirs(os.path.join(out_dir, 'mask'), exist_ok=True)

    image_list = glob(os.path.join(work_dir, 'images/*.png'))
    image_list = sorted(glob(os.path.join(work_dir, 'images/*.jpg')) + image_list)
    image_list.sort()
    imgs = []
    max_size = (0, 0)
    for i, image_path in enumerate(image_list):
        img = cv.imread(image_path)
        max_size = (max(img.shape[0], max_size[0]), max(img.shape[1], max_size[1]))
        imgs.append(img)
    for i, img in enumerate(imgs):
        img, mask = pad(img, max_size, color=0)
        cv.imwrite(os.path.join(out_dir, 'image', '{:0>3d}.png'.format(i)), img)
        cv.imwrite(os.path.join(out_dir, 'mask', '{:0>3d}.png'.format(i)), mask)
    print(f'Padded images: {i+1}')

if __name__ == '__main__':
    work_dir = sys.argv[1]
    pad_images(work_dir)
