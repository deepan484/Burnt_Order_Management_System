import pandas as pd
from pinecone import Pinecone
import torch
from transformers import AutoTokenizer, AutoModel
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

load_dotenv()

pinecone_api_key = os.getenv('pincone_key')
hugging_face_api = os.getenv('hugging_face_key')

def calculate_order_summary(order_details):

    df = pd.read_csv('products.csv') 
    order = []
    total_price = 0
    for detail in order_details:
        item_name, quantity, product_code = detail.split(':')
        quantity = int(quantity)
        price = df[df['product_code'] == product_code]['product_price'].values[0]
        total = price * quantity
        order.append({
            'name': item_name,
            'code': product_code,
            'quantity': quantity,
            'price': price,
            'total': total
        })
        total_price += total
    
    return order, round(total_price, 2)

def backend(user_input):
    # Initialize Pinecone and Hugging Face models
    pc = Pinecone(api_key = pinecone_api_key)
    index = pc.Index("product-embedding")
    client = InferenceClient(api_key = hugging_face_api)
    tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-large-en")
    model = AutoModel.from_pretrained("BAAI/bge-large-en")

    def get_embedding(text):
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

    # Create LLaMA prompt
    messages = [
        {
            "role": "user",
            "content": f"""
    You are an AI assistant tasked with extracting grocery items and their quantities from the provided text. The response must strictly adhere to the following rules:

    **Output Format:**
    - [Item Name and Size/Unit]: [Quantity]

    **Examples:**
    - Saku Tuna Blocks 2lbs: 1
    - Shrimp 8/12: 2
    - Brisket 10lbs: 1
    - Onion Beer Case: 1
    - Dashi Mushroom Bag: 1

    **Important Extraction Guidelines:**
    1. **Quantity vs. Size/Unit**:
    - If a size/unit like "2lbs" appears, it is always part of the item name.
    - The quantity refers only to the **number of items** (e.g., 1 block of Saku Tuna 2lbs → `Saku Tuna Blocks 2lbs: 1`).
    - If the Quantity is not specified assume it to be **1**
    - Example:
        - Input: "2lbs Saku Tuna Blocks" → Output: Saku Tuna Blocks 2lbs: 1
        - Input: "2 8/12 shrimp" → Output: Shrimp 8/12: 2
    2. **Units or Packaging Types**:
    - Include units like `case`, `bag`, `pcs`, or specific sizes (e.g., `16/24oz`) as part of the item name.
    - Example:
        - Input: "1 case onion beer" → Output: Onion Beer Case: 1
        - Input: "1 bag dashi mushroom" → Output: Dashi Mushroom Bag: 1
    3. **Only Numeric Quantities in the Quantity Field**:
    - The numeric quantity represents the count of the item, not its size or weight.
    - Example:
        - Input: "10 lbs brisket" → Output: Brisket 10lbs: 1
    4. **Exclude Filler Text**:
    - Ignore phrases like "Hi, I need," or "Can you get me."
    - Focus only on the product names and quantities.
    5. **Capture Order of Words**:
    - If the size/unit appears before or after the item name (e.g., "2lbs brisket" or "brisket 2lbs"), treat it consistently as part of the item name.
    

    **Input Text:**
    {user_input}

    **Output Requirements:**
    - Each item should be on a new line in the format `[Item Name and Size/Unit]: [Quantity]`.
    - Do not add extra explanations or comments. Only provide the extracted data in the specified format.

    Begin extracting the grocery items and quantities.
    """
        }
    ]

    try:
        # LLaMA response
        completion = client.chat.completions.create(
            model="meta-llama/Llama-3.2-3B-Instruct", messages=messages, max_tokens=500
        )
        response = completion.choices[0].message.content

        # Process extracted items
        items = {}
        for line in response.split("\n"):
            if ":" in line:
                item, quantity = line.split(":", 1)
                items[item.strip()] = quantity.strip()

        # Load CSV and query Pinecone
        df_products = pd.read_csv("products.csv")
        results_for_html = []
        for item, quantity in items.items():
            query_vector = get_embedding(item).tolist()
            results = index.query(
                vector=query_vector, top_k=1, include_metadata=True
            )
            top_match = results["matches"][0] if results["matches"] else None

            # Fetch product details from CSV
            product_row = (
                df_products[df_products["product_code"] == top_match["metadata"]["product_code"]]
                if top_match
                else None
            )

            # Prepare result entry for this item
            results_for_html.append({
                "original_item": item,
                "quantity": quantity,
                "matched_product": product_row.iloc[0]["product_description"] if not product_row.empty else "N/A",
                "similarity_score": top_match["score"] if top_match else 0,
                "product_code": top_match["metadata"]["product_code"] if top_match else "N/A"
            })

        # Return results for rendering
        return results_for_html

    except Exception as e:
        return {"error": str(e)}
