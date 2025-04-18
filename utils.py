def clean_python_response(content: str) -> str:
    if content.startswith("```python\n") and content.endswith("```"):
        content = content.replace("```python\n", "", 1)
        content = content.replace("```", "", 1)

    return content
