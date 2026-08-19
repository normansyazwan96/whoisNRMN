from pathlib import Path
import chromadb

# Read resume
text = Path("resume.md").read_text(encoding="utf-8")

# Split resume into chunks
chunks = [
    chunk.strip()
    for chunk in text.split("\n\n")
    if chunk.strip()
]

# Create persistent ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")

# Delete existing collection so re-running ingestion updates it
try:
    client.delete_collection("resume")
except Exception:
    pass

collection = client.create_collection(name="resume")

# Store chunks
collection.add(
    documents=chunks,
    ids=[f"resume-{i}" for i in range(len(chunks))]
)

print(f"Resume successfully ingested.")
print(f"Created {len(chunks)} chunks.")