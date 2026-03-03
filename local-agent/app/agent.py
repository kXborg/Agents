from openai import OpenAI
import json 

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)

tools = {
    "calculator": calculator,
    "get_current_time": get_current_time,
    "read_file": read_file,
    "simple_search": simple_search
}

system_prompt = """
You are an agent.
if you need to use a tool, respond in JSON format:
    {
        "tool_name": "tool_name_here",
        "arguments": { ... }
    }
Otherwise respond normally.
"""

messages = [
    {"role": "system", "content": system_prompt}
]


def run_agent(user_input):
    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-oss-20b",
        messages=messages,
        temperature=0
    )

    content = response.choices[0].message.content 

    try:
        tool_call = json.loads(content)
        tool_name = tool_call["tool_name"]
        args = tool_call.get("arguments", {})

        result = tools[tool_name](**args)

        messages.append({
            "role": "assistant",
            "content": content
        })

        messages.append({
            "role": "tool",
            "content": result
        })

        final_response = client.chat.completions.create(
            model="gpt-oss-20b",
            messages=messages,
            temperature=0
        )

        return final_response.choices[0].message.content

    except:
        return content