import imutils
from imutils.convenience import resize, grab_contours
from imutils.perspective import four_point_transform
from imutils import opencv2matplotlib
from skimage.filters import threshold_local
import copy
import matplotlib.pyplot as plt
import cv2
import numpy as np


def img2gray(image):
    if len(image.shape) <= 2:
        return copy.deepcopy(image)
    else:
        src = copy.deepcopy(image)
        return cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)


def any2rgb(image):
    if len(image.shape) <= 2:
        return cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    else:
        return opencv2matplotlib(image)


def plt_imshow(title='image', img=None, fig_size=(8, 5)):
    plt.figure(figsize=fig_size)
    titles = []
    rgbImg = []

    if type(img) == list:
        if type(title) == list:
            titles = title
        else:
            for i in range(len(img)):
                titles.append(title + '#' + str(i))
        n_figure = len(titles)
        for i in range(n_figure):
            rgbImg = any2rgb(img[i])
            plt.subplot(1, n_figure, i + 1)
            plt.imshow(rgbImg)
            plt.title(titles[i])
    else:
        rgbImg = any2rgb(img)
        plt.imshow(rgbImg)
        plt.title(title)

    plt.show()



def approximate_contour(contour):
    peri = cv2.arcLength(contour, True)
    return cv2.approxPolyDP(contour, 0.032 * peri, True)


def get_receipt_contour(contours):
    for c in contours:
        approx = approximate_contour(c)

        if len(approx) == 4:
            return approx


def remove_shadow(image):
    rgb_planes = cv2.split(image)

    result = []

    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((8, 8), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        norm_img = cv2.normalize(diff_img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        result.append(norm_img)
    result = cv2.merge(result)

    return result


def plot_contours(img, contours):
    src = copy.deepcopy(img)
    cv2.drawContours(src, contours, -1, (0, 255, 0), 2)
    plt_imshow('outline', src)


def morph_close(img):
    gray = copy.deepcopy(img)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 20))
    square_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 50))

    gray = cv2.GaussianBlur(gray, (11, 11), 0)
    blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, rect_kernel)

    grad = cv2.Sobel(blackhat, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=-1)
    grad = np.absolute(grad)
    min_val, max_val = np.min(grad), np.max(grad)
    grad = (grad - min_val) / (max_val - min_val)
    grad = (grad * 255).astype('uint8')

    grad = cv2.morphologyEx(grad, cv2.MORPH_CLOSE, rect_kernel)
    thresh = cv2.threshold(grad, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    square_thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, square_kernel)
    square_thresh = cv2.erode(square_thresh, None, iterations=2)

    plt_imshow('result', square_thresh)
    return square_thresh
