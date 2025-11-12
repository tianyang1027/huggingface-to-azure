from huggingface_hub import snapshot_download
from azure.ai.ml import MLClient
from azure.identity import ManagedIdentityCredential
from azure.ai.ml.entities import Model
import os


# 1. in Azure compute environment download LTX-Video
model_dir = "/mnt/azureml_models/LTX-Video"
os.makedirs(model_dir, exist_ok=True)

snapshot_download(
    repo_id="Lightricks/LTX-Video",
    local_dir=model_dir,
    repo_type="model"
)
print(f"Model downloaded to {model_dir}")

# 2. Authenticate and connect to workspace
os.environ["SUBSCRIPTION_ID"] = f"b6fe3c19-982e-48e3-ba33-7237e20ccd0e"
os.environ["RESOURCE_GROUP"] = f"BingGrowth"
os.environ["AI_FOUNDRY_HUB_PROJECT"] = f"bing_growth"
credential = ManagedIdentityCredential()
# print token for debugging
print("Access Token:", credential.get_token("https://management.azure.com/.default").token)

ml_client = MLClient(
    credential=credential,
    subscription_id=os.getenv("SUBSCRIPTION_ID"),
    resource_group_name=os.getenv("RESOURCE_GROUP"),
    workspace_name=os.getenv("AI_FOUNDRY_HUB_PROJECT"),
)
print("✅ MLClient created successfully")
# 3. Register Azure ML model
registered_model = ml_client.models.create_or_update(
    Model(
        name="LTX-Video",
        version="1",
        path=model_dir,
        description="LTX-Video is the first DiT-based video generation model capable of generating high-quality videos in real-time"
    )
)

print(f"Model Registered：{registered_model.name} v{registered_model.version}")
