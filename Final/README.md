# SmartTask AI: Final Project (PKMS + Task Manager)

## Overview
SmartTask AI is a robust, terminal-based application that combines a Personal Knowledge Management System (PKMS) with a Priority-Based Task Manager. It utilizes a unified SQLite database for reliable storage and integrates OpenAI's GPT models to act as an intelligent agent that can reason across both your tasks and your notes.

## Key Features

### 🧠 Intelligent PKMS (Notes)
* **Storage:** Notes are stored in a local SQLite database (`pkms_data.db`) for reliability and speed.
* **Search:** Includes a SQL-based search engine to find notes by keyword.
* **AI Integration:** The AI agent can read your notes to answer questions or generate study plans.

### ✅ Advanced Task Management
* **Prioritization:** Supports **High**, **Medium**, and **Low** priorities with color-coded visual indicators (Red/Cyan).
* **State Tracking:** Mark tasks as **DONE** (Green) with visual strikethrough.
* **Persistence:** Tasks persist between sessions using SQL.
* **CRUD:** Full support to Create, Read, Update (Complete), and Delete tasks.

### 🤖 AI Agent Integration
* **Contextual Awareness:** Unlike standard chatbots, this agent has read-access to your specific database state.
* **Reasoning:** It can answer questions like *"Based on my High Priority tasks, what should I work on first?"*

## Architecture
This application follows a Monolithic Script architecture (`main.py`) to ensure maximum portability and ease of execution.
* **Database:** `sqlite3` (Zero-configuration, serverless).
* **API:** `openai` (Chat Completions API).
* **Interface:** CLI (Command Line Interface) with a Read-Eval-Print Loop (REPL) and ASCII art banner.

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

### Task Commands
* `task <description> [High/Med/Low]` : Add a new task with optional priority.
* `done <id>` : Mark a task as completed.
* `delete task <id>` : Permanently remove a task.
* `list` : View all tasks (Color-coded by priority and status).

### Note Commands
* `note <title> | <content>` : Save a new note (use `|` to separate title).
* `search <query>` : Search your notes for specific keywords.
* `notes` : List all knowledge base entries.

### AI Commands
* `ask <query>` : Ask the AI agent for help (uses your data as context).
* `quit` : Exit the application.