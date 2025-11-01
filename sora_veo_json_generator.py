import streamlit as st
from openai import OpenAI
import json

# 페이지 설정
st.set_page_config(
    page_title="SORA/VEO JSON Prompt Generator",
    page_icon="🎬",
    layout="wide"
)

# 예시 프롬프트들 (구체적 상품명 제거, 더 일반적으로)
EXAMPLE_PROMPTS = {
    "식품 CF": "병이 터지면서 내용물과 재료들이 공중에서 춤추듯 날아다니며 완성된 음식 위에 쌓이는 장면",
    "음료 CF": "원두가 천천히 떨어지며 컵 안에서 아름다운 라떼아트가 만들어지는 과정, 김이 피어오르는 모습",
    "자동차 CF": "미래형 전기차가 네온 불빛 가득한 도시를 질주하며, 비 내리는 밤거리에 반사되는 불빛들",
    "패션 CF": "모델이 화려한 의상을 입고 회전하며, 천이 공중에서 우아하게 펼쳐지는 슬로우모션",
    "요리 영상": "신선한 재료들이 도마 위로 떨어지며 자동으로 썰리고, 프라이팬에서 불꽃과 함께 조리되는 장면",
    "스포츠 영상": "공이 슬로우모션으로 날아가 골대를 통과하는 순간, 관중들이 환호하는 모습",
    "캐릭터 애니": "귀여운 동물 캐릭터들이 카페에서 만나 어색하게 대화하다 친해지는 이야기",
    "게임 트레일러": "판타지 세계의 영웅이 무기를 들고 몬스터와 대결하는 액션 장면",
    "뷰티 CF": "화장품이 피부에 스며들며 빛나는 효과가 나타나고, 모델의 얼굴이 클로즈업되는 장면",
    "여행 영상": "드론이 아름다운 해변과 산을 가로지르며, 석양이 지는 풍경을 담는 장면"
}

# 카메라 움직임 프리셋
CAMERA_MOVEMENTS = {
    "슬로우 오비탈": "slow orbital shot rotating around subject",
    "탑다운 → 정면": "top-down view transitioning to front view",
    "저각도 올라가기": "low angle moving upward",
    "줌인": "smooth zoom in focusing on subject",
    "트래킹 샷": "tracking shot following subject",
    "360도 회전": "360-degree rotation around center",
    "크레인 샷": "crane shot moving up and away",
    "슬라이드": "sliding lateral movement"
}

# 캐릭터 목소리 톤 프리셋
VOICE_TONES = {
    "밝고 경쾌한": "bright and cheerful tone",
    "차분하고 따뜻한": "calm and warm tone",
    "활기찬 에너제틱": "energetic and lively tone",
    "부드럽고 온화한": "soft and gentle tone",
    "신나는 유쾌한": "excited and playful tone",
    "조용하고 섬세한": "quiet and delicate tone",
    "힘찬 자신감": "strong and confident tone",
    "수줍은 소심한": "shy and timid tone"
}

