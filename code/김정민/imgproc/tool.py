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


def detect_receipt_contours(image, kernel=(5, 5), min_threshold=100, max_threshold=200):
    """ image resize """
    src = copy.deepcopy(image)
    dst = imutils.resize(src, src.shape[1], src.shape[0])
    ratio = src.shape[1] / float(dst.shape[1])
    """ 1. convert image to grayscale """
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    # plot grayscale image
    plt_imshow('gray', gray)
    """ 2. Apply Gaussian filter 5 * 5 to get rid of noise """
    blurred = cv2.GaussianBlur(gray, kernel, 0)
    """ 3. Run Canny edge detector """
    edged = cv2.Canny(blurred, min_threshold, max_threshold, apertureSize=3)
    plt_imshow('edge', edged)
    """ 4. find Contours and sort by contours area """
    contours = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    plot_contours(src, contours)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    """ 5. find Poly(4 Points) in sorted contours """
    find_contours = get_receipt_contour(contours)

    if find_contours is None:
        raise Exception('Could not find outline')

    transform_image = four_point_transform(src, find_contours.reshape(4, 2) * ratio)
    plt_imshow('transform_image', transform_image)
    transform_image = remove_shadow(transform_image)
    plt_imshow('Transform', transform_image)

    return transform_image
