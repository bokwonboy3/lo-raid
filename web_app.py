import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="로아 공대 전략 보드", layout="wide")
st.title("🛡️ 요일별 24시간 가동 인원 타임라인")

def load_data():
    if os.path.exists("raid_data.json"):
        with open("raid_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

data = load_data()

if data:
    # 1. 데이터 정밀 가공 (카테고리화)
    records = []
    # 00시~23시까지의 모든 라벨 생성
    all_times = [f"{i:02d}시" for i in range(24)]
    
    for char_name, info in data.items():
        scheds = info.get('schedules', {})
        if scheds:
            # 첫 번째 레이드 일정 기준
            first_raid = list(scheds.keys())[0]
            for s in scheds[first_raid]:
                if '/' in s:
                    day, time_str = s.split('/')
                    records.append({
                        "요일": day,
                        "시간대": time_str, 
                        "캐릭터명": char_name,
                        "인원": 1
                    })

    if records:
        df = pd.DataFrame(records)
        
        # 2. [핵심] X축 24시간 고정 적층형 그래프
        st.subheader("📊 24시간 타임라인 분석 (막대가 높을수록 사람 많음)")
        
        day_order = ["수", "목", "금", "토", "일", "월", "화", "상관없음"]
        
        # 요일별로 섹션을 나누어 가독성 극대화
        fig = px.bar(
            df, 
            x="시간대", 
            y="인원", 
            color="캐릭터명",
            facet_row="요일", # 요일별 독립 층 구성
            category_orders={"요일": day_order, "시간대": all_times}, # X축 00-23시 고정
            color_discrete_sequence=px.colors.qualitative.Pastel,
            height=900 # 요일이 많으므로 높이를 충분히 확보
        )

        fig.update_layout(
            barmode='stack', # 위아래로 쌓기
            showlegend=True,
            xaxis=dict(tickangle=0), # 시간 라벨 똑바로 보기
            margin=dict(t=50, b=50, l=100, r=50)
        )

        # 요일 라벨 가독성 (오른쪽 '요일=수' -> '수요일'로 변경)
        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1] + "요일"))
        # 모든 층의 X축을 00시-23시로 통일
        fig.update_xaxes(showticklabels=True, title_text="")
        
        st.plotly_chart(fig, use_container_width=True)

    # 3. 상세 일정 리스트
    st.divider()
    st.subheader("📋 공대원별 세부 일정")
    char_list = []
    for name, info in data.items():
        scheds = info.get('schedules', {})
        time_text = ", ".join(scheds[list(scheds.keys())[0]]) if scheds else "미신청"
        char_list.append({
            "이름": name, "레벨": info.get('level', '0'), 
            "직업": "서포터" if info.get('is_sup') else "딜러", "가능 시간": time_text
        })
    st.table(pd.DataFrame(char_list))

else:
    st.warning("데이터가 아직 없습니다. 디스코드에서 신청을 먼저 진행해 주세요!")
