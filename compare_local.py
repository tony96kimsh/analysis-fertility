'''
1. 출산율 그래프 그리기 
- fertility_local.csv
2. 전력 소비 그래프 그리기
- electricity_local
3. 그래프 모형 비교하여 연관성 확인하기
'''

import csv
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

import numpy as np

# plt.rcParams['font.family'] = 'AppleGothic'
# 폰트 설정 
## 컴파일 20초 정도 소요됨
font_candidates = ['Noto Sans CJK KR', 'AppleGothic', 'NanumGothic', 'Malgun Gothic']
available_fonts = set()

for fp in fm.findSystemFonts():
    try:
        name = fm.FontProperties(fname=fp).get_name()
        available_fonts.add(name)
    except Exception:
        continue

for font in font_candidates:
    if font in available_fonts:
        plt.rcParams['font.family'] = font
        print(f"사용 가능한 한글 폰트 설정됨: {font}")
        break
else:
    print("사용 가능한 한글 폰트를 찾지 못했습니다.")

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
        # elc_local_list.append(list(map(float, row[1:])))
        elc_local_list.append([float(x.replace(',', '')) for x in row[1:]])
'''
### list comprehension

elc_local_list.append([float(x.replace(',', '')) for x in row[1:]])
위 코드를 풀어쓰면,


converted = []
for x in row[1:]:
    no_comma = x.replace(',', '')    # 문자열에서 , 제거
    num = float(no_comma)            # 실수로 변환
    converted.append(num)

elc_local_list.append(converted)
'''

for i in range(0, len(ftt_local_list)) :    
    plt.plot(h_elc_year, elc_local_list[i], label=local_name[i])
plt.title("지역별 전기 소비")
plt.legend()
plt.show()            


for i in range(0, len(ftt_local_list)) :    
    plt.plot(ftt_local_term, ftt_local_list[i], label=local_name[i])
plt.title("지익별 출산율")
plt.legend()
plt.show()

'''상관계수 막대 그래프'''
# 1. 출산율 리스트에서 연도 2011~2020 구간만 잘라내기
ftt_local_list_cut = []
for row in ftt_local_list:
    cut_row = []
    for i in range(11, 21):  # 2011~2020에 해당하는 인덱스
        cut_row.append(row[i])
    ftt_local_list_cut.append(cut_row)

# 2. None 값을 NaN으로 바꾸기
for i in range(len(ftt_local_list_cut)):
    for j in range(len(ftt_local_list_cut[i])):
        if ftt_local_list_cut[i][j] is None:
            ftt_local_list_cut[i][j] = np.nan

# 3. 각 지역별 출산율과 전기소비 간의 상관계수 계산
correlations = []

for fert, elec in zip(ftt_local_list_cut, elc_local_list):
    fert_arr = np.array(fert)
    elec_arr = np.array(elec)

    # NaN이 아닌 값들만 골라내는 마스크
    mask = ~np.isnan(fert_arr)

    if np.any(mask):  # 유효한 값이 하나라도 있으면
        corr = np.corrcoef(fert_arr[mask], elec_arr[mask])[0, 1]
        correlations.append(corr)
    else:
        correlations.append(np.nan)
# 상관계수 막대그래프
plt.figure(figsize=(12, 6))
plt.bar(local_name, correlations)
plt.xticks(rotation=90)
plt.title("지역별 출산율과 전기 소비 상관계수 (2011~2020)")
plt.ylabel("상관계수")
plt.tight_layout()
plt.show()
