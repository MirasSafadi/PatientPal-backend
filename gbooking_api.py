import requests

class GBookingAPI:
    def __init__(self, user=None, token=None):
        """
        Initialize the GBookingAPI instance.
        :param user: Username for authentication (optional for guest access)
        :param token: Token for authentication (optional for guest access)
        """
        self.url = "https://api.gbooking.net/json/"
        self.user = user
        self.token = token

    def _build_payload(self, method, params):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params
        }
        if self.user and self.token:
            payload["cred"] = {
                "user": self.user,
                "token": self.token
            }
        return payload

    def _post(self, method, params):
        payload = self._build_payload(method, params)
        response = requests.post(self.url, json=payload)
        response_data = response.json()

        if 'error' in response_data:
            raise Exception(f"API Error: {response_data['error']['message']}")

        return response_data.get("result", {})

    ### פונקציות לפי רמות גישה:

    # GUEST: קריאות ציבוריות (ללא התחברות)
    def get_top_services(self, business_id):
        return self._post("business.get_top_services", {
            "business": {"id": business_id}
        })

    def get_business_info(self, business_id):
        return self._post("business.get", {
            "id": business_id
        })

    # CLIENT: קריאות עבור לקוח מסוים
    def reserve_appointment(self, business_id, client_info, start, services):
        """
        Reserve an appointment.
        client_info = {"full_name": "John Doe", "phone": "+123456789"}
        start = "2025-05-01T12:00:00Z"
        services = [{"id": "service_id"}]
        """
        return self._post("appointment.reserve", {
            "business": {"id": business_id},
            "client": client_info,
            "start": start,
            "services": services
        })

    def update_appointment(self, appointment_id, update_fields):
        """
        Update an existing appointment.
        update_fields = {"start": "2025-05-02T14:00:00Z"}
        """
        return self._post("appointment.update", {
            "id": appointment_id,
            **update_fields
        })

    def cancel_appointment(self, appointment_id):
        """
        Cancel an appointment.
        """
        return self._post("appointment.cancel", {
            "id": appointment_id
        })

    # ADMIN: קריאות ניהוליות לעסקים/רשתות
    def get_all_employees(self, business_id):
        return self._post("employee.get_many", {
            "business": {"id": business_id}
        })

    def get_branch_network(self, branch_id):
        return self._post("branch.get_network", {
            "id": branch_id
        })

    def get_client_info(self, client_id):
        return self._post("client.get", {
            "id": client_id
        })

    ### פונקציה עזר לשנות יוזר/טוקן תוך כדי עבודה
    def set_credentials(self, user, token):
        self.user = user
        self.token = token
    # ✔️ 1. קבלת נתונים מלאים על עסק
def get_business_full_data(self, business_id):
    """
    Get complete business data including settings, name, address, phone, working schedule, etc.
    """
    return self._post("business.get", {"id": business_id})

# ✔️ 2. קבלת מידע על סניף בודד
def get_branch_info(self, branch_id):
    """
    Get information about a single branch (shop, salon, etc.).
    """
    return self._post("branch.get", {"id": branch_id})

# ✔️ 3. קבלת מידע על Showcase
def get_showcase_info(self, showcase_id):
    """
    Get information about a showcase (group of branches).
    """
    return self._post("showcase.get", {"id": showcase_id})

# ✔️ 4. קבלת מידע על רשת סניפים (Branch Network)
def get_branch_network_info(self, branch_id):
    """
    Get network information related to a branch (other branches connected to it).
    """
    return self._post("branch.get_network", {"id": branch_id})
# ✔️ קבלת מידע מלא על עובד מסוים לפי ID
def get_employee_info(self, employee_id):
    """
    Get detailed information about a specific employee.
    """
    return self._post("employee.get", {"id": employee_id})

# ✔️ קבלת כל העובדים לעסק מסוים (אם רוצים לסנן אחר כך)
def get_all_employees(self, business_id):
    """
    Get a list of all employees of a specific business.
    """
    return self._post("employee.get_many", {
        "business": {"id": business_id}
    })

# ✔️ קבלת שירותים של עובד ספציפי
def get_employee_services(self, employee_id):
    """
    Get a list of services provided by a specific employee.
    """
    employee_info = self.get_employee_info(employee_id)
    return employee_info.get("employee", {}).get("services", [])

# ✔️ קבלת מקצוע ותיאור נוסף של עובד
def get_employee_profession_details(self, employee_id):
    """
    Get the profession and additional description of an employee.
    """
    employee_info = self.get_employee_info(employee_id)
    return {
        "profession": employee_info.get("employee", {}).get("profession"),
        "additional_info": employee_info.get("employee", {}).get("info")
    }

