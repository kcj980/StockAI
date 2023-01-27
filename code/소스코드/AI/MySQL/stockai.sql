create database StockAI;
use StockAI;

#테이블 생성
#주식 용어
create table Dictionary(
    id int not null auto_increment PRIMARY KEY,
    title char(200),
    content text(30000)
);

#거시지표
create table MacroeconomicIndicators(
	id int not null auto_increment PRIMARY KEY,
    date_time date,
    kospi float(10), #코스피
    america_top_500 float(10), #미국 상장된 상위500개의 주식의 지표
    gold float(10), #금
    copper float(10), #구리
    k_gov3 float(10), #3년 한국채 수익율
    usd_k float(10), #환율
    inflation int, #인플레이션
    treasury_bonds int, #국채
    tightening int, #긴축
    normality int, #정상
    powell int, #파월
    dispute int, #분쟁
    japan int, #일본
    volume int, #물량
    chairman int, #의장
    remarks int, #발언
    thought int, #사상
    effect int, #효과
    anxiety int, #불안
    buying int, #매수세
    volatility int, #유동
    early_stage int, #초반
    decline int, #낙폭
    learning_result float(20) #학습결과
);

#종목정보
create table StockData(
	id int not null auto_increment PRIMARY KEY,
    stock_code char(7),
    data_time date,
    start_open float(10),#시가
    high float(10),#고가
    low float(10),#저가
    end_close float(10),#종가
    trading_volume float(15), #거래량
    transaction_amount float(15), #거래대금
    end_rate_change float(10), #등락율
    institutional_total float(20),#기관 합계
    other_corporations float(15),#기타 법인
    individual float(15),#개인
    foreigner_total float(15), # 외국인 합계
    short_selling float(10),#공매도
    short_buying float(15),# 공매도 매수
    short_importance float(10)#공매도 비중
);

#종목코드-이름
create table StockCode(
    stock_code char(7) not null PRIMARY KEY,
    stock_name char(50),
    xgb_short_pred float(20),
	xgb_long_pred float(20),
    ltms_short_pred float(20),
    ltms_long_pred float(20)
);

#유저모의투자 현황
create table UserStock(
    id int not null auto_increment PRIMARY KEY,
    userid char(30),
    stock_code char(7),
    count int,
    stock_mean_price int, #내가 구매한 평균단가
    stock_value int, #해당 날 종목의 종가 #수정됨
    sum_stock_value bigint #수정됨
);

#유저정보
create table UserData(
    userid char(30) not null,
    user_password char(128) not null,
    mail char(50) not null,
    user_name char(30) not null,
    date_of_birth date,
    experience int not null,
    now_money bigint default 100000000,
    invest_value bigint default 0,
    total_money bigint default 100000000, 
    is_active bool default true,
	is_admin bool default false,
	is_staff bool default false,
	is_superuser bool default false,
    
    PRIMARY KEY(userid),
    UNIQUE INDEX (user_password),
    UNIQUE INDEX (mail)
);

#종목 모델링 결과
create table ModelResult(
    id int not null auto_increment,
    stock_code char(7) not null,
    date_time date not null,
    xgb_short_result float(20),
    xgb_long_result float(20),
    lstm_short_result float(20),
    lstm_long_result float(20),

    PRIMARY KEY(id)
);

