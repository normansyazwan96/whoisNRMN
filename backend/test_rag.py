import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_collection(name="resume")

results = collection.get()

print("Documents:", len(results["documents"]))

for document in results["documents"]:
    print("\n--- Resume ---")
    print(document[:1000])