# ✔️ קבלת פרטי יצירת קשר (טלפון, אימייל) של עובד
def get_employee_contact_info(self, employee_id):
    """
    Get phone number and email of an employee.
    """
    employee_info = self.get_employee_info(employee_id)
    return {
        "phone": employee_info.get("employee", {}).get("phone"),
        "email": employee_info.get("employee", {}).get("email")
    }
# ✔️ קבלת כל השירותים לעסק
def get_all_services(self, business_id):
    """
    Get a list of all services (taxonomy) offered by the business.
    """
    return self._post("taxonomy.get_many", {
        "business": {"id": business_id}
    })

# ✔️ קבלת שירות לפי ID
def get_service_info(self, service_id):
    """
    Get detailed information about a specific service.
    """
    return self._post("taxonomy.get", {"id": service_id})

# ✔️ קבלת שירותים עבור עובד מסוים
def get_employee_services(self, employee_id):
    """
    Get services provided by a specific employee.
    (already exists — נשאיר אותו גם פה לשימוש נוח)
    """
    employee_info = self.get_employee_info(employee_id)
    return employee_info.get("employee", {}).get("services", [])

# ✔️ קבלת שם, תיאור, מחיר והנחות של שירות
def get_service_details(self, service_id):
    """
    Get name, description, duration, price, and discounts of a service.
    """
    service_info = self.get_service_info(service_id)
    service = service_info.get("service", {})
    return {
        "name": service.get("name"),
        "description": service.get("description"),
        "duration": service.get("duration"),  # minutes
        "price": service.get("price"),
        "discounts": service.get("discounts")
    }
def get_static_business_data(self, business_id, 
                              only_active_workers=True,
                              worker_sorting_type="none",
                              with_networks=False,
                              show_inactive_workers=False):
    """
    Get static business data including employees, services, and settings.

    Args:
        business_id (str): ID of the business
        only_active_workers (bool): Return only active workers if True
        worker_sorting_type (str): 'none', 'workload', 'most_free'
        with_networks (bool): Include branch network data
        show_inactive_workers (bool): Include inactive employees if True

    Returns:
        dict: Business static data
    """

    params = {
        "business": {"id": business_id},
        "only_active_workers": only_active_workers,
        "worker_sorting_type": worker_sorting_type,
        "with_networks": with_networks,
        "show_inactive_workers": show_inactive_workers
    }

    return self._post("business.get_static", params)
def get_showcase_business_data(self, business_id, 
                                only_active_workers=True,
                                worker_sorting_type="none",
                                with_networks=False,
                                show_inactive_workers=False):
    """
    Get and process showcase business data.
    
    Returns:
        dict: structured data including origin branch info and services per employee.
    """

    # שולפים את כל הנתונים הסטטיים
    business_data = self.get_static_business_data(
        business_id,
        only_active_workers=only_active_workers,
        worker_sorting_type=worker_sorting_type,
        with_networks=with_networks,
        show_inactive_workers=show_inactive_workers
    )

    # האם מדובר בעסק מסוג Showcase
    is_showcase = business_data.get("business", {}).get("general_info", {}).get("isShowcase", False)

    # טיפול בעובדים
    workers = []
    for resource in business_data.get("resources", []):
        worker_info = {
            "id": resource.get("id"),
            "full_name": resource.get("full_name"),
            "status": resource.get("status"),
            "displayInWidget": resource.get("displayInWidget", False),
            "origin_business_id": resource.get("originBusinessID"),
            "origin_general_info": resource.get("origin_general_info", {}),
            "origin_taxonomy_ids": resource.get("originTaxonomyIDs", []),
            "taxonomies": resource.get("taxonomies", [])
        }
        workers.append(worker_info)

    # טיפול בשירותים
    services = []
    for taxonomy in business_data.get("taxonomies", []):
        service_info = {
            "id": taxonomy.get("id"),
            "name": taxonomy.get("name"),
            "price": taxonomy.get("price", {}).get("amount", None),
            "showcases": taxonomy.get("showcases", [])
        }
        services.append(service_info)

    return {
        "is_showcase": is_showcase,
        "workers": workers,
        "services": services,
        "raw_data": business_data  # אפשר לשמור גם את כל המידע המקורי למי שצריך
    }
def get_branch_network_data(self, branch_id, source="GENERAL"):
    """
    Get list of network branch IDs for a given branch.

    Args:
        branch_id (str): ID of one of the branches
        source (str): Source of networkWidgetConfiguration (default is "GENERAL")

    Returns:
        list: List of branch IDs in the network
    """

    params = {
        "business": {"id": branch_id},
        "source": source
    }

    response = self._post("business.get_network_data", params)

    # הוצאת מזהי הסניפים מהרשת
    network_branches = []
    try:
        network_widget_config = response.get("networkWidgetConfiguration", {})
        if source in network_widget_config:
            network_branches = network_widget_config[source].get("businessIDs", [])
        else:
            network_branches = network_widget_config.get("GENERAL", {}).get("businessIDs", [])
    except Exception as e:
        print(f"Error parsing network branches: {e}")

    return network_branches
