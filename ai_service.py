import google.generativeai as genai
import settings
from ai_configs import SYSTEM_INSTRUCTIONS

class GeminiAPIWrapperManager:
    """
    A manager class to handle instances of GeminiAPIWrapper based on the username.
    """
    def __init__(self):
        self.instances = {}  # Dictionary to store instances by username

    def get_instance(self, username):
        """
        Returns an instance of GeminiAPIWrapper for the given username.

        Args:
            username (str): The username for which to get the API wrapper instance.

        Returns:
            GeminiAPIWrapper: An instance of the GeminiAPIWrapper for the given username.
        """
        if username not in self.instances:
            # Create a new instance if one doesn't already exist for the username
            self.instances[username] = GeminiAPIWrapper(username=username)
        return self.instances[username]

    def clear_instance(self, username):
        """
        Clears the instance of GeminiAPIWrapper for the given username.

        Args:
            username (str): The username whose instance should be cleared.
        """
        if username in self.instances:
            del self.instances[username]

    def clear_all_instances(self):
        """
        Clears all instances of GeminiAPIWrapper.
        """
        self.instances.clear()



class GeminiAPIWrapper:
    """
    A wrapper class for interacting with the Google Gemini API.
    """
    def __init__(self, api_key=None, model_name="gemini-1.5-pro-latest", username=None):
        """
        Initializes the GeminiAPIWrapper.

        Args:
            api_key (str, optional): Your Google Gemini API key.
                Defaults to the 'GEMINI_API_KEY' environment variable.
            model_name (str, optional): The name of the Gemini model to use.
                Defaults to "gemini-1.5-pro-latest".
            system_instruction (str, optional): A default system instruction (persona)
                to use for all queries.  Can be overridden in the query() method.
                Defaults to None.
        """
        self.api_key = api_key or settings.GEMINI_API_KEY
        if not self.api_key:
            raise ValueError(
                "API key not provided. Set the 'GEMINI_API_KEY' "
                "environment variable or pass it during initialization."
            )
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)
        self.system_instruction = SYSTEM_INSTRUCTIONS  # Default system instruction
        self.username = username  # Optional username for user-specific sessions
        self.chat_sessions = {}  # To store chat history per session

    def query(self, prompt, context=None, persona=None, generation_config=None, format_spec=None):  # Added format_spec
        """
        Sends an individual query to the Gemini API.

        Args:
            prompt (str): The user's query.
            context (list, optional): A list of previous messages in the conversation
                (as dictionaries with 'role' and 'parts'). Defaults to None.
            persona (str, optional): A system instruction defining the model's
                persona or behavior for this query. Overrides the default
                system_instruction. Defaults to None.
            generation_config (genai.types.GenerationConfig, optional):
                Configuration options for content generation.
                Defaults to None.
            format_spec (str, optional): Instructions on the desired output format
                (e.g., "Return in JSON format", "Return as a comma-separated list").
                This is appended to the prompt.

        Returns:
            str: The text response from the Gemini API, or None on error.
        """
        messages = []
        if context:
            messages.extend(context)
        # Incorporate format spec into the prompt
        effective_prompt = prompt
        if format_spec:
            effective_prompt += f" {format_spec}"
        messages.append({"role": "user", "parts": [effective_prompt]})

        # Use provided persona, or default if available
        effective_persona = persona if persona is not None else self.system_instruction

        config = generation_config or genai.types.GenerationConfig()  # Get a mutable copy
        if effective_persona:
            config.system_instruction = effective_persona

        try:
            response = self.model.generate_content(messages, generation_config=config)
            return response.text
        except Exception as e:
            print(f"Error during Gemini API query: {e}")
            return None

    def start_chat(self, session_id, persona=None, history=None):
        """
        Starts a new chat session.

        Args:
            session_id (str): A unique identifier for the chat session (e.g., user ID).
            persona (str, optional): A system instruction to set the initial persona
                for this chat session.  Defaults to the class-level
                system_instruction.
            history (list, optional): Initial chat history.
        """
        effective_persona = persona if persona else self.system_instruction
        # chat = self.model.start_chat(system_instruction=effective_persona, history=history) # Removed problematic line
        chat = self.model.start_chat(history=history)
        self.chat_sessions[session_id] = chat
        if effective_persona: # added this
            self.chat_sessions[session_id].send_message(effective_persona) # send the persona as the first message

    def send_chat_message(self, session_id, message):
        """
        Sends a message to an ongoing chat session.

        Args:
            session_id (str): The identifier of the chat session.
            message (str): The user's message.

        Returns:
            str: The text response from the Gemini API, or None on error or if
                the session doesn't exist.
        """
        if session_id not in self.chat_sessions:
            print(f"Error: Chat session '{session_id}' not found.")
            return None
        try:
            response = self.chat_sessions[session_id].send_message(message)
            return response.text
        except Exception as e:
            print(f"Error during Gemini API chat message: {e}")
            return None

    def get_chat_history(self, session_id):
        """
        Retrieves the message history for a given chat session.

        Args:
            session_id (str): The identifier of the chat session.

        Returns:
            list: A list of message turns (dicts with 'role' and 'parts'),
            or None if the session doesn't exist.
        """
        if session_id not in self.chat_sessions:
            print(f"Error: Chat session '{session_id}' not found.")
            return None

        history = []
        for turn in self.chat_sessions[session_id].history:
            history.append({"role": turn.role, "parts": turn.parts})
        return history

    def end_chat(self, session_id):
        """
        Ends a chat session and removes it from the active sessions.

        Args:
            session_id (str): The identifier of the chat session to end.
        """
        if session_id in self.chat_sessions:
            del self.chat_sessions[session_id]
        else:
            print(f"Warning: Chat session '{session_id}' not found.")

    def clear_all_chats(self):
        """Clears all active chat sessions."""
        self.chat_sessions.clear()