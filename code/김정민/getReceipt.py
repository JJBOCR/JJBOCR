import cv2
import pytesseract
from imgproc.tool import detect_receipt_contours, plt_imshow

#
# # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
image = cv2.imread('../../PIC/receipt.jpg')

receipt_image = detect_receipt_contours(image, kernel=(5, 5), min_threshold=20, max_threshold=100)
cv2.imwrite('../../PIC/return_receipt_section.png', receipt_image)
# options = '--psm 4'
# text = pytesseract.image_to_string(cv2.cvtColor(receipt_image, cv2.COLOR_BGR2RGB),
#                                    config=options, lang='kor')
#
# print(text)