def get_crac_timetable_slots(self, business_id, resource_ids, date_from, date_to):
    """
    Get available timetable slots from CRAC server (deprecated).

    Args:
        business_id (str): ID of the business
        resource_ids (list): List of employee (resource) IDs
        date_from (str): Start date ISO format ("YYYY-MM-DDTHH:MM:SS.sssZ")
        date_to (str): End date ISO format

    Returns:
        dict: Timetable slots data
    """

    # Note: Different URL for CRAC
    crac_url = "https://crac-prod3.gbooking.ru/rpc"

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "cred": {},  # Guest access - no credentials
        "method": "Crac.GetCRACResourcesAndRooms",
        "params": [{
            "business": {
                "id": business_id
            },
            "filters": {
                "resources": resource_ids,
                "date": {
                    "from": date_from,
                    "to": date_to
                }
            }
        }]
    }

    response = requests.post(crac_url, json=payload)
    response_data = response.json()

    if 'error' in response_data:
        raise Exception(f"CRAC API Error: {response_data['error']['message']}")

    return response_data.get("result", {})
def get_showcase_timetable_slots(self, business_info, resources, taxonomies, date_from, date_to):
    """
    Get available timetable slots from CRACSlots server for a showcase.

    Args:
        business_info (dict): Business object containing id, widget_configuration, general_info
        resources (list): List of resources, each with 'resource' and 'business' fields
        taxonomies (list): List of taxonomy (service) IDs
        date_from (str): Start date ISO format
        date_to (str): End date ISO format

    Returns:
        dict: Timetable slots ready for booking
    """

    cracslots_url = "https://cracslots.gbooking.ru/rpc"

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "cred": {},  # Guest access
        "method": "CracSlots.GetCRACDistributedResourcesAndRooms",
        "params": {
            "business": business_info,
            "filters": {
                "resources": resources,
                "taxonomies": taxonomies,
                "rooms": [],
                "date": {
                    "from": date_from,
                    "to": date_to
                }
            }
        }
    }

    response = requests.post(cracslots_url, json=payload)
    response_data = response.json()

    if 'error' in response_data:
        raise Exception(f"CRACSlots API Error: {response_data['error']['message']}")

    return response_data.get("result", {})
def get_branch_timetable_slots(self, business_info, resources_with_durations, taxonomies, date_from, date_to):
    """
    Get available timetable slots from CRACSlots server for a branch.

    Args:
        business_info (dict): Business object containing id, widget_configuration, general_info
        resources_with_durations (list): List of resources, each with 'id' and 'duration'
        taxonomies (list): List of taxonomy (service) IDs
        date_from (str): Start date ISO format
        date_to (str): End date ISO format

    Returns:
        dict: Timetable slots ready for booking
    """

    cracslots_url = "https://cracslots.gbooking.ru/rpc"

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "cred": {},  # Guest access
        "method": "CracSlots.GetCRACResourcesAndRooms",
        "params": {
            "business": business_info,
            "filters": {
                "resources": resources_with_durations,
                "taxonomies": taxonomies,
                "rooms": [],
                "date": {
                    "from": date_from,
                    "to": date_to
                }
            }
        }
    }

    response = requests.post(cracslots_url, json=payload)
    response_data = response.json()

    if 'error' in response_data:
        raise Exception(f"CRACSlots Branch API Error: {response_data['error']['message']}")

    return response_data.get("result", {})
def get_closest_appointment_showcase(self, business_id, taxonomy_id, resource_ids):
    """
    Get the closest appointment date for a service across a list of employees (for showcase).

    Args:
        business_id (str): ID of the showcase business
        taxonomy_id (str): ID of the showcase service
        resource_ids (list): List of showcase employee IDs

    Returns:
        list: List of resources with their closest available date
    """

    crac_url = "https://crac-prod3.gbooking.ru/rpc"

    payload = {
        "jsonrpc": "2.0",
        "id": 9,
        "cred": {},
        "method": "Crac.CRACDistributedResourcesFreeByDate",
        "params": [
            {
                "business": {
                    "id": business_id
                },
                "taxonomy": {
                    "id": taxonomy_id
                },
                "resources": resource_ids
            }
        ]
    }

    response = requests.post(crac_url, json=payload)
    response_data = response.json()

    if 'error' in response_data:
        raise Exception(f"CRAC Showcase Closest Appointment Error: {response_data['error']['message']}")

    return response_data.get("result", {}).get("Free", [])
