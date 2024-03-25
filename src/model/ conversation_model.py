from langchain.llms import LlamaCPP
from langchain.chains import RetrieverGenerator
from langchain.retrievers import MultiRetriever, LocalRetriever, WebRetriever
from src.utils.config import DB_PARAMS
from ..db.database import DatabaseHandler

class ConversationHandler:
    """
    Handles conversations using a Llama model with local and web retrievers.

    Attributes:
        llm (LlamaCPP): The LlamaCPP model used for generating responses.
        rg_chain (RetrieverGenerator): The RetrieverGenerator chain combining the Llama model with retrievers.
        db_handler (DatabaseHandler): The DatabaseHandler used for database operations.
    """

    def __init__(self, model_path: str, documents_folder: str, db_params: dict):
        """
        Initialises the ConversationHandler with specified model, document folder paths, and database parameters.

        Args:
            model_path: The file path to the Llama model.
            documents_folder: The folder path containing local documents.
            db_params: A dictionary containing the database parameters.
        """
        # Initialise the LlamaCPP model
        self.llm = LlamaCPP(model_path=model_path)

        # Initialise the local and web retrievers
        local_retriever = LocalRetriever(documents_folder)
        web_retriever = WebRetriever()

        # Create a composite retriever
        multi_retriever = MultiRetriever([local_retriever, web_retriever])

        # Create a retriever-generator chain
        self.rg_chain = RetrieverGenerator(
            retriever=multi_retriever,
            llm=self.llm,
            retriever_weight=0.3,
            generator_weight=0.7,
            max_tokens=50,
            temperature=0.7
        )

        # Initialise the DatabaseHandler
        self.db_handler = DatabaseHandler(**db_params)

    def handle_conversation_with_pdf(self, user_name: str, new_question: str, document_name: str) -> str:
        """
        Handles a new question within a conversation, storing and retrieving past conversations,
        and includes content from a specified PDF document in the database.

        Args:
            user_name: The name of the user.
            new_question: The new question asked by the user.
            document_name: The name of the PDF document to refer to in the response.

        Returns:
            The generated response to the question.
        """
        # Retrieve user's conversation history and the specified PDF content
        history = self.db_handler.get_user_history(user_name)
        pdf_content = '\n'.join(self.db_handler.get_pdf_content(document_name))

        # Combine history, PDF content, and new question
        combined_history = "\n".join(f"{msg['message_sent']} {msg['reply_received']}" for msg in history)
        full_prompt = f"{combined_history}\n{pdf_content}\n{new_question}"

        # Generate the new reply using the RetrieverGenerator chain
        output = self.rg_chain(full_prompt)

        # Insert new conversation into the database
        self.db_handler.insert_conversation(user_name, new_question, output)

        # Return the new reply
        return output

# Example usage
if __name__ == '__main__':
    user_name = "example_user"
    new_question = "This is your new English question"
    model_path = "/path/to/your/llama-model.gguf"
    documents_folder = "/path/to/your/documents/folder"

    conversation_handler = ConversationHandler(model_path, documents_folder, DB_PARAMS)
    new_reply = conversation_handler.handle_conversation_with_pdf(user_name, new_question, "Example Document")
    print(new_reply)
