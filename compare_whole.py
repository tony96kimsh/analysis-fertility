import csv
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib
import numpy as np

# 한글 및 마이너스 기호 깨짐 방지 설정
plt.rcParams['font.family'] = 'AppleGothic'
matplotlib.rcParams['axes.unicode_minus'] = False

# 연도, 출산율, 에너지 소비 데이터를 저장할 리스트 초기화
years = []         # 연도 리스트
fertility = []     # 전국 출산율 리스트
energy = []        # 전국 에너지 소비량 리스트 (1인당 기준)

# -------------------------------
# 1. 전국 출산율 데이터 읽기
# -------------------------------
with open('./csv/fertility_whole.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # 헤더 제거
    for row in reader:
        try:
            year = row[0]
            rate = float(row[1])
            years.append(year)
            fertility.append(rate)
        except ValueError:
            continue

# -------------------------------
# 2. 전국 에너지 소비 데이터 읽기 (가로 구조)
# -------------------------------
with open('./csv/energy_total.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        if row[0].strip().startswith("1인당 에너지소비량"):
            for val in row[2:]:  # 첫 두 열은 항목명이므로 제외
                try:
                    energy.append(float(val))
                except ValueError:
                    continue
            break

# -------------------------------
# 3. 연도/출산율 슬라이싱 (1981~2020)
# -------------------------------
years = years[11:51]         # 1981~2020 (40개)
fertility = fertility[11:51] # 같은 범위 슬라이싱

# -------------------------------
# 4. 출산율과 에너지 소비 추이 그래프 (보조 축 적용)
# -------------------------------
min_len = min(len(fertility), len(energy))
years = years[:min_len]
fertility = fertility[:min_len]
energy = energy[:min_len]

fig, ax1 = plt.subplots(figsize=(10, 5))

# 첫 번째 Y축 (출산율)
ax1.plot(years, fertility, 'b-o', label='출생아 수')
ax1.set_xlabel('연도')
ax1.set_ylabel('출생아 수(명)', color='b')
ax1.tick_params(axis='y', labelcolor='b')

# 두 번째 Y축 (에너지 소비)
ax2 = ax1.twinx()
ax2.plot(years, energy, 'r-s', label='1인당 에너지 소비량')
ax2.set_ylabel('1인당 에너지 소비량 (toe)', color='r')
ax2.tick_params(axis='y', labelcolor='r')

# 제목 & 레이아웃
plt.title('전국 출생아 수와 1인당 에너지 소비량 추이')
fig.tight_layout()
plt.show()

# -------------------------------
# 5. 출산율과 에너지 소비 상관계수 출력
# -------------------------------
fertility_arr = np.array(fertility)
energy_arr = np.array(energy)

if len(fertility_arr) >= 2 and len(energy_arr) >= 2:
    corr = np.corrcoef(fertility_arr, energy_arr)[0, 1]
else:
    corr = 0

print(f"1981년부터 2020년까지, 총 40년간의 전국 출산율과 에너지 소비의 상관계수: {corr:.2f}")
