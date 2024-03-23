# Conversational-Llama-Integration

This project integrates the power of Llama 2, a large language model, with the versatility of LangChain and the efficiency of Llama Index to create a sophisticated conversational agent. Aimed at extracting and utilizing both local and online data, it provides a seamless experience for users across different messaging platforms including LINE and Telegram. The conversations are logged in a PostgreSQL database, offering insights and continuous improvement opportunities.

## Features

- **Llama 2 Integration**: Leverages the capabilities of Llama 2 for understanding and generating human-like text.
- **LangChain & Llama Index**: Enhances the conversational context and efficiency by incorporating external data sources.
- **Fine-Tuning**: Customizes the model to cater to specific conversation styles or topics.
- **Data Extraction**: Utilizes both local files and online resources for comprehensive dialogues.
- **PostgreSQL Logging**: Records all interactions for analysis and future reference.
- **Messaging Platform Integration**: Supports interaction through popular platforms like LINE and Telegram.

## Getting Started

### Prerequisites

- Python 3.8 or later
- PostgreSQL
- API keys for LINE and Telegram bots

### Installation

1. Clone the repository:
```bash
git https://github.com/yihong1120/Conversational-Llama-Integration
```

2. Install the required packages:
```bash
cd Conversational-Llama-Integration
pip install -r requirements.txt
```

3. Set up your environment variables for database credentials and API keys.

### Usage

1. Start by configuring your PostgreSQL database to store conversation logs.
2. Register and set up your bots on LINE and Telegram.
3. Run the main script to start interacting with the conversational agent:
```bash
python main.py
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- Thanks to the Llama 2, LangChain, and Llama Index projects for providing the technologies that made this possible.
- Appreciation for the open-source community for continuous support and inspiration.
