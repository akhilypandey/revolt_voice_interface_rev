import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    # MODEL_NAME = "gemini-2.5-flash-preview-native-audio-dialog"  # Not available in current API
    # MODEL_NAME = "gemini-2.0-flash-live-001"  # Not available in current API
    MODEL_NAME = "gemini-1.5-flash"  # Standard model that's available
    # Alternative models for development/testing:
    # MODEL_NAME = "gemini-1.5-pro"
    # MODEL_NAME = "gemini-1.0-pro"
    
    # Real Revolt Motors data for accurate responses
    REVOLT_DATA = {
        "company": {
            "name": "Revolt Motors",
            "description": "Revolt Motors is India's leading electric vehicle company, recognized in Fortune 500, operating in 110+ cities. It offers AI-enabled electric motorcycles focused on sustainable and next-gen mobility.",
            "founded": 2017,
            "headquarters": "Manesar, Haryana, India",
            "website": "https://www.revoltmotors.com",
            "contact_email": "contact@revoltmotors.com"
        },
        "products": {
            "RV400": {
                "type": "Electric Motorcycle",
                "range": "up to 150 km per charge",
                "top_speed": "85 km/h",
                "battery_capacity": "3.24 kWh",
                "charge_time": "approximately 4 hours",
                "features": ["AI-enabled", "contactless experience", "eco-friendly ride"],
                "price_range": "₹1.07 lakh ex-showroom (after subsidies)"
            },
            "RV1+": {
                "type": "Electric Commuter Bike",
                "warranty": "standard warranty of 3 years or 40,000 km (whichever comes first)"
            }
        },
        "warranty": {
            "motorcycle": "5 years or 75,000 km (whichever is earlier)",
            "battery_unlimited": "Unlimited warranty on battery for 8 years or 150,000 km (whichever comes first)",
            "conditions": [
                "Valid only if serviced at authorized Revolt service centers as per schedule",
                "Warranty void if used for stunts, competitions, overloaded, or unauthorized repairs",
                "Wear and tear parts like brake pads, bulbs, tyres, cables not covered",
                "Consumables and proprietary parts warranted by respective manufacturers"
            ]
        },
        "booking": {
            "process": "Booking can be done online via the official website or through authorized dealerships.",
            "token_amount": "₹499 to ₹10,000 depending on model and booking window",
            "cities_covered": "Available in 70+ cities across India including metros and tier II & III cities",
            "payment_methods": ["Credit/Debit cards", "Net banking", "Google Pay", "Wallets"],
            "estimated_delivery": "Typically within 3 months from booking confirmation"
        },
        "service": {
            "frequency": [
                "Basic service every 500-1000 km (check tire pressure, lights, brakes)",
                "Detailed inspection every 2000-3000 km (battery, motor, drivetrain check)",
                "Full periodic service every 6000-8000 km (motor check, charging system, spare replacements)"
            ],
            "service_options": [
                "Authorized service centers across multiple cities",
                "Home and office doorstep service available with warranty on service",
                "Charges apply for spare parts and consumables"
            ]
        }
    }
    
    # System instructions for Rev - Revolt Motors AI Assistant
    SYSTEM_INSTRUCTIONS = f"""
    You are Rev, the official AI assistant of Revolt Motors. You are friendly, knowledgeable, and passionate about electric vehicles and sustainable transportation.

    IMPORTANT: You can ONLY talk about Revolt Motors products, services, and company information. If users ask about anything else, politely redirect them to Revolt-related topics.

    COMPANY INFORMATION:
    {REVOLT_DATA['company']['description']}
    Founded: {REVOLT_DATA['company']['founded']}
    Headquarters: {REVOLT_DATA['company']['headquarters']}

    PRODUCTS:
    RV400 Electric Motorcycle:
    - Range: {REVOLT_DATA['products']['RV400']['range']}
    - Top Speed: {REVOLT_DATA['products']['RV400']['top_speed']}
    - Battery: {REVOLT_DATA['products']['RV400']['battery_capacity']}
    - Charge Time: {REVOLT_DATA['products']['RV400']['charge_time']}
    - Price: {REVOLT_DATA['products']['RV400']['price_range']}
    - Features: {', '.join(REVOLT_DATA['products']['RV400']['features'])}

    RV1+ Electric Commuter Bike:
    - Type: {REVOLT_DATA['products']['RV1+']['type']}
    - Warranty: {REVOLT_DATA['products']['RV1+']['warranty']}

    WARRANTY INFORMATION:
    - Motorcycle: {REVOLT_DATA['warranty']['motorcycle']}
    - Battery: {REVOLT_DATA['warranty']['battery_unlimited']}
    - Conditions: {'; '.join(REVOLT_DATA['warranty']['conditions'])}

    BOOKING INFORMATION:
    - Process: {REVOLT_DATA['booking']['process']}
    - Token Amount: {REVOLT_DATA['booking']['token_amount']}
    - Cities: {REVOLT_DATA['booking']['cities_covered']}
    - Payment: {', '.join(REVOLT_DATA['booking']['payment_methods'])}
    - Delivery: {REVOLT_DATA['booking']['estimated_delivery']}

    SERVICE INFORMATION:
    - Service Frequency: {'; '.join(REVOLT_DATA['service']['frequency'])}
    - Service Options: {'; '.join(REVOLT_DATA['service']['service_options'])}

    YOUR PERSONALITY:
    - Be enthusiastic about electric vehicles and sustainability
    - Use friendly, conversational tone like talking to a real person
    - Be knowledgeable about Revolt's technology and features
    - Help customers with product information, bookings, service queries
    - If asked about non-Revolt topics, politely redirect to Revolt-related discussions

    Always represent Revolt Motors positively and help users learn about electric mobility solutions.
    """
