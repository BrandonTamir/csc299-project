import sqlite3
import os
import sys
import datetime
from openai import OpenAI

# ==========================================
# CONFIGURATION & COLORS
# ==========================================
try:
    client = OpenAI()
except:
    print("Warning: OpenAI API Key not found. AI features will fail nicely.")
    client = None

DB_NAME = "pkms_data.db"

# ANSI Color Codes for Terminal Output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# ==========================================
# DATABASE SETUP (SQLite)
# ==========================================
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Create Tasks Table with Priority and Date
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY, 
                    description TEXT, 
                    status TEXT, 
                    priority TEXT,
                    created_at TEXT
                )''')
    
    # Create Notes Table
    c.execute('''CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY, 
                    title TEXT, 
                    content TEXT,
                    created_at TEXT
                )''')
    conn.commit()
    conn.close()

# ==========================================
# CORE FUNCTIONS
# ==========================================
def add_task(description, priority="Medium"):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Validate priority
    if priority.lower() not in ["high", "medium", "low"]:
        priority = "Medium"
        
    c.execute("INSERT INTO tasks (description, status, priority, created_at) VALUES (?, ?, ?, ?)", 
              (description, 'pending', priority.capitalize(), date))
    conn.commit()
    conn.close()
    print(f"{Colors.GREEN}✅ Task added: {description} [{priority}]{Colors.ENDC}")

def mark_done(task_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tasks SET status = 'DONE' WHERE id = ?", (task_id,))
    if c.rowcount == 0:
        print(f"{Colors.FAIL}❌ Task ID {task_id} not found.{Colors.ENDC}")
    else:
        print(f"{Colors.GREEN}🎉 Task {task_id} marked as COMPLETED!{Colors.ENDC}")
    conn.commit()
    conn.close()

def delete_item(item_type, item_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    table = "tasks" if item_type == "task" else "notes"
    c.execute(f"DELETE FROM {table} WHERE id = ?", (item_id,))
    conn.commit()
    print(f"{Colors.WARNING}🗑️  Deleted {item_type} #{item_id}{Colors.ENDC}")
    conn.close()

def list_tasks():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, description, status, priority, created_at FROM tasks")
    rows = c.fetchall()
    conn.close()
    
    print(f"\n{Colors.HEADER}--- 📝 YOUR TASK LIST ---{Colors.ENDC}")
    if not rows:
        print("(No tasks found)")
    
    for r in rows:
        t_id, desc, status, prio, date = r
        
        # Color Logic
        color = Colors.CYAN
        if status == 'DONE':
            color = Colors.GREEN
            desc = f"~{desc}~" # Strikethrough style
        elif prio == 'High':
            color = Colors.FAIL
        
        print(f"{color}[{t_id}] {desc} | Status: {status} | Priority: {prio} | {date}{Colors.ENDC}")
    print("-----------------------\n")

def add_note(title, content):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    c.execute("INSERT INTO notes (title, content, created_at) VALUES (?, ?, ?)", (title, content, date))
    conn.commit()
    conn.close()
    print(f"{Colors.BLUE}✅ Note saved: {title}{Colors.ENDC}")

def search_notes(query):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, title, content FROM notes WHERE title LIKE ? OR content LIKE ?", 
              (f'%{query}%', f'%{query}%'))
    rows = c.fetchall()
    conn.close()
    print(f"\n{Colors.HEADER}--- 🔍 SEARCH RESULTS FOR '{query}' ---{Colors.ENDC}")
    for r in rows:
        print(f"{Colors.BOLD}[{r[0]}] {r[1]}{Colors.ENDC}: {r[2]}")

def list_notes():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, title, content FROM notes")
    rows = c.fetchall()
    conn.close()
    print(f"\n{Colors.HEADER}--- 📚 KNOWLEDGE BASE ---{Colors.ENDC}")
    for r in rows:
        print(f"{Colors.BLUE}[{r[0]}] {r[1]}{Colors.ENDC}")
    print("-----------------------\n")

# ==========================================
# AI AGENT
# ==========================================
def ask_ai(user_query):
    if not client:
        print(f"{Colors.FAIL}❌ OpenAI client not initialized.{Colors.ENDC}")
        return

    # 1. Gather context
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT description, priority FROM tasks WHERE status='pending'")
    tasks = [f"{r[0]} ({r[1]} Priority)" for r in c.fetchall()]
    c.execute("SELECT title, content FROM notes")
    notes = [f"{r[0]}: {r[1]}" for r in c.fetchall()]
    conn.close()

    context_str = f"User's Pending Tasks: {tasks}\nUser's Notes: {notes}"
    
    print(f"{Colors.WARNING}🤖 AI is thinking...{Colors.ENDC}")
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a smart productivity assistant. Use the user's tasks and notes to give specific advice. If they have High priority tasks, warn them."},
                {"role": "system", "content": f"DATABASE STATE:\n{context_str}"},
                {"role": "user", "content": user_query}
            ]
        )
        print(f"\n{Colors.CYAN}AI Response:\n{response.choices[0].message.content}{Colors.ENDC}\n")
    except Exception as e:
        print(f"AI Error: {e}")

# ==========================================
# MAIN LOOP
# ==========================================
def print_banner():
    print(f"""{Colors.HEADER}
  _____                      _   _______        _    
 / ____|                    | | |__   __|      | |   
| (___  _ __ ___   __ _ _ __| |_   | | __ _ ___| | __
 \___ \| '_ ` _ \ / _` | '__| __|  | |/ _` / __| |/ /
 ____) | | | | | | (_| | |  | |_   | | (_| \__ \   < 
|_____/|_| |_| |_|\__,_|_|   \__|  |_|\__,_|___/_|\_\\
                                                     
    FINAL PROJECT | PKMS + TASK MANAGER | AI
    {Colors.ENDC}""")

def main():
    init_db()
    print_banner()
    print("Commands: 'task <desc> [High/Med/Low]', 'done <id>', 'delete task <id>', 'list', 'note <title>|<content>', 'search <text>', 'ask <query>'")
    
    while True:
        try:
            command = input(f"{Colors.BOLD}COMMAND > {Colors.ENDC}").strip()
            
            if command.lower() in ["quit", "exit"]:
                break
            
            # --- TASK COMMANDS ---
            elif command.lower().startswith("task "):
                parts = command[5:].split()
                # Check if last word is a priority
                if parts[-1].lower() in ["high", "medium", "low"]:
                    prio = parts[-1]
                    desc = " ".join(parts[:-1])
                    add_task(desc, prio)
                else:
                    add_task(" ".join(parts))
            
            elif command.lower().startswith("done "):
                try:
                    t_id = int(command.split()[1])
                    mark_done(t_id)
                except:
                    print("Usage: done <id>")

            elif command.lower() == "list":
                list_tasks()

            # --- NOTE COMMANDS ---    
            elif command.lower().startswith("note "):
                parts = command[5:].split("|")
                if len(parts) < 2:
                    print("❌ Use format: note Title | Content")
                else:
                    add_note(parts[0].strip(), parts[1].strip())

            elif command.lower() == "notes":
                list_notes()
                
            elif command.lower().startswith("search "):
                query = command[7:]
                search_notes(query)

            # --- DELETION ---
            elif command.lower().startswith("delete task "):
                try:
                    delete_item("task", int(command.split()[2]))
                except:
                    print("Usage: delete task <id>")
                    
            elif command.lower().startswith("delete note "):
                try:
                    delete_item("note", int(command.split()[2]))
                except:
                    print("Usage: delete note <id>")

            # --- AI ---    
            elif command.lower().startswith("ask "):
                ask_ai(command[4:])
                
            else:
                print("Unknown command. Try: list, task, note, ask, quit")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()
