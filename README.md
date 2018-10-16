# OMR SCANNER

This is a project that will be using some image processing techniques to evaluate the OMR Sheet.
Much of help is taken from [this blog](https://www.pyimagesearch.com/2016/10/03/bubble-sheet-multiple-choice-scanner-and-test-grader-using-omr-python-and-opencv/)

## How this works?

I will try to explain as effectively as possible.

This has mainly **4 steps**:

1. Do the edge detection.
2. Find the corner points of paper and apply perpective transform.
3. Do the thresholding.
4. Extract the question and detect the answer(_using masking_)

## Algorithm

1. Find the edges of paper and do the **perpective transform** to get the **bird's eye view** of paper.
2. Do binarisation of image for simplicity.
3. Find the options contours.
4. Loop over each option and find **how many pixels are white**.
5. Calculate the score.

### Step#1 Edge Detection

Before doing edge detection we do

- Black and White
- Blur

### Why do we do this?

We do this because,

- Black and white image has only 1 shade of color mainly black. This helps in easy computation of pixel values as we don't have to compute on different channels(**Mainly RGB**).

Code for Black and white.
`gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)`

- Blurring the image will **reduce the noise**.

#### Code for edge detection

```py
# gray it
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# blur it
gray = cv2.GaussianBlur(gray, (5, 5), 0)
# canny edge detection
edged = cv2.Canny(gray, 5, 10)
```
