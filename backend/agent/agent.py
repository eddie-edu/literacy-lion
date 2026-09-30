import yaml
import os

# using the openai library as every major AI provider supports the OpenAI protocol
from openai import AsyncOpenAI

#for Ai config
with open("agent/config.yaml", "r") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

client = AsyncOpenAI(
    api_key=os.environ["AI_API_KEY"],
    base_url=config["PROVIDER_URL"],
) #should be ready on import