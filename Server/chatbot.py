import requests
import json

# Replace this with your actual Gemini API Key
GEMINI_API_KEY = "AIzaSyASoWBojxZUyjP-Wb4ZWc8lzA-sRUYA3qM"

def ask_chatbot(prompt: str) -> str:
    try:

        list_models_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_API_KEY}"

        response = requests.get(list_models_url)
        if response.status_code == 200:
            print("Available models:", response.json())
        else:
            print("Error listing models:", response.text)

        # Define the Gemini API endpoint with your API key in the URL
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={GEMINI_API_KEY}"
        
        # Prepare the payload for the Gemini API.
        # This payload sends the prompt as the user message to be processed.
        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}],
                    "role": "user"
                }
            ]
        }
        
        # Set the necessary headers
        headers = {
            'Content-Type': 'application/json'
        }
        
        # Send a POST request to the Gemini API
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        # If the request was successful, extract the reply from the response JSON.
        if response.status_code == 200:
            data = response.json()
            # The structure here may depend on the API's response.
            # In this example, we assume it returns a key "candidates" with the reply text in:
            # data["candidates"][0]["content"]["parts"][0]["text"]
            reply = data["candidates"][0]["content"]["parts"][0]["text"]
            return reply.strip()
        else:
            # If the API returns an error, return the error details.
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"
