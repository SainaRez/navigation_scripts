#!/usr/bin/env python

""" this script reads in distroted images and rectifies them """

import cv2
assert cv2.__version__[0] == '3', 'The fisheye module requires opencv version >= 3.0.0'

import numpy as np
import os
import sys
import glob

# You should replace these 3 lines with the output in calibration step
DIM=(848, 800)
K=np.array([[284.5556945800781, 0.0, 423.9186096191406], [0.0, 285.72711181640625, 396.7340087890625], [0.0, 0.0, 1.0]])
D=np.array([[-0.0008939161780290306], [0.03393154963850975], [-0.03224578872323036], [0.004643863998353481]])
def undistort(img_path):
    img = cv2.imread(img_path)
    h,w = img.shape[:2]
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    cv2.imwrite(img_path, undistorted_img)
    #cv2.imshow("undistorted", undistorted_img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
if __name__ == '__main__':
    images = glob.glob('imgs/cam1/*.png')
    for i in images:
        undistort(i)
    # for p in sys.argv[1:]:
    #     undistort(p)