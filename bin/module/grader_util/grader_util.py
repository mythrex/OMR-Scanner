import cv2
import numpy as np
from .grader_errors import BubbleDetectionError
import sys
# loop over countours
# this function find the question bubbles
# outputs matrix([contour, box])


def find_questions(cnts, image, show_boxes=False):
    questions = []
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        ar = w / float(h)
        if (w >= 15 and h >= 15) and (w <= 50 and h <= 50) and ar >= 0.7 and ar <= 1.3:
            box = [(x//5)*5, y]
            questions.append([c, box])
            if show_boxes == True:
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 1)
    try:
        if len(questions) != 240:
            raise BubbleDetectionError('Bubbles not detected Properly.')
    except BubbleDetectionError as e:
        sys.exit(e.message)
    return questions


'''
We are now sorting from left to right by taking a batch of 16 contours
that are basically a whole row and then sorting them from increasing order of x
'''


def find_ques_cnts(questions):
    # sort the question contours from top to bottom
    questions = sorted(questions, key=lambda q: q[1][1])
    questionCnts = []
    for i in np.arange(0, len(questions), 16):
        # take a row of bubbles
        q = list(questions[i: i+16])
        # append each contour sorted from left to right in a row
        # sort them using x
        q = sorted(q, key=lambda k: k[1][0])
        for o in q:
            # append each contour sorted from left to right in a row
            questionCnts.append(o[0])
    return questionCnts

# calculate the old question no
# this function converts the old question no to
# new question no. By default it assumes that questions
# are to be converted from horizontal to vertical fashion


def convert_ques_no(q, rows_cnt=15, cols_cnt=4, hori_to_vert=True):
    if hori_to_vert:
        row = q // cols_cnt
        col = q % cols_cnt
        return col * rows_cnt + row
    col = q // rows_cnt
    row = q % rows_cnt
    return row * cols_cnt + col
