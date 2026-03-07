from agent.agent import Agent
from agent.tool_registry import ToolRegistry
from llm.lmstudio_client import LMStudioClient

def main():
    registry = ToolRegistry()
    llm_client = LMStudioClient()
    agent = Agent(llm_client, registry)

    print("Agent is ready. Type 'exit' to end the conversation.")

    while True:
        user_input = input("\nYou: ")

        if user_input.lower() == "exit":
            break
        
        response = agent.run(user_input)
        print(f"\nAgent: {response}")

if __name__ == "__main__":
    main()
