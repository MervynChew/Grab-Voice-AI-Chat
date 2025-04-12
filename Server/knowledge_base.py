import re
from typing import Dict, List, Any

# Knowledge Base
KNOWLEDGE_BASE: Dict[str, Any] = {
    "general_info": {
        "app_name": "Voice AI Chat Assistant",
        "capabilities": [
            "Voice transcription", "Natural language understanding",
            "Contextual responses", "Multi-turn conversations"
        ],
        "supported_languages": [
            "English", "Chinese", "Spanish", "French", "Malay",
            "Sabah Malay", "Sarawak Malay", "Kelantanese Malay",
            "Terengganu Malay", "Tamil (Malaysia)", "Mandarin (Malaysia)",
            "Hokkien", "Cantonese"
        ],
    },
    "faqs": {
        "what_can_you_do": "I can help you with voice transcription, answer questions, and engage in natural conversations.",
        "how_to_use": "Just speak into your device and I'll transcribe and respond to your message.",
        "voice_quality": "For best results, speak clearly in a quiet environment."
    },
    "conversation_guidelines": {
        "greeting": "Hello! How can I assist you today?",
        "clarification": "Could you please provide more details about that?",
        "error": "I apologize, but I'm having trouble understanding. Could you rephrase that?"
    },
    "orders": [
        {"order_id": 1, "pickup_location": "Gurney Plaza", "delivery_location": "Komtar", "reward": 10, "time_estimate": 12, "traffic_condition": "moderate", "priority": "high", "score": 0},
        {"order_id": 2, "pickup_location": "Queensbay Mall", "delivery_location": "USM", "reward": 11, "time_estimate": 18, "traffic_condition": "heavy", "priority": "medium", "score": 0},
        {"order_id": 3, "pickup_location": "Penang Hill Base", "delivery_location": "Ayer Itam Market", "reward": 8, "time_estimate": 15, "traffic_condition": "light", "priority": "high", "score": 0},
        {"order_id": 4, "pickup_location": "Chulia Street", "delivery_location": "Beach Street", "reward": 9, "time_estimate": 10, "traffic_condition": "light", "priority": "high", "score": 0},
        {"order_id": 5, "pickup_location": "Sunshine Square", "delivery_location": "Bayan Baru Market", "reward": 6, "time_estimate": 8, "traffic_condition": "moderate", "priority": "low", "score": 0},
        {"order_id": 6, "pickup_location": "Penang International Airport", "delivery_location": "Relau", "reward": 14, "time_estimate": 20, "traffic_condition": "heavy", "priority": "high", "score": 0},
        {"order_id": 7, "pickup_location": "Tesco Jelutong", "delivery_location": "Macallum Street", "reward": 10, "time_estimate": 13, "traffic_condition": "moderate", "priority": "medium", "score": 0},
        {"order_id": 8, "pickup_location": "Penang Sentral", "delivery_location": "Butterworth Ferry Terminal", "reward": 12, "time_estimate": 17, "traffic_condition": "moderate", "priority": "high", "score": 0},
        {"order_id": 9, "pickup_location": "Bukit Jambul Complex", "delivery_location": "Taman Lip Sin", "reward": 7, "time_estimate": 9, "traffic_condition": "light", "priority": "medium", "score": 0},
        {"order_id": 10, "pickup_location": "Farlim", "delivery_location": "Taman Sri Nibong", "reward": 8, "time_estimate": 14, "traffic_condition": "moderate", "priority": "low", "score": 0},
        {"order_id": 11, "pickup_location": "Penang General Hospital", "delivery_location": "Padang Kota Lama", "reward": 13, "time_estimate": 11, "traffic_condition": "light", "priority": "high", "score": 0},
        {"order_id": 12, "pickup_location": "Straits Quay", "delivery_location": "Tanjung Tokong", "reward": 10, "time_estimate": 10, "traffic_condition": "moderate", "priority": "medium", "score": 0},
        {"order_id": 13, "pickup_location": "Gurney Drive", "delivery_location": "Penang Road", "reward": 9, "time_estimate": 12, "traffic_condition": "moderate", "priority": "medium", "score": 0},
        {"order_id": 14, "pickup_location": "Batu Ferringhi", "delivery_location": "Tanjung Bungah", "reward": 15, "time_estimate": 25, "traffic_condition": "heavy", "priority": "high", "score": 0},
        {"order_id": 15, "pickup_location": "Karpal Singh Drive", "delivery_location": "Jelutong", "reward": 7, "time_estimate": 10, "traffic_condition": "light", "priority": "medium", "score": 0},
        {"order_id": 16, "pickup_location": "Island Glades", "delivery_location": "Green Lane", "reward": 6, "time_estimate": 8, "traffic_condition": "light", "priority": "low", "score": 0},
        {"order_id": 17, "pickup_location": "Pulau Tikus Market", "delivery_location": "Lebuh Armenian", "reward": 11, "time_estimate": 9, "traffic_condition": "moderate", "priority": "high", "score": 0},
        {"order_id": 18, "pickup_location": "SPICE Arena", "delivery_location": "Sungai Ara", "reward": 10, "time_estimate": 15, "traffic_condition": "heavy", "priority": "medium", "score": 0},
        {"order_id": 19, "pickup_location": "Bayan Lepas Free Industrial Zone", "delivery_location": "Bukit Gambir", "reward": 13, "time_estimate": 20, "traffic_condition": "heavy", "priority": "high", "score": 0}
]

}

