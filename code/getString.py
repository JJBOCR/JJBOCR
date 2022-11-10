"""

    이미지 영역 중 영수증 부분만 골라 나와

    결과를 출력 후

    영역 중 글자부분만 OCR을 적용하는 파일

"""
import copy
import math

import cv2
import imutils
import numpy as np
import pytesseract
from imutils.contours import sort_contours
from imgproc.tool import plt_imshow


# def morph_close(img):
#     gray = copy.deepcopy(img)
#     rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 20))
#     square_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 50))
#
#     gray = cv2.GaussianBlur(gray, (11, 11), 0)
#     blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, rect_kernel)
#
#     grad = cv2.Sobel(blackhat, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=-1)
#     grad = np.absolute(grad)
#     min_val, max_val = np.min(grad), np.max(grad)
#     grad = (grad - min_val) / (max_val - min_val)
#     grad = (grad * 255).astype('uint8')
#
#     grad = cv2.morphologyEx(grad, cv2.MORPH_CLOSE, rect_kernel)
#     thresh = cv2.threshold(grad, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
#
#     square_thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, square_kernel)
#     square_thresh = cv2.erode(square_thresh, None, iterations=2)
#
#     plt_imshow('result', square_thresh)
#     return square_thresh
#
#
# def detection(img):
#     img_clone = copy.deepcopy(img)
#     gray = cv2.cvtColor(img_clone, cv2.COLOR_BGR2GRAY)
#
#     adap_thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 3, 12)
#
#     morph_img = morph_close(adap_thresh)
#     contours, hierarchy = cv2.findContours(morph_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     contours = sort_contours(contours, method='top-to-bottom')[0]
#
#     return contours, gray

#
# def extraction(org_img, contours):
#     receipt = copy.deepcopy(org_img)
#     plot_img = copy.deepcopy(org_img)
#     margin = 20
#     roi_list = []
#     roi_title_list = []
#
#     for c in contours:
#         (x, y, w, h) = cv2.boundingRect(c)
#         # ar = w // float(h)
#         ar = w * h
#         if w > 50 and h > 10:
#             roi = receipt[y - margin:y + h + margin, x - margin:x + w + margin]
#             if len(roi)==0:
#                 continue
#             roi_list.append(roi)
#             roi_title_list.append("Roi_{}".format(len(roi_list)))
#             color = (0, 0, 255)
#
#             cv2.rectangle(plot_img, (x - margin, y - margin), (x + w + margin, y + h + margin), color, 2)
#             cv2.putText(plot_img, "".join(str(ar)), (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.65, color, 2)
#
#     plt_imshow(roi_title_list, roi_list)
#     plt_imshow(["Grouping Image"], [plot_img], fig_size=(16, 10))
#
#     return roi_list


def mergeResize(img, row=600, col=100):
    src = copy.deepcopy(img)
    DST_COL = int((row * col) / row)
    DST_ROW = row
    RATIO = DST_COL / DST_ROW
    SRC_COL = src.shape[0]
    SRC_ROW = src.shape[1]
    SRC_RATIO = SRC_COL / SRC_ROW
    border_v = 0
    border_h = 0

    if RATIO >= SRC_RATIO:
        border_v = int(((RATIO * SRC_ROW) - SRC_COL) / 2)
    else:
        border_h = int(((RATIO * SRC_COL) - SRC_ROW) / 2)

    dst = cv2.copyMakeBorder(src, top=border_v, bottom=border_v, left=0, right=border_h * 2,
                             borderType=cv2.BORDER_CONSTANT, value=(255, 255, 255))
    dst = cv2.resize(dst, (DST_ROW, DST_COL))
    return dst


def merge_roi(roi_list):
    for idx, roi in enumerate(roi_list):
        if idx == 0:
            mergeImg = mergeResize(roi)
        else:
            cropImg = mergeResize(roi)
            mergeImg = np.concatenate((mergeImg, cropImg), axis=0)

    dst = cv2.threshold(mergeImg, 150, 255, cv2.THRESH_BINARY)[1]

    return dst


# def image2string(img, title=None):
#     options = '--psm 4'
#     if title is None:
#         file = open('result/result.txt', 'w+')
#     else:
#         file = open('result'+title, 'w+')
#     file.write("")
#     file.close()
#     if type(img) is list:
#         for roi in img:
#             text = pytesseract.image_to_string(roi, lang='kor+kor_vert+eng', config=options)
#             file = open('result/result.txt', 'a', encoding='UTF-8')
#             file.write(text)
#             file.write('\n')
#             file.close()
#     else:
#         text = pytesseract.image_to_string(img, lang='kor+kor_vert+eng', config=options)
#         file = open('result/result.txt', 'a', encoding='UTF-8')
#         file.write(text)
#         file.close()
#
#
# image = cv2.imread('../../PIC/return_receipt_section.png')
# cnt, gray = detection(image)
# roi_part = extraction(image, cnt)
# # result = merge_roi(roi_part)
# # plt_imshow('result', result)
# image2string(roi_part)
