# 🌟 Gen AI-Based Order Management System 🌟  

> **Transforming natural language into actionable structured orders!**  

---

## 📖 Overview  
This project is a cutting-edge **Gen AI-based order management system** that uses conversational AI and vector databases to streamline order processing. From interpreting natural language to generating precise orders, the system is designed to handle the complexities of modern grocery orders with finesse.  

✨ **Key Highlights**:  
- Parse natural language into structured data using **LLM (LLaMA)**.  
- Match products with a vector database powered by **Pinecone**.  
- Generate polished, structured orders with detailed line items.  
- Intuitive user interface for seamless order review and confirmation.  

---

## 🛠️ Features  
- **Conversational Parsing**: Extract items, quantities, and units from user input.  
- **Intelligent Matching**: Use embeddings to find the closest product matches in a database.  
- **Order Generation**: Create structured orders with:  
  - 🆔 **Order ID**  
  - 📅 **Order Date**  
  - 📦 **Line Items**: Product Code, Description, Quantity, and Price.  
- **Interactive Review**:  
  - Adjust quantities.  
  - View similar product alternatives.  
  - Confirm and finalize the order.  

---

## 🏗️ Technical Stack  

| **Component**        | **Technology**                |  
|-----------------------|-------------------------------|  
| Programming Language  | Python                        |  
| Framework             | Flask                         |  
| LLM                  | Open-source LLaMA Model       |  
| Embedding Model       | `BAAI/bge-large-en`           |  
| Vector Database       | Pinecone                      |  

---

## 🛤️ Architecture and Workflow  

### 1️⃣ **Input Handling**  
Users enter conversational purchase requests into a simple and intuitive text area. For example:  
> "I need 2 bags of 1kg rice and 1 bottle of 500ml olive oil."

---

### 2️⃣ **Text Parsing**  
Using **LLaMA**, the input is processed to extract structured data:  
- **Product Name**: "rice"  
- **Quantity**: "2"  
- **Unit**: "1kg"  

The parsed results are formatted as:  
`[Item Name and Size/Unit]: [Quantity]`  

---

### 3️⃣ **Embedding and Matching**  
- The **BAAI/bge-large-en** model converts extracted item names into embeddings (vector representations).  
- These embeddings are queried against a **Pinecone** index to find the most similar product matches.  
- The matched products include:  
  - Product Code  
  - Description  
  - Price  

---

### 4️⃣ **Order Generation**  
The system assembles the matched products into a structured order, which includes:  
- **Order ID**: Generated using Python's `uuid`.  
- **Order Date**: Fetched dynamically using `datetime`.  
- **Line Items**: Each item contains the product code, description, quantity, and price.  

---

### 5️⃣ **Interactive Review**  
Users are presented with an order summary for review:  
- Modify quantities using increment (+) and decrement (-) buttons.  
- View alternative products for each item(Working on that feature)  
- Confirm the order when satisfied.  

---

### 6️⃣ **Order Finalization**  
Once confirmed, the system generates an **Order Summary** with:  
- Total Price  
- Detailed Line Items  
- Clear Formatting  

---
### 7️⃣ **Downloading Pdf**:
User can have a copy of the final Order:
- locally have a copy


## 🖼️ Application Walkthrough  

### 1. **Homepage**  
![image](https://github.com/user-attachments/assets/fa2198b2-3628-49b8-8856-93cf4fb09110)
_A clean and welcoming page with a simple input form._  

---

### 2. **Input Form**  
![image](https://github.com/user-attachments/assets/cca04f63-1472-4982-a2e7-32e427471dd2)
  
_Users can input their conversational grocery requests here._  

---

### 3. **Results Page**  
![image](https://github.com/user-attachments/assets/6cbb0b64-f1fd-48e6-85a8-bb7fb500171b)
_Parsed and matched results are displayed with options to adjust quantities or view alternatives._  

---

### 4. **Order Summary**  
![image](https://github.com/user-attachments/assets/86a38c7e-5701-422d-a492-b33ea71bffff)
_The final summary of the order with a detailed breakdown._  

---
### 5. **Printing Pdf**
![image](https://github.com/user-attachments/assets/b5fe6912-d1bd-4d98-9b1d-9f9f8de5af8a)
_printing the order summary._


## 🚀 How to Run  

### Prerequisites  
1. **Install Python**: Version 3.9 or higher.  
2. **Install Dependencies**: Use the provided `requirements.txt`.  
   ```bash
   pip install -r requirements.txt
### 🔑 Set Up API Keys  

To run the application, you need to set up API keys for **Pinecone** and **Hugging Face**. Follow these steps:  

### 1. **Pinecone API Key**  
- Go to [Pinecone's official website](https://www.pinecone.io/).  
- Sign up or log in to your account.  
- Navigate to the **API Keys** section in the dashboard.  
- Copy your API key.  

### 2. **Hugging Face API Key**  
- Go to [Hugging Face's official website](https://huggingface.co/).  
- Sign up or log in to your account.  
- Navigate to your **Account Settings** > **Access Tokens**.  
- Generate a new token (select the "Write" scope).  
- Copy the token.  

---

### 3. **Store API Keys in an `.env` File**  
For security, store your API keys in a `.env` file instead of hardcoding them into your application.  

1. Create a new file named `.env` in the root directory of your project.  
2. Add the following lines, replacing `YOUR_PINECONE_API_KEY` and `YOUR_HUGGINGFACE_API_KEY` with your actual keys:  

   ```env
   PINECONE_API_KEY=YOUR_PINECONE_API_KEY
   HUGGINGFACE_API_KEY=YOUR_HUGGINGFACE_API_KEY

## 🚀 Running the Application  

### Clone the Repository:  
```bash
git clone https://github.com/deepan484/Burnt_Order_Management_System.git
cd <repository-folder>
```
Under Terminal type in:

`python app.py`

## 📚 Code Structure  

| **File**                   | **Purpose**                                              |  
|-----------------------------|---------------------------------------------------------|  
| `app.py`                   | Main Flask application logic.                            |  
| `functions.py`             | Core functions for embedding, matching, and ordering.    |  
| `initialisation_Testing.py`| Includes the complete process of testing and setting up Pinecone, including embedding generation, upserting, and querying. |  
| `templates/`               | HTML templates for UI.                                   |  
| `static/`                  | CSS and JavaScript files for styling and interaction.    |  
| `products.csv`             | Product database (code, description, price).             |  
