from math import log
import requests
import json
from logger import Logger

logger = Logger("GBookingService")

'''
For reference, this is what the AI will knows about each category.
The AI will provide the args dictionary and expects the return values specified below.
The AI will also provide a human readable response based on the category and the args provided.
You will need to implement the functions for each category and return the values specified in the return_values list.

CREATE_APPOINTMENT: { 
                        "args": {
                                    "doctor_name": "<doctor_name>",
                                    "specialty": "<specialty>", 
                                    "date": "<date>", 
                                    "time": "<time>"
                                    "patient_name": "<patient_name>",
                                    "patient_id": "<patient_id>"
                                },
                        "return_values": ["appointment_id"] 
                    }
CANCEL_APPOINTMENT: {
                        "args": {
                                    "appointment_id": "<appointment_id>"
                                },
                        "return_values": [] 
                    }
RESCHEDULE_APPOINTMENT: {
                        "args": {
                                    "appointment_id": "<appointment_id>", 
                                    "new_date": "<new_date>", 
                                    "new_time": "<new_time>"
                                }, 
                        "return_values": [] 
                    }
GET_APPOINTMENT_DETAILS: {
                        "args": {
                                    "appointment_id": "<appointment_id>"
                                },
                        "return_values": ["appointment_id", "doctor_name", "specialty", "date", "time", "patient_name", "patient_id"] 
                    }
GET_NEXT_AVAILABLE_TIMESLOT_FOR_APPOINTMENT: {
                        "args": {
                                    "doctor_name": "<doctor_name>", 
                                    "specialty": "<specialty>",
                                    "date": "<date>"
                                }, 
                        "return_values": ["list_of_time_slots"] 
                    }
GET_DOCTOR_DETAILS: {
                        "args": {}, 
                        "return_values": [] 
                    } --> TBD 
GET_HOSPITAL_DETAILS: {
                        "args": {}, 
                        "return_values": [] 
                    } --> TBD 
GET_PATIENT_DETAILS: {
                        "args": {}, 
                        "return_values": [] 
                    } --> TBD 
GET_SERVICES:      {
                        "args": {}, 
                        "return_values": [] 
                    } --> TBD 
'''

class GBookingService:
    """
    A class to handle the GBooking service operations.
    It maps the category of the user request to the appropriate function and executes it.
    For now, it will contain placeholder functions for each category.
    The actual implementation of these functions will depend on the specific requirements and the data sources available.
    
    """
    def __init__(self):
        """
        Map the category and arguments to the appropriate booking function.
        """        
        self.category_map = {
            "CREATE_APPOINTMENT": self.__create_appointment,
            "CANCEL_APPOINTMENT": self.__cancel_appointment,
            "RESCHEDULE_APPOINTMENT": self.__reschedule_appointment,
            "GET_APPOINTMENT_DETAILS": self.__get_appointment_details,
            "GET_NEXT_AVAILABLE_TIMESLOT_FOR_APPOINTMENT": self.__get_next_available_time_slots,
            "GET_DOCTOR_DETAILS": self.__get_doctor_details,
            "GET_HOSPITAL_DETAILS": self.__get_hospital_details,
            "GET_PATIENT_DETAILS": self.__get_patient_details,
            "GET_SERVICES": self.__get_services,
        }
    
    def gbooking_invoker(self, category, args: dict):
        logger.debug(f"Invoking category: {category} with args: {args}")
        # invoke the appropriate function based on the category and pass the arguments to it
        if category not in self.category_map:
            raise ValueError(f"Invalid category: {category}.")
        return self.category_map.get(category)(**args)
    
    def __get_next_available_time_slots(self, **kwargs):
        doctor_name = kwargs.get("doctor_name")
        specialty = kwargs.get("specialty")
        date = kwargs.get("date")
        # Here you would typically call an API or a database to get the next available time slots
        # For now, we will just return a dummy list of time slots

        return [", ".join(["09:00", "10:00", "11:00", "14:00", "15:00"])]

    def __get_doctor_details(self, **kwargs):
        pass

    def __get_hospital_details(self, **kwargs):
        pass

    def __get_patient_details(self, **kwargs):
        pass

    def __get_services(self, **kwargs):
        pass

    def __create_appointment(self, **kwargs):
        doctor_name = kwargs.get("doctor_name")
        specialty = kwargs.get("specialty") 
        date = kwargs.get("date") 
        time = kwargs.get("time")
        patient_name = kwargs.get("patient_name")
        patient_id = kwargs.get("patient_id")
        # Here you would typically call an API or a database to create the appointment
        # For now, we will just return a dummy appointment ID

        # return 1 value based on the above specifications
        return "123456" # Dummy appointment ID

    def __cancel_appointment(self, **kwargs):
        appointment_id = kwargs.get("appointment_id")
        # Here you would typically call an API or a database to cancel the appointment
        return

    def __reschedule_appointment(self, **kwargs):
        appointment_id = kwargs.get("appointment_id")
        new_date = kwargs.get("new_date")
        new_time = kwargs.get("new_time")
        # Here you would typically call an API or a database to reschedule the appointment

        return

    def __get_appointment_details(self, **kwargs):
        appointment_id = kwargs.get("appointment_id")
        # Here you would typically call an API or a database to get the appointment details
        # For now, we will just return dummy appointment details

        return "1245", "Dr. Smith", "Cardiology", "7/5/2025", "14:00", "John Appleseed", "1234854545" # Dummy appointment details



"""
gbooking = GBookingService()  # Create an instance of the GBookingService class
return_values = gbooking.gbooking_invoker("GET_NEXT_AVAILABLE_TIMESLOT_FOR_APPOINTMENT", {"doctor_name": "<doctor_name>", "specialty": "<specialty>","date": "<date>"})  # Create a reference to the gbooking_invoker method for easy access

human_readable_response = 'Sure! I can help you with that. Here are some available time slots for an appointment with Dr. Sam in Cardiology tomorrow: <1>. Please let me know which one works for you.'
if return_values is not None:
    # replace indexed values in the human-readable response with the actual values from the return_values
    for i in range(len(return_values)):
        human_readable_response = human_readable_response.replace(f"<{i+1}>", str(return_values[i]))
print(human_readable_response)  # Print the final human-readable response
"""