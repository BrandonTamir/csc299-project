# SUMMARY.md — Detailed Development Process

## Project Overview
This document outlines the comprehensive development lifecycle of the **CSC 299 Final Project** (located in the `tasks5` directory). The final software is a terminal-based Personal Knowledge Management System (PKMS) and Task Manager. It has been engineered to provide persistent data storage via **SQLite** and intelligent, context-aware assistance via the **OpenAI API**.

The project represents a synthesis of skills acquired throughout the semester, moving from simple script-based file manipulation to a robust, database-backed application with a professional Command Line Interface (CLI).

---

## 1. AI-Assisted Development Strategy
A core requirement of this project was to utilize AI-coding assistants. I adopted a "Multi-Model" approach, leveraging the specific strengths of different AI tools to simulate a real-world software engineering team.

### Gemini: The Primary Thought Partner & Debugger
My experience working with **Gemini** was particularly impactful. Rather than treating it solely as a code generator, I used it as a "tutor" and debugging partner.
* **Learning & Debugging:** When I encountered obscure errors (such as `sqlite3` cursor issues or specific Python variable scope errors), I pasted the traceback into Gemini. It didn't just fix the code; it explained *why* the error happened. This was crucial for my learning process, allowing me to understand the difference between local and global variables in Python functions.
* **Drafting & Logic:** I used Gemini to help draft the logic for the `ask_ai` function, specifically figuring out how to format the database strings effectively before sending them to the LLM.

### GitHub Copilot: The "Pair Programmer"
I utilized GitHub Copilot in two distinct modes:
1.  **Ghost Text (Autocomplete):** This was invaluable for boilerplate code. When writing the main `while True:` loop, Copilot accurately predicted the `elif` structures for parsing user commands (e.g., splitting `task <name>` into command and argument), which saved significant typing time.
2.  **Copilot Chat:** I used the sidebar chat to quickly look up syntax for the `colorama` and ANSI escape codes used to style the terminal output (red for High priority, green for Done).

### Claude Code, DeepSeek & ChatGPT: High-Level Architecture
I employed **Claude Code**, **DeepSeek**, and **ChatGPT** for high-level architectural decisions and "second opinions."
* **Brainstorming:** I used these models to brainstorm the database schema. For example, asking DeepSeek "What is the best way to link tasks and notes?" led to the decision to keep them in separate tables but accessible via a single SQL connection.
* **Logic Verification:** When I was unsure if my "Search" algorithm was efficient, I cross-referenced the SQL query logic (`WHERE title LIKE ?`) with Claude to ensure it was the standard industry approach.

---

## 2. Technical Decisions & Architecture

### The Shift from JSON to SQLite
In the earlier stages of the course (`tasks1`, `tasks2`), I relied on JSON files for storage. While simple, I found that rewriting the entire JSON file for every single task update was inefficient and prone to corruption if the program crashed mid-write.
* **Decision:** I migrated to **SQLite** for the final version. This provides atomic transactions, meaning data is saved instantly and reliably. It also allowed me to implement advanced features like "Search" using native SQL queries rather than writing complex Python loops to filter text.

### Monolithic Architecture
I decided to structure the final application as a **Monolithic Script** (`main.py`). While splitting code into `agents.py` and `storage.py` is common, keeping the logic in one self-contained file ensures maximum portability. The entire app can be run on any machine (Windows/Linux/Mac) by simply transferring a single file, reducing the risk of `ImportError` or pathing issues.

---

## 3. Testing and Verification
The development process was informed by the **Spec-Kit** assignment (`tasks5`), which taught me the value of defining behavior before coding.
* **Manual "Black Box" Testing:** I rigorously tested the CLI by running the application in a fresh environment. I specifically tested edge cases, such as trying to delete a task ID that doesn't exist (to ensure the app prints an error message rather than crashing) and trying to run the AI command without an API key.
* **Prototype Validation:** Before writing the final code, I created a `prototype_main.py` (committed in the repository history). This small script proved that I could successfully connect to the database and the OpenAI API simultaneously, serving as a "green light" to proceed with the full UI development.

---

## 4. False Starts and Challenges
The process was not without its hurdles:
* **Git Merge Conflicts:** One significant challenge was managing the repository structure. Because the `spec-kit` assignment was done in a separate environment, trying to merge that history into the main `csc299-project` caused complex conflicts. **What didn't work:** I initially tried to force a git merge, which resulted in duplicate directories. **The Fix:** I learned to manually migrate the stable code into a clean `tasks5` directory to preserve the integrity of the final submission.
* **Context Window Overload:** Early attempts at the AI agent involved dumping *every* note into the prompt. This worked for small tests but failed as the database grew. **The Fix:** I refined the `ask_ai` function to only pull active tasks and titles, optimizing the token usage.

## Conclusion
The final result is a polished, production-ready productivity tool. By leveraging a suite of AI tools—from Gemini for deep debugging to Copilot for speed—I was able to focus on high-level feature implementation rather than getting stuck on syntax, resulting in a more capable and robust final product.
