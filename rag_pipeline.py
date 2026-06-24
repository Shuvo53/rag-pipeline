from pypdf import PdfReader
import ollama
import chromadb
import os

# Step 1: Load and chunk
def load_and_chunk(pdf_path, chunk_size=500, overlap=50):
    reader = PdfReader(pdf_path)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text()

    chunks = []
    start = 0
    while start < len(full_text):
        end = start + chunk_size
        chunks.append(full_text[start:end])
        start += chunk_size - overlap

    return chunks

# Step 2: Embed and store in ChromaDB
def build_vector_store(chunks):
    client = chromadb.PersistentClient(path="./chroma_db")
    try:
        client.delete_collection("rag_docs")
    except:
        pass
    collection = client.create_collection("rag_docs")
    for i, chunk in enumerate(chunks):
        response = ollama.embeddings(
            model="nomic-embed-text",
            prompt=chunk
        )
        collection.add(
            ids=[str(i)],
            embeddings=[response['embedding']],
            documents=[chunk]
        )
        print(f"Stored chunk {i+1}/{len(chunks)}")
    return collection

# Step 3: Query + Retrieve + Generate
def ask(question):
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection("rag_docs")
    q_embedding = ollama.embeddings(
        model="nomic-embed-text",
        prompt=question
    )
    results = collection.query(
        query_embeddings=[q_embedding['embedding']],
        n_results=3
    )
    context = "\n\n".join(results['documents'][0])
    prompt = f"""Answer the question using only the context below.
If the answer is not in the context, say "I don't know."

Context:
{context}

Question: {question}
"""
    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['message']['content']

# Main
if not os.path.exists("./chroma_db"):
    chunks = load_and_chunk("rag_architecture.pdf")
    print(f"Total chunks: {len(chunks)}")
    build_vector_store(chunks)
else:
    print("Vector store already exists, skipping indexing.")

while True:
    question = input("\nAsk a question (or type 'exit' to quit): ")
    if question.lower() == "exit":
        break
    print("\n" + ask(question))