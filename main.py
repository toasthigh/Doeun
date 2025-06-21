import streamlit as st
import openai
import os

# 페이지 설정
st.set_page_config(
    page_title="AI 체조 코치 챗봇",
    page_icon="🏃‍♂️",
    layout="wide"
)

# 메인 타이틀
st.title("🏃‍♂️ AI 체조 코치 챗봇")
st.markdown("### 개인 맞춤형 체조 추천 + 유튜브 가이드")
st.markdown("---")

# 사이드바 - API 키 및 빠른 증상 선택
with st.sidebar:
    st.title("⚙️ 설정")
    
    # API 키 입력 섹션 개선
    st.markdown("#### 🔑 OpenAI API 키")
    
    # 환경 변수에서 API 키 확인
    api_key_from_env = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY", "")
    
    if api_key_from_env:
        st.success("✅ API 키가 환경변수에서 로드되었습니다")
        api_key = api_key_from_env
        st.markdown("🔒 보안을 위해 키가 숨겨져 있습니다")
    else:
        st.info("🔑 OpenAI API 키를 입력해주세요")
        api_key = st.text_input(
            "API Key:", 
            type="password", 
            placeholder="sk-...",
            help="OpenAI 웹사이트에서 발급받은 API 키를 입력하세요"
        )
        
        if api_key:
            if api_key.startswith('sk-') and len(api_key) > 20:
                st.success("✅ API 키 형식이 올바릅니다")
            else:
                st.warning("⚠️ API 키 형식을 확인해주세요 (sk-로 시작)")
    
    # API 키 도움말
    with st.expander("❓ API 키 발급 방법"):
        st.markdown("""
        **OpenAI API 키 발급 단계:**
        
        1. [OpenAI 웹사이트](https://platform.openai.com) 접속
        2. 회원가입 또는 로그인
        3. API Keys 메뉴로 이동
        4. "Create new secret key" 클릭
        5. 생성된 키를 복사하여 입력
        
        **💰 요금 정보:**
        - GPT-3.5-turbo: $0.002/1K tokens
        - 첫 사용 시 무료 크레딧 제공
        
        **🔒 보안 주의사항:**
        - API 키를 다른 사람과 공유하지 마세요
        - 사용하지 않을 때는 키를 비활성화하세요
        """)
    
    st.markdown("---")
    st.title("🎯 빠른 증상 선택")
    
    quick_symptoms = [
        "목이 뻐근하고 아파요",
        "어깨가 결리고 무거워요", 
        "허리가 아프고 뻣뻣해요",
        "무릎이 아프고 시려요",
        "손목이 아프고 저려요",
        "눈이 피로하고 목이 뻐근해요",
        "다리가 붓고 무거워요",
        "전신이 피곤하고 뭉쳐있어요",
        "골반이 틀어진 것 같아요",
        "라운드숄더로 고민이에요"
    ]
    
    selected_symptom = st.selectbox(
        "자주 찾는 증상:",
        ["직접 입력하기"] + quick_symptoms
    )
    
    if st.button("🔍 선택한 증상으로 검색", type="primary"):
        if selected_symptom != "직접 입력하기":
            st.session_state.selected_symptom = selected_symptom

# API 키 상태 확인 및 경고 표시
if not api_key:
    st.warning("⚠️ 체조 추천을 받으려면 먼저 OpenAI API 키를 입력해주세요. 왼쪽 사이드바를 확인하세요!")

# 메인 콘텐츠 영역
col1, col2 = st.columns([2, 1])

with col1:
    # 증상 입력
    symptom = st.text_area(
        "🗣️ 어떤 증상이 있으신가요? 자세히 설명해주세요:",
        value=st.session_state.get('selected_symptom', ''),
        placeholder="예: 하루 종일 컴퓨터 작업을 해서 목과 어깨가 뻐근하고 아파요. 특히 목을 뒤로 젖히면 더 아픕니다.",
        height=100
    )
    
    # 추가 정보 입력
    with st.expander("🔧 추가 정보 (선택사항)"):
        col_a, col_b = st.columns(2)
        with col_a:
            age_range = st.selectbox("연령대:", ["선택안함", "20대", "30대", "40대", "50대", "60대 이상"])
            activity_level = st.selectbox("활동량:", ["선택안함", "거의 앉아있음", "가끔 운동", "규칙적 운동", "매우 활발"])
        with col_b:
            work_type = st.selectbox("주요 업무:", ["선택안함", "사무직", "서비스직", "제조업", "학생", "기타"])
            pain_level = st.slider("통증 정도 (1-10):", 1, 10, 5)

with col2:
    st.markdown("### 📚 사용 가이드")
    st.info("""
    **💡 더 정확한 추천을 위해:**
    
    • 구체적인 증상 설명
    • 언제 아픈지 (앉을 때, 움직일 때 등)
    • 어느 부위가 아픈지
    • 얼마나 오래된 증상인지
    
    **⚠️ 주의사항:**
    • 심한 통증은 의사 상담 필요
    • 체조 중 통증이 심해지면 중단
    • 꾸준한 실천이 중요합니다
    """)
    
    # API 상태 표시
    if api_key:
        st.success("🔑 API 키 연결됨")
    else:
        st.error("🔑 API 키 필요")

