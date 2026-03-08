import json
from agent.prompts import get_system_prompt


class Agent:
    def __init__(self, llm_client, registry):

        self.llm = llm_client
        self.registry = registry

        self.messages = [
            {
                "role": "system",
                "content": get_system_prompt()
            }
        ]

    def run(self, user_input):
        self.messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        # Get schema (schemas is a list of tool schemas)
        schemas = self.registry.get_schemas()
        print("\n LIST OF SCHEMAS: ", schemas)

        for _ in range(5):
            print("\nMESSAGES SENT TO LLM:")
            for m in self.messages:
                print(m)

            message = self.llm.chat(
                self.messages,
                schemas
            )

            print("\nMODEL RESPONSE:")
            print(message)

            # Check if the model wants to call a tool
            tool_calls = message.get("tool_calls")

            if tool_calls:
                # Append the assistant message (with tool_calls) to history
                self.messages.append(message)

                for tool_call in tool_calls:
                    tool_name = tool_call["function"]["name"]
                    arguments = json.loads(tool_call["function"]["arguments"])
                    tool_call_id = tool_call["id"]

                    print("TOOL CALLED:", tool_name)

                    tool_function = self.registry.get_function(tool_name)
                    result = tool_function(**arguments)

                    # Append tool result with matching tool_call_id
                    self.messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call_id,
                            "content": json.dumps(result)
                        }
                    )

                # After tool call, don't send schemas again
                schemas = None
                continue

            # Normal final response (no tool calls)
            self.messages.append(message)
            return message.get("content", "")

        raise RuntimeError("Agent exceeded maximum tool iterations")