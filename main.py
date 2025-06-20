#main.py

import streamlit as st
from openai import OpenAI

# 페이지 설정
st.set_page_config(
    page_title="체조 챗봇",
    page_icon="🏃‍♂️"
)

st.title("🏃‍♂️ 증상별 체조 챗봇")

# API 키 입력
api_key = st.text_input("OpenAI API Key를 입력하세요:", type="password")

if api_key:
    # 증상 입력
    symptom = st.text_input("어떤 증상이 있으신가요?", placeholder="예: 목이 뻐근해요, 어깨가 아파요")
    
    if st.button("체조 추천받기"):
        if symptom:
            try:
                # OpenAI 클라이언트 초기화
                client = OpenAI(api_key=api_key)
                
                # ChatGPT API 호출
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "너는 물리치료사이자 체조 전문가야. 사용자의 증상에 맞는 안전한 체조를 3-5가지 추천해줘. 각 체조마다 방법과 횟수, 주의사항을 포함해서 한국어로 친근하게 설명해줘."},
                        {"role": "user", "content": symptom}
                    ],
                    temperature=0.7,
                    max_tokens=500
                )
                
                # 응답 출력
                st.success("추천 체조:")
                st.write(response.choices[0].message.content)
                
            except Exception as e:
                st.error(f"오류가 발생했습니다: {str(e)}")
        else:
            st.warning("증상을 입력해주세요.")
else:
    st.info("OpenAI API 키를 입력해주세요.")
