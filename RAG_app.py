
# Step 3.1: Suppress Noisy Logs
import logging
import warnings
from transformers import logging as hf_logging

# Suppress LangChain text splitter logs
logging.getLogger("langchain.text_splitter").setLevel(logging.ERROR)

# Suppress HuggingFace/transformers logs
hf_logging.set_verbosity_error()

# Suppress Python warnings
warnings.filterwarnings("ignore")



# Step 3.2: Load ChatGPT API Credentials
import os
from dotenv import load_dotenv
import openai

# Load environment variables from .env
load_dotenv()

# Read the API key
openai.api_key = os.getenv("OPENAI_API_KEY")



# Step 3.3: RAG Parameters
chunk_size = 500
chunk_overlap = 50
model_name = "sentence-transformers/all-distilroberta-v1"
top_k = 20



# Step 3.4: Re-ranking Parameters
cross_encoder_name = "cross-encoder/ms-marco-MiniLM-L-6-v2"
top_m = 8


# Read the Pre-scraped Document
with open("Selected_Document.txt", "r", encoding="utf-8") as f:
    text = f.read()

print("Loaded document length:", len(text))


# Step 3.5: Split into Appropriately-Sized Chunks
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    separators=["", "\n", " ", ""],
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap
)

chunks = text_splitter.split_text(text)
print("Number of chunks:", len(chunks))


# Step 3.6: Embed & Build FAISS Index
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

# Load the embedding model
embedder = SentenceTransformer(model_name)

# Encode chunks into embeddings (progress bar hidden)
embeddings = embedder.encode(
    chunks,
    show_progress_bar=False
)

# Convert to NumPy float32 array
embeddings = np.array(embeddings).astype("float32")

# Initialize FAISS index with correct dimension
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)

# Add embeddings to the index
index.add(embeddings)



# Step 3.7: Retrieval Function
def retrieve_chunks(question, k=top_k):
    # Encode the question
    q_vec = embedder.encode([question], show_progress_bar=False)

    # Convert to NumPy float32 array
    q_arr = np.array(q_vec).astype("float32")

    # Search FAISS index for top-k nearest neighbors
    D, I = index.search(q_arr, k)

    print("FAISS returned indices:", I)

    # Build retrieved chunk list
    retrieved_chunks = [chunks[i] for i in I[0] if i != -1]

    print("Retrieved chunk count:", len(retrieved_chunks))

    return retrieved_chunks


# Step 3.8: Cross-Encoder Re-Ranker
from sentence_transformers import CrossEncoder
import re

# Initialize the cross-encoder model
reranker = CrossEncoder(cross_encoder_name)

# Helper: remove duplicates while preserving order
def dedupe_preserve_order(items):
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

# Normalize whitespace to avoid near-duplicate slices
def normalize_whitespace(text):
    return re.sub(r"\s+", " ", text).strip()

# Re-ranking function
def rerank_chunks(question: str, candidate_chunks: list[str], m: int = top_m) -> list[str]:
    # Normalize candidate chunks
    cleaned = [normalize_whitespace(c) for c in candidate_chunks]

    # Create (question, chunk) pairs
    pairs = [(question, c) for c in cleaned]

    # Score with cross-encoder (higher = more relevant)
    scores = reranker.predict(pairs)

    # Sort by score descending
    ranked = sorted(zip(cleaned, scores), key=lambda x: x[1], reverse=True)

    # Select top m chunks
    top_chunks = [chunk for chunk, score in ranked[:m]]

    # Remove duplicates while preserving order
    return dedupe_preserve_order(top_chunks)



# Step 3.9: Q&A with ChatGPT

def answer_question(question: str) -> str:
    """
    Retrieve relevant chunks, re-rank them, build a context string,
    and query the ChatGPT API for an answer grounded in that context.
    """

    # Retrieve top_k candidate chunks
    candidate_chunks = retrieve_chunks(question)

    # Re-rank and keep only the top_m most relevant chunks
    relevant_chunks = rerank_chunks(question, candidate_chunks, m=top_m)

    # Build the context string
    context = "\n\n".join(relevant_chunks)

    # System prompt to enforce grounding
    system_prompt = (
        "You are a knowledgeable assistant that answers questions based on the provided context. "
        "If the answer is not in the context, say you don’t know."
    )

    # User prompt containing context + question
    user_prompt = f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"

    # Call the Chat Completions API
    response = openai.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_completion_tokens=500
    )

    # Return the assistant's reply
    return response.choices[0].message.content.strip()



# Step 3.10: Interactive Loop
if __name__ == "__main__":
    print("Enter 'exit' or 'quit' to end.")
    while True:
        question = input("Your question: ")
        if question.lower() in ("exit", "quit"):
            break
        print("Answer:", answer_question(question))