def get_knowledge_base_context() -> str:
    """
    Formats the knowledge base into a string context for the AI model.
    """
    context = "Knowledge Base Information:\n\n"
    
    # Add general information
    context += "General Information:\n"
    for key, value in KNOWLEDGE_BASE["general_info"].items():
        if isinstance(value, list):
            context += f"{key}: {', '.join(value)}\n"
        else:
            context += f"{key}: {value}\n"
    
    # Add FAQs
    context += "\nFrequently Asked Questions:\n"
    for question, answer in KNOWLEDGE_BASE["faqs"].items():
        context += f"Q: {question}\nA: {answer}\n"
    
    return context

def get_conversation_guideline(key: str) -> str:
    """
    Retrieves a specific conversation guideline.
    """
    return KNOWLEDGE_BASE["conversation_guidelines"].get(key, "")

def update_knowledge_base(category: str, key: str, value: str) -> bool:
    """
    Updates the knowledge base with new information.
    """
    try:
        if category in KNOWLEDGE_BASE:
            if isinstance(KNOWLEDGE_BASE[category], dict):
                KNOWLEDGE_BASE[category][key] = value
                return True
        return False
    except Exception:
        return False 
    

def calculate_order_score(order: dict) -> float:
    traffic_map = {"light": 3, "moderate": 2, "heavy": 1}
    priority_map = {"high": 2, "medium": 1, "low": 0}
    
    traffic = traffic_map.get(order.get("traffic_condition", "moderate"), 2)
    priority = priority_map.get(order.get("priority", "medium"), 1)
    reward = order.get("reward", 0)
    time = order.get("time_estimate", 0)
    
    reward_score = (reward / 15) * 10  # assuming 15 is max reward possible
    time_penalty = min(time / 5, 5)    # normalize time penalty (max 5)
    
    score = traffic + priority + reward_score - time_penalty
    return round(score, 2)


def get_best_order() -> str:
    """
    Finds the order with the highest score and returns a recommendation.
    """
    best_order = None
    highest_score = float('-inf')

    for order in KNOWLEDGE_BASE["orders"]:
        score = calculate_order_score(order)
        if score > highest_score:
            highest_score = score
            best_order = order

        """
        return f"Best Order ID: {best_order['order_id']}\nPickup: {best_order['pickup_location']} → Delivery: {best_order['delivery_location']}"
        """

    
    if best_order:
        recommendation = get_order_recommendation(best_order["order_id"])
        return (
            f"📦 Best Order Recommendation 📦\n"
            f"───────────────────────────\n"
            f"🆔 Order ID       : {best_order['order_id']}\n"
            f"📍 Pickup         : {best_order['pickup_location']}\n"
            f"🏁 Delivery       : {best_order['delivery_location']}\n\n"
            f"💡 Recommendation : {recommendation}"
        )
    else:
        return "No orders available to evaluate."
    


def get_order_recommendation(order_id: int) -> str:
    """
    Provides a recommendation based on the order's score.
    """
    print(f"Hello1")

    # Retrieve the order from the knowledge base
    order = next((order for order in KNOWLEDGE_BASE["orders"] if order["order_id"] == order_id), None)

    # Debug: Print out the retrieved order
    print(f"Debug1 — Retrieved order for ID {order_id}: {order}")
    
    if not order:
        return "Order not found."
    
    # Calculate the order score
    score = calculate_order_score(order)

    # Common info to include in all responses
    info = (
        f"Order ID {order_id}: Pickup at {order['pickup_location']}, "
        f"deliver to {order['delivery_location']}. "
        f"Reward: RM{order['reward']}, "
        f"Time Estimate: {order['time_estimate']} mins, "
        f"Traffic: {order['traffic_condition'].capitalize()}, "
        f"Priority: {order['priority'].capitalize()}.\n"
    )
    
    # Provide recommendation based on score
    if score >= 15:
        recommendation = "✅ Highly recommended! The order has a great reward and favorable conditions."
    elif score >= 10:
        recommendation = "👍 Recommended. The order is decent but has some drawbacks."
    else:
        recommendation = "⚠️ Not recommended. The order has a low reward or less efficient route."


    return info + '\n' + recommendation

