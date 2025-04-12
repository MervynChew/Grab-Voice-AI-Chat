import requests
import re
import json
import os
import random
from dotenv import load_dotenv
from typing import List, Dict
from .knowledge_base import (
    get_knowledge_base_context, get_conversation_guideline, 
    get_order_recommendation, get_suggested_orders, 
    get_ride_request_details, get_suggested_rides
)

# Construct the path to the .env file relative to this script
script_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(script_dir, '.env')
load_dotenv(dotenv_path=dotenv_path) # Load environment variables from the specified .env file

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Make sure it's set in your .env file.")

def create_prompt(user_message: str, driver_type: str, chat_history: List[Dict[str, str]]) -> str:
    """
    Creates a well-structured prompt with context, instructions, and chat history,
    tailored to the driver type ('ride' or 'delivery').
    """
    knowledge_context = get_knowledge_base_context(driver_type)

    # Format the recent chat history
    history_str = "\nRecent Conversation History:\n"
    if chat_history:
        for msg in chat_history:
            sender = msg.get('sender', 'unknown').capitalize()
            text = msg.get('text', '')
            history_str += f"{sender}: {text}\n"
    else:
        history_str += "(No history provided)\n"

    # Tailor the initial instruction based on driver type
    if driver_type == 'ride':
        role_description = "Your role is to help the driver manage ride requests efficiently using voice commands."
        capabilities_focus = "Handle simulated ride requests (notifications, acceptance, rejection)."
        interaction_mode = "Focus on ride-related commands and general queries."
    elif driver_type == 'delivery':
        role_description = "Your role is to help the driver manage delivery orders efficiently using voice commands."
        capabilities_focus = "Handle delivery order requests (suggestions, details, acceptance)."
        interaction_mode = "Focus on delivery-related commands and general queries."
    else: # Default/unknown type
        role_description = "Your role is to assist the driver with available tasks using voice commands."
        capabilities_focus = "Handle ride requests or delivery orders as applicable."
        interaction_mode = "Respond to ride or delivery commands and general queries."

    prompt = f"""You are a Grab Driver Assistant AI powered by Gemini.
{role_description}

**Strictly use the following Knowledge Base Information and Available Order/Ride Data when responding to requests about orders or rides. Do not invent details.**

Knowledge Base Information:
{knowledge_context}
{history_str}

Instructions:
1. Act as a helpful assistant for the specified driver type ({driver_type}).
2. {capabilities_focus}
3. **Prioritize using the provided Knowledge Base (including specific order/ride data if relevant) and Conversation History to answer driver requests accurately.**
4. Use the Recent Conversation History to understand the context of the Driver Message.
5. Maintain a clear, concise, and professional tone suitable for voice interaction.
6. If unsure about a command or if the request cannot be fulfilled with the provided data, ask for clarification using appropriate guidelines. **Do not make up information.**
7. {interaction_mode}
8. Keep responses short.

Driver Message: {user_message}

Please provide a helpful and concise response based **only** on the provided history, knowledge base, and driver message:"""
    
    return prompt

