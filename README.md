# Z-Image MPS (Local AI Image Generator)

네이버 블로그 자동화를 위한 로컬 AI 이미지 생성기입니다.  
Apple Silicon (M1/M2/M3)의 MPS 가속을 사용하여 빠르고 효율적으로 이미지를 생성합니다.

## 🚀 주요 기능

- **로컬 구동**: 외부 API 비용 0원, 무제한 생성
- **고속 생성**: MPS 가속 + Turbo 모델 사용 (장당 1~2분)
- **API 서버**: 블로그 자동화 프로그램과 연동 가능한 HTTP API 제공
- **인터랙티브 CLI**: 터미널에서 대화형으로 이미지 생성

## 🛠️ 설치 및 실행

### 1. 설치
```bash
# uv가 설치되어 있어야 합니다
uv sync
```

### 2. API 서버 실행 (추천)
블로그 자동화 프로그램과 연동하려면 서버를 실행하세요.
```bash
uv run z-image-server
```
- 주소: `http://localhost:8000`
- 모델이 메모리에 상주하여 즉시 생성 가능

### 3. 인터랙티브 CLI 실행
직접 프롬프트를 입력하여 테스트하려면 CLI를 사용하세요.
```bash
uv run z-image-interactive
```

## 📝 블로그 연동 가이드

`blog_client.py`를 참고하여 블로그 자동화 프로그램에 통합하세요.

```python
import requests

response = requests.post("http://localhost:8000/generate", json={
    "prompt": "맛있는 삼겹살 사진",
    "width": 896,
    "height": 512,
    "steps": 5
})
print(response.json()["image_path"])
```

## 📊 최적 설정 (워크벤치 결과)

| 용도 | 크기 | Steps | 100장 소요시간 |
|------|------|-------|----------------|
| **블로그 표준 (추천)** | **896 x 512** | **5** | **약 2시간 47분** |
| 속도 우선 | 768 x 432 | 5 | 약 1시간 30분 |
| 고화질 (HD) | 1280 x 720 | 5 | 약 4시간 30분 |

자세한 내용은 `FINAL_WORKBENCH.md`를 참고하세요.