def get_closest_appointment_branch(self, taxonomy_id, resource_ids, duration):
    """
    Get the closest appointment date for a service across a list of employees (for branch).

    Args:
        taxonomy_id (str): ID of the service (taxonomy)
        resource_ids (list): List of employee IDs
        duration (int): Duration of the service in minutes

    Returns:
        list: List of resources with their closest available date
    """

    crac_url = "https://crac-prod3.gbooking.ru/rpc"

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "cred": {},
        "method": "Crac.CRACResourcesFreeByDate",
        "params": [
            {
                "taxonomy": {
                    "id": taxonomy_id
                },
                "resources": resource_ids,
                "duration": duration
            }
        ]
    }

    response = requests.post(crac_url, json=payload)
    response_data = response.json()

    if 'error' in response_data:
        raise Exception(f"CRAC Branch Closest Appointment Error: {response_data['error']['message']}")

    return response_data.get("result", {}).get("Free", [])
def get_closest_appointment_branch_v2(self, business_id, resource_ids, location, taxonomy_id="", duration=None, durations=None):
    """
    Get closest appointment dates for employees (branch, version 2).

    Args:
        business_id (str): ID of the branch business
        resource_ids (list): List of employee IDs
        location (str): Timezone, e.g., "Europe/Moscow"
        taxonomy_id (str, optional): ID of the service (optional, empty for all services)
        duration (int, optional): Default duration for all employees (optional)
        durations (list, optional): Specific duration per employee (optional)

    Returns:
        list: List of resources with their closest available date
    """

    crac_url = "https://crac-prod3.gbooking.ru/rpc"

    params = {
        "business": {
            "id": business_id
        },
        "taxonomy": {
            "id": taxonomy_id
        },
        "resources": resource_ids,
        "location": location
    }

    if duration is not None:
        params["duration"] = duration

    if durations is not None:
        params["durations"] = durations

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "cred": {},
        "method": "Crac.CRACResourcesFreeByDateV2",
        "params": [params]
    }

    response = requests.post(crac_url, json=payload)
    response_data = response.json()

    if 'error' in response_data:
        raise Exception(f"CRAC Branch v2 Closest Appointment Error: {response_data['error']['message']}")

    return response_data.get("result", {}).get("Free", [])
def reserve_appointment(self, business_id, taxonomy_id, resource_id, appointment_start,
                         duration, price_amount, price_currency, source, client_appear="NONE"):
    """
    Reserve (tentatively) an appointment slot.

    Args:
        business_id (str): Business ID
        taxonomy_id (str): Service ID
        resource_id (str): Employee ID
        appointment_start (str): Appointment start datetime in ISO format (e.g., '2024-05-01T15:00:00')
        duration (int): Duration of appointment in minutes
        price_amount (float): Price amount
        price_currency (str): Price currency (e.g., 'RUB')
        source (str): Source string for analytics
        client_appear (str): Client appearance status ("YES_APPEAR", "NO_APPEAR", "NONE")

    Returns:
        dict: Reserved appointment data
    """

    payload = {
        "jsonrpc": "2.0",
        "id": 19,
        "cred": {
            "token": self.token,
            "user": self.user
        },
        "method": "appointment.reserve_appointment",
        "params": {
            "appointment": {
                "start": appointment_start,
                "duration": duration,
                "price": {
                    "amount": price_amount,
                    "currency": price_currency
                }
            },
            "source": source,
            "business": {
                "id": business_id
            },
            "taxonomy": {
                "id": taxonomy_id
            },
            "client_appear": client_appear,
            "resource": {
                "id": resource_id
            }
        }
    }

    response = requests.post(self.url, json=payload)
    response_data = response.json()

    if 'error' in response_data:
        raise Exception(f"Reserve Appointment Error: {response_data['error']['message']}")

    return response_data.get("result", {})
