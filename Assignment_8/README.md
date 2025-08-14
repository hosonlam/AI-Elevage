# Product Semantic Search Engine

## Overview

This project demonstrates a simple semantic search engine for product descriptions using Azure OpenAI embeddings and cosine similarity.

---

## How Embeddings Were Created and Used

- **Embeddings Creation:**  
  For each product, the short description was sent to the Azure OpenAI embedding endpoint (using a deployed embedding model, e.g., `text-embedding-3-small` or `text-embedding-ada-002`). The returned embedding vector represents the semantic meaning of the product description.
- **Query Embedding:**  
  The user's search query is also converted into an embedding vector using the same model.
- **Usage:**  
  Both product and query embeddings are used to measure semantic similarity, allowing the search engine to match products to the user's intent, even if the wording differs.

---

## Explanation of Cosine Similarity for Ranking

- **Cosine Similarity:**  
  Cosine similarity measures the cosine of the angle between two vectors in high-dimensional space. It ranges from -1 (opposite) to 1 (identical), with 0 indicating orthogonality (no similarity).
- **Ranking:**  
  For each product, the cosine similarity between its embedding and the query embedding is computed. Products are then ranked in descending order of similarity, so the most semantically relevant products appear first.

---

## Challenges and Limitations

- **Model Deployment:**  
  The embedding model must be deployed in Azure OpenAI, and the correct deployment name must be used. Using an unavailable or incorrect model name results in errors.
- **API Costs and Latency:**  
  Each embedding request is an API call, which may incur costs and can be slow for large product catalogs.
- **Semantic Limitations:**  
  Embeddings capture general meaning but may not always reflect nuanced user intent or product features, especially for very short or ambiguous descriptions.
- **Similarity Metric:**  
  Cosine similarity works well for semantic matching but may not capture all aspects of relevance (e.g., price, popularity).
- **Error Handling:**  
  Proper error handling is needed for missing embeddings, API failures, or malformed data.

---

## Conclusion

This approach enables more flexible and intelligent product search by leveraging modern language models and vector similarity, but it requires careful deployment and consideration of API usage and