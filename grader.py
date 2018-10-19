# import the necessary packages
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
import random
from math import ceil
from matplotlib import pyplot as plt

# construct the argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to the input image")
args = vars(ap.parse_args())

# Answer Key
ques = [i for i in range(60)]
opts = [random.randrange(0, 4) for _ in range(60)]
ANSWER_KEY = dict(zip(ques, opts))
bubble_thresh = 90
positive_marking = 1
negative_marking = 0
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
edged = cv2.Canny(gray, 20, 50)


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
# instead of otsu thresholding
# we have used adaptive thresholding

thresh = cv2.adaptiveThreshold(
    warped, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

# find contours in threshholded image
cnts = cv2.findContours(thresh.copy(), cv2.RETR_TREE,
                        cv2.CHAIN_APPROX_SIMPLE)

# filter out contours with parents
heirarchy = cnts[2][0]
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
filter_cnts = []
for h in range(len(heirarchy)):
    # if the contour has parent 1 keep it
    if heirarchy[h][3] == 1:
        filter_cnts.append(cnts[h])


# find question contours
questions = []

# loop over countours
for c in filter_cnts:
    (x, y, w, h) = cv2.boundingRect(c)
    ar = w / float(h)
    if w >= 10 and h >= 10 and ar >= 0.7 and ar <= 1.3:
        box = [(x//5)*5, y//30]
        questions.append([c, box])
        # cv2.rectangle(paper, (x, y), (x+w, y+h), (0, 255, 0), 1)


# sort the question contours from left to right
questions = sorted(questions, key=lambda q: q[1][0])
# sort the question contours from top to bottom
questions = sorted(questions, key=lambda q: q[1][1])
questionCnts = [q[0] for q in questions]
# cv2.drawContours(paper, questionCnts, 15, 255, 2)
score = 0
# each question has 4 possible answers, to loop over the
# question in batches of 4

mini = float('inf')
for (q, i) in enumerate(np.arange(0, len(questionCnts), 4)):
    cnts = questionCnts[i:i+4]
    bubbled = None
    bubble_count = 0
    for (j, c) in enumerate(cnts):
        mask = np.zeros(thresh.shape, dtype='uint8')
        cv2.drawContours(mask, [c], -1, 255, -1)
        # apply the mask to the thresholded image, then
        # count the number of non-zero pixels in the
        # bubble area
        mask = cv2.bitwise_and(thresh, thresh, mask=mask)
        total = cv2.countNonZero(mask)
        # if total > current bubbled then
        # bubbled = total
        # print('total', total, 'bubbled', bubbled)
        if bubbled is None or bubbled[0] < total:
            if total > bubble_thresh:
                bubble_count += 1
            bubbled = (total, j)
    # change the q to old q
    # as q0 -> 0
    # as q1 -> 15
    # as q2 -> 30 and so on
    row = q // 4
    col = q % 4
    old_question_no = col*15 + row
    color = (0, 0, 255)
    k = ANSWER_KEY[old_question_no]
    # check to see if the bubbled answer is correct
    if k == bubbled[1] and bubble_count == 1:
        color = (0, 255, 0)
        score += positive_marking
    # wrongly attempted and negative marking
    elif k != bubbled[1] and bubble_count == 1:
        score += negative_marking

    if bubbled[0] > bubble_thresh and bubble_count == 1:
        cv2.drawContours(paper, [cnts[k]], -1, color, 2)

# grab the test taker
# score = (score / 240) * 100
print("[INFO] score: {:.2f}%".format(score))
cv2.putText(paper, "{:.2f}%".format(score), (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

cv2.imshow("Original", paper)
cv2.imshow("Paper", paper)
cv2.waitKey(0)
cv2.destroyAllWindows()
