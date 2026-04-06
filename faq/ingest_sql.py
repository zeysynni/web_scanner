import sqlite3
import os
from mcp_params import sql_db_name

def init_db(db_path: str = f"./memory/{sql_db_name}.db"):
    con = sqlite3.connect(db_path)
    con.execute("""
        CREATE TABLE IF NOT EXISTS knowledge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            content TEXT
        )
    """)
    con.commit()
    con.close()

def ingest_md_files(folder: str = "outputs", db_path: str = f"./memory/{sql_db_name}.db"):
    con = sqlite3.connect(db_path)
    files = [f for f in os.listdir(folder) if f.endswith(".md")]
    for fname in files:
        path = os.path.join(folder, fname)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        topic = fname.replace(".md", "")
        con.execute("INSERT INTO knowledge (topic, content) VALUES (?, ?)", (topic, content))
        print(f"Ingested {fname}")
    con.commit()
    con.close()
    print("Done.")

if __name__ == "__main__":
    init_db()
    ingest_md_files()