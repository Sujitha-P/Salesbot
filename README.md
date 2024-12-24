# Sales Chatbot

## Overview

The **Sales Chatbot** is an intelligent assistant built to help customers with product recommendations, sales queries, pricing information, and more. It utilizes various AI models for natural language understanding, sentiment analysis, tone detection, and intent analysis. The chatbot provides real-time interaction with customers and allows them to communicate through text or voice. The backend is powered by **Flask**, and the frontend is created using **HTML**, **CSS**, and **JavaScript** for a dynamic user experience.

### Features
- **Speech Recognition**: Converts speech input into text for seamless interaction.
- **Sentiment Analysis**: Determines the sentiment of user input (positive, negative, or neutral).
- **Tone Detection**: Detects the tone of the user (calm, excited, angry, etc.).
- **Intent Analysis**: Recognizes whether the user is looking to purchase a product or gather information.
- **Real-time Responses**: Real-time communication with the chatbot through Server-Sent Events (SSE).
- **Sentiment Graph**: Visualizes sentiment changes as the conversation progresses using **Chart.js**.

## Backend

### Technologies Used
- **Flask**: A lightweight Python web framework to build the backend API.
- **Groq API**: AI model integration to generate intelligent chatbot responses.
- **Transformers**: Hugging Face library for sentiment analysis and natural language processing.
- **SpeechRecognition**: Converts user speech to text using Google’s speech recognition API.
- **pyttsx3**: Text-to-Speech library for generating voice responses from the chatbot.
- **Chart.js**: For visualizing sentiment data on the frontend.

### Main Components of Backend:
1. **app.py**:
   - The core of the application, containing all routes and logic.
   - Uses Flask to serve the frontend and handle API requests.
   - Connects to **Groq API** for product recommendations and responses.
   - Integrates **Transformers** to perform sentiment analysis on user input.
   - Uses **pyttsx3** to provide speech output from the chatbot.
   - Handles **Server-Sent Events (SSE)** to push data from the backend to the frontend in real-time.

2. **products.json**:
   - A mock database of products that the chatbot can recommend based on user queries.
   - Example content:
     ```json
     [
       {
         "name": "Laptop",
         "price": "$1000",
         "description": "A high-performance laptop."
       },
       {
         "name": "Headphones",
         "price": "$200",
         "description": "Noise-canceling headphones."
       }
     ]
     ```

### Libraries Used in Backend:
- **Flask**: Web framework to handle HTTP requests (`flask==2.2.2`).
- **Transformers**: Pre-trained models for sentiment analysis (`transformers==4.12.3`).
- **SpeechRecognition**: Speech-to-text library (`SpeechRecognition==3.8.1`).
- **pyttsx3**: Text-to-speech conversion library (`pyttsx3==2.90`).
- **Groq API**: Used for AI-driven responses (`groq==1.0.0`).
- **Chart.js**: JavaScript library for visual representation of sentiment analysis.

## Frontend

### Technologies Used
- **HTML/CSS**: The backbone for the layout and design of the chatbot interface.
- **JavaScript**: Dynamically handles chat interaction, updates the chat window, and visualizes sentiment analysis.
- **Chart.js**: A library for drawing dynamic, real-time charts.

### Key Frontend Components:
1. **HTML/CSS**: 
   - Defines the structure of the chatbot interface, including chat history, sentiment graph, and input forms.
   - Responsive design to ensure the UI is mobile-friendly.
  
2. **JavaScript**:
   - Handles real-time communication with the backend using **Server-Sent Events (SSE)**.
   - Updates the chat interface dynamically without needing page reloads.
   - Visualizes sentiment analysis using **Chart.js**. The graph updates with each new input, showing changes in sentiment over time (positive, negative, neutral).

3. **Chart.js Integration**:
   - Visualizes sentiment analysis dynamically as a line graph, with:
     - Positive sentiment as `1`,
     - Negative sentiment as `-1`,
     - Neutral sentiment as `0`.

4. **User Interaction**:
   - Users can type messages or use voice input.
   - Sentiment, tone, and intent analysis are displayed dynamically as the conversation progresses.
   - The chatbot responds with text and/or voice depending on user preference.

## Setup Instructions

### Prerequisites
- **Python 3.x**: Make sure Python 3.x is installed.
- **Node.js**: Ensure Node.js is installed to manage frontend dependencies (if applicable).

