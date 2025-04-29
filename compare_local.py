'''
1. 출산율 그래프 그리기 
- fertility_local.csv
2. 전력 소비 그래프 그리기
- electricity_local
3. 그래프 모형 비교하여 연관성 확인하기
'''

import csv
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Malgun Gothic'

ftt_local_list = [] 
ftt_local = []
local_name = []
ftt_local_term = []
local_list = []

with open('./csv/fertility_local.csv', 'r', encoding="UTF-8") as f:
    reader = csv.reader(f)

    # 위 3줄 제목 (연도, 분류, 전국)
    h_ftt_year = next(reader)
    h_kind = next(reader)
    h_kor = next(reader)
    
    # 연도 리스트
    temp = list(h_ftt_year)
    for i in range(0, len(temp)):
        if (i * 2) + 1 < len(temp):
           ftt_local_term.append(temp[ (i * 2) + 1])
    
    data = list(reader)
    
    #출산율 리스트 (지역별 이중 리스트 생성)
    for row in data:
        local_list.append(row[0])
        ftt_local = []

        # 지역명 리스트 삽업 
        local_name.append(row[0])
        
        for i in range(1, len(row)):
            #출산율만 리스트 삽입
            if (2 * i) < len(row):
                if row[ 2 * i ] != '-':
                    ftt_local.append(float(row[ 2 * i ]))
                else:
                    ftt_local.append(None)
        # 지역 구분
        ftt_local_list.append(ftt_local)


elc_local_list = [] 
elc_local_term = []
h_elc_year = []

# 지역별 전기 사용량
with open('./csv/electricity_local.csv', 'r', encoding="UTF-8") as f:
    reader = csv.reader(f)
    # 헤더 제거 및 자료 기간 저장
    h_elc_year = next(reader)[1:]    
    data = list(reader)

    # 값 저장
    for row in data:
        elc_local_list.append(list(map(float, row[1:])))        

plt.plot(h_elc_year, elc_local_list[0], label=local_name[0])
plt.show()


            


'''
for i in range(0, len(ftt_local_list)) :    
    plt.plot(ftt_local_term, ftt_local_list[i], label=local_name[i])
plt.legend()
plt.show()

'''