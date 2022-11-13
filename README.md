JJBOCR
------------------
영수증 이미지에 대한 한글 OCR 인식율 향상 프로젝트

목차
-----------------

  * [요구사항](#요구사항)
  * [OCR Process](#OCR Process Flow)
  * [사용법](#사용법) 
  * [개선방향](#개선방향)
    * 이미지 전처리
    * 데이터 학습
  * [License](#license)

요구사항
------------

OCR 한글 영수증 인식을 위한 요구사항

  * [pytesseract][pytessearct]
  * [tessearact-OCR][tessearact-OCR]
  * [OpenCV][opencv]


[opencv]: https://opencv.org/
[python]: https://www.python.org/
[pytessearct]: https://github.com/madmaze/pytesseract/
[tessearact-OCR]: https://github.com/UB-Mannheim/tesseract/wiki
[ananaconda]: https://www.anaconda.com/
 * 기타 설치 요구사항은 requirement.txt 참고
 * 해당 requirement.txt는 [Ananaconda][ananaconda] 가상환경을 사용함
```
$ conda create -n <environment-name> --file requriement.txt
```


사용법
----------------------------
Anaconda prompt을 실행시킨 후 가상환경으로 설정한 후 다음을 실행한다. 
```shell
conda activate [가상환경_name]
python main.py --process [N, 0, 1] --path [relative path to load image] --s [relative path to save the image] --r [relative path to save the result.txt]
```

OCR Process Flow
-------------------------
![image](https://user-images.githubusercontent.com/64830434/198179750-1136d80b-a302-4a57-a9ce-eefe359f73b8.png)

개선방향
----------------------
## 이미지 전처리(Image Processing)
이미지 전처리(Image Processing)는 Tesseract가 보다 명확하게 글자를 인식할 수 있도록 하기위한
방법이다. Image Processing의 대표적인 기법으로는 이진화, 노이즈 제거, 이미지 팽창과
침식, 이미지 회전 및 기울기 보정, 투명도 조절, 테두리 제거 등이 있다.

## 데이터 학습