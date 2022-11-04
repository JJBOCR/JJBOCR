from imutils.convenience import resize, grab_contours
from imutils.perspective import four_point_transform
from imutils import opencv2matplotlib
from skimage.filters import threshold_local
import copy
import matplotlib.pyplot as plt
import cv2
import numpy as np


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
        diff_img = 255 - cv2.absdiff(plane, dilated_img)
        norm_img = cv2.normalize(diff_img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        result.append(norm_img)
    result = cv2.merge(result)

    return result


def get_receipt_from_img(image, height=None, width=None, kernel=(5, 5), min_threshold=100, max_threshold=200):
    org_image = copy.deepcopy(image)
    image = resize(org_image, height, width)
    ratio = org_image.shape[1] / float(image.shape[1])

    # image_list에 gray, blurred, edge 검출 넣기
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, kernel, 0)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    dilated = cv2.dilate(blurred, rect_kernel)
    edged = cv2.Canny(dilated, min_threshold, max_threshold, apertureSize=3)

    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    receipt_contours = get_receipt_contour(contours)

    if receipt_contours is None:
        raise Exception('Could not find outline')

    transform_image = four_point_transform(org_image, receipt_contours.reshape(4, 2) * ratio)
    transform_image = remove_shadow(transform_image)

    plt_imshow('Transform', transform_image)

    return transform_image
