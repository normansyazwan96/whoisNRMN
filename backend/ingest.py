from pathlib import Path

import chromadb

BASE_DIR = Path(__file__).resolve().parent
RESUME_PATH = BASE_DIR / "resume.md"
DB_PATH = BASE_DIR / "chroma_db"

text = RESUME_PATH.read_text(encoding="utf-8")

chunks = [
    chunk.strip()
    for chunk in text.split("\n\n")
    if chunk.strip()
]

client = chromadb.PersistentClient(path=str(DB_PATH))

try:
    client.delete_collection("resume")
except Exception:
    pass

collection = client.create_collection(name="resume")
collection.add(
    documents=chunks,
    ids=[f"resume-{i}" for i in range(len(chunks))],
)

print("Resume successfully ingested.")
print(f"Created {len(chunks)} chunks in {DB_PATH}.")
