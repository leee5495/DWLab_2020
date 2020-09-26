# Pattern Classification Model for Traffic Data including Missing Values 실험 결과

### 실험 데이터 설명
- 다저스타디움과 거리가 가까운 101 North freeway에서 5분마다 교통량이 측정되어 하루 288개의 원소로 구성되어 있는 데이터 사용
- 데이터가 측정된 날짜와 다저스타디움의 경기 일자를 비교해 다저스 경기 여부의 레이블을 지정하고 각 레이블을 분류하는 모델 설계

  ![image](https://user-images.githubusercontent.com/39192405/93020209-c8fda180-f616-11ea-9221-4b1e169d5da5.png)

##
### 시계열 교통량 데이터를 이용해 야구 경기장에서 경기가 개최되었는지 분류 
![image](https://user-images.githubusercontent.com/39192405/93021618-84760400-f61e-11ea-815a-61b6173f836f.png)

- 분류 실험 결과, 제안한 어텐션 메커니즘이 분류 정확도를 높이는 것을 보였다

##
### 추가연도의 데이터를 이용해 손실 데이터 유무에 따른 교통량 데이터 분류 성능 비교
![image](https://user-images.githubusercontent.com/39192405/93021578-58f31980-f61e-11ea-8126-a0ad990bcd67.png)

- 결측값이 포함된 데이터의 경우 어텐션 메커니즘이 적용되었을 때 정확도가 향상되는 것을 확인할 수 있다. 
- 결측값이 없는 경우에도 대부분 어텐션 메커니즘이 있는 경우의 성능이 더 높은 것을 볼 수 있다.
