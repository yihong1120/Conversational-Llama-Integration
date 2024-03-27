from typing import List
from langchain_community.llms import LlamaCpp  # 确保正确导入
from src.utils.config import DB_PARAMS
from src.db.database import DatabaseHandler

class ConversationHandler:
    """
    Handles conversations using a Llama model.

    Attributes:
        llm (LlamaCpp): The LlamaCpp model used for generating responses.
        db_handler (DatabaseHandler): Handles database operations.
    """

    def __init__(self, model_path: str):
        """
        Initialises the ConversationHandler with specified model.

        Args:
            model_path: The file path to the Llama model.
        """
        # Initialise the LlamaCpp model
        self.llm = LlamaCpp(model_path=model_path)
        # Initialise the DatabaseHandler with parameters from DB_PARAMS
        self.db_handler = DatabaseHandler(**DB_PARAMS)

    def handle_conversation(self, user_name: str, new_question: str) -> str:
        """
        Handles a new question within a conversation, incorporating previous conversations for context.

        Args:
            user_name: The name of the user.
            new_question: The new question asked by the user.

        Returns:
            The generated response to the question.
        """
        # Retrieve user's conversation history
        history = self.db_handler.get_user_history(user_name)
        # Combine previous conversations with the new question
        context = "\n".join([f"Q: {item['message_sent']} A: {item['reply_received']}" for item in history])
        full_prompt = f"{context}\nQ: {new_question}\nA:"
        
        # Generate the new reply using the Llama model
        output = self.llm.generate([full_prompt])[0]  # Assume generate returns a list of responses

        # Insert new conversation into the database
        self.db_handler.insert_conversation(user_name, new_question, output)

        # Return the new reply
        return output

# Example usage
if __name__ == '__main__':
    user_name = "arthurfr"
    new_question = "法國的首都是哪裡？"
    model_path = "../../models/llama2/firefly-llama2-13b-chat.Q8_0.gguf"

    conversation_handler = ConversationHandler(model_path)
    new_reply = conversation_handler.handle_conversation(user_name, new_question)
    print(new_reply)
