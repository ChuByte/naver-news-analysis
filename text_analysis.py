# 기사 요약 텍스트 분석


import requests
import json
import pandas as pd
import re  # HTML 태그 제거용

# 네이버 API 키
CLIENT_ID = "D56ninQpGKqRvNqWzcGK"
CLIENT_SECRET = "al1Y20SreN"

# 검색할 키워드
query = "다이소 건기식"

# API 요청 URL
url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display=5"

# API 요청 헤더 설정
headers = {
    "X-Naver-Client-Id": CLIENT_ID,
    "X-Naver-Client-Secret": CLIENT_SECRET
}

# 요청 보내기
response = requests.get(url, headers=headers)
news_data = response.json()

# 뉴스 데이터를 리스트로
news_list = []
for item in news_data['items']:
    title = item['title']  # 제목
    description = item['description']  # 기사 요약
    link = item['link']  # 링크
    news_list.append([title, description, link])

# pandas DataFrame 생성
df = pd.DataFrame(news_list, columns=["제목", "요약", "링크"])




import re

def clean_text(text):
    pattern = r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)' # E-mail제거
    text = re.sub(pattern, '', text)
    pattern = r'(http|ftp|clean_texthttps)://(?:[-\w.]|(?:%[\da-fA-F]{2}))+' # URL제거
    text = re.sub(pattern, '', text)
    pattern = '([ㄱ-ㅎㅏ-ㅣ]+)'  # 한글 자음, 모음 제거
    text = re.sub(pattern, '', text)
    pattern = '([a-zA-Z0-9]+)'   # 알파벳, 숫자 제거
    text = re.sub(pattern, '', text)
    pattern = '<[^>]*>'         # HTML 태그 제거
    text = re.sub(pattern, '', text)
    pattern = r'[^\w\s]'         # 특수기호제거
    text = re.sub(pattern, '', text)
    return text


df["제목"] = df["제목"].apply(clean_text)
df["요약"] = df["요약"].apply(clean_text)

# 정리된 데이터 출력
print(df.head())

df.to_csv("naver_news_clean.csv", index=False, encoding="utf-8-sig")
print("뉴스 데이터 'naver_news_clean.csv' 파일로 저장됨!")


from collections import Counter
import pandas as pd
import re

# 저장된 뉴스 데이터 불러오기
df = pd.read_csv("naver_news_clean.csv")

# 모든 기사 요약을 하나의 문자열로 합치기
all_summary_text = " ".join(df["요약"])

# 한글 단어만 추출하는 정규 표현식 적용
words = re.findall(r"[가-힣]+", all_summary_text)

# 단어별 등장 횟수 계산
word_counts = Counter(words)

# 상위 10개 단어 출력
print("◼️ 가장 많이 등장한 단어 TOP 5:", word_counts.most_common(5))




# 불용어 리스트 추가
stopwords = ["대해","따라","것", "를","대한","용", "있는", "과","들","들에게","한다", "위한", "등", "수", "및", "이번", "에서", "하고","것으로", "의", "에", "도", "은","는","이","가","까지","을"]

# 특정 단어 뒤에 조사가 붙은 경우 제거
filtered_words = []
for word in words:
    for stopword in stopwords:
        if word.endswith(stopword):  # 단어가 조사로 끝나면 제거
            word = word[:-len(stopword)]
    if len(word) > 1:  # 빈 문자열 & 1글자 단어 제거
        filtered_words.append(word)


# 단어 빈도수 다시 계산
filtered_word_counts = Counter(filtered_words)

# 상위 10개 단어 출력
print("🔹 불용어 제거 후 가장 많이 등장한 단어 TOP 5:", filtered_word_counts.most_common(5))


import matplotlib.pyplot as plt
from matplotlib import rc

# Mac 한글 폰트 설정
rc('font', family='AppleGothic')

# 가장 많이 등장한 단어 5개 선택
top_words = filtered_word_counts.most_common(5)
words, counts = zip(*top_words)

# 그래프 생성
plt.figure(figsize=(10, 5))
plt.bar(words, counts, color="yellowgreen")
plt.xlabel("단어")
plt.ylabel("빈도수")
plt.title("뉴스 기사에서 가장 많이 등장한 단어 (조사 제거)")
plt.xticks(rotation=45)
plt.show()



from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib import rc
from collections import Counter

# Mac 한글 폰트 설정 (AppleGothic)
rc('font', family='AppleGothic')

# 단어 빈도 데이터 준비 (조사 제거된 단어들)
word_freq = Counter(filtered_words)

# 워드클라우드 생성
wordcloud = WordCloud(
    font_path="/System/Library/Fonts/Supplemental/AppleGothic.ttf",  # Mac 한글 폰트
    background_color="white",
    width=800,
    height=400
).generate_from_frequencies(word_freq)

# 워드클라우드 표시
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")  # 축 제거
plt.show()




from soynlp.tokenizer import RegexTokenizer
from collections import Counter

# 🔹 한글 토크나이저 사용
tokenizer = RegexTokenizer()

# 🔹 감성 사전 확장 (더 많은 긍정 & 부정 단어 추가)
positive_words = [
    "좋다", "훌륭", "최고", "긍정적", "기쁨", "만족", "행복", "추천", "사랑", "최상", "완벽", "멋지다",
    "고맙다", "감사", "최고다", "뛰어나다", "기대", "즐겁다", "소중", "좋아요", "행운", "사랑스럽다"
]
negative_words = [
    "나쁘다", "최악", "불만", "실망", "짜증", "화남", "슬픔", "실패", "끔찍", "불편", "비효율", "절망",
    "악몽", "분노", "고통", "형편없다", "두렵다", "짜증난다", "피곤", "불쾌", "짜증스러움", "악재"
]


# 🔹 감성 점수 계산 함수 (확장된 감성 사전 사용)
def sentiment_score(text):
    tokens = tokenizer.tokenize(text)  # 문장 토큰화
    pos_count = sum(1 for word in tokens if word in positive_words)
    neg_count = sum(1 for word in tokens if word in negative_words)

    # 감성 점수 계산 (긍정 단어 개수 - 부정 단어 개수)
    return pos_count - neg_count


# 🔹 감성 점수 적용
df["감성 점수"] = df["요약"].apply(sentiment_score)

# 🔹 감성 점수 확인
print(df[["요약", "감성 점수"]].head())


import matplotlib.pyplot as plt

# 🔹 긍정, 부정, 중립 뉴스 개수 계산
positive_count = (df["감성 점수"] > 0).sum()
negative_count = (df["감성 점수"] < 0).sum()
neutral_count = (df["감성 점수"] == 0).sum()

# 🔹 파이 차트 시각화
labels = ["긍정 뉴스", "부정 뉴스", "중립 뉴스"]
counts = [positive_count, negative_count, neutral_count]

plt.figure(figsize=(7, 7))
plt.pie(counts, labels=labels, autopct="%1.1f%%", colors=["lightblue", "salmon", "lightgray"])
plt.title("네이버 뉴스 감성 분석 결과")
plt.show()


