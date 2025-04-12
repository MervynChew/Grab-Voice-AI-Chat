import re
from typing import Dict, List, Any

# Knowledge Base
KNOWLEDGE_BASE: Dict[str, Any] = {
    "general_info": {
        "app_name": "Grab Driver Assistant",
        "capabilities": [
            "Voice transcription", "Natural language understanding",
            "Notifying of new ride requests (simulated)",
            "Managing ride acceptance/rejection (simulated)",
            "Providing delivery order information",
            "Suggesting best delivery orders based on preference",
            "Multi-turn conversations"
        ],
        "supported_languages": [
            "English", "Chinese", "Spanish", "French", "Malay",
            "Sabah Malay", "Sarawak Malay", "Kelantanese Malay",
            "Terengganu Malay", "Tamil (Malaysia)", "Mandarin (Malaysia)",
            "Hokkien", "Cantonese"
        ],
    },
    "faqs": {
        "what_can_you_do": "I can notify you about new ride requests, answer questions, and help you on the road.",
        "how_to_use": "Just speak your command or question clearly.",
        "voice_quality": "For best results, speak clearly, especially in noisy environments.",
        "check_rides": "Ask me 'Are there any new rides?' or 'Check for rides'.",
        "check_deliveries": "Ask me 'Suggest a delivery order' or 'What are the details for delivery order 5?'"
    },
    "conversation_guidelines": {
        "greeting": "Hello! Ready to drive?",
        "clarification": "Could you please provide more details about that?",
        "error": "Sorry, I didn't quite catch that. Could you please repeat?",
        "ride_notification": "New ride request: Pickup near {pickup}, drop-off at {destination}. Estimated fare {fare}. Say 'accept ride' or 'reject ride'.",
        "no_rides": "No new ride requests at the moment.",
        "ride_accepted": "Okay, ride accepted. Proceed to pickup.",
        "ride_rejected": "Okay, ride rejected.",
        "ride_accepted_id": "Okay, accepting ride {ride_id}. Proceed to pickup.",
        "delivery_accepted": "Okay, accepting delivery order {order_id}."
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
    ],
    # New section for ride requests
    "ride_requests": [
        {"ride_id": 101, "pickup_location": "KLCC", "destination": "Bangsar South", "estimated_fare": 18, "time_estimate": 25, "passenger_rating": 4.8, "traffic_condition": "heavy"},
        {"ride_id": 102, "pickup_location": "Pavilion Bukit Bintang", "destination": "Mont Kiara", "estimated_fare": 22, "time_estimate": 30, "passenger_rating": 4.9, "traffic_condition": "heavy"},
        {"ride_id": 103, "pickup_location": "Sunway Pyramid", "destination": "Subang Airport", "estimated_fare": 15, "time_estimate": 20, "passenger_rating": 4.7, "traffic_condition": "moderate"},
        {"ride_id": 104, "pickup_location": "Mid Valley Megamall", "destination": "Damansara Utama", "estimated_fare": 12, "time_estimate": 15, "passenger_rating": 5.0, "traffic_condition": "light"},
        {"ride_id": 105, "pickup_location": "1 Utama Shopping Centre", "destination": "TTDI", "estimated_fare": 9, "time_estimate": 10, "passenger_rating": 4.6, "traffic_condition": "light"}
    ]
}

