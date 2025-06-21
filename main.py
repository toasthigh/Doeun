import streamlit as st
import openai

# 페이지 설정
st.set_page_config(
    page_title="체조 챗봇",
    page_icon="🏃‍♂️"
)

st.title("🏃‍♂️ 증상별 체조 챗봇")

# API 키 입력 (환경 변수 우선 사용)
api_key = st.secrets.get("OPENAI_API_KEY", "")
if not api_key:
    api_key = st.text_input("OpenAI API Key를 입력하세요:", type="password")

# 증상 입력
symptom = st.text_input("어떤 증상이 있으신가요?", placeholder="예: 목이 뻐근해요, 어깨가 아파요")

if st.button("체조 추천받기"):
    if not api_key:
        st.error("OpenAI API 키를 먼저 입력해주세요.")
    elif not symptom:
        st.warning("증상을 입력해주세요.")
    else:
        try:
            with st.spinner("체조를 추천하고 있습니다..."):
                # OpenAI API 키 설정
                openai.api_key = api_key
                
                # ChatGPT API 호출
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",  # gpt-4 대신 더 안정적인 모델 사용
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
            st.info("API 키가 올바른지 확인해주세요.")
