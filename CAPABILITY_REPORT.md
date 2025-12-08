# 블로그 실전 이미지 생성 능력 검증 리포트 (Capability Report)

**테스트 일시**: 2025-12-03  
**모델**: Tongyi-MAI/Z-Image-Turbo  
**설정**: 896x512, Steps 5 (블로그 최적 설정)

---

## 🧪 테스트 개요
블로그 포스팅에 자주 사용되는 **4대 핵심 카테고리**를 선정하여, 실제 포스팅에 사용할 수 있는 품질인지 검증했습니다.

| 카테고리 | 주제 | 테스트 목적 | 결과 |
|----------|------|-------------|------|
| **맛집 (Food)** | 삼겹살, 카페 라떼 | 질감 표현, 김(Steam), 조명 | ✅ 성공 |
| **여행 (Travel)** | 제주도, 한옥마을 | 자연 경관, 야경, 광각 표현 | ✅ 성공 |
| **제품 (Product)** | 스마트폰, 화장품 | 깔끔한 배경, 반사 재질, 고급스러움 | ✅ 성공 |
| **정보 (Info)** | 코딩, 금융 | 추상적 개념 시각화, 3D 일러스트 | ✅ 성공 |

---

## 📸 카테고리별 분석 및 팁

### 1. 맛집/푸드 (Food)
- **강점**: 음식의 윤기와 질감 표현이 매우 뛰어납니다.
- **팁**: `steam rising` (김이 모락모락), `close-up` (근접 촬영) 프롬프트를 쓰면 더 먹음직스럽게 나옵니다.
- **추천 프롬프트**: `delicious texture`, `warm lighting`, `food photography`

### 2. 여행/풍경 (Travel)
- **강점**: 복잡한 풍경도 안정적으로 그려냅니다. 특히 야경(Night view)의 조명 처리가 훌륭합니다.
- **팁**: `wide angle shot` (광각)을 추가하면 시원한 느낌을 줍니다.
- **추천 프롬프트**: `cinematic lighting`, `scenic view`, `landmark`

### 3. 제품/리뷰 (Product)
- **강점**: 스튜디오 조명처럼 깔끔한 배경 처리가 가능합니다.
- **팁**: 배경을 단순하게 하려면 `clean background`, `minimalist`를 추가하세요.
- **추천 프롬프트**: `product photography`, `studio lighting`, `high detail`

### 4. 정보/추상 (Info)
- **강점**: 눈에 보이지 않는 개념(금융, IT)을 3D 일러스트 스타일로 잘 표현합니다.
- **팁**: `3D render`, `isometric` 키워드를 쓰면 전문적인 인포그래픽 느낌이 납니다.
- **추천 프롬프트**: `concept art`, `digital art`, `cyberpunk`

---

## 💡 실전 프롬프트 가이드 (복사해서 쓰세요)

### 맛집 포스팅용
```
High quality food photography of [음식 이름], steam rising, delicious texture, warm lighting, photorealistic, 8k
```

### 여행 포스팅용
```
Beautiful landscape of [장소 이름], wide angle shot, clear blue sky, cinematic lighting, travel photography, high resolution
```

### 제품 리뷰용
```
Product photography of [제품 이름], clean desk setup, soft studio lighting, modern vibe, high detail, 8k
```

### 정보성 글용
```
3D render illustration of [개념 키워드], isometric view, clean background, professional business concept, digital art
```

---

## ✅ 종합 결론
**"모든 카테고리에서 블로그 포스팅용으로 즉시 사용 가능한 품질을 확인했습니다."**
특히 **Steps 5** 설정만으로도 충분한 퀄리티가 나오므로, 속도와 품질 두 마리 토끼를 모두 잡을 수 있습니다.
