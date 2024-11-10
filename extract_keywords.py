from openai import OpenAI
import os
import json
from dotenv import load_dotenv
from prompts import KEYWORD_EXTRACTION_PROMPT

# Load environment variables
load_dotenv()

MAX_RETRIES = int(os.getenv('MAX_RETRIES_KEYWORDS', '3')) 

def setup_openai():
    """Configure OpenAI client"""
    return OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def validate_keywords(keywords) -> bool:
    """
    Validate if the keywords output has the expected format
    
    Args:
        keywords: The output to validate
        
    Returns:
        bool: True if format is valid, False otherwise
    """
    try:
        # Check if it's a list or can be converted to one
        if isinstance(keywords, str):
            keywords = json.loads(keywords)
            
        if not isinstance(keywords, list):
            return False
            
        # Check length
        if not (3 <= len(keywords) <= 7):  # Ajustado para coincidir con el prompt
            return False
            
        # Check all elements are strings and not empty
        if not all(isinstance(k, str) and k.strip() for k in keywords):
            return False
            
        return True
        
    except Exception as e:
        print(f"Validation error: {str(e)}")
        return False

def extract_keywords(description: str, client: OpenAI) -> list:
    """
    Extract relevant keywords from a description using ChatGPT API
    
    Args:
        description (str): Input text description
        client (OpenAI): OpenAI client instance
        
    Returns:
        list: List of extracted keywords
    """
    for attempt in range(MAX_RETRIES):
        try:
            response = client.chat.completions.create(
                model=os.getenv('MODEL_KEYWORDS'),
                messages=[
                    {
                        "role": "system",
                        "content": KEYWORD_EXTRACTION_PROMPT["system"]
                    },
                    {
                        "role": "user",
                        "content": KEYWORD_EXTRACTION_PROMPT["user"].format(description)
                    }
                ],
                temperature=0.3,
                max_tokens=100
            )
            
            content = response.choices[0].message.content.strip()
            print(f"API Response: {content}")  # Debug
            
            # Limpiar cualquier formato markdown o texto adicional
            content = content.replace('```json', '').replace('```', '').strip()
            
            try:
                keywords = json.loads(content)
                if isinstance(keywords, dict) and "keywords" in keywords:
                    keywords = keywords["keywords"]
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {str(e)}")
                continue
            
            # Validate output format
            if validate_keywords(keywords):
                return keywords
            else:
                print(f"Attempt {attempt + 1}: Invalid format received, retrying...")
                continue

        except Exception as e:
            print(f"Attempt {attempt + 1}: Error processing request: {str(e)}")
            if attempt == MAX_RETRIES - 1:
                raise Exception("Maximum retries reached. Could not get valid keywords.")
            continue
    
    return []

def save_keywords(keywords: list, output_file: str = 'extracted_keywords.json'):
    """Save keywords to a JSON file"""
    with open(output_file, 'w') as f:
        json.dump(keywords, f, indent=2)

def read_description() -> str:
    """Read description from environment variable"""
    try:
        description = os.getenv('INPUT_DESCRIPTION')
        if not description:
            raise Exception("INPUT_DESCRIPTION environment variable not found")
        return description.strip()
    except Exception as e:
        raise Exception(f"Error reading description from environment: {str(e)}")

def main():
    try:
        # Read description from file
        description = read_description()
        
        if len(description) > 300:
            print("Description exceeds 300 characters limit")
            return
            
        client = setup_openai()
        keywords = extract_keywords(description, client)
        
        if keywords:
            print(f"\nInput description:\n{description}")
            print(f"\nExtracted keywords: {keywords}")
            save_keywords(keywords)
            print(f"\nKeywords saved to extracted_keywords.json")
        else:
            print("\nError: Could not extract valid keywords after multiple attempts")
            
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main() 