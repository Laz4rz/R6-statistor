import os

import cv2
import numpy as np
import matplotlib.pyplot as plt

debug = True

img_path = 'images/terrohunt.png'
img_name = img_path.split(sep='.')[0].split(sep='/')[1]

img = cv2.imread(img_path)
height = img.shape[0]
width = img.shape[1]

img = img[height//6:height//3, (width//32)*22:(width//32)*28]
# img = cv2.resize(img, (img.shape[1] // 4, img.shape[0] // 4))

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(img_gray, 170, 255, cv2.THRESH_BINARY)
cv2.imwrite(f'results/{img_name}_thresh.jpg', thresh)

contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
image_copy = img.copy()
cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
cv2.imwrite(f'results/{img_name}_contours_none.jpg', image_copy)

contours1, hierarchy1 = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
image_copy1 = img.copy()
cv2.drawContours(image_copy1, contours1, -1, (0, 255, 0), 2, cv2.LINE_AA)
cv2.imwrite(f'results/{img_name}_contours_simple.jpg', image_copy1)

if debug:
    horizontal1 = np.concatenate((cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR), cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)), axis=1)
    horizontal2 = np.concatenate((image_copy, image_copy1), axis=1)
    vertical = np.concatenate((horizontal1, horizontal2), axis=0)

    cv2.imshow('VERTICAL', vertical)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
