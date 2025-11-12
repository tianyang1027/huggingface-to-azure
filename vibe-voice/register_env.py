import os
from azure.ai.ml import MLClient
from azure.identity import AzureCliCredential
from azure.ai.ml.entities import Environment

# Authenticate and connect to workspace
os.environ["SUBSCRIPTION_ID"] = f"b6fe3c19-982e-48e3-ba33-7237e20ccd0e"
os.environ["RESOURCE_GROUP"] = f"BingGrowth"
os.environ["AI_FOUNDRY_HUB_PROJECT"] = f"bing_growth"

credential = AzureCliCredential()
ml_client = MLClient(
    credential=credential,
    subscription_id=os.getenv("SUBSCRIPTION_ID"),
    resource_group_name=os.getenv("RESOURCE_GROUP"),
    workspace_name=os.getenv("AI_FOUNDRY_HUB_PROJECT"),
)

current_dir = os.path.dirname(os.path.abspath(__file__))

env = Environment(
    name="vibe-voice-env",
    version="1",
    description="Environment for Vibe Voice project",
    image="mcr.microsoft.com/azureml/curated/acpt-pytorch-2.2-cuda12.1:latest",
    conda_file=os.path.join(current_dir, "env.yml")
)

print(f"Environment '{env.name}' configuration created.")

# -------------------------------
# 3. Register the environment in Azure ML workspace
# -------------------------------
print("Registering environment to Azure ML workspace...")
registered_env = ml_client.environments.create_or_update(env)
print(f"Environment '{registered_env.name}' registered successfully with version {registered_env.version}.")
