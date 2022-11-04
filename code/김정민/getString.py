import copy

import cv2
import imutils
import numpy as np
import pytesseract
from imutils.contours import sort_contours
from imgproc.tool import get_receipt_from_img, plt_imshow

image = cv2.imread('../../PIC/receipt.jpg')
receipt_image = get_receipt_from_img(image, width=200, kernel=(5, 5), min_threshold=20, max_threshold=100)


def morph_close(img):
    gray = img.copy()
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 20))

    gray = cv2.GaussianBlur(gray, (11, 11), 0)
    blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, rect_kernel)

    grad = cv2.morphologyEx(blackhat, cv2.MORPH_CLOSE, rect_kernel)

    thresh = cv2.threshold(grad, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    plt_imshow('thresh', thresh)
    return thresh


def detection(img):
    img_clone = img.copy()
    gray = cv2.cvtColor(img_clone, cv2.COLOR_BGR2GRAY)

    adap_thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 3, 12)

    morph_img = morph_close(adap_thresh)
    # LongLine Remove
    contours, hierarchy = cv2.findContours(morph_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sort_contours(contours, method='top-to-bottom')[0]

    return contours, gray


def extraction(org_img, contours):
    # file = open('result/recongized.txt', 'w+')
    # file.write("")
    # file.close()
    receipt = org_img.copy()
    margin = 20
    roi_list = []
    roi_title_list = []

    for c in contours:
        (x, y, w, h) = cv2.boundingRect(c)
        ar = w // float(h)
        if w > 50 and h > 10:
            roi = receipt[y - margin:y + h + margin, x - margin:x + w + margin]
            roi_list.append(roi)
            roi_title_list.append("Roi_{}".format(len(roi_list)))
            color = (0, 0, 255)

            cv2.rectangle(receipt, (x - margin, y - margin), (x + w + margin, y + h + margin), color, 2)
            cv2.putText(receipt, "".join(str(ar)), (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.65, color, 2)

            # plt_imshow('roi', roi)
            # file = open('result/recongized.txt', 'a')
            # text = pytesseract.image_to_string(roi, lang='kor')
            # file.write(text)
            # file.write('\n')
            # file.close

    plt_imshow(["Grouping Image"], [receipt], fig_size=(16, 10))


cnt, gray = detection(receipt_image)
extraction(receipt_image, cnt)
