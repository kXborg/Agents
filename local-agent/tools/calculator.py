schema = {
    "name": "calculator",
    "description": "Performs a basic math operation on two numbers. Supports add, subtract, multiply, and divide",
    "parameters": {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "description": "The math operation to perform",
                "enum": ["add", "subtract", "multiply", "divide"]
            },
            "a": {
                "type": "number",
                "description": "The first number"
            },
            "b": {
                "type": "number",
                "description": "The second number"
            }
        },
        "required": ["operation", "a", "b"]
    }

}

def calculate(operation, a, b):
    if operation == "add":
        result = a + b 
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b 
    elif operation == "divide":
        if b == 0:
            return {"error": "Can not divide by zero"}
        result = a / b 

    else:
        return {"error": f"Unknown operation: {operation}"}
    
    return result


TOOL = {
    "schema": schema,
    "function": calculate
}