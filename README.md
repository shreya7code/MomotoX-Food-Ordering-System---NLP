# Momotox - AI Chatbot for Food Ordering 🍔🤖

This is an **End-to-End NLP Chatbot** built using **Dialogflow**, **FastAPI**, and **MySQL** for an online food ordering system. The chatbot assists users in placing, modifying, and tracking their food orders through a conversational interface. The backend leverages FastAPI for webhook handling, connecting to a MySQL database for storing and processing order data.

## 📺 Tutorial Reference  
This project follows the tutorial:  
[End-to-End NLP Project | Build a Chatbot in Dialogflow | NLP Tutorial | S3 E2](https://www.youtube.com/watch?v=2e5pQqBvGco)

## 🚀 Features  
- 🤖 **Dialogflow Integration** for Natural Language Understanding  
- 🍽️ **FastAPI** for webhook processing and backend logic  
- 🛠️ **MySQL Database** for storing orders and tracking status  
- 🔄 **Real-time Order Tracking**  
- 💬 **Order Modification** through the chatbot (add/remove items)  
- ✅ **Order Completion** and receipt generation

## 🛠️ Tech Stack  
- **Natural Language Processing (NLP)**  
- **Dialogflow** (CX or ES) for the conversational interface  
- **FastAPI** (Python) for backend services  
- **MySQL** for database storage  
- **Python** for backend and script execution  
- **MySQL Connector** for database interaction  

## 📌 Setup & Installation  
1. **Clone the repository**  
   ```bash
   git clone https://github.com/your-username/momotox.git
   cd momotox
   ```
   
2. **Create a virtual environment (Optional but recommended)**  
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activa
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Setup MySQL Database**
  - Make sure you have MySQL installed and running.
  - Create a new database MomotoX (or modify the database name in the code as needed).
  - Run the required schema and stored procedures for the project. (This might include tables like orders, order_tracking, and stored procedures like insert_order_item.)

## 🚀 Running the FastAPI Webhook
1. **Start FastAPI Server**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

3. **Expose locally for Dialogflow testing**
  Use Ngrok to expose your local server:
   ```bash
   ngrok http 8000
   ```

3. **Set the Webhook URL in Dialogflow:**
  After exposing your server, set the URL in your Dialogflow webhook settings:
   ```bash
   https://your-ngrok-url/webhook
   ```

## 🎯 Usage
  - Users interact with the chatbot through Dialogflow, sending intents like "order.add", "order.remove", and "order.complete".
  - FastAPI processes these intents and manages order data.
  - Users can add/remove items from their orders, track the order status, and complete their orders for delivery.

## 📝 Future Improvements
  - ✅ Integrate payment processing
  - ✅ Add multi-language support
  - ✅ Deploy to Google Cloud Run
  - ✅ Implement order delivery status notifications
