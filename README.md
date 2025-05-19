# AI Chat Log Summarizer

A Python tool that analyzes and summarizes AI chat conversations, providing insights into the content, topics, and patterns within the dialogue.

## Features

- Parses chat logs with User/AI message format
- Extracts key topics and themes from conversations
- Identifies the most common keywords used by both parties
- Categorizes conversations by topic (programming, AI, web development, etc.)
- Calculates message statistics (count, length, exchanges)
- Generates comprehensive summaries with detailed analytics
- Processes individual files or entire directories of chat logs

## Installation

### Prerequisites

- Python 3.6 or higher

### Setup

1. Clone this repository:
   ```
   git clone https://github.com/anik007-code/AiChatLogSummarizer.git
   cd AiChatLogSummarizer
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install nltk
   ```

5. Download the required NLTK data:
   ```python
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
   ```

## Usage

### Basic Usage

Run the script and enter the path to a chat log file or directory when prompted:

```
python main.py
```

### Input Format

The chat log files should follow this format:

```
User: [User message here]
AI: [AI response here]
User: [Next user message]
AI: [Next AI response]
...
```

### Sample Files

A sample chat log file (`sample_chat.txt`) is included in the repository for testing.

### Output

The script generates a summary for each processed chat log, including:

- Number of exchanges between user and AI
- Total message counts
- Main conversation topics
- Most common keywords (overall, user-specific, and AI-specific)
- Average message length statistics

Summaries are both printed to the console and saved to a file named `chat_summaries.txt`.

