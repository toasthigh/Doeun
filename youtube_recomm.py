import streamlit as st
import openai

# 페이지 설정
st.set_page_config(
    page_title="유튜브 & 팟캐스트 추천 챗봇",
    page_icon="📺",
    layout="wide"
)

# 메인 타이틀
st.title("📺 유튜브 & 팟캐스트 추천 챗봇")
st.markdown("### 당신의 관심사에 맞는 채널을 찾아드려요!")
st.markdown("---")

# 사이드바
with st.sidebar:
    st.title("⚙️ 설정")
    
    # 간단한 API 키 입력
    st.markdown("#### API Key 입력")
    api_key = st.text_input("OpenAI API Key:", type="password", placeholder="sk-...")
    
    st.markdown("---")
    st.title("🎯 관심 분야")
    
    categories = [
        "직접 입력하기",
        "🏃‍♂️ 운동/헬스/체조",
        "🍳 요리/레시피",
        "💼 비즈니스/자기계발", 
        "🎨 예술/창작",
        "💻 IT/프로그래밍",
        "📚 교육/학습",
        "🎵 음악/엔터테인먼트",
        "🧘‍♀️ 명상/힐링",
        "💰 투자/재테크",
        "🌍 여행/문화",
        "🎮 게임/취미",
        "👶 육아/교육",
        "🏠 인테리어/DIY",
        "🐕 반려동물",
        "📖 독서/책리뷰"
    ]
    
    selected_category = st.selectbox("카테고리 선택:", categories)
    
    if st.button("🔍 선택한 분야로 검색", type="primary"):
        if selected_category != "직접 입력하기":
            st.session_state.selected_category = selected_category

# 메인 콘텐츠 영역
col1, col2 = st.columns([2, 1])

with col1:
    # 관심사 입력
    interest = st.text_area(
        "🎯 어떤 채널을 찾고 계신가요? 관심사를 자세히 알려주세요:",
        value=st.session_state.get('selected_category', ''),
        placeholder="예: 집에서 할 수 있는 간단한 홈트레이닝 영상을 찾고 있어요. 초보자도 따라할 수 있는 것으로요.",
        height=100
    )
    
    # 추가 옵션
    with st.expander("🔧 세부 옵션"):
        col_a, col_b = st.columns(2)
        with col_a:
            platform = st.multiselect(
                "플랫폼 선택:", 
                ["유튜브", "팟캐스트", "네이버TV", "인스타그램"],
                default=["유튜브", "팟캐스트"]
            )
            difficulty = st.selectbox("난이도:", ["상관없음", "초보자용", "중급자용", "고급자용"])
        with col_b:
            language = st.selectbox("언어:", ["한국어", "영어", "상관없음"])
            duration = st.selectbox("영상 길이:", ["상관없음", "짧은 영상 (10분 이내)", "중간 길이 (10-30분)", "긴 영상 (30분 이상)"])

with col2:
    st.markdown("### 📚 이용 가이드")
    st.info("""
    **💡 더 정확한 추천을 위해:**
    
    • 구체적인 관심사 설명
    • 원하는 콘텐츠 스타일
    • 학습 목적이나 취미 목적인지
    • 선호하는 진행 방식
    
    **🎯 추천 받을 수 있는 것:**
    • 유튜브 채널 & 영상
    • 팟캐스트 프로그램
    • 인스타그램 계정
    • 관련 커뮤니티
    """)