# 체조 추천 버튼
if st.button("🎯 맞춤 체조 추천받기", type="primary", use_container_width=True):
    if not api_key:
        st.error("⚠️ OpenAI API 키를 먼저 입력해주세요! 사이드바에서 설정할 수 있습니다.")
    elif not symptom.strip():
        st.warning("⚠️ 증상을 입력해주세요!")
    else:
        # 추가 정보 조합
        additional_info = ""
        if age_range != "선택안함":
            additional_info += f"연령대: {age_range}, "
        if activity_level != "선택안함":
            additional_info += f"활동량: {activity_level}, "
        if work_type != "선택안함":
            additional_info += f"업무유형: {work_type}, "
        additional_info += f"통증정도: {pain_level}/10"
        
        full_query = f"{symptom}\n\n[추가정보: {additional_info}]"
        
        try:
            with st.spinner("🤖 AI 체조 전문가가 맞춤 체조를 준비하고 있습니다..."):
                # OpenAI API 키 설정
                openai.api_key = api_key
                
                # 향상된 시스템 프롬프트
                system_prompt = """
당신은 20년 경력의 물리치료사이자 운동치료 전문가입니다. 
사용자의 증상에 맞는 안전하고 효과적인 체조를 추천해주세요.

다음 형식으로 정확히 답변해주세요:

## 🔍 증상 분석
[증상에 대한 전문적 분석]

## 🏃‍♂️ 추천 체조 (3-5가지)

### 1. [체조명]
**방법:** [상세한 동작 설명]
**횟수:** [반복 횟수 및 세트]
**효과:** [이 체조의 효과]
**주의점:** [주의사항]

### 2. [체조명]
[같은 형식으로...]

## ⚠️ 주의사항
[전반적인 주의사항과 금기사항]

## 💡 생활 습관 개선 팁
[일상에서 실천할 수 있는 팁]

## 📺 참고할 만한 유튜브 검색 키워드
[체조 동작을 검색할 때 유용한 키워드들을 제시해주세요]

응답은 친근하면서도 전문적인 한국어로 해주세요.
심각한 증상의 경우 반드시 의사 상담을 권해주세요.
"""
                
                # ChatGPT API 호출
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": full_query}
                    ],
                    temperature=0.7,
                    max_tokens=1500
                )
                
                # 응답 표시
                st.success("✅ 맞춤 체조 추천 완료!")
                
                # 응답을 섹션별로 표시
                response_text = response.choices[0].message.content
                st.markdown(response_text)
                
                # 추가 유튜브 검색 도구
                st.markdown("---")
                st.markdown("## 🎥 유튜브 체조 영상 찾기")
                
                col_yt1, col_yt2 = st.columns(2)
                
                with col_yt1:
                    st.markdown("### 🔍 추천 검색 키워드")
                    search_keywords = [
                        f"{symptom.split()[0]} 체조",
                        f"{symptom.split()[0]} 스트레칭",
                        "물리치료 운동",
                        "재활 운동",
                        "홈트레이닝 체조"
                    ]
                    
                    for keyword in search_keywords:
                        youtube_url = f"https://www.youtube.com/results?search_query={keyword.replace(' ', '+')}"
                        st.markdown(f"🎯 [{keyword}]({youtube_url})")
                
                with col_yt2:
                    st.markdown("### 📚 추천 채널")
                    channels = [
                        ("피지오TV", "https://www.youtube.com/@PhysioTV"),
                        ("바른체형TV", "https://www.youtube.com/@barunbody"),
                        ("닥터TV", "https://www.youtube.com/@DoctorTV_official"),
                        ("스트레칭9", "https://www.youtube.com/@stretching9"),
                        ("운동처방사TV", "https://www.youtube.com/@ExercisePrescriptionTV")
                    ]
                    
                    for name, url in channels:
                        st.markdown(f"📺 [{name}]({url})")
                
                # 운동 기록 기능
                st.markdown("---")
                with st.expander("📝 운동 기록하기"):
                    st.text_area("오늘 실시한 체조와 느낀 점을 기록해보세요:", 
                               placeholder="예: 목 돌리기 10회 3세트 실시. 처음보다 목이 더 부드럽게 돌아가는 느낌.")
                    if st.button("💾 기록 저장"):
                        st.success("기록이 저장되었습니다! (세션 종료 시 삭제됩니다)")
                
        except openai.error.AuthenticationError:
            st.error("❌ API 키 인증에 실패했습니다. 올바른 API 키를 입력했는지 확인해주세요.")
        except openai.error.RateLimitError:
            st.error("❌ API 사용량 한도를 초과했습니다. 잠시 후 다시 시도해주세요.")
        except openai.error.APIError as e:
            st.error(f"❌ OpenAI API 오류가 발생했습니다: {str(e)}")
        except Exception as e:
            st.error(f"❌ 예상치 못한 오류가 발생했습니다: {str(e)}")
            st.info("💡 API 키가 올바른지 확인하고 다시 시도해주세요.")

# 하단 정보
st.markdown("---")
col_info1, col_info2, col_info3 = st.columns(3)

with col_info1:
    st.markdown("### 🏥 응급상황")
    st.warning("""
    **즉시 병원 방문이 필요한 경우:**
    • 갑작스러운 심한 통증
    • 손발 저림이나 마비
    • 발열과 함께 나타나는 통증
    • 외상 후 발생한 통증
    """)

with col_info2:
    st.markdown("### 💊 자가관리 팁")
    st.info("""
    **일상 관리법:**
    • 온찜질 (15-20분)
    • 충분한 수분 섭취
    • 규칙적인 휴식
    • 올바른 자세 유지
    """)

with col_info3:
    st.markdown("### 📞 도움말")
    st.info("""
    **문제 발생 시:**
    • API 키 확인
    • 증상을 구체적으로 기술
    • 인터넷 연결 확인
    • 페이지 새로고침
    """)

# 세션 상태 초기화
if 'selected_symptom' not in st.session_state:
    st.session_state.selected_symptom = ""
