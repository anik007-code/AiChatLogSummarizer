from functions import parse_chat_log, generate_summary


def main():
    file_name = "Data/sample_chat.txt"
    user_msgs, ai_msgs = parse_chat_log(file_name)
    if user_msgs and ai_msgs:
        generate_summary(file_name, user_msgs, ai_msgs)
    else:
        print("No messages to summarize!")


if __name__ == "__main__":
    main()


