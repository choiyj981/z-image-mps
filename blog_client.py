import requests
import time
import os

class ZImageClient:
    """
    Z-Image 로컬 API 서버와 통신하는 클라이언트 클래스
    블로그 자동화 프로그램의 ImageGenerator 부분에 통합하여 사용하세요.
    """
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url

    def generate_image(self, prompt, width=896, height=512, steps=5, seed=None):
        """
        이미지 생성 요청을 보내고 생성된 이미지 경로를 반환합니다.
        
        Args:
            prompt (str): 이미지 생성 프롬프트 (한국어 가능)
            width (int): 너비 (기본: 896)
            height (int): 높이 (기본: 512)
            steps (int): 생성 단계 수 (기본: 5)
            seed (int, optional): 시드 값
            
        Returns:
            str: 생성된 이미지의 절대 경로
        """
        print(f"[Z-Image] 이미지 생성 요청: {prompt[:30]}... ({width}x{height}, Steps: {steps})")
        
        try:
            payload = {
                "prompt": prompt,
                "width": width,
                "height": height,
                "steps": steps,
                "seed": seed
            }
            
            response = requests.post(f"{self.base_url}/generate", json=payload)
            response.raise_for_status()
            
            result = response.json()
            
            if result["status"] == "success":
                image_path = result["image_path"]
                print(f"[Z-Image] ✅ 생성 완료: {image_path} ({result['time_taken']:.1f}초)")
                return image_path
            else:
                raise Exception(f"이미지 생성 실패: {result}")
                
        except requests.exceptions.ConnectionError:
            print("[Z-Image] ❌ 서버 연결 실패! 'uv run z-image-server'가 실행 중인지 확인하세요.")
            raise
        except Exception as e:
            print(f"[Z-Image] ❌ 오류 발생: {e}")
            raise

# --- 사용 예시 (블로그 프로그램 연동 시 참고) ---
if __name__ == "__main__":
    # 1. 클라이언트 초기화
    client = ZImageClient()
    
    # 2. 테스트 프롬프트
    test_prompt = "서울의 화려한 야경, 남산타워가 보이는 풍경, 사이버펑크 스타일, 고화질"
    
    try:
        # 3. 이미지 생성 (블로그 포스팅용 최적 설정: 896x512, Steps 5)
        image_path = client.generate_image(
            prompt=test_prompt,
            width=896,
            height=512,
            steps=5
        )
        
        print(f"\n🎉 테스트 성공! 생성된 이미지: {image_path}")
        
    except Exception as e:
        print("\n⚠️ 테스트 실패")
