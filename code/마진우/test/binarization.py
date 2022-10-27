import cv2
import pytesseract

path = '../pic/test01.jpeg'
image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
text = pytesseract.image_to_string(image, lang='kor+eng')

t, otsu = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
print(t)

cv2.imshow('img', image)
cv2.imshow('otsu', otsu)

text_gray = pytesseract.image_to_string(otsu, lang='kor+eng')
print(text_gray)

cv2.waitKey()
cv2.destroyAllWindows()