#ai모의투자 수익률
create table AIRate(
	date_time date not null,
	synthesis_rate float(20),
	A000060 float(10),
	A000100 float(10),
	A000270 float(10),
	A000660 float(10),
	A000720 float(10),
	A000810 float(10),
	A003490 float(10),
	A003550 float(10),
	A003670 float(10),
	A004020 float(10),
	A004990 float(10),
	A005380 float(10),
	A005490 float(10),
	A005830 float(10),
	A005930 float(10),
	A005935 float(10),
	A005940 float(10),
	A006400 float(10),
	A006800 float(10),
	A007070 float(10),
	A008560 float(10),
	A008770 float(10),
	A009150 float(10),
	A009540 float(10),
	A009830 float(10),
	A010130 float(10),
	A010140 float(10),
	A010620 float(10),
	A010950 float(10),
	A011070 float(10),
	A011170 float(10),
	A011200 float(10),
	A011780 float(10),
	A011790 float(10),
	A012330 float(10),
	A012450 float(10),
	A015760 float(10),
	A016360 float(10),
	A017670 float(10),
	A018260 float(10),
	A018880 float(10),
	A021240 float(10),
	A024110 float(10),
	A028050 float(10),
	A028260 float(10),
	A028300 float(10),
	A029780 float(10),
	A030200 float(10),
	A032640 float(10),
	A032830 float(10),
	A033780 float(10),
	A034020 float(10),
	A034220 float(10),
	A034730 float(10),
	A035250 float(10),
	A035420 float(10),
	A035720 float(10),
	A036460 float(10),
	A036570 float(10),
	A047810 float(10),
	A051900 float(10),
	A051910 float(10),
	A055550 float(10),
	A066570 float(10),
	A066970 float(10),
	A068270 float(10),
	A071050 float(10),
	A078930 float(10),
	A086280 float(10),
	A086790 float(10),
	A088980 float(10),
	A090430 float(10),
	A091990 float(10),
	A096770 float(10),
	A097950 float(10),
	A105560 float(10),
	A128940 float(10),
	A137310 float(10),
	A138040 float(10),
	A161390 float(10),
	A207940 float(10),
	A241560 float(10),
	A247540 float(10),
	A251270 float(10),
	A259960 float(10),
	A267250 float(10),
	A271560 float(10),
	A282330 float(10),
	A293490 float(10),
	A302440 float(10),
	A316140 float(10),
	A323410 float(10),
	A326030 float(10),
	A329180 float(10),
	A352820 float(10),
	A361610 float(10),

	PRIMARY KEY(date_time)
);

#ai모의투자 자금 현황
create table AIFunds(
	date_time date not null,
	A000060 float(10),
	A000100 float(10),
	A000270 float(10),
	A000660 float(10),
	A000720 float(10),
	A000810 float(10),
	A003490 float(10),
	A003550 float(10),
	A003670 float(10),
	A004020 float(10),
	A004990 float(10),
	A005380 float(10),
	A005490 float(10),
	A005830 float(10),
	A005930 float(10),
	A005935 float(10),
	A005940 float(10),
	A006400 float(10),
	A006800 float(10),
	A007070 float(10),
	A008560 float(10),
	A008770 float(10),
	A009150 float(10),
	A009540 float(10),
	A009830 float(10),
	A010130 float(10),
	A010140 float(10),
	A010620 float(10),
	A010950 float(10),
	A011070 float(10),
	A011170 float(10),
	A011200 float(10),
	A011780 float(10),
	A011790 float(10),
	A012330 float(10),
	A012450 float(10),
	A015760 float(10),
	A016360 float(10),
	A017670 float(10),
	A018260 float(10),
	A018880 float(10),
	A021240 float(10),
	A024110 float(10),
	A028050 float(10),
	A028260 float(10),
	A028300 float(10),
	A029780 float(10),
	A030200 float(10),
	A032640 float(10),
	A032830 float(10),
	A033780 float(10),
	A034020 float(10),
	A034220 float(10),
	A034730 float(10),
	A035250 float(10),
	A035420 float(10),
	A035720 float(10),
	A036460 float(10),
	A036570 float(10),
	A047810 float(10),
	A051900 float(10),
	A051910 float(10),
	A055550 float(10),
	A066570 float(10),
	A066970 float(10),
	A068270 float(10),
	A071050 float(10),
	A078930 float(10),
	A086280 float(10),
	A086790 float(10),
	A088980 float(10),
	A090430 float(10),
	A091990 float(10),
	A096770 float(10),
	A097950 float(10),
	A105560 float(10),
	A128940 float(10),
	A137310 float(10),
	A138040 float(10),
	A161390 float(10),
	A207940 float(10),
	A241560 float(10),
	A247540 float(10),
	A251270 float(10),
	A259960 float(10),
	A267250 float(10),
	A271560 float(10),
	A282330 float(10),
	A293490 float(10),
	A302440 float(10),
	A316140 float(10),
	A323410 float(10),
	A326030 float(10),
	A329180 float(10),
	A352820 float(10),
	A361610 float(10),

	PRIMARY KEY(date_time)
);

