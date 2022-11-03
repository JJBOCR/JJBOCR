import cv2
import pytesseract
from imgproc.tool import get_receipt_from_img, plt_imshow

#
# # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
image = cv2.imread('../../PIC/receipt.jpg')

receipt_image = get_receipt_from_img(image, width=200, kernel=(5, 5), min_threshold=20, max_threshold=100)

options = '--psm 4'
text = pytesseract.image_to_string(cv2.cvtColor(receipt_image, cv2.COLOR_BGR2RGB),
                                   config=options, lang='kor+eng')

print(text)
