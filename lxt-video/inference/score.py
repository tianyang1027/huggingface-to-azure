import os
import torch
from diffusers import DiffusionPipeline
import requests
from PIL import Image
import imageio
import json
import tempfile
import io

# Global variables
model = None
device = "cuda" if torch.cuda.is_available() else "cpu"

def init():
    global model
    print(f"🚀 Initializing model on device: {device}")

    # 直接从 Hugging Face Hub 加载模型
    model_id = "Lightricks/LTX-Video"
    try:
        model = DiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32
        )
        model.to(device)
        print(f"✅ Model loaded successfully from {model_id}")
    except Exception as e:
        print(f"❌ Failed to load model: {str(e)}")
        raise e

def run(raw_data):
    global model
    try:
        data = json.loads(raw_data)
        image_url = data.get("image_url")
        if not image_url:
            return {"error": "No image_url provided"}

        print(f"🌐 Downloading image from: {image_url}")
        resp = requests.get(image_url)
        if resp.status_code != 200:
            return {"error": f"Failed to download image: {resp.status_code}"}

        image = Image.open(io.BytesIO(resp.content)).convert("RGB")

        num_frames = data.get("num_frames", 16)
        num_inference_steps = data.get("num_inference_steps", 25)
        guidance_scale = data.get("guidance_scale", 7.5)

        print(f"🎨 Generating video: frames={num_frames}, steps={num_inference_steps}, guidance_scale={guidance_scale}")
        output = model(
            image=image,
            num_frames=num_frames,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale
        )

        frames = output.frames if hasattr(output, "frames") else output[0]

        temp_dir = tempfile.gettempdir()
        video_path = os.path.join(temp_dir, "output.mp4")
        imageio.mimsave(video_path, frames, fps=8)
        print(f"✅ Video saved to {video_path}")

        return {
            "video_path": video_path,
            "message": "success"
        }

    except Exception as e:
        print(f"❌ Error in run(): {str(e)}")
        return {"error": str(e)}
