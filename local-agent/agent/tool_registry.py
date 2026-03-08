from tools.datetime_tool import TOOL as DATETIME_TOOL
from tools.calculator import TOOL as CALCULATOR_TOOL

class ToolRegistry:
    def __init__(self):
        self._schemas = []
        self._functions = {}
        self._load_tools()
    
    def _load_tools(self):

        tools = [DATETIME_TOOL, CALCULATOR_TOOL]

        for tool in tools:
            schema = tool["schema"]
            function = tool["function"]

            name = schema["name"]

            self._schemas.append(schema)
            self._functions[name] = function

    def get_schemas(self):
        return self._schemas

    def get_function(self, name):
        return self._functions.get(name)