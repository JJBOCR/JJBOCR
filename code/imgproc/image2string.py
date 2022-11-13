import pytesseract


def image2string(img, title=None):
    """
        전처리된 이미지에서 글자를 OCR로 읽어들이는 함수
    """
    options = '--psm 4'
    if title is None:
        path = 'result/result.txt'
    else:
        path = title
    file = open(path, 'w+')
    file.write("")
    file.close()
    if type(img) is list:
        for roi in img:
            text = pytesseract.image_to_string(roi, lang='kor+kor_vert+eng', config=options)
            file = open(path, 'a', encoding='UTF-8')
            file.write(text)
            file.write('\n')
            file.close()
    else:
        text = pytesseract.image_to_string(img, lang='kor+kor_vert+eng', config=options)
        file = open(path, 'a', encoding='UTF-8')
        file.write(text)
        file.close()
