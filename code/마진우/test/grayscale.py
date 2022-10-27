import cv2
import pytesseract

path = 'pic/test01.jpeg'
image = cv2.imread(path)
text = pytesseract.image_to_string(image, lang='kor+eng')
print('Texto: ', text)
cv2.imshow('Image', image)

img_gray = cv2.imread(path, cv2.COLOR_BGR2GRAY)
img_gray = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
cv2.imshow("grayscale", img_gray)

text_gray = pytesseract.image_to_string(img_gray, lang='kor+eng')
print(text_gray)

cv2.waitKey(0)
cv2.destroyAllWindows()