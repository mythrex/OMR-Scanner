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
# ques = [i for i in range(60)]
# opts = [random.randrange(0, 4) for _ in range(60)]
ANSWER_KEY = {0: 0, 1: 0, 2: 0, 3: 2, 4: 1}
bubble_thresh = 0

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
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    for c in cnts:
        # calc the perimeter
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02*peri, True)
        if len(approx) == 4:
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

# find question contours
questionCnts = []

# loop over countours
for c in cnts:
    (x, y, w, h) = cv2.boundingRect(c)
    ar = w / float(h)
    if w >= 20 and h >= 20 and ar >= 0.9 and ar <= 1.1:
        questionCnts.append(c)
        # cv2.rectangle(paper, (x, y), (x+w, y+h), (0, 255, 0), 1)

# sort the question contours from top to bottom
questionCnts = contours.sort_contours(questionCnts, method='top-to-bottom')[0]
# cv2.drawContours(paper, questionCnts, -1, 255, 1)
correct = 0
# each question has 4 possible answers, to loop over the
# question in batches of 4
for (q, i) in enumerate(np.arange(0, len(questionCnts), 5)):
    cnts = contours.sort_contours(questionCnts[i:i+5])[0]
    bubbled = None
    bubble_count = 0
    for (j, c) in enumerate(cnts):
        mask = np.zeros(thresh.shape, dtype='uint8')
        cv2.drawContours(mask, [c], -1, 255, -1)
        # apply the mask to the thresholded image, then
        # count the number of non-zero pixels in the
        # bubble area
        mask = cv2.bitwise_and(thresh, thresh, mask=mask)
        # cv2.imshow('Mask', mask)
        # cv2.waitKey(100)
        total = cv2.countNonZero(mask)
        # if total > current bubbled then
        # bubbled = total
        # print('total', total, 'bubbled', bubbled)
        if bubbled is None or bubbled[0] < total:
            # if total > bubble_thresh:
            #     bubble_count += 1
            bubbled = (total, j)

    color = (0, 0, 255)
    k = ANSWER_KEY[q]

    # check to see if the bubbled answer is correct
    # print(bubbled)
    # print('bubbled[1]', bubbled[1], 'k:', k)
    if k == bubbled[1]:
        color = (0, 255, 0)
        correct += 1

    if bubbled[0] > bubble_thresh:
        cv2.drawContours(paper, [cnts[k]], -1, color, 2)

# grab the test taker
score = (correct / 240) * 100
print("[INFO] score: {:.2f}%".format(score))
cv2.putText(paper, "{:.2f}%".format(score), (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

cv2.imshow("Original", image)
cv2.imshow("Exam", paper)
cv2.waitKey(0)
cv2.destroyAllWindows()