# CSS for better UI
st.markdown("""
<style>
.stButton > button {
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# 제목 및 설명
st.title("🎬 SORA/VEO JSON Prompt Generator")
st.markdown("AI 비디오 생성을 위한 전문적인 JSON 프롬프트 생성기")

# 사이드바
with st.sidebar:
    st.header("⚙️ 설정")
    api_key = st.text_input("OpenAI API Key", type="password", help="OpenAI API 키를 입력하세요")
    
    st.markdown("---")
    
    # 템플릿 선택
    template_type = st.radio(
        "템플릿 선택",
        ["SORA/VEO 기본형 (단일 씬)", "VEO 스토리텔링형 (멀티 컷)"],
        help="생성할 JSON 템플릿 유형을 선택하세요"
    )
    
    # 언어 선택 (스토리텔링형에서만)
    if template_type == "VEO 스토리텔링형 (멀티 컷)":
        st.markdown("---")
        dialogue_language = st.radio(
            "대사 언어",
            ["한국어", "영어"],
            help="캐릭터 대사를 어떤 언어로 생성할지 선택하세요"
        )
    
    st.markdown("---")
    st.markdown("### 📖 사용 방법")
    st.markdown("""
    1. OpenAI API 키 입력
    2. 템플릿 유형 선택
    3. 예시 버튼 클릭 또는 직접 입력
    4. 화면 비율 및 옵션 선택
    5. '프롬프트 생성' 클릭
    """)
    
    st.markdown("---")
    st.markdown("### 💡 팁")
    st.markdown("""
    - 예시 버튼으로 빠르게 시작
    - 카메라 움직임 프리셋 활용
    - 구체적인 장면 설명이 중요
    """)

# 메인 컨텐츠
col1, col2 = st.columns([1, 1])

with col1:
    st.header("입력")
    
    # 예시 선택 버튼들
    st.subheader("💡 예시 아이디어 (클릭하여 자동 입력)")
    
    # 2열로 버튼 배치
    example_cols = st.columns(2)
    for idx, (name, prompt) in enumerate(EXAMPLE_PROMPTS.items()):
        col_idx = idx % 2
        with example_cols[col_idx]:
            if st.button(name, key=f"example_{idx}", use_container_width=True):
                st.session_state.video_description = prompt
    
    st.markdown("---")
    
    # 비디오 설명
    video_description = st.text_area(
        "비디오 아이디어를 설명하세요",
        value=st.session_state.get('video_description', ''),
        height=150,
        placeholder="예: 석양이 지는 해변에서 서핑하는 사람"
    )
    
    # 템플릿별 추가 입력
    if template_type == "SORA/VEO 기본형 (단일 씬)":
        st.subheader("🎯 비디오 세부 설정")
        
        # 화면 비율 버튼 (2개만)
        st.write("**화면 비율**")
        aspect_cols = st.columns(2)
        with aspect_cols[0]:
            aspect_169 = st.button("16:9 (가로)", use_container_width=True, type="primary" if st.session_state.get('aspect_ratio') == '16:9' else "secondary")
            if aspect_169:
                st.session_state.aspect_ratio = '16:9'
        with aspect_cols[1]:
            aspect_916 = st.button("9:16 (세로)", use_container_width=True, type="primary" if st.session_state.get('aspect_ratio') == '9:16' else "secondary")
            if aspect_916:
                st.session_state.aspect_ratio = '9:16'
        
        aspect_ratio = st.session_state.get('aspect_ratio', '16:9')
        st.info(f"✓ 선택된 비율: {aspect_ratio}")
        
        st.markdown("---")
        
        # 카메라 움직임 프리셋
        st.write("**카메라 움직임**")
        
        # 프리셋 버튼 (2열)
        camera_preset_cols = st.columns(2)
        for idx, (name, movement) in enumerate(CAMERA_MOVEMENTS.items()):
            col_idx = idx % 2
            with camera_preset_cols[col_idx]:
                if st.button(name, key=f"camera_{idx}", use_container_width=True):
                    st.session_state.camera_movement = movement
        
        # 직접 입력 옵션
        camera_custom = st.text_input(
            "또는 직접 입력",
            value=st.session_state.get('camera_movement', ''),
            placeholder="예: slow pan from left to right"
        )
        
        if camera_custom:
            st.session_state.camera_movement = camera_custom
        
        camera_movement = st.session_state.get('camera_movement', '')
        
        st.markdown("---")
        
        with st.expander("⚙️ 추가 옵션 (선택사항)"):
            style = st.text_input("스타일", placeholder="예: photorealistic cinematic")
            lighting = st.text_input("조명", placeholder="예: morning sunlight, golden hour")
    
    else:  # 스토리텔링형
        st.subheader("🎯 비디오 세부 설정")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            # 화면 비율 버튼 (2개만)
            st.write("**화면 비율**")
            aspect_169_story = st.button("16:9", key="story_169", use_container_width=True, type="primary" if st.session_state.get('aspect_ratio_story') == '16:9' else "secondary")
            if aspect_169_story:
                st.session_state.aspect_ratio_story = '16:9'
            aspect_916_story = st.button("9:16", key="story_916", use_container_width=True, type="primary" if st.session_state.get('aspect_ratio_story') == '9:16' else "secondary")
            if aspect_916_story:
                st.session_state.aspect_ratio_story = '9:16'
            
            aspect_ratio = st.session_state.get('aspect_ratio_story', '9:16')
            st.success(f"✓ {aspect_ratio}")
            
        with col_b:
            video_type = st.selectbox("영상 스타일", ["3D cartoon", "2D animation", "realistic", "anime"], index=0)
            duration = st.text_input("길이", value="15s", placeholder="예: 15s")
        
        tone = st.text_input("톤/분위기", placeholder="예: Warm, cute, and comically awkward")
        
        st.markdown("---")
        
        with st.expander("👥 캐릭터 설정 (선택사항)", expanded=True):
            num_characters = st.number_input("캐릭터 수", min_value=0, max_value=5, value=2)
            
            if num_characters > 0:
                character_info = st.text_area(
                    "캐릭터 설명",
                    placeholder="예:\n캐릭터1: 수다스럽지만 긴장하는 다람쥐\n캐릭터2: 차분하고 예의 바른 햄스터",
                    height=100
                )
                
                st.write("**캐릭터 목소리 톤 프리셋**")
                st.caption("캐릭터별로 목소리 톤을 선택하세요")
                
                # 캐릭터별 목소리 톤 선택
                for i in range(num_characters):
                    st.write(f"캐릭터 {i+1} 목소리:")
                    voice_cols = st.columns(4)
                    for idx, (name, tone_desc) in enumerate(list(VOICE_TONES.items())):
                        col_idx = idx % 4
                        with voice_cols[col_idx]:
                            if st.button(name, key=f"voice_{i}_{idx}", use_container_width=True):
                                st.session_state[f'voice_tone_{i}'] = f"{name} ({tone_desc})"
                    
                    selected_voice = st.session_state.get(f'voice_tone_{i}', '')
                    if selected_voice:
                        st.caption(f"✓ 선택됨: {selected_voice}")
    
    st.markdown("---")
    # 생성 버튼
    generate_button = st.button("🚀 JSON 프롬프트 생성", type="primary", use_container_width=True)

with col2:
    st.header("결과")
    
    if generate_button:
        if not api_key:
            st.error("⚠️ OpenAI API 키를 입력해주세요!")
        elif not video_description:
            st.error("⚠️ 비디오 아이디어를 입력해주세요!")
        else:
            try:
                client = OpenAI(api_key=api_key)
                
                # 템플릿별 시스템 프롬프트
                if template_type == "SORA/VEO 기본형 (단일 씬)":
                    system_prompt = """당신은 SORA와 VEO를 위한 JSON 프롬프트 전문가입니다.
사용자의 입력을 받아 다음 구조의 JSON을 생성하세요:

{
  "description": "상세한 장면 설명 (영어, 3-4문장)",
  "style": "영상 스타일",
  "camera": "카메라 움직임 설명",
  "lighting": "조명 설정",
  "room": "공간/배경 설명",
  "elements": ["장면의 주요 요소들을 배열로"],
  "motion": "움직임과 동작의 흐름 설명",
  "ending": "마지막 장면 설명",
  "text": "none",
  "keywords": ["관련 키워드들"]
}

규칙:
1. description은 반드시 영어로 작성
2. 모든 설명은 구체적이고 시각적으로
3. elements는 최소 5개 이상
4. motion은 시간 순서대로 설명
5. keywords에는 화면비율, 스타일, 주요 요소 포함
6. text는 항상 "none" (자막 없음)
7. 응답은 유효한 JSON만 출력 (설명 없이)"""

                else:  # 스토리텔링형
                    dialogue_lang = dialogue_language if 'dialogue_language' in locals() else '한국어'
                    
                    system_prompt = f"""당신은 VEO 스토리텔링용 JSON 프롬프트 전문가입니다.
사용자의 입력을 받아 다음 구조의 JSON을 생성하세요:

{{
  "video_type": "영상 스타일",
  "duration": "총 길이",
  "resolution": "해상도",
  "aspect_ratio": "화면 비율",
  "fps": 30,
  "tone": "전체적인 톤과 분위기",
  "restrictions": ["제약사항 배열"],
  "bgm": {{
    "style": "배경음악 스타일 설명"
  }},
  "characters": {{
    "CHARACTER1": {{
      "design_reference": "캐릭터 디자인 설명",
      "personality": "성격 설명",
      "voice": "목소리 톤 설명"
    }}
  }},
  "cuts": [
    {{
      "id": 1,
      "time": "0.0-5.0s",
      "scene": "장면 설명 (영어)",
      "action": "액션 설명 (영어)",
      "dialogue": "대사 ({'한국어' if dialogue_lang == '한국어' else '영어'})"
    }}
  ]
}}

규칙:
1. cuts는 최소 3개 이상의 씬으로 구성
2. scene과 action은 영어로 상세하게
3. dialogue는 **반드시 {dialogue_lang}로 작성**
4. 각 cut의 시간은 연속적으로
5. characters는 입력된 캐릭터 수만큼
6. 영상 내 자막(text overlay)은 없음 - 대사만 음성으로
7. 응답은 유효한 JSON만 출력 (설명 없이)"""

                # 사용자 프롬프트 구성
                user_prompt_parts = [f"비디오 아이디어: {video_description}"]
                
                if template_type == "SORA/VEO 기본형 (단일 씬)":
                    user_prompt_parts.append(f"화면비율: {aspect_ratio}")
                    if camera_movement:
                        user_prompt_parts.append(f"카메라 움직임: {camera_movement}")
                    if style:
                        user_prompt_parts.append(f"스타일: {style}")
                    if lighting:
                        user_prompt_parts.append(f"조명: {lighting}")
                else:
                    user_prompt_parts.append(f"영상 스타일: {video_type}")
                    user_prompt_parts.append(f"길이: {duration}")
                    user_prompt_parts.append(f"화면비율: {aspect_ratio}")
                    user_prompt_parts.append(f"대사 언어: {dialogue_lang}")
                    if tone:
                        user_prompt_parts.append(f"톤: {tone}")
                    if 'character_info' in locals() and character_info:
                        user_prompt_parts.append(f"캐릭터:\n{character_info}")
                        
                        # 목소리 톤 추가
                        for i in range(num_characters):
                            voice = st.session_state.get(f'voice_tone_{i}', '')
                            if voice:
                                user_prompt_parts.append(f"캐릭터{i+1} 목소리: {voice}")
                
                user_prompt = "\n".join(user_prompt_parts)
                
                # API 호출
                with st.spinner("JSON 프롬프트 생성 중..."):
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                        temperature=0.7,
                        max_tokens=2000
                    )
                    
                    # 결과 추출 및 JSON 파싱
                    generated_text = response.choices[0].message.content.strip()
                    
                    # JSON 코드 블록 제거
                    if generated_text.startswith("```json"):
                        generated_text = generated_text[7:]
                    if generated_text.startswith("```"):
                        generated_text = generated_text[3:]
                    if generated_text.endswith("```"):
                        generated_text = generated_text[:-3]
                    
                    generated_text = generated_text.strip()
                    
                    # JSON 파싱 및 재포맷
                    try:
                        json_data = json.loads(generated_text)
                        formatted_json = json.dumps(json_data, indent=2, ensure_ascii=False)
                    except:
                        formatted_json = generated_text
                    
                    # 결과 표시
                    st.success("✅ JSON 프롬프트가 생성되었습니다!")
                    
                    # JSON 표시
                    st.json(json_data if isinstance(json_data, dict) else json.loads(formatted_json))
                    
                    st.markdown("---")
                    
                    # 복사용 JSON
                    st.subheader("📋 복사용 JSON")
                    
                    # 텍스트 영역 (선택하여 복사 가능)
                    st.text_area(
                        "클릭하여 전체 선택 후 Ctrl+C (또는 Cmd+C)로 복사",
                        value=formatted_json,
                        height=300,
                        label_visibility="collapsed"
                    )
                    
                    st.info("💡 팁: 위 텍스트 박스를 클릭 → Ctrl+A (전체선택) → Ctrl+C (복사)")
                    
                    # 다운로드 버튼
                    st.download_button(
                        label="💾 JSON 파일 다운로드",
                        data=formatted_json,
                        file_name=f"video_prompt_{aspect_ratio.replace(':', 'x')}.json",
                        mime="application/json",
                        use_container_width=True
                    )
                    
            except Exception as e:
                error_msg = str(e)
                if "authentication" in error_msg.lower() or "api key" in error_msg.lower():
                    st.error("❌ API 키가 유효하지 않습니다. 올바른 OpenAI API 키를 입력해주세요.")
                elif "rate limit" in error_msg.lower() or "quota" in error_msg.lower():
                    st.error("❌ API 사용 한도를 초과했습니다. 잠시 후 다시 시도해주세요.")
                else:
                    st.error(f"❌ 오류가 발생했습니다: {error_msg}")

# 푸터
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Made with ❤️ for AI Video Creators | Powered by OpenAI GPT-4</p>
</div>
""", unsafe_allow_html=True)
