from extensions.math_executor import process_math

def math_agent(prompt: str) -> str:
    """
    Math Agent: Processes math expressions using math_executor.
    """
    try:
        result = process_math(prompt)
        return f"🧮 Math Agent Result:\n{result}"
    except Exception as e:
        return f"⚠️ Math Agent Error: {e}"
