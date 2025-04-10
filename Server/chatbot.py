import requests

# Replace this with your Wit.ai access token
WIT_ACCESS_TOKEN = "WM46J5TN6GPY42GTB2A6RGUIJD5FCYM7"

def ask_chatbot(prompt: str) -> str:
    try:
        # Set the request headers for Wit.ai API authentication
        headers = {
            'Authorization': f'Bearer {WIT_ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }

        # Define the query parameters
        params = {
            'q': prompt
        }

        # Send the GET request to Wit.ai API
        response = requests.get('https://api.wit.ai/message', headers=headers, params=params)

        # Check for successful response
        if response.status_code == 200:
            data = response.json()
            
            # Extract and return the first intent or entity (you can adjust based on your needs)
            if "intents" in data and len(data["intents"]) > 0:
                intent = data["intents"][0]["name"]
                return f"Detected intent: {intent}"
            else:
                return "No intent detected."
        else:
            return f"Error: {response.status_code} - {response.text}"

    except Exception as e:
        return f"Error: {str(e)}"

