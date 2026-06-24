import ollama

# Test 1: Embedding
response = ollama.embeddings(
    model="nomic-embed-text",
    prompt="hello world"
)
print("Embedding size:", len(response['embedding']))

# Test 2: Generation
response = ollama.chat(
    model="llama3.2",
    messages=[{"role": "user", "content": "say hi in one word"}]
)
print("LLM response:", response['message']['content'])