def reserve_appointment_showcase(self, origin_business_id, business_id, taxonomy_id, resource_id, appointment_start,
                                  duration, price_amount, price_currency, source, client_appear="NONE"):
    """
    Reserve (tentatively) an appointment slot for a service from a showcase.

    Args:
        origin_business_id (str): Branch business ID where the employee actually works
        business_id (str): Showcase business ID
        taxonomy_id (str): Showcase service ID
        resource_id (str): Showcase employee ID
        appointment_start (str): Appointment start datetime in ISO format (e.g., '2024-05-01T13:00:00')
        duration (int): Duration of appointment in minutes
        price_amount (float): Price amount
        price_currency (str): Price currency (e.g., 'RUB')
        source (str): Source string for analytics
        client_appear (str): Client appearance status ("YES_APPEAR", "NO_APPEAR", "NONE")

    Returns:
        dict: Reserved appointment data
    """

    payload = {
        "jsonrpc": "2.0",
        "id": 19,
        "cred": {
            "token": self.token,
            "user": self.user
        },
        "method": "appointment.reserve_appointment",
        "params": {
            "originBusinessID": origin_business_id,
            "appointment": {
                "start": appointment_start,
                "duration": duration,
                "price": {
                    "amount": price_amount,
                    "currency": price_currency
                }
            },
            "source": source,
            "business": {
                "id": business_id
            },
            "taxonomy": {
                "id": taxonomy_id
            },
            "client_appear": client_appear,
            "resource": {
                "id": resource_id
            }
        }
    }

    response = requests.post(self.url, json=payload)
    response_data = response.json()

    if 'error' in response_data:
        raise Exception(f"Reserve Showcase Appointment Error: {response_data['error']['message']}")

    return response_data.get("result", {})
def add_client(self, business_id, name, surname, country_code, area_code, number, email=None):
    """
    Add a new client or fetch an existing one based on phone.

    Args:
        business_id (str): Business ID
        name (str): Client's first name
        surname (str): Client's last name
        country_code (str): Phone country code
        area_code (str): Phone area/provider code
        number (str): Rest of the phone number
        email (str, optional): Client's email address

    Returns:
        dict: Client data
    """

    client_data = {
        "name": name,
        "surname": surname,
        "phone": [
            {
                "country_code": country_code,
                "area_code": area_code,
                "number": number
            }
        ]
    }

    if email:
        client_data["email"] = [email]  # חייב להיות רשימה לפי הדוקומנטציה

    payload = {
        "jsonrpc": "2.0",
        "id": 18,
        "cred": {
            "token": self.token,
            "user": self.user
        },
        "method": "client.add_client",
        "params": {
            "business": {
                "id": business_id
            },
            "client": client_data
        }
    }

    response = requests.post(self.url, json=payload)
    response_data = response.json()

    if 'error' in response_data:
        raise Exception(f"Add Client Error: {response_data['error']['message']}")

    return response_data.get("result", {})
def update_client(self, client_id, business_id, name, surname, country_code, area_code, number, email=None):
    """
    Update an existing client's data.

    Args:
        client_id (str): Client's ID
        business_id (str): Business ID
        name (str): Client's first name
        surname (str): Client's last name
        country_code (str): Phone country code
        area_code (str): Phone area/provider code
        number (str): Rest of the phone number
        email (str, optional): Client's email address

    Returns:
        dict: Updated client data
    """

    client_data = {
        "id": client_id,
        "name": name,
        "surname": surname,
        "phone": [
            {
                "country_code": country_code,
                "area_code": area_code,
                "number": number
            }
        ]
    }

    if email:
        client_data["email"] = [email]

    payload = {
        "jsonrpc": "2.0",
        "id": 18,
        "cred": {
            "token": self.token,
            "user": self.user
        },
        "method": "client.update_client",
        "params": {
            "business": {
                "id": business_id
            },
            "client": client_data
        }
    }

    response = requests.post(self.url, json=payload)
    response
def confirm_appointment(self, appointment_id, client_id):
    """
    Confirm a reserved appointment and finalize it.

    Args:
        appointment_id (str): ID of the reserved appointment (TENTATIVE)
        client_id (str): ID of the client confirming the appointment

    Returns:
        dict: Confirmation result
    """

    payload = {
        "jsonrpc": "2.0",
        "id": 19,
        "cred": {},
        "method": "appointment.client_confirm_appointment",
        "params": {
            "appointment": {
                "id": appointment_id
            },
            "client": {
                "id": client_id
            }
        }
    }

    response = requests.post(self.url, json=payload)
    response_data = response.json()

    if 'error' in response_data:
        raise Exception(f"Confirm Appointment Error: {response_data['error']['message']}")

    return response_data.get("result", {})
def cancel_appointment_by_client(self, appointment_id, client_id):
    """
    Cancel an existing appointment by the client.

    Args:
        appointment_id (str): ID of the appointment to cancel
        client_id (str): ID of the client requesting the cancellation

    Returns:
        dict: Cancellation result
    """

    payload = {
        "jsonrpc": "2.0",
        "id": 19,
        "cred": {},
        "method": "appointment.cancel_appointment_by_client",
        "params": {
            "appointment": {
                "id": appointment_id
            },
            "client": {
                "id": client_id
            }
        }
    }

    response = requests.post(self.url, json=payload)
    response_data = response.json()

    if 'error' in response_data:
        raise Exception(f"Cancel Appointment Error: {response_data['error']['message']}")

    return response_data.get("result", {})
