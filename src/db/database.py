import psycopg2
from psycopg2.extras import DictCursor
from contextlib import contextmanager
from src.utils.config import DB_PARAMS
from typing import List, Dict, Any

class DatabaseHandler:
    """
    Handles database operations for storing and retrieving conversation histories.
    
    Attributes:
        dbname (str): The name of the database.
        user (str): The database user.
        password (str): The database password.
        host (str): The database host.
    """

    def __init__(self, dbname: str, user: str, password: str, host: str):
        """
        Initialises the DatabaseHandler with database connection details.

        Args:
            dbname: The name of the database.
            user: The database user.
            password: The database password.
            host: The database host.
        """
        self.dbname = DB_PARAMS['dbname']
        self.user = DB_PARAMS['user']
        self.password = DB_PARAMS['password']
        self.host = DB_PARAMS['host']

    @contextmanager
    def get_db_connection(self):
        """
        Generates a database connection context.
        """
        conn = psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password, host=self.host)
        try:
            yield conn
        finally:
            conn.close()

    @contextmanager
    def get_db_cursor(self, commit: bool = False):
        """
        Generates a database cursor context, optionally committing on exit.

        Args:
            commit: Whether to commit the transaction on exit.
        """
        with self.get_db_connection() as connection:
            cursor = connection.cursor(cursor_factory=DictCursor)
            try:
                yield cursor
                if commit:
                    connection.commit()
            finally:
                cursor.close()

    def insert_conversation(self, user_name: str, message_sent: str, reply_received: str):
        """
        Inserts a new conversation record into the database.

        Args:
            user_name: The name of the user.
            message_sent: The message sent by the user.
            reply_received: The reply received by the user.
        """
        with self.get_db_cursor(commit=True) as cursor:
            cursor.execute(
                "INSERT INTO user_conversations (user_name, message_sent, reply_received) VALUES (%s, %s, %s)",
                (user_name, message_sent, reply_received)
            )

    def get_user_history(self, user_name: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Retrieves the user's conversation history up to a specified limit.

        Args:
            user_name: The name of the user.
            limit: The maximum number of records to retrieve.

        Returns:
            A list of dictionaries containing the messages sent and replies received.
        """
        with self.get_db_cursor() as cursor:
            cursor.execute(
                "SELECT message_sent, reply_received FROM user_conversations WHERE user_name = %s ORDER BY date_time DESC LIMIT %s",
                (user_name, limit)
            )
            return cursor.fetchall()

    def get_pdf_content(self, document_name: str) -> List[str]:
        """
        Retrieves text content from a specific PDF stored in the database.

        Args:
            document_name: The name of the document to retrieve content for.

        Returns:
            A list of strings where each string represents the text content of a PDF page.
        """
        with self.get_db_cursor() as cursor:
            cursor.execute(
                "SELECT content FROM pdf_contents WHERE document_name = %s ORDER BY page_number ASC",
                (document_name,)
            )
            return [row['content'] for row in cursor.fetchall()]

# Example usage
if __name__ == '__main__':
    db_handler = DatabaseHandler(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST)
    user_name = "example_user"
    message_sent = "What is the weather like today?"
    reply_received = "The weather is sunny."

    # Insert a new conversation into the database
    db_handler.insert_conversation(user_name, message_sent, reply_received)

    # Retrieve and print the user's conversation history
    history = db_handler.get_user_history(user_name)
    for record in history:
        print(f"Sent: {record['message_sent']}, Received: {record['reply_received']}")