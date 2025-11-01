# 🎬 SORA/VEO JSON Prompt Generator

ChatGPT API를 활용한 SORA와 VEO를 위한 전문적인 JSON 프롬프트 생성기입니다.

## 주요 기능

- **2가지 템플릿 지원**
  - SORA/VEO 기본형: 단일 씬, 상품/광고 영상에 적합
  - VEO 스토리텔링형: 멀티 컷, 캐릭터 대화가 있는 애니메이션에 적합

- **자동 JSON 생성**: 한국어 설명을 완벽한 JSON 구조로 변환
- **템플릿 기반**: 검증된 구조로 일관성 있는 출력
- **다운로드 지원**: 생성된 JSON을 바로 다운로드
- **직관적 UI**: Streamlit 기반의 깔끔한 인터페이스

## 설치 방법

### 1. 레포지토리 클론
```bash
git clone <your-repo-url>
cd <your-repo-name>
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. OpenAI API 키 준비
[OpenAI Platform](https://platform.openai.com/)에서 API 키를 발급받으세요.

## 실행 방법

```bash
streamlit run sora_veo_json_generator.py
```

브라우저에서 자동으로 열립니다 (기본: http://localhost:8501)

## 사용 방법

### SORA/VEO 기본형 (단일 씬)
1. 템플릿 선택: "SORA/VEO 기본형"
2. 비디오 아이디어 입력
3. 스타일, 카메라, 조명 등 세부사항 입력 (선택사항)
4. 생성 버튼 클릭

### VEO 스토리텔링형 (멀티 컷)
1. 템플릿 선택: "VEO 스토리텔링형"
2. 비디오 아이디어 입력
3. 영상 스타일, 길이, 화면비율 설정
4. 캐릭터 정보 입력 (선택사항)
5. 생성 버튼 클릭

## 예시

### 입력 (기본형)
```
비디오 아이디어: 누텔라 병이 터지면서 초콜릿과 헤이즐넛이 공중에서 춤추듯 날아다니며 토스트 위에 쌓이는 장면
스타일: photorealistic cinematic
카메라: slow orbital shot
조명: morning sunlight
```

### 출력 (기본형)
```json
{
  "description": "Photorealistic cinematic shot of a sunlit kitchen...",
  "style": "photorealistic cinematic",
  "camera": "slow orbital shot from low angle upward...",
  "lighting": "morning sunlight streaming through soft white curtains...",
  "elements": [...],
  "motion": "jar shakes, lid pops and spins off...",
  "keywords": [...]
}
```

### 입력 (스토리텔링형)
```
비디오 아이디어: 카페에서 어색하게 대화하는 다람쥐와 햄스터
영상 스타일: 3D cartoon
길이: 15s
캐릭터:
캐릭터1: 수다스럽지만 긴장하는 다람쥐
캐릭터2: 차분하고 예의 바른 햄스터
```

### 출력 (스토리텔링형)
```json
{
  "video_type": "3D cartoon",
  "duration": "15s",
  "characters": {...},
  "cuts": [
    {
      "id": 1,
      "time": "0.0-5.0s",
      "scene": "A cozy cafe corner...",
      "dialogue": "..."
    }
  ]
}
```

## JSON 구조

### 기본형 필드
- `description`: 전체 장면 설명
- `style`: 영상 스타일
- `camera`: 카메라 움직임
- `lighting`: 조명 설정
- `room`: 배경/공간
- `elements`: 주요 요소 배열
- `motion`: 움직임 흐름
- `ending`: 마지막 장면
- `text`: 텍스트 오버레이
- `keywords`: 키워드 배열

### 스토리텔링형 필드
- `video_type`: 영상 타입
- `duration`: 총 길이
- `resolution`: 해상도
- `aspect_ratio`: 화면 비율
- `tone`: 전체 톤
- `bgm`: 배경음악
- `characters`: 캐릭터 정보
- `cuts`: 씬별 상세 정보

## 기술 스택

- **Frontend**: Streamlit
- **AI Model**: OpenAI GPT-4o-mini
- **Language**: Python 3.8+

## 주의사항

- OpenAI API 키가 필요합니다 (유료)
- API 사용량에 따라 비용이 발생할 수 있습니다
- 생성된 JSON은 SORA/VEO API 구조를 따릅니다

## 팁

1. **구체적으로 설명하세요**: "아름다운 풍경" 보다 "석양이 지는 바다, 파도가 부서지는 해변"
2. **카메라 움직임 명시**: "줌인", "오비탈 샷", "탑다운" 등
3. **조명 디테일**: "자연광", "네온사인", "황금빛 시간" 등
4. **시간 순서 고려**: 처음-중간-끝의 흐름을 생각하며 작성

## 라이센스

MIT License

## 기여

이슈와 풀 리퀘스트를 환영합니다!

---

Made with ❤️ for AI Video Creators
