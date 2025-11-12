import os
from uuid import uuid4
from azure.ai.ml import MLClient
from azure.identity import AzureCliCredential
from azure.ai.ml.entities import ManagedOnlineEndpoint, ManagedOnlineDeployment, CodeConfiguration

# Authenticate and connect to workspace
print("🔑 Setting environment variables...")
os.environ["SUBSCRIPTION_ID"] = "b6fe3c19-982e-48e3-ba33-7237e20ccd0e"
os.environ["RESOURCE_GROUP"] = "BingGrowth"
os.environ["AI_FOUNDRY_HUB_PROJECT"] = "bing_growth"

print("🔑 Authenticating with AzureCliCredential...")
credential = AzureCliCredential()
ml_client = MLClient(
    credential=credential,
    subscription_id=os.getenv("SUBSCRIPTION_ID"),
    resource_group_name=os.getenv("RESOURCE_GROUP"),
    workspace_name=os.getenv("AI_FOUNDRY_HUB_PROJECT"),
)
print("✅ MLClient created successfully")

model_id = "Lightricks/LTX-Video"

# Generate endpoint and deployment names
os.environ["ENDPOINT_NAME"] = f"LTX-Video-endpoint-{str(uuid4())[:8]}"
os.environ["DEPLOYMENT_NAME"] = f"LTX-Video-deployment-{str(uuid4())[:8]}"
endpoint_name = os.getenv("ENDPOINT_NAME")
deployment_name = os.getenv("DEPLOYMENT_NAME")
print(f"📌 Endpoint name: {endpoint_name}")
print(f"📌 Deployment name: {deployment_name}")

# Define and create endpoint
print("🚀 Creating Endpoint...")
endpoint = ManagedOnlineEndpoint(name=endpoint_name)
ml_client.online_endpoints.begin_create_or_update(endpoint).result()
print("✅ Endpoint created successfully")

# Get registered model
print("📥 Retrieving registered model...")
registered_model = ml_client.models.get(name="LTX-Video", version=1)
print(f"✅ Model retrieved: {registered_model.name}, version={registered_model.version}")

# Get environment
print("📥 Retrieving environment...")
env = ml_client.environments.get(name="ltx-video-env", version=12)
print(f"✅ Environment retrieved: {env.name}, version={env.version}")

# Define deployment
print("⚙️ Configuring Deployment...")
deployment = ManagedOnlineDeployment(
    name=deployment_name,
    endpoint_name=endpoint_name,
    model=registered_model,
    environment=env,
    code_configuration=CodeConfiguration(
        code="./inference",
        scoring_script="score.py"
    ),
    instance_type="Standard_NC16as_T4_v3",
    instance_count=1,
)
print("✅ Deployment configuration completed")

# Deploy the model
print("🚀 Deploying model...")
ml_client.online_deployments.begin_create_or_update(deployment).result()
print("🎉 Model deployed successfully")