#게시판 - Message
create table Message(
    message_id int not null auto_increment PRIMARY KEY,
    userid char(30),
    title char(200),
    content  text(30000),
    date_time date
);

#게시판 - Comment
create table Comment(
    comment_id int not null auto_increment PRIMARY KEY,
    userid char(30),
    message_id int,
    content  text(30000),
    date_time date
);

#데이터 테스트
INSERT INTO UserData(userid,user_password, mail, user_name, date_of_birth, experience) VALUES('kcj98','asdf34!@', '김창준@naver.com', '김창준', STR_TO_DATE("2020-02-24","%Y-%m-%d"), 1);
INSERT INTO UserData(userid,user_password, mail, user_name, date_of_birth, experience) VALUES(2,'asdf34!@2', '김창준@naver.com2', '김창준2', STR_TO_DATE("2020-02-03","%Y-%m-%d"), 2);
INSERT INTO UserData(userid,user_password, mail, user_name, date_of_birth, experience) VALUES('asdf3','asdf34!@3', '김창준@naver.com3', '김창준3', STR_TO_DATE("2020-03-03","%Y-%m-%d"), 3);
INSERT INTO UserData(userid,user_password, mail, user_name, date_of_birth, experience) VALUES('','45445', '김창준@naver.com445', '김창준45', STR_TO_DATE("2020-03-13","%Y-%m-%d"), 3);
INSERT INTO UserStock(userid,stock_code, count) VALUES('kcj98','A003550', 1);
INSERT INTO UserStock(userid,stock_code, count) VALUES('asdf2','A004020', 2);

update StockCode set stock_code = 'asdf' where stock_name = '삼성전자';

DELETE FROM StockCode WHERE stock_name = '삼성전자';
DELETE FROM UserData WHERE userid=2;
DELETE FROM UserData;


#검색
select * from Dictionary;
select * from MacroeconomicIndicators;
select * from StockData;
select * from StockCode;
select * from UserData;
select * from UserStock;
select * from ModelResult;
select * from AIRate;
select * from AIFunds;
select * from Message;
select * from Comment;


select user_name from UserData where UserData.userid = "kcj98";

#외래키 지정
alter table StockData add foreign key(stock_code) references StockCode(stock_code) on update cascade on delete cascade; #StockCode.stock_code -> StockData.stock_code : stockdata_ibfk_1
alter table UserStock add foreign key(stock_code) references StockCode(stock_code) on update cascade on delete cascade; #UserStock.stock_code -> StockData.stock_code : userstock_ibfk_1
alter table UserStock add foreign key(userid) references UserData(userid) on update cascade on delete cascade; #UserStock.userid -> UserData.userid : userstock_ibfk_2
alter table ModelResult add foreign key(stock_code) references StockCode(stock_code) on update cascade on delete cascade; #ModelResult.stock_code -> StockCode.stock_code : modelresult_ibfk_1
alter table Message add foreign key(userid) references UserData(userid) on update cascade on delete cascade; #Message.userid -> UserData.userid : message_ibfk_1
alter table Comment add foreign key(userid) references UserData(userid) on update cascade on delete cascade; #Comment.userid -> UserData.userid : comment_ibfk_1
alter table Comment add foreign key(message_id) references Message(message_id) on update cascade on delete cascade; #Comment.message_id -> Message.message_id :  comment_ibfk_2

#제약조건 확인(외래키 이름 확인용)
select * from information_schema.table_constraints where constraint_schema = 'stockai';
select * from information_schema.table_constraints where table_name = 'StockData';


#제약조건 삭제userdata
alter table UserStock drop foreign key userstock_ibfk_1;
ALTER TABLE UserData DROP PRIMARY KEY;

#컬럼이름변경
alter table Userstock change sum_stock_velue sum_stock_value bigint; #변경전 컬럼 이름, 변경후 컬럼 이름, 데이터타입
alter table AIRate change data_tiem date_time date;
