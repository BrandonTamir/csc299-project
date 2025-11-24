# SmartTask AI: Final Project (PKMS + Task Manager)

## Overview
SmartTask AI is a robust, terminal-based application that combines a Personal Knowledge Management System (PKMS) with a Task Manager. It utilizes a unified SQLite database for reliable storage and integrates OpenAI's GPT models to act as an intelligent agent that can reason across both your tasks and your notes.

## Key Features

### 🧠 Intelligent PKMS (Notes)
* **Storage:** Notes are stored in a local SQLite database (`pkms_data.db`) for reliability and speed.
* **Retrieval:** Instant access to your knowledge base via the command line.
* **AI Integration:** The AI agent can read your notes to answer questions or generate study plans.

### ✅ Task Management
* **Tracking:** Add and list tasks with status tracking.
* **Persistence:** Tasks persist between sessions using SQL.
* **Context:** The AI agent uses your pending tasks to help you prioritize work.

### 🤖 AI Agent Integration
* **Contextual Awareness:** Unlike standard chatbots, this agent has read-access to your specific database state.
* **Reasoning:** It can answer questions like "Based on my notes about History, what tasks should I add?"

## Architecture
This application follows a Monolithic Script architecture (`main.py`) to ensure maximum portability and ease of execution.
* **Database:** `sqlite3` (Zero-configuration, serverless).
* **API:** `openai` (Chat Completions API).
* **Interface:** CLI (Command Line Interface) with a Read-Eval-Print Loop (REPL).

## How to Run
1.  **Install Dependencies:**
    ```bash
    pip install openai
    ```
2.  **Set API Key:**
    Ensure your `OPENAI_API_KEY` is set in your environment.
3.  **Launch:**
    ```bash
    python main.py
    ```

## Usage Guide
Once inside the application, use the following commands:
* `task <description>` : Add a new task.
* `list` : View all tasks and their IDs.
* `note <title> | <content>` : Save a new note into the PKMS.
* `notes` : List all knowledge base entries.
* `ask <query>` : Ask the AI agent for help (uses your data as context).
* `quit` : Exit the application.