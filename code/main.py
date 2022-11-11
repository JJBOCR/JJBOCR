import cv2
import pytesseract
from imgproc.tool import *
from imgproc.detection import *
from imgproc.extraction import *
from imgproc.image2string import image2string


def detect_read_string_from_receipt(img):
    receipt_image = detect_receipt_contours(img, kernel=(5, 5), min_threshold=20, max_threshold=100)
    cv2.imwrite('../../PIC/refactor_test.png', receipt_image)

    options = '--psm 4'
    text = pytesseract.image_to_string(cv2.cvtColor(receipt_image, cv2.COLOR_BGR2RGB),
                                       config=options, lang='kor+kor_vert+eng')

    file = open('result/refactor_result.txt', 'w+', encoding='UTF-8')
    file.write(text)
    file.write('\n refactor 결과 call detect_receipt_contours => pytesseract.image2string')
    file.close()


def detect_read_string_from_roi(img):
    cnt, gray = detection_string_contours(img)
    roi_part = extraction(img, cnt)
    image2string(roi_part, 'refactor_roi_test.txt')


if __name__ == '__main__':
    print('이미지 인식을 위해서 다음과 같은 파일을 load함')
    path = '../../PIC/receipt.jpg'
    image = cv2.imread(path)
    print('영수증 부분만 인식 : 1')
    print('영수증에서 글자 부분만 인식: 2\n')
    menu = int(input())

    if menu == 1:
        detect_read_string_from_receipt(image)
    elif menu == 2:
        path = '../../PIC/refactor_test.png'
        image = cv2.imread(path)
        detect_read_string_from_roi(image)
    else:
        raise Exception(print('해당 항목이 없습니다.'))
    print('완료')
