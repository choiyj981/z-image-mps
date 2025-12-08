#!/usr/bin/env python3
"""
인터랙티브 CLI - 모델을 메모리에 상주시켜 빠른 생성
GUI와 동일한 방식으로 작동
"""

import os
import sys
import time
import secrets
from datetime import datetime

import torch
from diffusers import ZImagePipeline


class InteractiveImageGenerator:
    def __init__(self):
        self.pipe = None
        self.device = None
        self.dtype = None
        
    def pick_device(self):
        """디바이스 선택 (MPS > CUDA > CPU)"""
        if torch.backends.mps.is_available():
            return "mps", torch.bfloat16
        if torch.cuda.is_available():
            return "cuda", torch.bfloat16
        return "cpu", torch.float32
    
    def load_model(self):
        """모델을 메모리에 로딩 (한 번만 실행)"""
        print("=" * 60)
        print("🎨 Z-Image-Turbo 인터랙티브 CLI")
        print("=" * 60)
        print("\n⏳ 모델 로딩 중... (Tongyi-MAI/Z-Image-Turbo)")
        
        start_time = time.time()
        
        # 1. 디바이스 선택
        self.device, self.dtype = self.pick_device()
        print(f"📱 디바이스: {self.device} ({self.dtype})")
        
        # 2. 파이프라인 로드
        load_kwargs = {
            "low_cpu_mem_usage": False,
            "torch_dtype": self.dtype
        }
        
        self.pipe = ZImagePipeline.from_pretrained(
            "Tongyi-MAI/Z-Image-Turbo",
            **load_kwargs
        )
        
        # 3. VAE 설정 (NaN 방지)
        if self.dtype != torch.float32 and hasattr(self.pipe, "vae"):
            self.pipe.vae.to(dtype=torch.float32)
            self.pipe.vae.config.force_upcast = True
            print("✅ VAE setup (Float32 Upcast)")
        
        # 4. Attention Backend
        try:
            self.pipe.transformer.set_attention_backend("sdpa")
        except Exception:
            pass
        
        # 5. 디바이스로 이동
        self.pipe.to(self.device)
        
        elapsed = time.time() - start_time
        print(f"✅ 모델 로딩 완료! ({elapsed:.1f}초)")
        print("=" * 60)
        
    def generate(self, prompt, negative_prompt="", steps=5, width=880, height=1184, seed=None):
        """이미지 생성"""
        if not self.pipe:
            print("❌ 모델이 로딩되지 않았습니다.")
            return
        
        # Seed 처리
        if seed is None:
            seed = secrets.randbits(63)
        
        # Generator 생성 (MPS는 CPU generator 사용)
        generator_device = "cpu" if self.device == "mps" else self.device
        generator = torch.Generator(device=generator_device).manual_seed(seed)
        
        print(f"\n🎨 생성 중...")
        print(f"  📝 프롬프트: {prompt[:60]}...")
        print(f"  📐 크기: {width} x {height}")
        print(f"  🔢 Steps: {steps}")
        print(f"  🎲 Seed: {seed}")
        
        start_time = time.time()
        
        # 생성
        with torch.inference_mode():
            result = self.pipe(
                prompt=prompt,
                negative_prompt=negative_prompt if negative_prompt else None,
                height=height,
                width=width,
                num_inference_steps=steps,
                guidance_scale=0.0,  # Turbo 모델은 0.0 권장
                generator=generator
            )
        
        image = result.images[0]
        
        # 저장
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"z-image-{timestamp}-{seed}.png"
        save_path = os.path.join(output_dir, filename)
        
        image.save(save_path)
        
        elapsed = time.time() - start_time
        print(f"✅ 완료! ({elapsed:.1f}초)")
        print(f"💾 저장: {save_path}")
        
        return save_path
    
    def run_interactive(self):
        """인터랙티브 모드 실행"""
        print("\n" + "=" * 60)
        print("🚀 인터랙티브 모드 시작!")
        print("=" * 60)
        print("\n명령어:")
        print("  - 프롬프트 입력: 바로 생성")
        print("  - 'q' 또는 'quit': 종료")
        print("  - 'help': 도움말")
        print("  - 'settings': 현재 설정 보기")
        print("=" * 60)
        
        # 기본 설정
        settings = {
            "steps": 5,
            "width": 880,
            "height": 1184,
            "seed": None  # None이면 랜덤
        }
        
        while True:
            try:
                print("\n" + "-" * 60)
                user_input = input("프롬프트 입력 (또는 명령어): ").strip()
                
                if not user_input:
                    continue
                
                # 종료
                if user_input.lower() in ['q', 'quit', 'exit']:
                    print("\n👋 종료합니다!")
                    break
                
                # 도움말
                elif user_input.lower() == 'help':
                    print("\n📖 도움말:")
                    print("  - 프롬프트: 직접 입력하면 즉시 생성")
                    print("  - set steps <값>: Steps 변경 (예: set steps 7)")
                    print("  - set size <width> <height>: 크기 변경")
                    print("  - set seed <값>: 고정 Seed 설정 (random으로 랜덤)")
                    print("  - settings: 현재 설정 확인")
                    print("  - q/quit: 종료")
                
                # 설정 보기
                elif user_input.lower() == 'settings':
                    print("\n⚙️  현재 설정:")
                    print(f"  Steps: {settings['steps']}")
                    print(f"  크기: {settings['width']} x {settings['height']}")
                    print(f"  Seed: {'랜덤' if settings['seed'] is None else settings['seed']}")
                
                # 설정 변경
                elif user_input.lower().startswith('set '):
                    parts = user_input.split()
                    if len(parts) >= 3:
                        cmd = parts[1].lower()
                        if cmd == 'steps':
                            settings['steps'] = int(parts[2])
                            print(f"✅ Steps를 {settings['steps']}로 변경했습니다.")
                        elif cmd == 'size' and len(parts) >= 4:
                            settings['width'] = int(parts[2])
                            settings['height'] = int(parts[3])
                            print(f"✅ 크기를 {settings['width']}x{settings['height']}로 변경했습니다.")
                        elif cmd == 'seed':
                            if parts[2].lower() == 'random':
                                settings['seed'] = None
                                print("✅ Seed를 랜덤으로 변경했습니다.")
                            else:
                                settings['seed'] = int(parts[2])
                                print(f"✅ Seed를 {settings['seed']}로 변경했습니다.")
                
                # 이미지 생성 (프롬프트)
                else:
                    self.generate(
                        prompt=user_input,
                        steps=settings['steps'],
                        width=settings['width'],
                        height=settings['height'],
                        seed=settings['seed']
                    )
                    
            except KeyboardInterrupt:
                print("\n\n⚠️  Ctrl+C 감지. 종료하려면 'q'를 입력하세요.")
            except Exception as e:
                print(f"\n❌ 오류: {e}")


def main():
    generator = InteractiveImageGenerator()
    
    # 모델 로딩 (한 번만!)
    generator.load_model()
    
    # 인터랙티브 모드 실행
    generator.run_interactive()


if __name__ == "__main__":
    main()
