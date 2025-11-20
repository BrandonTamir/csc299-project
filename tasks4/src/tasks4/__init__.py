import os
from openai import OpenAI
# We don't need 'load_dotenv' anymore

def main():
    # The key is now loaded from Windows, not a .env file
    # The OpenAI client will find it automatically if you set it correctly.
    api_key = os.environ.get("OPENAI_API_KEY")
    
    if not api_key:
        print("Error: OPENAI_API_KEY not found in your environment.")
        print("Please make sure you set it in the Control Panel and RESTARTED your terminal.")
        return

    try:
        # When you initialize OpenAI without an api_key argument,
        # it automatically looks for the 'OPENAI_API_KEY' environment variable.
        client = OpenAI()
    except Exception as e:
        print(f"Error initializing OpenAI client: {e}")
        return

    # 1. Your two sample paragraph-length descriptions
    task_descriptions = [
        "Create a new Python script that reads a JSON file named 'tasks.json'. The script needs to parse this file, find all tasks that have a 'status' key set to 'pending', and then print their 'task_name' and 'due_date' to the console.",
        "Refactor the existing user authentication module. The current implementation uses a simple text file to store passwords. This needs to be updated to use hashed passwords (bcrypt) and store the user data in our SQLite database in the 'users' table."
    ]

    print("--- Task Summarization Bot ---")

    # 2. Add a loop to summarize each description
    for i, desc in enumerate(task_descriptions):
        print(f"\nProcessing Task {i+1}...")
        print(f"Original: \"{desc}\"")

        try:
            # 3. Use the Chat Completions API
            chat_completion = client.chat.completions.create(
                model="gpt-5-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert summarizer. Your job is to take a long task description and summarize it into a short, actionable phrase of 10 words or less."
                    },
                    {
                        "role": "user",
                        "content": desc
                    }
                ]
            )
            
            summary = chat_completion.choices[0].message.content
            
            # 4. Print the summary
            print(f"Summary: {summary}")

        except Exception as e:
            print(f"An error occurred while contacting OpenAI: {e}")

if __name__ == "__main__":
    main()