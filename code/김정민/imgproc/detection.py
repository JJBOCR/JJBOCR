"""
    1. 영수증 부분만 detect
    2. 영수증 내용의 글자 부분만 detect

"""
import imutils
from imutils.convenience import resize, grab_contours
from imutils.perspective import four_point_transform
from imutils.contours import sort_contours
from imutils import opencv2matplotlib
from skimage.filters import threshold_local
import copy
import matplotlib.pyplot as plt
import cv2
import numpy as np
from .tool import get_receipt_contour, remove_shadow, morph_close, plt_imshow, plot_contours


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
    plt_imshow('blurred', blurred)
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


def detection_string_contours(img):
    """
        이미지 영역(영수증 부분만 전처리한 후)에서 글자 부분을 인식함
    """
    img_clone = copy.deepcopy(img)
    gray = cv2.cvtColor(img_clone, cv2.COLOR_BGR2GRAY)

    adap_thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 3, 12)

    morph_img = morph_close(adap_thresh)
    contours, hierarchy = cv2.findContours(morph_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sort_contours(contours, method='top-to-bottom')[0]

    return contours, gray



