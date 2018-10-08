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
cv2.drawContours(image, cnts, -1, (255, 0, 0), 1)
cv2.imshow('Edged', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
