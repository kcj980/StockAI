# 스토끼
- 서버비 문제로 2023-01-12 서버를 종료하였습니다.

## 프로젝트 소개

초보자도 쉽게 투자 할 수 있는 모의투자 사이트입니다.
- 어렵게 느껴지는 주식에 대한 접근성을 높이고자 함
- 주식(stock) + 토끼(2023토끼의해)

## 개발 기간 / 참여 인원
- 2022.11.27 ~ 2023.01.06

- 이동비, 김현수, 박동주, 이형찬, 김창준, 문준수, 정주원

## 프로젝트 선정 배경
- 2020년 이후 코로나시기 주식시장 열풍, 개인투자자가 급격히 증가함.

- 하지만 개인투자자들의 손실이 큰 사례들이 많음.

- 개인투자 실패 이유중 가장 큰 이유는 정보력/지식 부족인 것으로 조사 됨.

- 추가적으로 로보어드바이저 시장이 급격하게 활성화 됨.

- 그러나 대부분 유로 서비스이며 AI에게 모든 돈을 맡기는 형태로 직접투자 불가.

## 차별성
- AI포트폴리오를 참고하여 투자 가능

- 종목별로 투자 조언 – AI로 분석한 종목별 예측 결과를 참고하여 투자 가능

- 타 사이틀보다 주식 입문자들을 위해 보기 쉽고 이용하기 간편하게 제작

