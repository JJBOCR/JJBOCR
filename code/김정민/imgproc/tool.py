from imutils.convenience import resize, grab_contours
from imutils.perspective import four_point_transform
from imutils import opencv2matplotlib
import copy
import matplotlib.pyplot as plt
import cv2


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


def get_receipt_from_img(image, height=None, width=None, kernel=(5, 5), min_threshold=75, max_threshold=200):
    org_image = copy.deepcopy(image)
    image = resize(org_image, height, width)
    ratio = org_image.shape[1] / float(image.shape[1])

    # image_list에 gray, blurred, edge 검출 넣기
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, kernel, 0)
    edged = cv2.Canny(blurred, min_threshold, max_threshold)

    image_list = {'gray': gray, 'blurred': blurred, 'edged': edged}
    contours = cv2.findContours(image_list['edged'].copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = grab_contours(contours)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    receipt_contours = get_receipt_contour(contours)

    if receipt_contours is None:
        raise Exception('Could not find outline')
    output = copy.deepcopy(image)
    cv2.drawContours(output, [receipt_contours], -1, (0, 255, 0), 2)
    image_list['Outline'] = output

    transform_image = four_point_transform(org_image, receipt_contours.reshape(4, 2) * ratio)

    titles = list(image_list.keys())
    images = list(image_list.values())

    plt_imshow('Transform', transform_image)
    plt_imshow(title=titles, img=images)

    return transform_image
