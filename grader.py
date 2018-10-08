# import the necessary packages
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
import random

# construct the argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to the input image")
args = vars(ap.parse_args())

# Answer Key
ques = [i for i in range(50)]
opts = [random.randrange(0, 4) for _ in range(50)]
ANSWER_KEY = dict(zip(ques, opts))

# load the image
orig = cv2.imread(args['image'])
image = orig.copy()
ratio = image.shape[0] / 800.0
image = imutils.resize(image, height=800)

# gray it
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# blur it
gray = cv2.GaussianBlur(gray, (5, 5), 0)
# canny edge detection
edged = cv2.Canny(gray, 5, 10)

# Find the contours
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
docCnts = None
if len(cnts) > 0:
    sorted(cnts, key=cv2.contourArea, reverse=True)
    for c in cnts:
        # calc the perimeter
        peri = cv2.arcLength(cnts[0], True)
        approx = cv2.approxPolyDP(cnts[0], 0.09*peri, True)
        if len(c) == 4:
            docCnts = approx
            break

# apply perspective transform to the shape
paper = four_point_transform(image, docCnts.reshape(4, 2))
warped = four_point_transform(gray, docCnts.reshape(4, 2))

# binarisation of image
# thresh[0] is th peak val
# thresh[1] is array
thresh = cv2.threshold(
    warped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

# find contours in threshholded image
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]

cv2.drawContours(paper, cnts, -1, (0, 0, 255), 1)
cv2.imshow('Warped', paper)
cv2.waitKey(0)
cv2.destroyAllWindows()
