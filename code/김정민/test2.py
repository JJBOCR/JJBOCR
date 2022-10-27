import cv2
import pytesseract

image = cv2.imread('../PIC/lotto.png')
text = pytesseract.image_to_string(image, lang='kor+eng')
print('Texto: ', text)

cv2.imshow('Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
