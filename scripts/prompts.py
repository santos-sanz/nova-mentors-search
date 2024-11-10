KEYWORD_EXTRACTION_PROMPT = {
    "system": "You are an AI trained to extract the most relevant keywords from any given text. You must return only a JSON array with no additional formatting or markdown.",
    "user": """Extract 3-7 most relevant keywords from the following text. Return only a raw JSON array of strings, with no markdown formatting, explanations, or additional text.

Text: "{}"
"""
}

AFFINITY_EVALUATION_PROMPT = {
    "system": "You are an AI trained to evaluate semantic affinity between keywords and contexts.",
    "user": """You are an expert in semantic affinity analysis. Evaluate the relationship between each keyword and the provided context, assigning an affinity score between 1 and 100. Use the context to judge how relevant each keyword is in relation to it.

Action:
1. For each keyword in the input list, analyze its semantic relationship with the context.
2. Assign an affinity score between 1 and 100, where 1 indicates very low affinity and 100 indicates very high affinity.
3. Return a list of integers representing the affinity of each keyword in the order presented.

Input:
- Keywords: {keywords}
- Context: "{context}"

Return only the list of numbers, nothing else."""
} 