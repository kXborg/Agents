import json

from agent.prompts import get_system_prompt

class Agent:
    def __init__(self, llm_client, registry):
        self.llm = llm_client
        self.registry = registry

        self.messages = [
            {
                "role": "system",
                "content": get_system_prompt(),
            }
        ]
    
    def run(self, user_input):
        self.messages.append(
            {
                "role":"user",
                "content": user_input,
            }
        )

        while True:
            message = self.llm.chat(
                self.messages,
                self.registry.get_schemas()
            )

            if "function_call" not in message:
                return message["content"]
            
            function_call = message["function_call"]
            tool_name = function_call["name"]
            arguments = json.loads(function_call["arguments"])

            tool_function = self.registry.get_function(tool_name)
            
            # Tool calling function here
            result = tool_function(**arguments)

            self.messages.append(
                {
                    "role": "tool",
                    "content": json.dumps(result),
                    "name": tool_name,
                }
            )