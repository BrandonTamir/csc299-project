import os
from openai import OpenAI
from dotenv import load_dotenv

def main():
    # Load the API key from the .env file
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../../.env'))
    
    # Check if the key was loaded
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found.")
        print("Please check your .env file in the 'tasks4' directory.")
        return

    # Initialize the OpenAI client (it automatically uses the env variable)
    try:
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
                model="gpt-5-mini",  # The model from your instructions
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
            # This is where you might see a 401 again if the key is valid but billing is not set up.

if __name__ == "__main__":
    main()