def cancel_appointment_by_business(self, appointment_id, client_id):
    """
    Cancel an existing appointment by the business.

    Args:
        appointment_id (str): ID of the appointment to cancel
        client_id (str): ID of the client related to the appointment

    Returns:
        dict: Cancellation result
    """

    payload = {
        "jsonrpc": "2.0",
        "id": 19,
        "cred": {
            "token": self.token,
            "user": self.user
        },
        "method": "appointment.cancel_appointment_by_business",
        "params": {
            "appointment": {
                "id": appointment_id
            },
            "client": {
                "clientID": client_id  # שים לב לשם השדה לפי הדוקומנטציה
            }
        }
    }

    response = requests.post(self.url, json=payload)
    response_data = response.json()

    if 'error' in response_data:
        raise Exception(f"Cancel Appointment By Business Error: {response_data['error']['message']}")

    return response_data.get("result", {})
def remove_reserved_appointment(self, appointment_id, business_id):
    """
    Remove (un-reserve) a reserved tentative appointment.

    Args:
        appointment_id (str): ID of the reserved appointment (TENTATIVE)
        business_id (str): Business ID

    Returns:
        dict: Removal result
    """

    payload = {
        "jsonrpc": "2.0",
        "id": 19,
        "cred": {},
        "method": "appointment.client_remove_empty_appointment",
        "params": {
            "appointment": {
                "id": appointment_id
            },
            "business": {
                "id": business_id
            }
        }
    }

    response = requests.post(self.url, json=payload)
    response_data = response.json()

    if 'error' in response_data:
        raise Exception(f"Remove Reserved Appointment Error: {response_data['error']['message']}")

    return response_data.get("result", {})
def get_appointments_by_showcase(self, business_id, created_from, created_to, source, page=1, page_size=100):
    """
    Get a list of appointments for a showcase business.

    Args:
        business_id (str): Business ID
        created_from (str): Start creation date ISO format (e.g., '2024-04-01T00:00:00')
        created_to (str): End creation date ISO format
        source (str): Source string to filter appointments
        page (int, optional): Page number (default 1)
        page_size (int, optional): Number of records per page (default 100)

    Returns:
        dict: Appointments data
    """

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "cred": {
            "token": self.token,
            "user": self.user
        },
        "method": "appointment.get_appointment_by_showcase",
        "params": {
            "business": {
                "id": business_id
            },
            "pageSize": page_size,
            "page": page,
            "source": source,
            "created": {
                "from": created_from,
                "to": created_to
            }
        }
    }

    response = requests.post(self.url, json=payload)
    response_data = response.json()

    if 'error' in response_data:
        raise Exception(f"Get Appointments By Showcase Error: {response_data['error']['message']}")

    return response_data.get("result", {})
def get_appointments_by_filter(self, business_id=None, network_id=None, 
                                start_date=None, end_date=None, 
                                created_start=None, created_end=None,
                                updated_start=None, updated_end=None,
                                services=None, workers=None,
                                skip_business_cancelled=False, skip_updated=False,
                                page=1, page_size=100, sort_field="created", sort_dir="desc"):
    """
    Get a list of appointments by filter.

    Args:
        business_id (str, optional): Business ID
        network_id (str, optional): Network ID
        start_date (str, optional): Start datetime for filtering appointments
        end_date (str, optional): End datetime for filtering appointments
        created_start (str, optional): Filter by creation start date
        created_end (str, optional): Filter by creation end date
        updated_start (str, optional): Filter by updated start date
        updated_end (str, optional): Filter by updated end date
        services (list, optional): List of service IDs
        workers (list, optional): List of worker IDs
        skip_business_cancelled (bool, optional): Skip cancelled appointments
        skip_updated (bool, optional): Skip updated appointments
        page (int, optional): Page number
        page_size (int, optional): Page size
        sort_field (str, optional): Sort by field (default: "created")
        sort_dir (str, optional): Sort direction ("asc" or "desc")

    Returns:
        dict: Appointments data
    """

    if not business_id and not network_id:
        raise ValueError("At least business_id or network_id must be provided.")

    params = {
        "pageSize": page_size,
        "page": page,
        "skipBusinessCancelled": skip_business_cancelled,
        "filter": {
            "skipUpdated": skip_updated,
            "services": services or [],
            "workers": workers or []
        },
        "extraFilters": {
            "sort": [{
                "dir": sort_dir,
                "field": sort_field
            }]
        }
    }

    if business_id:
        params["business"] = {"id": business_id}
    if network_id:
        params["network"] = {"id": network_id}

    if start_date and end_date:
        params["filter"]["start"] = start_date
        params["filter"]["end"] = end_date

    if created_start and created_end:
        params["filter"]["created"] = {
            "start": created_start,
            "end": created_end
        }

    if updated_start and updated_end:
        params["filter"]["updated"] = {
            "start": updated_start,
            "end": updated_end
        }

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "cred": {
            "token": self.token,
            "user": self.user
        },
        "method": "appointment.get_appointment_by_filter",
        "params": params
    }

    response = requests.post(self.url, json=payload)
    response_data = response.json()

    if 'error' in response_data:
        raise Exception(f"Get Appointments By Filter Error: {response_data['error']['message']}")

    return response_data.get("result", {})
