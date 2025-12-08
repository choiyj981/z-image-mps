import os
import time
import secrets
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import torch
from diffusers import ZImagePipeline

# --- 설정 ---
MODEL_ID = "Tongyi-MAI/Z-Image-Turbo"
DEFAULT_STEPS = 5
DEFAULT_WIDTH = 896
DEFAULT_HEIGHT = 512

# --- FastAPI 앱 초기화 ---
app = FastAPI(title="Z-Image Local API", version="1.0.0")

# --- 전역 모델 변수 ---
pipe = None
device = None
dtype = None

class GenerationRequest(BaseModel):
    prompt: str
    width: Optional[int] = DEFAULT_WIDTH
    height: Optional[int] = DEFAULT_HEIGHT
    steps: Optional[int] = DEFAULT_STEPS
    seed: Optional[int] = None

class GenerationResponse(BaseModel):
    status: str
    image_path: str
    time_taken: float
    meta: dict

def load_model():
    """서버 시작 시 모델 로딩"""
    global pipe, device, dtype
    print("=" * 60)
    print("🚀 Z-Image API 서버 시작")
    print("⏳ 모델 로딩 중... (Tongyi-MAI/Z-Image-Turbo)")
    
    start_time = time.time()
    
    # 디바이스 선택
    if torch.backends.mps.is_available():
        device = "mps"
        dtype = torch.bfloat16
    elif torch.cuda.is_available():
        device = "cuda"
        dtype = torch.bfloat16
    else:
        device = "cpu"
        dtype = torch.float32
        
    print(f"📱 디바이스: {device} ({dtype})")
    
    load_kwargs = {
        "low_cpu_mem_usage": False,
        "torch_dtype": dtype
    }
    
    pipe = ZImagePipeline.from_pretrained(MODEL_ID, **load_kwargs)
    
    if dtype != torch.float32 and hasattr(pipe, "vae"):
        pipe.vae.to(dtype=torch.float32)
        pipe.vae.config.force_upcast = True
    
    try:
        pipe.transformer.set_attention_backend("sdpa")
    except Exception:
        pass
        
    pipe.to(device)
    
    elapsed = time.time() - start_time
    print(f"✅ 모델 로딩 완료! ({elapsed:.1f}초)")
    print("📡 서버 대기 중... (http://localhost:8000)")
    print("=" * 60)

@app.on_event("startup")
async def startup_event():
    load_model()

@app.post("/generate", response_model=GenerationResponse)
async def generate_image(req: GenerationRequest):
    global pipe
    
    if pipe is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    print(f"\n📩 요청 수신: {req.prompt[:30]}... ({req.width}x{req.height}, Steps: {req.steps})")
    
    try:
        # Seed 설정
        seed = req.seed if req.seed is not None else secrets.randbits(63)
        generator_device = "cpu" if device == "mps" else device
        generator = torch.Generator(device=generator_device).manual_seed(seed)
        
        start_time = time.time()
        
        # 이미지 생성
        with torch.inference_mode():
            result = pipe(
                prompt=req.prompt,
                negative_prompt="",
                height=req.height,
                width=req.width,
                num_inference_steps=req.steps,
                guidance_scale=0.0,
                generator=generator
            )
            
        elapsed = time.time() - start_time
        
        # 저장
        output_dir = "generated_images"
        os.makedirs(output_dir, exist_ok=True)
        timestamp = int(time.time())
        filename = f"img_{timestamp}_{seed}.png"
        save_path = os.path.abspath(os.path.join(output_dir, filename))
        
        result.images[0].save(save_path)
        
        print(f"✅ 생성 완료: {elapsed:.1f}초")
        
        return {
            "status": "success",
            "image_path": save_path,
            "time_taken": elapsed,
            "meta": {
                "width": req.width,
                "height": req.height,
                "steps": req.steps,
                "seed": seed
            }
        }
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # uv run z-image-server 로 실행 가능하도록
    uvicorn.run(app, host="0.0.0.0", port=8000)