# 추천 버튼
if st.button("🎯 맞춤 채널 추천받기", type="primary", use_container_width=True):
    if not api_key:
        st.error("⚠️ API Key를 입력해주세요!")
    elif not interest.strip():
        st.warning("⚠️ 관심사를 입력해주세요!")
    else:
        # 추가 정보 조합
        additional_info = f"플랫폼: {', '.join(platform)}, 난이도: {difficulty}, 언어: {language}, 영상길이: {duration}"
        full_query = f"{interest}\n\n[추가정보: {additional_info}]"
        
        try:
            with st.spinner("🤖 AI가 당신에게 맞는 채널을 찾고 있습니다..."):
                openai.api_key = api_key
                
                system_prompt = """
당신은 유튜브와 팟캐스트 전문 큐레이터입니다. 
사용자의 관심사에 맞는 최고의 채널들을 추천해주세요.

다음 형식으로 정확히 답변해주세요:

## 🎯 추천 분석
[사용자 관심사에 대한 분석과 추천 방향]

## 📺 유튜브 채널 추천 (3-5개)

### 1. [채널명]
**구독자:** [구독자 수 정보]
**특징:** [채널의 특색과 콘텐츠 스타일]  
**추천 영상:** [대표 영상이나 시리즈]
**추천 이유:** [왜 이 채널을 추천하는지]
**링크:** [채널 링크 - 실제 존재하는 채널만]

### 2. [채널명]
[같은 형식으로...]

## 🎧 팟캐스트 추천 (2-3개)

### 1. [프로그램명]
**플랫폼:** [어디서 들을 수 있는지]
**진행자:** [진행자 정보]
**특징:** [프로그램 특색]
**추천 에피소드:** [추천할 만한 에피소드]

## 📱 기타 추천

**인스타그램 계정:** [관련 인플루언서나 계정들]
**커뮤니티:** [관련 온라인 커뮤니티나 카페]
**앱/웹사이트:** [유용한 관련 서비스들]

## 💡 채널 활용 팁
[추천 채널들을 어떻게 활용하면 좋을지 조언]

응답은 친근하고 실용적인 한국어로 해주세요.
실제 존재하는 채널만 추천하고, 정확한 정보를 제공해주세요.
"""
                
                response = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": full_query}
                    ],
                    temperature=0.7,
                    max_tokens=1500
                )
                
                st.success("✅ 맞춤 채널 추천 완료!")
                response_text = response.choices[0].message.content
                st.markdown(response_text)
                
                # 인기 채널 모음
                st.markdown("---")
                st.markdown("## 🔥 분야별 인기 채널 모음")
                
                tab1, tab2, tab3 = st.tabs(["🏃‍♂️ 운동/건강", "📚 교육/자기계발", "🎵 엔터테인먼트"])
                
                with tab1:
                    fitness_channels = [
                        ("땅끄부부", "https://www.youtube.com/@ddangkk", "홈트레이닝"),
                        ("빅씨스 Bigsis", "https://www.youtube.com/@bigsis_official", "다이어트 운동"),
                        ("소미핏 SomiFit", "https://www.youtube.com/@SomiFit", "전신 운동"),
                        ("바른체형TV", "https://www.youtube.com/@barunbody", "체형교정"),
                        ("피지오TV", "https://www.youtube.com/@PhysioTV", "물리치료")
                    ]
                    for name, url, desc in fitness_channels:
                        st.markdown(f"💪 **[{name}]({url})** - {desc}")
                
                with tab2:
                    edu_channels = [
                        ("북튜버 책그림", "https://www.youtube.com/@bookgrim", "책 리뷰"),
                        ("슈카월드", "https://www.youtube.com/@shukaworld", "자기계발"),
                        ("조승연의 탐구생활", "https://www.youtube.com/@thethinker_jo", "지식 탐구"),
                        ("문과남자", "https://www.youtube.com/@moongwa", "인문학"),
                        ("김미경TV", "https://www.youtube.com/@kimmikyungtv", "성공 마인드")
                    ]
                    for name, url, desc in edu_channels:
                        st.markdown(f"📖 **[{name}]({url})** - {desc}")
                
                with tab3:
                    entertainment_channels = [
                        ("침착맨", "https://www.youtube.com/@ChimChakMan_Official", "예능/토크"),
                        ("워크맨", "https://www.youtube.com/@workman", "직업 체험"),
                        ("문복희", "https://www.youtube.com/@eat_moon", "먹방"),
                        ("원지의 하루", "https://www.youtube.com/@oneday_oneji", "일상 브이로그"),
                        ("쯔양", "https://www.youtube.com/@Tzuyang", "대식가")
                    ]
                    for name, url, desc in entertainment_channels:
                        st.markdown(f"🎬 **[{name}]({url})** - {desc}")
                
                # 개인화 기록
                st.markdown("---")
                with st.expander("📝 관심 채널 메모"):
                    memo = st.text_area("추천받은 채널 중 관심 있는 것들을 메모해보세요:", 
                                       placeholder="예: 땅끄부부 - 매일 아침 10분 루틴 따라하기\n빅씨스 - 주 3회 하체운동 영상 시청")
                    if st.button("💾 메모 저장"):
                        st.success("메모가 저장되었습니다! (세션 종료 시 삭제됩니다)")
                
        except Exception as e:
            st.error(f"❌ 오류가 발생했습니다: {str(e)}")
            st.info("💡 API 키가 올바른지 확인하고 다시 시도해주세요.")

# 하단 정보
st.markdown("---")
col_info1, col_info2, col_info3 = st.columns(3)

with col_info1:
    st.markdown("### 🎯 추천 받는 팁")
    st.info("""
    **더 나은 추천을 위해:**
    • 구체적인 관심사 명시
    • 현재 수준이나 경험 언급
    • 선호하는 콘텐츠 스타일 설명
    • 학습 목표나 즐기는 방식 공유
    """)

with col_info2:
    st.markdown("### 📱 플랫폼별 특징")
    st.info("""
    **각 플랫폼의 장점:**
    • 유튜브: 시각적 학습, 다양한 길이
    • 팟캐스트: 이동 중 청취, 깊이 있는 토론
    • 인스타그램: 짧고 트렌디한 콘텐츠
    • 네이버TV: 한국 콘텐츠 특화
    """)

with col_info3:
    st.markdown("### 💡 활용 가이드")
    st.info("""
    **채널 구독 후:**
    • 알림 설정으로 새 영상 확인
    • 플레이리스트 만들어 체계적 시청
    • 댓글로 크리에이터와 소통
    • 유사 채널 탐색으로 확장
    """)

# 세션 상태 초기화
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = ""
