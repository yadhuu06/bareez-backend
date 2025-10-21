import asyncio
import random
from typing import Literal, Dict, Any, Callable


ServiceType = Literal["category", "sentiment", "response"]

def get_ai_analysis_service() -> Callable[[ServiceType, str], str]:


    MOCK_RESPONSES: Dict[str, str] = {
        "Positive": "Thank you for the wonderful feedback! We are delighted to hear you enjoyed your stay.",
        "Neutral": "Thank you for taking the time to share your feedback. We appreciate your input.",
        "Negative": "We sincerely apologize for the issues you experienced. We are looking into this immediately and will contact you directly to resolve this. Thank you for bringing this to our attention."
    }

    MOCK_CATEGORIES: list[str] = [
        "Housekeeping", "Maintenance", "Food & Beverage", "Front Desk", "Concierge"
    ]

    async def mock_ai_service_function(service_type: ServiceType, text: str) -> str:

        delay = random.uniform(0.5, 2)
        await asyncio.sleep(delay)

        text_lower = text.lower()

        if service_type == "sentiment":

            if any(word in text_lower for word in ["dirty", "stain", "broken", "leak", "noise", "unhappy", "terrible", "bad", "apology", "wait time"]):
                return "Negative"
            

            elif any(word in text_lower for word in ["great", "excellent", "loved", "amazing", "best", "perfect", "compliment", "wonderful"]):
                return "Positive"
            else:
                return "Neutral"
        
        elif service_type == "category":

            
            if any(word in text_lower for word in ["towels", "soap", "shampoo", "bedding", "cleaning"]):
                return "Housekeeping"
            elif any(word in text_lower for word in ["ac", "heating", "broken", "light", "plumbing", "fix", "maintenance"]):
                return "Maintenance"
            elif any(word in text_lower for word in ["food", "drink", "room service", "dinner", "breakfast", "bar"]):
                return "Food & Beverage"
            elif any(word in text_lower for word in ["check in", "check out", "key", "bill", "invoice"]):
                return "Front Desk"
            else:
                
                return "Concierge"
        
        elif service_type == "response":
           
            return MOCK_RESPONSES.get("Negative", "A smart response could not be generated at this time.")

        raise ValueError(f"Invalid service type: {service_type}")


    return mock_ai_service_function


async def get_ai_analysis_service_dep() -> Callable[[ServiceType, str], str]:
    """Dependency for use in FastAPI routes."""
    return get_ai_analysis_service()
