import os
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoProcessor,
    AutoTokenizer,
    AutoFeatureExtractor
)
import soundfile as sf
import json
import tempfile

# Global variables
model = None
processor = None
device = "cuda" if torch.cuda.is_available() else "cpu"

def init():
    global model, processor
    print(f"🚀 Initializing model on device: {device}")

    model_path = os.path.join(os.getenv("AZUREML_MODEL_DIR"), "VibeVoice-1.5B")
    print(f"📂 Loading model from: {model_path}")

    try:
        # 先尝试 AutoProcessor
        try:
            processor = AutoProcessor.from_pretrained(model_path, trust_remote_code=True)
            print("✅ Loaded AutoProcessor")
        except Exception as e:
            print(f"⚠️ AutoProcessor failed: {e}")
            # fallback：尝试 tokenizer 或 feature extractor
            try:
                processor = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
                print("✅ Loaded AutoTokenizer")
            except Exception:
                processor = AutoFeatureExtractor.from_pretrained(model_path, trust_remote_code=True)
                print("✅ Loaded AutoFeatureExtractor")

        # 加载模型
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            trust_remote_code=True  # 必须有
        ).to(device)

        print("✅ Model loaded successfully")
    except Exception as e:
        print(f"❌ Failed to load model: {str(e)}")
        raise

def run(raw_data):
    global model, processor
    try:
        if isinstance(raw_data, str):
            data = json.loads(raw_data)
        else:
            data = raw_data

        text = data.get("text")
        if not text:
            return {"error": "No text provided"}

        speaker = data.get("speaker", "default")
        sample_rate = data.get("sample_rate", 16000)

        print(f"🎤 Generating speech for text='{text[:50]}...' speaker={speaker}, sample_rate={sample_rate}")

        # 推理
        inputs = processor(text=text, return_tensors="pt").to(device)
        with torch.no_grad():
            outputs = model.generate(**inputs)

        # 解码成音频（注意：有些 TTS 模型不是用 batch_decode，而是 model 输出直接就是 audio tensor）
        try:
            audio_values = processor.batch_decode(outputs, return_tensors="pt")[0].cpu().numpy()
        except Exception:
            # fallback：如果模型直接输出 audio
            if isinstance(outputs, torch.Tensor):
                audio_values = outputs[0].cpu().numpy()
            else:
                raise ValueError("Model outputs could not be converted to audio.")

        # 保存到临时文件
        temp_dir = tempfile.gettempdir()
        audio_path = os.path.abspath(os.path.join(temp_dir, "output.wav"))
        sf.write(audio_path, audio_values, samplerate=sample_rate)

        print(f"✅ Audio saved to {audio_path}")

        return {
            "audio_path": audio_path,
            "message": "success"
        }

    except Exception as e:
        print(f"❌ Error in run(): {str(e)}")
        return {"error": str(e)}
