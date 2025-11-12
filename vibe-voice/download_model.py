from huggingface_hub import snapshot_download

local_path = r"D:\\dev\\VibeVoice-1.5B"
snapshot_download(repo_id="microsoft/VibeVoice-1.5B", local_dir=local_path)
print(f"Model downloaded to {local_path}")