import copy
import math
import cv2
import numpy as np
from imutils.contours import sort_contours
from imgproc.tool import plt_imshow


def extraction(org_img, contours):
    """
        detection.detection_string_contours 에서 전처리된 이미지에서 글자에 Contour를 그리는 함수
    """

    receipt = copy.deepcopy(org_img)
    plot_img = copy.deepcopy(org_img)
    margin = 20
    roi_list = []
    roi_title_list = []

    for c in contours:
        (x, y, w, h) = cv2.boundingRect(c)
        # ar = w // float(h)
        ar = w * h
        if w > 50 and h > 10:
            roi = receipt[y - margin:y + h + margin, x - margin:x + w + margin]
            if len(roi) == 0:
                continue
            roi_list.append(roi)
            roi_title_list.append("Roi_{}".format(len(roi_list)))
            color = (0, 0, 255)

            cv2.rectangle(plot_img, (x - margin, y - margin), (x + w + margin, y + h + margin), color, 2)
            cv2.putText(plot_img, "".join(str(ar)), (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.65, color, 2)

    plt_imshow(roi_title_list, roi_list)
    plt_imshow(["Grouping Image"], [plot_img], fig_size=(16, 10))

    return roi_list
