import pandas as pd
import matplotlib.pyplot as plt

# 서울 인구수
population = pd.read_excel("202212_202212_연령별인구현황_월간.xlsx", engine='openpyxl', skiprows=3)

population_dict = {}
# [0] 총 인구 수
# [1] 남자인구수
# [2] 여자인구수

for index, row in population.iterrows():
    if row['행정기관'] and row['남 인구수'] and row['여 인구수']:
        population_dict[row['행정기관']] = [row["총 인구수"], row['남 인구수'], row['여 인구수']]

seoul_population_dict = {}

for key, value in population_dict.items():
    if "서울" in key:
        seoul_population_dict[key.split(" ")[1]] = value

print("seoul_population_dict.items()")
for key, value in seoul_population_dict.items():
    print(key, value)


# 서울 강력범죄 발생수
seoul_crime = pd.read_csv("22년_서울_5대+범죄+발생현황_20241008101408.csv", skiprows=3)

seoul_crime_dict = {}

for row in seoul_crime.iterrows():
    seoul_crime_dict[row[1]["자치구별(2)"]] = row[1]["발생"]

print("seoul_crime.iterrows()")
print(seoul_crime_dict)




# 지역명 배열
seoul_region_name = list(seoul_population_dict.keys())

# 서울 지역별 범죄율
seoul_crime_rate = {}

# 범죄율 계산 공식 (1만명 당 범죄 건수)
# 범죄율 = (범죄 발생 건수 / 인구수) * 10000
for name in seoul_region_name:
    # 지역 이름이 존재 하면
    if name:
        population = int(seoul_population_dict[name][0].replace(",", ""))
        rate = ( seoul_crime_dict[name] / population ) * 10000

        seoul_crime_rate[name] = round(rate, 2)

# 선진국의 일반 범죄율: 일반적으로 10만 명당 200 ~ 500건 내외
# 범죄가 높은 지역: 10만 명당 1,000건 이상
print("10000명당 범죄 건수")
print(seoul_crime_rate)



# 서울 유흥업소 신고 내역
# 스텐드바, 룸살롱, 노래클럽 등 주로 주류와 함께 음식류를 조리 및 판매하는 곳으로 유흥종사자를 두거나 유흥시설을 설치하여 운영하는 업소정보
data = pd.read_csv("서울시_유흥주점영업_인허가_정보.csv")

seoul_red_light_zone = {}

for name in seoul_region_name:
    if name and name not in "":
        seoul_red_light_zone[name] = 0

for row in data.iterrows():
    if row[1]["지번주소"] and type(row[1]["지번주소"]) == str and row[1]["상세영업상태명"] == "영업":
        # print(row[1]["지번주소"])
        region_name = row[1]["지번주소"].split(" ")[1]
        seoul_red_light_zone[region_name] = seoul_red_light_zone[region_name] + 1

print("seoul_red_light_zone")
print(seoul_red_light_zone)


region = seoul_crime_rate.keys()
crime_rate = seoul_crime_rate.values()
red_light_zone = seoul_red_light_zone.values()

# 한글 글꼴
plt.rcParams["font.family"] = "Pretendard"

plt.figure(figsize=(15, 5))

plt.title("서울 1만 명당 강력 범죄 건수 및 유흥 업소")
plt.bar(region, crime_rate, color="lightblue", label="범죄 건수")
plt.plot(red_light_zone, color='red', marker='o', label="유흥 업소")

plt.xlabel("지역명")
plt.xticks(rotation=45)  # 회전 및 간격 조정

plt.grid(True)
plt.legend()
plt.show()