import torch
from diffusers import DiffusionPipeline
from diffusers.utils import load_image, export_to_video

pipe = DiffusionPipeline.from_pretrained(
    "Lightricks/LTX-Video",
    torch_dtype=torch.float32,
    trust_remote_code=True
)
pipe.to("cpu")

prompt = "A man with short gray hair plays a red electric guitar."
image = load_image(
    "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/diffusers/guitar-man.png"
)


# output = pipe(image=image, prompt=prompt, num_inference_steps=10).frames
output = pipe(
    image=image, 
    prompt=prompt,
    num_inference_steps=10,
    height=64,
    width=64
).frames[0]
export_to_video(output, "output.mp4")