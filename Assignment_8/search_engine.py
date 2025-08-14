from openai import AzureOpenAI
from dotenv import load_dotenv
from scipy.spatial.distance import cosine
import os

load_dotenv()

client = AzureOpenAI(
    api_version="2024-02-15-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
)

# Step 2: Sample product data
products = [
    {
        "title": "Classic Blue Jeans",
        "short_description": "Comfortable blue denim jeans with a relaxed fit.",
        "price": 49.99,
        "category": "Jeans",
    },
    {
        "title": "Red Hoodie",
        "short_description": "Cozy red hoodie made from organic cotton.",
        "price": 39.99,
        "category": "Hoodies",
    },
    {
        "title": "Black Leather Jacket",
        "short_description": "Stylish black leather jacket with a slim fit design.",
        "price": 120.00,
        "category": "Jackets",
    },
    {
        "title": "Running Shoes",
        "short_description": "Lightweight running shoes designed for comfort and speed.",
        "price": 89.99,
        "category": "Shoes",
    },
    {
        "title": "Sports Watch",
        "short_description": "Durable sports watch with GPS and heart rate monitor.",
        "price": 199.99,
        "category": "Watches",
    },
    {
        "title": "White Cotton T-Shirt",
        "short_description": "Soft, breathable white t-shirt made from 100% cotton.",
        "price": 19.99,
        "category": "T-Shirts",
    },
    {
        "title": "Gray Wool Sweater",
        "short_description": "Warm and comfortable wool sweater with a classic crew neck.",
        "price": 59.99,
        "category": "Sweaters",
    },
    {
        "title": "Brown Leather Belt",
        "short_description": "Genuine brown leather belt with a polished silver buckle.",
        "price": 25.00,
        "category": "Accessories",
    },
    {
        "title": "Backpack",
        "short_description": "Spacious and durable backpack with multiple compartments.",
        "price": 69.99,
        "category": "Bags",
    },
    {
        "title": "Sunglasses",
        "short_description": "Polarized sunglasses with UV protection and modern style.",
        "price": 49.50,
        "category": "Accessories",
    },
    {
        "title": "Yoga Mat",
        "short_description": "Non-slip yoga mat with extra cushioning for comfort.",
        "price": 29.99,
        "category": "Fitness",
    },
    {
        "title": "Beanie Hat",
        "short_description": "Knitted beanie hat to keep you warm in cold weather.",
        "price": 15.99,
        "category": "Hats",
    },
    {
        "title": "Water Bottle",
        "short_description": "Insulated stainless steel water bottle keeps drinks cold or hot.",
        "price": 22.00,
        "category": "Accessories",
    },
]

# Step 3: Function to get embeddings from Azure OpenAI
def get_embedding(text):
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    embedding = response.data[0].embedding
    return embedding


# Step 4: Generate embeddings for all product descriptions
for product in products:
    product["embedding"] = get_embedding(product["short_description"])

# Step 5: Accept user input (query)
query = "Tshirt for summer wear"

# Step 6: Get embedding for the user query
query_embedding = get_embedding(query)


# Step 7: Compute cosine similarity between query and each product
def similarity_score(vec1, vec2):
    return 1 - cosine(vec1, vec2)  # cosine returns distance; 1 - distance = similarity


scores = []

for product in products:
    score = similarity_score(query_embedding, product["embedding"])
    scores.append((score, product))

# Step 8: Sort products by similarity descending
scores.sort(key=lambda x: x[0], reverse=True)

# Step 9: Display top matches
print(f"Top matching products for query: '{query}'\n")

for score, product in scores[:3]:  # top 3 results
    print(f"Title: {product['title']}")
    print(f"Description: {product['short_description']}")
    print(f"Price: ${product['price']}")
    print(f"Category: {product['category']}")
    print(f"Similarity Score: {score:.4f}\n")

print("End of results.")
