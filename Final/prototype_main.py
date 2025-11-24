# prototype_main.py - Initial Proof of Concept
import sqlite3
import os
from openai import OpenAI

# Uses a separate DB to avoid breaking the main app
DB_NAME = "prototype.db" 

try:
    client = OpenAI()
except:
    client = None

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, description TEXT, status TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, title TEXT, content TEXT)")
    conn.commit()
    conn.close()

def main():
    init_db()
    print("--- PROTOTYPE V1 (Basic Functionality) ---")
    print("Commands: task <name>, list, note <title>|<content>, ask <question>")
    
    while True:
        cmd = input("PROTO > ").strip()
        if cmd == "quit": break
        
        if cmd.startswith("task "):
            conn = sqlite3.connect(DB_NAME)
            conn.execute("INSERT INTO tasks (description, status) VALUES (?, ?)", (cmd[5:], 'pending'))
            conn.commit()
            print("Task saved.")
            
        elif cmd == "list":
            conn = sqlite3.connect(DB_NAME)
            rows = conn.execute("SELECT * FROM tasks").fetchall()
            for r in rows: print(r)
            
        elif cmd.startswith("ask "):
            if client:
                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": cmd[4:]}]
                )
                print("AI:", res.choices[0].message.content)
            else:
                print("AI not connected.")

if __name__ == "__main__":
    main()