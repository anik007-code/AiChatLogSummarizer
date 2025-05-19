import os
import re
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist

try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')


def parse_chat_log(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return None, None
    except UnicodeDecodeError:
        print(f"Error: File {file_path} is not a valid text file.")
        return None, None

    user_messages = []
    ai_messages = []
    for line in lines:
        line = line.strip()
        if line.startswith("User:"):
            user_messages.append(line[5:].strip())
        elif line.startswith("AI:"):
            ai_messages.append(line[3:].strip())

    return user_messages, ai_messages


def get_message_statistics(user_messages, ai_messages):
    total_messages = len(user_messages) + len(ai_messages)
    user_count = len(user_messages)
    ai_count = len(ai_messages)
    exchanges = min(user_count, ai_count)  # Number of complete exchanges
    return total_messages, user_count, ai_count, exchanges


def extract_keywords(messages, top_n=5):
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    all_text = " ".join(messages).lower()
    words = word_tokenize(all_text)
    filtered_words = []
    for word in words:
        if word.isalpha() and word not in stop_words and len(word) > 2:
            lemmatized = lemmatizer.lemmatize(word)
            filtered_words.append(lemmatized)
    freq_dist = FreqDist(filtered_words)
    return freq_dist.most_common(top_n)


def infer_conversation_nature(keywords):
    keyword_list = [word for word, _ in keywords]
    programming_keywords = ['python', 'programming', 'code', 'function', 'class', 'variable', 'algorithm', 'developer']
    ai_keywords = ['machine', 'learning', 'ai', 'data', 'model', 'neural', 'train', 'predict', 'nlp']
    web_keywords = ['web', 'html', 'css', 'javascript', 'frontend', 'backend', 'server', 'client', 'api']
    database_keywords = ['database', 'sql', 'query', 'table', 'schema', 'nosql', 'mongodb', 'postgres']

    programming_count = sum(1 for word in keyword_list if word in programming_keywords)
    ai_count = sum(1 for word in keyword_list if word in ai_keywords)
    web_count = sum(1 for word in keyword_list if word in web_keywords)
    database_count = sum(1 for word in keyword_list if word in database_keywords)

    if programming_count > max(ai_count, web_count, database_count):
        return "programming or Python-related topics"
    elif ai_count > max(programming_count, web_count, database_count):
        return "AI or machine learning topics"
    elif web_count > max(programming_count, ai_count, database_count):
        return "web development topics"
    elif database_count > max(programming_count, ai_count, web_count):
        return "database-related topics"
    else:
        return "general topics"


def generate_summary(file_path, user_messages, ai_messages):
    total_messages, user_count, ai_count, exchanges = get_message_statistics(user_messages, ai_messages)
    all_messages = user_messages + ai_messages
    keywords = extract_keywords(all_messages)

    user_keywords = extract_keywords(user_messages, top_n=3)
    user_keyword_str = ", ".join([f"{word} ({count})" for word, count in user_keywords])

    ai_keywords = extract_keywords(ai_messages, top_n=3)
    ai_keyword_str = ", ".join([f"{word} ({count})" for word, count in ai_keywords])

    conversation_nature = infer_conversation_nature(keywords)
    keyword_str = ", ".join([f"{word} ({count})" for word, count in keywords])

    avg_user_length = sum(len(msg.split()) for msg in user_messages) / max(1, len(user_messages))
    avg_ai_length = sum(len(msg.split()) for msg in ai_messages) / max(1, len(ai_messages))

    summary = f"Summary for {os.path.basename(file_path)}:\n"
    summary += f"- The conversation had {exchanges} exchanges.\n"
    summary += f"- Total messages: {total_messages} (User: {user_count}, AI: {ai_count}).\n"
    summary += f"- The user asked mainly about {conversation_nature}.\n"
    summary += f"- Most common keywords overall: {keyword_str}.\n"
    summary += f"- User frequently mentioned: {user_keyword_str}.\n"
    summary += f"- AI frequently mentioned: {ai_keyword_str}.\n"
    summary += f"- Average message length: User ({avg_user_length:.1f} words), AI ({avg_ai_length:.1f} words).\n"

    output_dir = os.path.dirname(file_path)
    output_file = os.path.join(output_dir, "summary.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(summary)
    print(f"Enhanced summary saved to {output_file}")
    return summary