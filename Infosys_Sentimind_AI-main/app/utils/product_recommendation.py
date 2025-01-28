import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer
from groq import Groq
import json
from datetime import datetime

from app.utils.crm_utils import load_crm_data,save_crm_data, add_user_interaction

from config import GROQ_API_KEY, LLM_MODEL, FAISS_INDEX_PATH, METADATA_CSV_PATH, ALLOWED_PRODUCTS

# Load FAISS index and metadata
model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.read_index(FAISS_INDEX_PATH)
metadata = pd.read_csv(METADATA_CSV_PATH)

# Groq client setup
client = Groq(api_key=GROQ_API_KEY)

# Define retrieval function
def retrieve_products(prompt, top_k=5, feedback=None):
    query_embedding = model.encode([prompt])
    distances, indices = index.search(query_embedding, top_k * 2)  # Fetch more to ensure stock availability
    retrieved = metadata.iloc[indices[0]]

    # Adjust retrieval based on feedback
    if feedback == "thumbs_down":
        # If feedback is negative, broaden the search or adjust filters
        retrieved = retrieved.sample(frac=1).reset_index(drop=True)  # Shuffle results
    elif feedback == "thumbs_up":
        # If feedback is positive, prioritize higher-rated products
        retrieved = retrieved.sort_values(by="Rating", ascending=False)

    # Separate in-stock and out-of-stock items
    in_stock = retrieved[retrieved["StockAvailability"] == "In Stock"]
    out_of_stock = retrieved[retrieved["StockAvailability"] == "Out of Stock"]

    # Ensure at least 2 in-stock products in the top 5
    final_selection = []
    if len(in_stock) >= 2:
        final_selection.extend(in_stock.head(2).to_dict(orient="records"))
    else:
        final_selection.extend(in_stock.to_dict(orient="records"))

    # If needed, fill up the remaining spots with out-of-stock products
    remaining_spots = top_k - len(final_selection)
    if remaining_spots > 0:
        final_selection.extend(out_of_stock.head(remaining_spots).to_dict(orient="records"))

    return final_selection

# RAG-based recommendation function
def recommend_product(user_prompt, email, user_name="You", feedback=None):
    # Load CRM data
    crm_data = load_crm_data()
    user = next((u for u in crm_data["users"] if u["email"] == email), None)

    # If user doesn't exist, initialize their data
    if not user:
        user = {
            "email": email,
            "preferences": [],
            "history": [],
            "budget": None,
            "feedback_history": []
        }
        crm_data["users"].append(user)
        save_crm_data(crm_data)

    # Step 1: Retrieve products based on feedback
    retrieved = retrieve_products(user_prompt, top_k=5, feedback=feedback)

    # Filter products based on the user's budget
    if user.get("budget"):
        retrieved = [p for p in retrieved if p["ProductPrice"] <= user["budget"]]

    # Separate in-stock and out-of-stock items
    in_stock = pd.DataFrame([p for p in retrieved if p['StockAvailability'] == 'In Stock'])
    out_of_stock = pd.DataFrame([p for p in retrieved if p['StockAvailability'] == 'Out of Stock'])

    # Ensure that exactly 3 products are suggested, with priority for in-stock
    final_selection = []
    if len(in_stock) >= 2:
        final_selection.extend(in_stock.head(2).to_dict(orient="records"))
    else:
        final_selection.extend(in_stock.to_dict(orient="records"))

    remaining_spots = 3 - len(final_selection)
    if remaining_spots > 0:
        final_selection.extend(out_of_stock.head(remaining_spots).to_dict(orient="records"))

    # Format product details for the response
    product_details = "\n\n".join([
        f"👉 **{p['ProductName']}**\n"
        f"   - 💰 Price: ₹{p['ProductPrice']}\n"
        f"   - ⭐ Rating: {p['Rating']}\n"
        f"   - 📦 Stock: {p['StockAvailability']}\n"
        f"   - 🔹 Features: {p['Features']}\n"
        f"   - 💡 Why you'll love it: {p.get('Description', 'Great performance and features')}"
        for p in final_selection
    ])

    # Step 2: Generate a context-aware response using Groq API
    response = client.chat.completions.create(
        messages=[{
            "role": "system",
            "content": (
                "You are a helpful and empathetic sales assistant. "
                "Your task is to respond to the user's input in a personalized and context-aware manner. "
                "Acknowledge their concerns, empathize with their situation, and provide relevant product recommendations. "
                "Keep the tone conversational and professional."
            )
        },
        {
            "role": "user",
            "content": (
                f"User input: {user_prompt}\n\n"
                f"Here are the top product recommendations:\n\n"
                f"{product_details}\n\n"
                f"Generate a personalized response that acknowledges the user's dissatisfaction (if any) and provides the recommendations in a natural and empathetic way."
            )
        }],
        model="llama3-8b-8192",  # Use the appropriate model
    )

    # Add the interaction to the user's history
    add_user_interaction(email, user_prompt, "searched")

    return response.choices[0].message.content