def get_knowledge_base_context(driver_type: str) -> str:
    """
    Formats the relevant knowledge base sections into a string context 
    based on the driver type ('ride' or 'delivery').
    """
    context = "Knowledge Base Information:\n\n"
    kb = KNOWLEDGE_BASE # Shortcut

    # General Info (Always include? Or tailor? Let's tailor slightly)
    context += "General Information:\n"
    context += f"app_name: {kb['general_info']['app_name']}\n"
    context += f"supported_languages: {', '.join(kb['general_info']['supported_languages'])}\n"
    context += "capabilities: "
    capabilities = []
    if driver_type == 'ride':
        capabilities = [c for c in kb['general_info']['capabilities'] if 'delivery' not in c.lower()]
    elif driver_type == 'delivery':
        capabilities = [c for c in kb['general_info']['capabilities'] if 'ride' not in c.lower()]
    else: # Default or unknown type? Include all for now.
        capabilities = kb['general_info']['capabilities']
    context += f"{', '.join(capabilities)}\n"

    # FAQs (Filter based on type)
    context += "\nFrequently Asked Questions:\n"
    for question, answer in kb["faqs"].items():
        if driver_type == 'ride' and ('delivery' in question or 'deliveries' in question):
            continue
        if driver_type == 'delivery' and ('ride' in question or 'rides' in question):
            continue
        # Adjust answers if needed based on type (Example)
        if question == "what_can_you_do":
             if driver_type == 'ride':
                 answer = "I can notify you about new ride requests, answer questions, and help you on the road."
             elif driver_type == 'delivery':
                 answer = "I can help you manage delivery orders, find the best ones, answer questions, and assist you."
        context += f"Q: {question}\nA: {answer}\n"

    # Delivery Orders (Only for delivery drivers)
    if driver_type == 'delivery':
        context += "\nAvailable Delivery Orders: (Details available upon request)\n"
        # Maybe list a few IDs or just mention they exist?
        # context += f"IDs: {[o['order_id'] for o in kb['orders'][:3]]}...\n"
        context += "You can ask for suggestions or details about specific order IDs.\n"
        
    # Ride Requests (Only for ride drivers)
    if driver_type == 'ride':
        context += "\nAvailable Ride Requests: (Details available upon request)\n"
        context += "You can ask for the best ride or details about specific ride IDs.\n"

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
        recommendation = "⚠ Not recommended. The order has a low reward or less efficient route."


    return info + '\n' + recommendation


def get_suggested_orders(preference: str, count: int = 3) -> str:
    """
    Sorts orders based on preference and returns a concise, comparative list 
    of top orders.
    """
    orders = KNOWLEDGE_BASE["orders"]
    if not orders:
        return "No orders available right now."

    # --- Sorting Logic (remains the same) ---
    sorted_orders = []
    pref_desc = ""
    if preference == "reward":
        sorted_orders = sorted(orders, key=lambda o: o.get("reward", 0), reverse=True)
        pref_desc = "highest reward"
    elif preference == "time":
        sorted_orders = sorted(orders, key=lambda o: o.get("time_estimate", float('inf')))
        pref_desc = "shortest time"
    elif preference == "traffic":
        traffic_sort_map = {"light": 0, "moderate": 1, "heavy": 2}
        sorted_orders = sorted(orders, key=lambda o: traffic_sort_map.get(o.get("traffic_condition", "heavy"), 2))
        pref_desc = "lightest traffic"
    else:
        sorted_orders = sorted(orders, key=calculate_order_score, reverse=True)
        pref_desc = "best overall score"

    top_orders = sorted_orders[:count]

    if not top_orders:
        return "Couldn't find orders matching that preference."

    # --- Build Comparative Response --- 
    response = f"Okay, prioritizing {pref_desc}. Here are the top options:\n"

    for i, order in enumerate(top_orders):
        order_id = order['order_id']
        reward = order['reward']
        time = order['time_estimate']
        traffic = order['traffic_condition']
        
        # Basic description for each
        response += f"- Order {order_id}: RM{reward} reward, takes about {time} mins with {traffic} traffic."

        # Add comparative notes based on preference
        if i == 0:
            if preference == "reward": response += " (Highest reward)"
            elif preference == "time": response += " (Shortest time)"
            elif preference == "traffic": response += " (Lightest traffic)"
        elif i == 1: # Compare second to first
            prev_order = top_orders[0]
            if preference == "reward": 
                if reward < prev_order['reward']: response += f" (Slightly less reward than Order {prev_order['order_id']})"
            elif preference == "time":
                if time > prev_order['time_estimate']: response += f" (Takes a bit longer than Order {prev_order['order_id']})"
            elif preference == "traffic":
                 prev_traffic_val = traffic_sort_map.get(prev_order['traffic_condition'], 2)
                 curr_traffic_val = traffic_sort_map.get(traffic, 2)
                 if curr_traffic_val > prev_traffic_val: response += f" (Slightly heavier traffic than Order {prev_order['order_id']})"
        # Add more comparisons if needed
        response += "\n" # Newline for next order

    response += "\nWhich one would you like details on, or say 'accept order number'?"

    return response.strip()

