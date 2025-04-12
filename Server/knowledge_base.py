from typing import Dict, List

# Knowledge Base Structure
KNOWLEDGE_BASE = {
    "general_info": {
        "app_name": "Voice AI Chat Assistant",
        "capabilities": [
            "Voice transcription",
            "Natural language understanding",
            "Contextual responses",
            "Multi-turn conversations"
        ],
        "supported_languages": ["English"]
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
    }
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