import requests
import re
import json
from .knowledge_base import get_knowledge_base_context, get_conversation_guideline, get_order_recommendation, get_best_order


# Replace this with your actual Gemini API Key
GEMINI_API_KEY = "AIzaSyASoWBojxZUyjP-Wb4ZWc8lzA-sRUYA3qM"

def create_prompt(user_message: str) -> str:
    """
    Creates a well-structured prompt with context and instructions.
    """
    knowledge_context = get_knowledge_base_context()
    
    prompt = f"""You are an AI voice assistant powered by Gemini. Here is important context about your capabilities and knowledge:

{knowledge_context}

Instructions:
1. Use the knowledge base information to provide accurate and consistent responses
2. Maintain a friendly and professional tone
3. If unsure, ask for clarification using the provided conversation guidelines
4. Keep responses concise but informative
5. Always stay within the scope of your capabilities

User Message: {user_message}

Please provide a helpful response:"""
    
    return prompt

def ask_chatbot(user_message: str) -> str:

    try:
        
        # 1. Check if user asks for best order
        if re.search(r'\bbest\b', user_message, re.IGNORECASE) and re.search(r'\border\b', user_message, re.IGNORECASE):
            return get_best_order()
        
        # Search for the word "order" followed by a digit in the user message
        match = re.search(r'order(?:\s*id)?[:#]?\s*(\d+)', user_message, re.IGNORECASE)
        
        if match:
            print(f"Hello3")
            # Extract the order ID
            order_id = int(match.group(1))  # Get the number after "order"

            print(f"Hello2 order ID: {order_id}")

            # Retrieve recommendation based on order ID
            recommendation = get_order_recommendation(order_id)
            
            # Check if recommendation was found
            if "Order not found" in recommendation:
                return "Sorry, I couldn't find any details for the provided order ID."
            
            return recommendation
        else:
            # Create the enhanced prompt for the chatbot based on user message
            prompt = create_prompt(user_message)

            # Define the Gemini API endpoint
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={GEMINI_API_KEY}"

            # Prepare the payload with the enhanced prompt
            payload = {
                "contents": [
                    {
                        "parts": [{"text": prompt}]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.7,
                    "topP": 0.8,
                    "topK": 40,
                    "maxOutputTokens": 1024
                }
            }

            # Set headers
            headers = {
                'Content-Type': 'application/json'
            }

            # Send request to Gemini API
            response = requests.post(url, headers=headers, json=payload)

            if response.status_code == 200:
                data = response.json()
                reply = data["candidates"][0]["content"]["parts"][0]["text"]
                return reply.strip()
            else:
                # Use error guideline from knowledge base
                return get_conversation_guideline("error")
            
    except Exception as e:
        return f"Error: {str(e)}"
