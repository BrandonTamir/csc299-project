# Software Specifications for Final Project

## 1. Functional Requirements
* [x] System must utilize SQLite for data persistence.
* [x] System must allow creating, reading, updating, and deleting (CRUD) tasks.
* [x] Tasks must support "High", "Medium", and "Low" priorities.
* [x] System must allow creating and searching text-based notes.
* [x] System must integrate with OpenAI API for context-aware queries.

## 2. Interface Requirements
* [x] CLI must use color coding (Red for High priority, Green for Done).
* [x] CLI must handle errors gracefully (e.g., missing API key).
* [x] CLI must provide a help menu.

## 3. Data Structure
* **Table: tasks** (id, description, status, priority, created_at)
* **Table: notes** (id, title, content, created_at)