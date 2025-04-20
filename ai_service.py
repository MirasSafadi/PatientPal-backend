"""
    This Module contains the AI service for the application.
    It includes the AI service class, which is responsible for handling the AI-related tasks.
    This service will utilize the GEMINI_API_KEY for AI functionalities.
    The AI service will be used to interact with the AI model and perform various tasks such as generating responses, etc.
    The AI service will be used in the socketIO.py file to handle the AI-related requests in the chat.
"""
from logger import Logger
import settings, constants, json, requests
from pprint import pprint

logger = Logger("ai_service_logger")

AI_REQUEST_URL  = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={settings.GEMINI_API_KEY}"
REQUEST_BODY = """
{
    "contents": [
        {
            "parts": [
                {
                    "text": "Explain how AI works"
                }
            ]
        }
    ]
}
"""
PROMPT_TEMPLATE = '''
    You are a helpful assistant helping people manage their appointments in a hostpital. Your task is to assist the user with their queries.
    Once the user asks a question, you will analyze their query, classify it into one of the following categories: 
    CREATE_APPOINTMENT, CANCEL_APPOINTMENT, RESCHEDULE_APPOINTMENT, GET_APPOINTMENT_DETAILS, GET_DOCTOR_DETAILS, 
    GET_HOSPITAL_DETAILS, GET_PATIENT_DETAILS, GET_SERVICES, GET_NEXT_AVAILABLE_TIMESLOT_FOR_APPOINTMENT, .
    
    After classifying the query, a function will run to execute the requested operation, so you will also need to provide a list of arguments.
    You will then generate a human readable response based on the user's query and the category it belongs to.
    The user will not always give you all the information you need, so you will need to ask them for any missing information. 
    Only once you have all the necessary information, you will execute the function and provide a response like the format below.

    If you do not have all the information you need, you will ask the user for the missing information and provide a response in the following format:
    {{
        "category": "INCOMPLETE",
        "response": "<your follow up question>"
    }}
    Do as many follow up questions as you need to get all the information you need.
    Once the user provides the missing information, you will reclassify the query and provide a response in the format below.
    if the user query is not clear or does not belong to any of the categories, you will ask them to rephrase their query or provide more information.

    Your final response should be in a JSON format with the following structure:
    {{
        "category": "<category>",
        "args": {{
            "arg1": "<value1>",
            "arg2": "<value2>"
        }},
        "response": "<human_readable_response>"
    }}

    Example:
    User: I want to book an appointment with Dr. Smith for Cardiology next week.
    Assistant: 
    {{
        "category": "GET_NEXT_AVAILABLE_TIMESLOT_FOR_APPOINTMENT",
        "args": {{
            "doctor_name": "Dr. Smith",
            "specialty": "Cardiology"
        }},
        "response": "Sure! I can help you with that. Here are some available time slots for an appointment with Dr. Smith in Cardiology next week: [list of time slots]. Please let me know which one works for you."
    }}

    User: {user_query}
'''

class AIService:
    def __init__(self):
        pass

    def generate_content(self, prompt):
        request_body = json.loads(REQUEST_BODY)
        request_body["contents"][0]["parts"][0]["text"] = prompt
        response = requests.post(
            AI_REQUEST_URL,
            json=request_body,
        )
        return response.json()


print(PROMPT_TEMPLATE)
print(PROMPT_TEMPLATE.format(user_query="I want to book an appointment with Dr. Smith for Cardiology next week."))
# ai_service = AIService()
# response = ai_service.generate_content("tell me a joke")
# print(response["candidates"][0]["content"]["parts"][0]["text"])