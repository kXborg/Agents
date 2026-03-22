from strands import Agent
from strands.models import BedrockModel

model = BedrockModel(
    model_id = "us.anthropic.claude-sonnet-4-6",
    region_name = "us-east-1",
    temperature = 0.7,
    max_tokens = 1024,
)

agent = Agent(model=model)

print("Model config:", agent.model.config)
agent("Explain what agentic AI is in 2-3 sentences.")
print("")