import streamlit as st
import json
import os

# 페이지 기본 설정
st.set_page_config(page_title="로아 공대 대시보드", layout="wide")
st.title("⚔️ 로아 공대 실시간 현황판")

# 데이터 파일 읽기 (기존 봇이 저장한 파일)
if os.path.exists("raid_data.json"):
    with open("raid_data.json", "r", encoding="utf-8") as f:
        char_data = json.load(f)
    
    # 1. 요약 정보
    total_chars = len(char_data)
    st.metric("총 신청 캐릭터 수", f"{total_chars} 캐릭")

    # 2. 레이드별 현황 (표 형식)
    st.subheader("📋 전체 캐릭터 명단")
    st.table([{"캐릭터명": n, "레벨": d['level'], "서포터": "✅" if d['is_sup'] else "⚔️"} 
              for n, d in char_data.items()])
else:
    st.warning("데이터 파일(raid_data.json)을 찾을 수 없습니다. 봇에서 먼저 신청을 진행해주세요.")