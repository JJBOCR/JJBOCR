import cv2   # 이미지 가져오기 및 가공
import pytesseract  # 글자인식

#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
image = cv2.imread('lotto.png')  #이미지를 불러오는 함수이며 두번째 인자를 옵션으로 줄수있음 # image의 타입은 numpy 배열임을 알수있다.
text = pytesseract.image_to_string(image, lang='kor+eng')
print('Texto: ', text)

cv2.imshow('Image', image)   # 이미지를 윈도우 창에 출력
cv2.waitKey(0)  # 사용자 입력을 기다려 주는 함수/ 여기선 destroyAllWindows()를 위해 기다리는 용도이다.
cv2.destroyAllWindows()