import os
import requests
import json

# 替换为你的 Azure OpenAI 资源信息
endpoint =  os.getenv("AZURE_OPENAI_APIKEY")
api_key = s.getenv("AZURE_OPENAI_ENDPOINT")
deployment = "gpt-4o-mini-tts"
api_version = "2025-03-01-preview"

url = f"{endpoint}/openai/deployments/{deployment}/audio/speech?api-version={api_version}"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

data = {
    "model": deployment,
    "input": "The quick brown fox jumped over the lazy dog",
    "voice": "alloy"
}

response = requests.post(url, headers=headers, data=json.dumps(data))

if response.status_code == 200:
    with open("speech.wav", "wb") as f:
        f.write(response.content)
    print("✅ 音频已保存到 speech.wav")
else:
    print("❌ 请求失败:", response.status_code, response.text)