## 개발 환경
|분야|개발 환경|
|:---:|---|
|Front|![image](https://user-images.githubusercontent.com/97291618/215204783-2b8f1439-583d-4851-8c1f-d1dec816ffb5.png)|
|Backend|![image](https://user-images.githubusercontent.com/97291618/215204451-0bba626b-7d38-4a3c-be6f-0ba14fa9dc57.png)|
|Data Pipeline & AI|![image](https://user-images.githubusercontent.com/97291618/215204570-4f256419-e402-4750-b0d9-43728bc95329.png)|
|Cloud Server|![image](https://user-images.githubusercontent.com/97291618/215204630-78d0d97f-e878-44e6-a482-fe404d977745.png)|

## 맡은 역할
- AI - 데이터 수집 및 전처리

- BE - ERD설계, MySQL을 사용한 DB구성, 데이터 파이프라인 설계

- Server - AWS를 사용해 서비스 배포

## 웹 화면
![image](https://user-images.githubusercontent.com/97291618/216814445-8be3cc2e-c8c6-4339-b8cb-1534f998e93e.png)
![image](https://user-images.githubusercontent.com/97291618/216814459-6cb18aed-bc54-4d9e-a72b-70814ca29f78.png)
![image](https://user-images.githubusercontent.com/97291618/216814496-883dfbc3-ae3a-4c34-816f-21e715e3db00.png)
![image](https://user-images.githubusercontent.com/97291618/216814509-5c6d45d8-6c94-443d-9715-7d8d6563b700.png)
![image](https://user-images.githubusercontent.com/97291618/216814553-c2874f7c-38ea-4656-ab45-337e20b49328.png)





--------------------------------------
# **0. 팀원 소개**

<details>
<summary> [ 접기 / 펼치기 버튼 ] </summary>

&nbsp;

- 김창준
    - 역할 : DB, AWS, 데이터 수집 및 적재
    - Email : ~
- 김현수
    - 역할 : Backend, git 관리
    - Email : ~
- 문준수
    - 역할 : AI, 데이터 수집 및 처리
    - Email : ~
- 박동주
    - 역할 : Backend, 웹 총괄
    - Email : ~
- 이동비
    - 역할 : 팀장, AI, AWS, 데이터 수집 및 처리
    - Email : ~
- 이형찬
    - 역할 : Frontend, 웹 디자인
    - Email : ~
- 정주원
    - 역할 : Frontend, 웹 디자인
    - Email : ~

</details>

&nbsp;

# **1. 프로젝트 소개**

### **스토끼(StocKAI)**
모의투자와 AI로 누구나 쉽게 주식 투자에 대한 지식과 경험을 쌓을 수 있는 플랫폼

✔ **개발배경**
- 코로나19 이후 사람들의 주식에 대한 관심도가 높아짐. 이러한 유행 속에서 주식과 관련된 AI 서비스들이 많이 선보였지만, 대부분 서비스 요금을 지불해야 하거나 입문자를 고려했을 때 주가 정보나 용어 습득의 어려움이 있었음

    - 기존 서비스 보다 간편하고 지식 습득이 용이해야 함
    - 입문자의 진입 장벽을 낮추기 위한 모의투자 서비스를 제작
    - 주식을 분석하고 주가를 예측하는 AI를 제작하여 사용자에게 종목 추천  

✔ **대상**
- 주식 투자 입문자 및 주식에 관심이 있는 사람 모두 

&nbsp;

# **2. 아키텍처**

- 2-Tier

![Alt text](./img/02_archi.png)
<!-- <img src="example" alt="example"></img> -->

&nbsp;

# **3. DB**

- ERD

![Alt text](./img/03_DB_3.png)
<!-- <img src="example" alt="example"></img> -->

>- **주식 데이터**
>    - StockData : 종목 데이터
>    - MacroeconomicIndicators : 거시지표 데이터
>- **AI 예측 결과**
>    - ModelResult : 자체제작 모델 예측결과 저장
>    - StockCode : 종목이름,코드와 종목별 모델 정확도 저장
>    - AIRate : AI모의투자 결과 저장
>    - AIFunds : AI모의투자 현재 자금 저장
>- **사용자 데이터**
>    - UserData : 사용자 정보 저장
>    - UserStock : 사용자 주식 현황 저장
>- **그 외(게시판, 용어사전)**
>    - Message : 게시판 글 저장
>    - Comment : 댓글 저장
>    - Dictionary : 주식 용어 저장

- **갱신 주기**
    - day : StockCode 외의 모든 테이블
    - week : StockCode

&nbsp;

# **4. 웹 구성도**

![Alt text](./img/04_web.png)

#### Flow
- **초기 시작** : Intro > 메인 화면 > 회원가입 > 로그인
- **모의 투자** : 메인 화면 > 주식현황 + 모의투자
- **AI 포트폴리오** : 메인화면 > StocKAI
- **보유 주식 현황** : 메인화면 > 마이페이지

&nbsp;

# **5. 데이터 파이프라인**

- 일괄처리(batch processing) 데이터 파이프라인 구성
    - 데이터 수집 -> 데이터 처리 -> 검증 -> DB 적재 -> web서비스 동기화

![Alt text](./img/05_data_pipe.png)

&nbsp;

# **6. AI 모델**

![Alt text](./img/06_ai.png)

&nbsp;

# **7. UI / UX**

| 메인 페이지 | 마이 페이지 |
| :-----: | :-----: |
| ![Alt text](./img/07_1_main3.png) | ![Alt text](./img/07_4_mypage2.png) |

| 주식현황 + 모의투자 | AI 포트폴리오 |
| :-----: | :-----: |
| ![Alt text](./img/07_3_stock2.png) | ![Alt text](./img/07_2_ai2.png) |

&nbsp;

# **8. 데모**

http://3.35.230.74:8000/welcome/

&nbsp;

# **9. 개발환경 및 데이터 출처**

- Front

| HTML | CSS | JavaScript | BootStrap5 |
| ---- | --- | ---------- | ---------- |
| ![Alt text](./img/09_1.png) | ![Alt text](./img/09_2.png) | ![Alt text](./img/09_3.png) | ![Alt text](./img/09_9.png) |

- Backend

| Python | Django | Django REST | MySQL |
| ------ | ------ | ----------- | ----- |
| <middle>![Alt text](./img/09_4.png)</middle> | ![Alt text](./img/09_5.png) | ![Alt text](./img/09_6.png) | ![Alt text](./img/09_7.png) |

- Data Pipeline & AI

| beautifulsoup | pandas | konlpy | sklearn | tensorflow |
| --- | --- | ------ | ------- | ---------- |
| ![Alt text](/img/dp_ai/Beautifulsoup.png) | ![Alt text](/img/dp_ai/pandas.png) | ![Alt text](/img/dp_ai/KoNLPy.png) | ![Alt text](/img/dp_ai/scikit%20learn.png) | ![Alt text](/img/dp_ai/Tensorflow.png) |

- Cloud Server

| AWS | ubuntu |
| --- | --- |
| ![Alt text](/img/others/aws.png) | ![Alt text](/img/others/ubuntu.png) |

<!-- <img src="example" alt="example"></img> -->
<!-- <img src="09_1.png" width="20%" height="30%" title="px(픽셀) 크기 설정" alt="web_config"></img> -->
