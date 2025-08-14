import chromadb
from openai import AzureOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# ---- EMBEDDING CONFIG ----
AZURE_OPENAI_EMBEDDING_API_KEY = os.getenv("AZURE_OPENAI_EMBEDDING_API_KEY")
AZURE_OPENAI_EMBEDDING_ENDPOINT = os.getenv("AZURE_OPENAI_EMBEDDING_ENDPOINT")
AZURE_OPENAI_EMBED_MODEL = os.getenv("AZURE_OPENAI_EMBED_MODEL")

# ---- LLM CONFIG ----
AZURE_OPENAI_LLM_API_KEY = os.getenv("AZURE_OPENAI_LLM_API_KEY")
AZURE_OPENAI_LLM_ENDPOINT = os.getenv("AZURE_OPENAI_LLM_ENDPOINT")
AZURE_OPENAI_LLM_MODEL = os.getenv("AZURE_OPENAI_LLM_MODEL")

# ---- CLIENTS ----
embedding_client = AzureOpenAI(
    api_key=AZURE_OPENAI_EMBEDDING_API_KEY,
    azure_endpoint=AZURE_OPENAI_EMBEDDING_ENDPOINT,
    api_version="2023-05-15",
)

llm_client = AzureOpenAI(
    api_key=AZURE_OPENAI_LLM_API_KEY,
    azure_endpoint=AZURE_OPENAI_LLM_ENDPOINT,
    api_version="2023-05-15",
)

# ---- GET EMBEDDING ----
def get_embedding(text):
    response = embedding_client.embeddings.create(
        input=text, model=AZURE_OPENAI_EMBED_MODEL
    )
    return response.data[0].embedding


# ---- CALL LLM ----
def ask_llm(context, user_input):
    system_prompt = (
        "You are a helpful assistant specializing in laptop recommendations. "
        "Use the provided context to recommend the best laptop(s) for the user needs."
    )
    user_prompt = (
        f"User requirements: {user_input}\n\n"
        f"Context (top relevant laptops):\n{context}\n\n"
        "Based on the above, which laptop(s) would you recommend and why?"
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    response = llm_client.chat.completions.create(
        model=AZURE_OPENAI_LLM_MODEL, messages=messages
    )
    return response.choices[0].message.content


# ---- CHROMADB ----
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="laptops")

laptops = [
    {
        "id": "1",
        "name": "Gaming Beast Pro",
        "description": "A high-end gaming laptop with RTX 4080, 32GB RAM, and 1TB SSD. Perfect for hardcore gaming.",
        "tags": "gaming, high-performance, windows",
    },
    {
        "id": "2",
        "name": "Business Ultrabook X1",
        "description": "A lightweight business laptop with Intel i7, 16GB RAM, and long battery life. Great for productivity.",
        "tags": "business, ultrabook, lightweight",
    },
    {
        "id": "3",
        "name": "Student Basic",
        "description": "Affordable laptop with 8GB RAM, 256GB SSD, and a reliable battery. Ideal for students and general use.",
        "tags": "student, budget, general",
    },
    {
        "id": "4",
        "name": "Creative Studio Pro",
        "description": "Powerful laptop with Intel i9, 64GB RAM, NVIDIA RTX 4070, and 2TB SSD. Designed for video editing and 3D rendering.",
        "tags": "creator, high-performance, windows",
    },
    {
        "id": "5",
        "name": "TravelMate Air",
        "description": "Ultra-portable laptop with AMD Ryzen 5, 8GB RAM, 512GB SSD, and 18-hour battery life. Ideal for frequent travelers.",
        "tags": "lightweight, travel, battery-life",
    },
    {
        "id": "6",
        "name": "EcoBook Green",
        "description": "Eco-friendly laptop made with recycled materials, Intel i5, 16GB RAM, and energy-efficient display.",
        "tags": "eco-friendly, business, general",
    },
    {
        "id": "7",
        "name": "Gaming Lite X",
        "description": "Budget gaming laptop with GTX 1650, 16GB RAM, and 512GB SSD. Good for casual gaming.",
        "tags": "gaming, budget, windows",
    },
    {
        "id": "8",
        "name": "Workstation Titan",
        "description": "Heavy-duty workstation with Intel Xeon, 128GB RAM, NVIDIA Quadro RTX, and ECC memory for professional workloads.",
        "tags": "workstation, professional, high-performance",
    },
    {
        "id": "9",
        "name": "2-in-1 FlexBook",
        "description": "Convertible touchscreen laptop with Intel i7, 16GB RAM, and stylus support. Great for note-taking and presentations.",
        "tags": "2-in-1, convertible, touchscreen",
    },
    {
        "id": "10",
        "name": "Chromebook Go",
        "description": "Lightweight Chromebook with 4GB RAM, 64GB storage, and long battery life. Ideal for web browsing and online learning.",
        "tags": "chromebook, budget, education",
    },
]


# ---- ADD LAPTOPS TO CHROMADB ----
for laptop in laptops:
    embedding = get_embedding(laptop["description"])
    collection.add(
        embeddings=[embedding],
        documents=[laptop["description"]],
        ids=[laptop["id"]],
        metadatas=[{"name": laptop["name"], "tags": laptop["tags"]}],
    )

# ---- AUTOMATED MOCK INPUTS ----
user_queries = [
    "I want a lightweight laptop with long battery life for business trips.",
    "I need a laptop for gaming with the best graphics card available.",
    "Looking for a budget laptop suitable for student tasks and general browsing.",
]


def build_context(results, n_context=3):
    docs = results["documents"][0]
    metas = results["metadatas"][0]
    context_str = ""
    for doc, meta in zip(docs, metas):
        context_str += (
            f"Name: {meta['name']}\n"
            f"Description: {doc}\n"
            f"Tags: {meta['tags']}\n\n"
        )
    return context_str.strip()


# ---- MAIN RAG LOOP ----
for user_input in user_queries:
    print("=" * 60)
    print(f"User input: {user_input}")
    # Step 1: Retrieve relevant laptops via vector search
    query_embedding = get_embedding(user_input)
    results = collection.query(query_embeddings=[query_embedding], n_results=3)
    # Step 2: Build context for LLM
    context = build_context(results)
    # Step 3: Get recommendation from LLM
    llm_output = ask_llm(context, user_input)
    print("\nLLM Recommendation:\n")
    print(llm_output)
    print("=" * 60 + "\n")