# --- New Functions for Ride Requests ---

def get_ride_request_details(ride_id: int) -> str:
    """
    Provides details for a specific ride request.
    """
    ride = next((r for r in KNOWLEDGE_BASE.get("ride_requests", []) if r["ride_id"] == ride_id), None)
    
    if not ride:
        return "Ride request not found."

    info = (
        f"Ride ID {ride_id}: Pickup at {ride['pickup_location']}, "
        f"Destination: {ride['destination']}. "
        f"Fare: ~RM{ride['estimated_fare']}, "
        f"Time: ~{ride['time_estimate']} mins, "
        f"Traffic: {ride['traffic_condition'].capitalize()}, "
        f"Passenger Rating: {ride['passenger_rating']} stars.\n"
    )
    # Simple recommendation based on fare/time
    if ride['estimated_fare'] / ride['time_estimate'] > 0.8:
        recommendation = "👍 Good fare for the estimated time."
    elif ride['estimated_fare'] / ride['time_estimate'] > 0.6:
        recommendation = "👌 Decent fare, consider traffic."
    else:
        recommendation = "🤔 Fare seems a bit low for the time/distance."
        
    return info + '\n' + recommendation

# New function for suggesting rides based on preference
def get_suggested_rides(preference: str, count: int = 3) -> str:
    """
    Sorts ride requests based on preference and returns a concise, comparative list 
    of top rides.
    """
    rides = KNOWLEDGE_BASE.get("ride_requests", [])
    if not rides:
        return "No ride requests available right now."

    # --- Sorting Logic for Rides ---
    sorted_rides = []
    pref_desc = ""
    if preference == "fare":
        sorted_rides = sorted(rides, key=lambda r: r.get("estimated_fare", 0), reverse=True)
        pref_desc = "highest fare"
    elif preference == "time":
        sorted_rides = sorted(rides, key=lambda r: r.get("time_estimate", float('inf')))
        pref_desc = "shortest time"
    elif preference == "rating":
        sorted_rides = sorted(rides, key=lambda r: r.get("passenger_rating", 0), reverse=True)
        pref_desc = "highest passenger rating"
    else: # Default to a balanced score (e.g., fare/time * rating?)
        # Simple default: fare first, then rating
        sorted_rides = sorted(rides, key=lambda r: (r.get('estimated_fare', 0), r.get('passenger_rating', 0)), reverse=True)
        pref_desc = "best overall (fare & rating)"

    top_rides = sorted_rides[:count]

    if not top_rides:
        return "Couldn't find rides matching that preference."

    # --- Build Comparative Response --- 
    response = f"Okay, prioritizing rides with {pref_desc}. Here are the top options:\n"

    for i, ride in enumerate(top_rides):
        ride_id = ride['ride_id']
        fare = ride['estimated_fare']
        time = ride['time_estimate']
        rating = ride['passenger_rating']
        pickup = ride['pickup_location'] # Added for context
        dest = ride['destination'] # Added for context
        
        # Basic description for each
        response += f"- Ride {ride_id}: From {pickup} to {dest}. Fare ~RM{fare}, Time ~{time} mins, Rating {rating} stars."

        # Add comparative notes based on preference (simplified example)
        if i == 0:
            if preference == "fare": response += " (Highest fare)"
            elif preference == "time": response += " (Shortest time)"
            elif preference == "rating": response += " (Highest rating)"
        response += "\n" # Newline for next ride

    response += "\nWhich ride would you like details on, or say 'accept ride number'?"

    return response.strip()