def ask_chatbot(user_message: str, driver_type: str, chat_history: List[Dict[str, str]]) -> str:

    try:
        user_message_lower = user_message.lower()

        # --- Ride Hailing Logic (Only for ride drivers) ---
        if driver_type == 'ride':
            preference_handled_locally = False # Flag for ride preference

            # 1. Check for accepting a specific ride
            accept_match = re.search(r'accept ride(?:\s*id)?[:#]?\s*(\d+)', user_message_lower)
            if accept_match:
                ride_id = int(accept_match.group(1))
                return get_conversation_guideline("ride_accepted_id").format(ride_id=ride_id)

            # 2. Check for rejecting a ride (keep simple)
            if re.search(r'\breject ride\b', user_message_lower):
                return get_conversation_guideline("ride_rejected")

            # 3. Check for ride suggestion requests (best, suggest, what, etc.)
            is_ride_suggestion_request = (
                re.search(r'\b(suggest|recommend|available|any|offer|best|top|good)\b.*\b(ride|rides|request|requests)', user_message_lower) or
                (re.search(r'\b(what|which)\b', user_message_lower) and re.search(r'\b(ride|rides|request|requests)', user_message_lower)) or
                re.search(r'\bcheck\b.*\b(ride|rides|request|requests)\b', user_message_lower) # Treat 'check' as suggestion
            )
            if is_ride_suggestion_request:
                # Check for preferences mentioned in the initial request
                preference = None
                if re.search(r'\b(fare|money|highest pay|most pay|more fare)\b', user_message_lower):
                    preference = "fare"
                elif re.search(r'\b(time|quick|fast|shortest|less time|faster)\b', user_message_lower):
                    preference = "time"
                elif re.search(r'\b(rating|passenger|high rating)\b', user_message_lower):
                    preference = "rating"
                
                # If preference found, use it. Otherwise, use default.
                effective_preference = preference if preference else "default"
                print(f"Handling ride suggestion request locally with preference: {effective_preference}") 
                return get_suggested_rides(effective_preference)

            # 4. Check if user is *responding* with a ride preference
            last_bot_message = chat_history[-1]['text'] if chat_history and chat_history[-1]['sender'] == 'bot' else ''
            if "what's most important" in last_bot_message.lower() and ("ride requests" in last_bot_message.lower() or "highest fare" in last_bot_message.lower()): # Check if last question was about rides
                preference = None
                if re.search(r'\b(fare|money|highest pay|most pay|more fare)\b', user_message_lower):
                    preference = "fare"
                elif re.search(r'\b(time|quick|fast|shortest|less time|faster)\b', user_message_lower):
                    preference = "time"
                elif re.search(r'\b(rating|passenger|high rating)\b', user_message_lower):
                    preference = "rating"

                if preference:
                    print(f"Handling ride preference locally: {preference}")
                    preference_handled_locally = True
                    return get_suggested_rides(preference)

            # 5. Check for specific ride details request
            details_match = re.search(r'\b(ride|details for|info on)(?:\s*id)?[:#]?\s*(\d+)', user_message_lower)
            if details_match and not accept_match: # Ensure not an accept command
                ride_id = int(details_match.group(2))
                return get_ride_request_details(ride_id)
            
            # If ride logic specific rules didn't match and preference wasn't handled, fall through to LLM
            if preference_handled_locally:
                 print("Warning: Ride preference handled locally flag set, but fallback reached unexpectedly.")

        # --- Delivery Order Logic (Only for delivery drivers) ---
        elif driver_type == 'delivery':
            accept_match_inner = re.search(r'accept (?:delivery|order)(?:\s*id)?[:#]?\s*(\d+)', user_message_lower)
            if accept_match_inner:
                order_id = int(accept_match_inner.group(1))
                return get_conversation_guideline("delivery_accepted").format(order_id=order_id)

            # --- Suggestion Logic --- 
            # Combine checks for any suggestion request
            is_suggestion_request = (
                re.search(r'\b(best|top|good|suggest|recommend|available|any|offer)\b.*\b(order|delivery)', user_message_lower) or
                (re.search(r'\b(what|which)\b', user_message_lower) and re.search(r'\b(delivery|deliveries|order)', user_message_lower))
            )
            if is_suggestion_request:
                # Check if preference is mentioned
                preference = None
                if re.search(r'\b(reward|money|highest pay|most pay|more reward)\b', user_message_lower):
                    preference = "reward"
                elif re.search(r'\b(time|quick|fast|shortest|less time|faster)\b', user_message_lower):
                    preference = "time"
                elif re.search(r'\b(traffic|light traffic|easy drive|less traffic|minimal traffic)\b', user_message_lower):
                    preference = "traffic"
                
                # If preference found, use it. Otherwise, use default.
                effective_preference = preference if preference else "default"
                print(f"Handling delivery suggestion request locally with preference: {effective_preference}") 
                return get_suggested_orders(effective_preference) # Handle suggestion with specific or default preference

            # Check if user is *responding* with a preference (Less likely now, but keep for robustness)
            last_bot_message = chat_history[-1]['text'] if chat_history and chat_history[-1]['sender'] == 'bot' else ''
            if "what's most important" in last_bot_message.lower() and ("delivery orders" in last_bot_message.lower() or "high reward" in last_bot_message.lower()):
                 preference = None
                 if re.search(r'\b(reward|money|highest pay|most pay|more reward)\b', user_message_lower):
                     preference = "reward"
                 elif re.search(r'\b(time|quick|fast|shortest|less time|faster)\b', user_message_lower):
                     preference = "time"
                 elif re.search(r'\b(traffic|light traffic|easy drive|less traffic|minimal traffic)\b', user_message_lower):
                     preference = "traffic"
                 
                 if preference:
                     print(f"Handling preference locally: {preference}")
                     preference_handled_locally = True # Set flag
                     return get_suggested_orders(preference) # Handle preference response locally

            # Check for specific delivery order details request
            details_match = re.search(r'\b(delivery|order|details for|info on)(?:\s*id)?[:#]?\s*(\d+)', user_message_lower)
            if details_match:
                order_id = int(details_match.group(2))
                recommendation = get_order_recommendation(order_id)
                if "Order not found" in recommendation:
                    return "Sorry, I couldn't find details for that delivery ID."
                return recommendation
            # Need flag for delivery preference handled locally if adding it to elif block
            # if preference_handled_locally: ... 

        # --- Fallback to Gemini API --- 
        # Check if any specific logic was hit (which would have returned already)
        # If we reach here, none of the specific rules matched.
        print(f"No specific rule matched for '{user_message}'. Falling back to LLM.")
        prompt = create_prompt(user_message, driver_type, chat_history) # Pass history 
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={GEMINI_API_KEY}"
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
                "maxOutputTokens": 256
            }
        }
        headers = {
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status() 
            data = response.json()
            if data.get("candidates") and data["candidates"][0].get("content", {}).get("parts"):
                reply = data["candidates"][0]["content"]["parts"][0].get("text", "")
                # Check if the LLM itself failed to understand despite history
                if "sorry" in reply.lower() and "understand" in reply.lower():
                     print("Warning: LLM indicated confusion despite history context.")
                     # Optionally return a more specific error or the LLM's confusion
                     # return get_conversation_guideline("clarification") 
                return reply.strip()
            else:
                print("Warning: Unexpected API response structure.")
                return get_conversation_guideline("error")
        except requests.exceptions.RequestException as api_err:
            print(f"Error calling Gemini API: {api_err}")
            return get_conversation_guideline("error")

    except Exception as e:
        print(f"Error in ask_chatbot: {str(e)}") 
        return "Sorry, I encountered an unexpected issue. Please try again."