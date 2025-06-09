import json
import re

def parse_llm_json_response(response_content):
    """
    Parse JSON from LLM response with comprehensive error handling.
    
    Args:
        response_content (str): The content string from the LLM response
        
    Returns:
        dict or None: Parsed JSON dictionary or None if parsing fails
    """
    if not response_content:
        print("Empty response content")
        return None
    
    # Clean the content
    content = response_content.strip()
    
    # Try different extraction methods in order of preference
    extraction_methods = [
        # Method 1: Extract from ```json code blocks
        lambda x: re.search(r'```json\s*\n(.*?)\n```', x, re.DOTALL),
        # Method 2: Extract from ``` code blocks
        lambda x: re.search(r'```\s*\n(.*?)\n```', x, re.DOTALL),
        # Method 3: Look for JSON object starting with {
        lambda x: re.search(r'(\{.*\})', x, re.DOTALL),
    ]
    
    for method in extraction_methods:
        try:
            match = method(content)
            if match:
                json_str = match.group(1).strip()
                parsed_json = json.loads(json_str)
                return parsed_json
        except (json.JSONDecodeError, AttributeError) as e:
            continue
    
    # If all methods fail, try parsing the entire content
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON from response: {e}")
        print(f"Content preview: {content[:200]}...")
        return None