def build_showcase(self, network_id, business_id, taxonomy_matching="name_parent"):
    """
    Build a showcase for a network of businesses.

    Args:
        network_id (str): Network ID
        business_id (str): Business ID of the showcase
        taxonomy_matching (str, optional): Taxonomy matching method (default is "name_parent")

    Returns:
        dict: Showcase build result
    """

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "cred": {
            "token": self.token,
            "user": self.user
        },
        "method": "business.build_showcase",
        "params": {
            "taxonomyMatching": taxonomy_matching,
            "network": {
                "id": network_id
            },
            "business": {
                "id": business_id
            }
        }
    }

    response = requests.post(self.url, json=payload)
    response_data = response.json()

    if 'error' in response_data:
        raise Exception(f"Build Showcase Error: {response_data['error']['message']}")

    return response_data.get("result", {})
def build_showcase_from_branches(self, origin_business_ids, business_id, taxonomy_matching="name_parent"):
    """
    Build a showcase from a random set of branch businesses.

    Args:
        origin_business_ids (list): List of origin business IDs (branches)
        business_id (str): Business ID for the showcase
        taxonomy_matching (str, optional): Taxonomy matching method (default is "name_parent")

    Returns:
        dict: Showcase build result
    """

    if not origin_business_ids or not isinstance(origin_business_ids, list):
        raise ValueError("origin_business_ids must be a non-empty list.")

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "cred": {
            "token": self.token,
            "user": self.user
        },
        "method": "business.build_showcase",
        "params": {
            "taxonomyMatching": taxonomy_matching,
            "originBusiness": {
                "id": origin_business_ids
            },
            "business": {
                "id": business_id
            }
        }
    }

    response = requests.post(self.url, json=payload)
    response_data = response.json()

    if 'error' in response_data:
        raise Exception(f"Build Showcase From Branches Error: {response_data['error']['message']}")

    return response_data.get("result", {})
def build_showcase_from_excel(self, file_token, origin_business_ids, business_id, base_business_id):
    """
    Build a showcase using a taxonomy mapping from an Excel file.

    Args:
        file_token (str): Token of the uploaded XLSX file
        origin_business_ids (list): List of branch business IDs
        business_id (str): Showcase business ID
        base_business_id (str): Base business ID for mapping

    Returns:
        dict: Showcase build result
    """

    if not file_token:
        raise ValueError("file_token is required for Excel showcase build.")

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "cred": {
            "token": self.token,
            "user": self.user
        },
        "method": "business.build_showcase",
        "params": {
            "taxonomyMatching": "excel",
            "fileToken": file_token,
            "originBusiness": {
                "id": origin_business_ids
            },
            "business": {
                "id": business_id
            },
            "baseBusinessID": base_business_id
        }
    }

    response = requests.post(self.url, json=payload)
    response_data = response.json()

    if 'error' in response_data:
        raise Exception(f"Build Showcase From Excel Error: {response_data['error']['message']}")

    return response_data.get("result", {})
def get_showcase_resources(self, business_id, taxonomy_id, page=0, page_size=100, worker_sorting_type="workload"):
    """
    Load showcase employees page-by-page.

    Args:
        business_id (str): Showcase business ID
        taxonomy_id (str): Service (taxonomy) ID
        page (int, optional): Page number (starting from 0)
        page_size (int, optional): Number of results per page
        worker_sorting_type (str, optional): Worker sorting method (default "workload")

    Returns:
        dict: Employees (resources) data
    """

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "cred": {
            "token": self.token,
            "user": self.user
        },
        "method": "resource.get_showcase_resources",
        "params": {
            "page": page,
            "pageSize": page_size,
            "worker_sorting_type": worker_sorting_type,
            "business": {
                "id": business_id
            },
            "taxonomy": {
                "id": taxonomy_id
            }
        }
    }

    response = requests.post(self.url, json=payload)
    response_data = response.json()

    if 'error' in response_data:
        raise Exception(f"Get Showcase Resources Error: {response_data['error']['message']}")

    return response_data.get("result", {})
