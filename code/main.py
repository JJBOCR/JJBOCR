import cv2
import pytesseract
import argparse
from imgproc.tool import *
from imgproc.detection import *
from imgproc.extraction import *
from imgproc.image2string import image2string


def detect_read_string_from_receipt(img, save_path, write_path):
    receipt_image = detect_receipt_contours(img, kernel=(5, 5), min_threshold=20, max_threshold=100)
    cv2.imwrite(save_path, receipt_image)

    options = '--psm 4'
    text = pytesseract.image_to_string(cv2.cvtColor(receipt_image, cv2.COLOR_BGR2RGB),
                                       config=options, lang='kor+kor_vert+eng')

    file = open(write_path, 'w+', encoding='UTF-8')
    file.write(text)
    file.write('\n refactor 결과 call detect_receipt_contours => pytesseract.image2string')
    file.close()


def detect_read_string_from_roi(img, write_path):
    cnt, gray = detection_string_contours(img)
    roi_part = extraction(img, cnt)
    image2string(roi_part, write_path)


if __name__ == '__main__':
    pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    print('이미지 인식을 위해서 다음과 같은 파일을 로드함')

    parser = argparse.ArgumentParser(
        description='detect a receipt from a whole image and detect a letter from receipt part'
    )
    parser.add_argument('--process', metavar='N', type=int, help='an integer for the process number '
                                                                 '\n 1: detect a receipt from image'
                                                                 '\n 2: detect a letter from receipt part')
    parser.add_argument('--path', type=str, help='relative path to load an image')
    parser.add_argument('--s', type=str, default='result/img/result_img.png', help='relative path to save an image /'
                                                                                   '\n ex) result/img/result_img.png')
    parser.add_argument('--r', type=str, default='result/result.txt', help='relative path to save a result'
                                                                           '\n ex) result/result.txt')
    args = parser.parse_args()

    path = args.path
    menu = args.process
    save = args.s
    write_result = args.r

    image = cv2.imread(path)
    if menu == 1:
        detect_read_string_from_receipt(image, save, write_result)
    elif menu == 2:
        detect_read_string_from_roi(image, write_result)

    print('완료')
    # path = '../PIC/receipt.jpg'
    # image = cv2.imread(path)
    # print('영수증 부분만 인식 : 1')
    # print('영수증에서 글자 부분만 인식: 2\n')
    # menu = int(input())
    #
    # if menu == 1:
    #     detect_read_string_from_receipt(image)
    # elif menu == 2:
    #     path = '../PIC/refactor_test.png'
    #     image = cv2.imread(path)
    #     detect_read_string_from_roi(image)
    # else:
    #     raise Exception(print('해당 항목이 없습니다.'))
    # print('완료')
