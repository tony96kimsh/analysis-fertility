'''
1. 출산율 그래프 그리기 
- fertility_local.csv
2. 전력 소비 그래프 그리기
- electricity_local
3. 그래프 모형 비교하기
'''

import csv
import matplotlib.pyplot as plt

start_year = 2000
ftt_local_list = [] 
ftt_local = []
ftt_local_term = []
local_list = []

with open('./csv/fertility_local.csv', 'r', encoding="UTF-8") as f:
    reader = csv.reader(f)

    # 위 3줄 제목 (연도, 분류, 전국)
    h_year = next(reader)
    h_kind = next(reader)
    h_kor = next(reader)
    
    # 연도 리스트
    temp = list(h_year)
    for i in range(0, len(temp)):
        if (i * 2) + 1 < len(temp):
           ftt_local_term.append(temp[ (i * 2) + 1])
    
    data = list(reader)
    
    #출산율 리스트
    for row in data:
        local_list.append(row[0])
        ftt_local = []
        for i in range(1, len(row)):
            if (2 * i) < len(row):
                if row[ 2 * i ] != '-':
                    ftt_local.append(float(row[ 2 * i ]))
                else:
                    ftt_local.append(None)
        # 지역 구분
        ftt_local_list.append(ftt_local)

for i in range(0, len(ftt_local_list)) :    
    plt.plot(ftt_local_term, ftt_local_list[i])
    print(ftt_local_list[i])
plt.show()