def check_showcase_integrity(self, business_id):
    """
    Verify the integrity of a showcase.

    Args:
        business_id (str): Showcase business ID

    Returns:
        dict: Showcase integrity check result
    """

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "cred": {
            "token": self.token,
            "user": self.user
        },
        "method": "business.check_showcase",
        "params": {
            "business": {
                "id": business_id
            }
        }
    }

    response = requests.post(self.url, json=payload)
    response_data = response.json()

    if 'error' in response_data:
        raise Exception(f"Check Showcase Integrity Error: {response_data['error']['message']}")

    return response_data.get("result", {})
def get_regular_discounts(self, business_id, taxonomy_id=None):
    """
    Get regular discounts for a business or a specific service.

    Args:
        business_id (str): Business ID
        taxonomy_id (str, optional): Taxonomy (service) ID. Optional.

    Returns:
        dict: Discount information
    """

    params = {
        "business": {
            "id": business_id
        }
    }

    if taxonomy_id:
        params["taxonomy"] = {
            "id": taxonomy_id
        }

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "cred": {
            "token": self.token,
            "user": self.user
        },
        "method": "business.get_business_taxonomy_discount",
        "params": params
    }

    response = requests.post(self.url, json=payload)
    response_data = response.json()

    if 'error' in response_data:
        raise Exception(f"Get Regular Discounts Error: {response_data['error']['message']}")

    return response_data.get("result", {})
def set_regular_discount(self, business_id, discount_data, taxonomy_id=None):
    """
    Save regular discount for a business or a specific service.

    Args:
        business_id (str): Business ID
        discount_data (dict): Discount data following the required schema
        taxonomy_id (str, optional): Service ID (optional)

    Returns:
        dict: Discount saving result
    """

    params = {
        "business": {
            "id": business_id
        },
        "discount": discount_data
    }

    if taxonomy_id:
        params["taxonomy"] = {
            "id": taxonomy_id
        }

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "cred": {
            "token": self.token,
            "user": self.user
        },
        "method": "business.set_business_taxonomy_discount",
        "params": params
    }

    response = requests.post(self.url, json=payload)
    response_data = response.json()

    if 'error' in response_data:
        raise Exception(f"Set Regular Discount Error: {response_data['error']['message']}")

    return response_data.get("result", {})
def get_day_specific_discounts(self, business_id, start_date, end_date, taxonomy_id=None):
    """
    Get day-specific discounts for a business or a specific service.

    Args:
        business_id (str): Business ID
        start_date (str): Start date in ISO format
        end_date (str): End date in ISO format
        taxonomy_id (str, optional): Service ID (optional)

    Returns:
        dict: Day-specific discount slots
    """

    params = {
        "business": {
            "id": business_id
        },
        "start": start_date,
        "end": end_date
    }

    if taxonomy_id:
        params["taxonomy"] = {
            "id": taxonomy_id
        }

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "cred": {
            "token": self.token,
            "user": self.user
        },
        "method": "business.get_business_taxonomy_discount_exception",
        "params": params
    }

    response = requests.post(self.url, json=payload)
    response_data = response.json()

    if 'error' in response_data:
        raise
def set_day_specific_discount(self, business_id, taxonomy_id, discount_data):
    """
    Save a single day-specific discount for a service.

    Args:
        business_id (str): Business ID
        taxonomy_id (str): Service ID
        discount_data (dict): Discount data

    Returns:
        dict: Discount save result
    """

    if not discount_data:
        raise ValueError("discount_data is required.")

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "cred": {
            "token": self.token,
            "user": self.user
        },
        "method": "business.set_business_taxonomy_discount_exception",
        "params": {
            "business": {
                "id": business_id
            },
            "taxonomy": {
                "id": taxonomy_id
            },
            "discount": discount_data
        }
    }

    response = requests.post(self.url, json=payload)
    response_data = response.json()

    if 'error' in response_data:
        raise Exception(f"Set Day-Specific Discount Error: {response_data['error']['message']}")

    return response_data.get("result", {})
def set_day_specific_discounts(self, business_id, taxonomy_id, discounts_data):
    """
    Save multiple day-specific discounts for a service.

    Args:
        business_id (str): Business ID
        taxonomy_id (str): Service ID
        discounts_data (list): List of discount objects

    Returns:
        dict: Result of saving multiple day-specific discounts
    """

    if not discounts_data or not isinstance(discounts_data, list):
        raise ValueError("discounts_data must be a non-empty list.")

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "cred": {
            "token": self.token,
            "user": self.user
        },
        "method": "business.set_business_taxonomy_discount_exceptions",
        "params": {
            "business": {
                "id": business_id
            },
            "taxonomy": {
                "id": taxonomy_id
            },
            "discounts": discounts_data
        }
    }

    response = requests.post(self.url, json=payload)
    response_data = response.json()

    if 'error' in response_data:
        raise Exception(f"Set Day-Specific Discounts Error: {response_data['error']['message']}")

    return response_data.get("result", {})
