# yorizori_crawling

서강대학교 2021-2학기 캡스톤디자인 <요리조리> 프로젝트의 CRAWLING repo

* [👀 프로젝트 세부 내용](http://cscp2.sogang.ac.kr/CSE4187/index.php/%EC%9A%94%EB%A6%AC%EC%A1%B0%EB%A6%AC)
* [📱 시연 영상](https://youtu.be/LtJN2qcoPyc)
  
  [![Video Label](http://img.youtube.com/vi/LtJN2qcoPyc/0.jpg)](https://youtu.be/LtJN2qcoPyc)

### sg-yorizori TEAM
* [@huttzza](https://github.com/huttzza)
* [@ceru](https://github.com/ceruuuu)
* [@emmajenny](https://github.com/emmajenny)
* [@LeeJHJH](https://github.com/LeeJHJH)

### 기술 Stack
* **YOLOv5m** : 재료 이미지 인식 모델
* **Python** : Crawling, DB uploader
* **Django** : Server
* **Flutter** : App

### 관련 Repo
* [SERVER](https://github.com/sg-yorizori/yorizori_server)
* [APP](https://github.com/sg-yorizori/yorizori_app)
* [CRAWLING](https://github.com/sg-yorizori/yorizori_recipe_crawling)

### HOW TO

1. pip install -r requirements.txt

2. main.py의 food_list 수정

3. python main.py
    
    * chrome 브라우저가 실행되며 크롤링됨

4. recipe.json, recipe.csv 파일 출력

    * recipe.json 생성 시 `please check [레시피_이름](url) : 재료_이름` 메시지가 터미널에 출력된다면, 해당 레시피의 해당 재료가 (i) 버튼으로 연결된 링크가 없는지 확인 필요.
    <br>
    있는데 오류가 발생한 것이라면 직접 수정 필요.
