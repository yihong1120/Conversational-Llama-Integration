from typing import List
from langchain_community.llms import LlamaCpp  # 确保正确导入
# from ..utils.config import DB_PARAMS

class ConversationHandler:
    """
    Handles conversations using a Llama model.

    Attributes:
        llm (LlamaCpp): The LlamaCpp model used for generating responses.
    """

    def __init__(self, model_path: str):
        """
        Initialises the ConversationHandler with specified model.

        Args:
            model_path: The file path to the Llama model.
        """
        # Initialise the LlamaCpp model
        self.llm = LlamaCpp(model_path=model_path)

    def handle_conversation(self, user_name: str, new_question: str) -> str:
        """
        Handles a new question within a conversation.

        Args:
            user_name: The name of the user.
            new_question: The new question asked by the user.

        Returns:
            The generated response to the question.
        """
        # Generate the new reply using the Llama model
        output = self.llm.generate([new_question])   # 注意: 根据实际API调整此行

        # Return the new reply
        return output

# Example usage
if __name__ == '__main__':
    user_name = "example_user"
    new_question = "法國的首都是哪裡？"
    model_path = "../../models/llama2/firefly-llama2-13b-chat.Q8_0.gguf"

    conversation_handler = ConversationHandler(model_path)
    new_reply = conversation_handler.handle_conversation(user_name, new_question)
    print(new_reply)
