# Sentimind AI

**Real-Time AI Sales Intelligence and Sentiment-Driven Deal Negotiation Assistant - Sentimind AI aims to transform the sales process by developing an AI-powered assistant that provides real-time sentiment analysis, intent detection, personalized recommendations, and negotiation coaching. It reduces manual effort, improves customer engagement, and optimizes the sales workflow.**

---

## **Features**

- **Sentiment Analysis**: Understand user sentiment (e.g., Positive, Negative, Neutral).
- **Emotion Detection**: Identify user emotions like Excitement, Frustration, or Confusion.
- **Purchase Intent Analysis**: Determine urgency and intent (e.g., Immediate, Exploratory, or Comparative).
- **Behavioral Insights**: Analyze browsing patterns and behavioral signals.
- **Advanced Intent Detection**: Spot high-value, sales-qualified leads.
- **Personalized Recommendations**: Offer customized product suggestions.
- **CRM Integration**: Track user interactions for a personalized experience.
- **Post-Call Insights**: Generate actionable summaries and follow-up suggestions.
- **Negotiation Coaching**: Provide strategies and objection-handling tips.
- **Google Sheets Integration**: Log analytics into Google Sheets automatically.
- **Real-Time Speech Recognition**: Capture user speech and provide real-time insights.
- **Dashboard Visualization**: Display real-time sentiment, emotion, and engagement metrics during calls.
- **Transcription & Analysis Export**: Save call transcripts and analysis results to Excel files.
- **Feedback Mechanism**: Improve recommendations through thumbs-up or thumbs-down feedback.

---

## **Demo**

<!-- Add a GIF or video demo of your project in action -->

---

## **Table of Contents**

1. [Installation](#installation)
2. [Usage](#usage)
3. [Features](#features)
4. [API Documentation](#api-documentation)
5. [License](#license)
6. [Contact](#contact)
7. [Acknowledgments](#acknowledgments)

---

## **Installation**

### **Prerequisites**

- Python 3.x
- Groq API Key ([Sign up at Groq](https://www.groq.com))
- Google Sheets & Drive API ([Enable at Google Cloud Console](https://console.cloud.google.com))

### **Steps**

1. Clone the repository:

    ```bash
    git clone https://github.com/Resultyst/Infosys_Sentimind_AI.git
    cd Infosys_Sentimind_AI
    ```

2. Set up the backend:

    ```bash
    pip install -r requirements.txt
    ```

3. Serve the frontend:

    Serve the `index.html` file using your preferred web server.

4. Configure environment variables:

    Add your Groq API key and preferred LLM model in the `config.py` file:

    ```env
    # Groq API Key
    GROQ_API_KEY=your_groq_api_key_here

    # LLM Model
    LLM_MODEL="any open source llm model"
    ```

5. Run the application:

    ```bash
    uvicorn app.main:app --reload
    ```

6. Open the application in your browser:

    ```
    http://127.0.0.1:8000
    ```

---

## **Usage**

### **Step-by-Step Guide**

1. **Open the Application**:
    - Use an audio-supported browser (e.g., Chrome, Firefox).
    - Navigate to the application URL: `http://127.0.0.1:8000`.

2. **Start the session**:
    - Click the microphone button (green) to begin speech recognition.

3. **Speak Naturally**:
    - Engage in a simulated sales conversation.
    - Real-time insights will display on the dashboard:
      - Sentiment: Positive, Negative, Neutral, etc.
      - Emotion: Excitement, Frustration, Confusion, etc.
      - Engagement: Low, Moderate, High.
      - Purchase Intent: Immediate, Exploratory, Comparative, etc.

4. **Provide Feedback**:
    - Thumbs Up: Satisfied with recommendations.
    - Thumbs Down: Unsatisfied—adjusts future recommendations.

5. **Stop the session**:
    - End the session by clicking the microphone button(red).
    - Save the transcription and analysis to an Excel file.

### **Example Workflow**

1. **Start a Call**:
    - Say: "Hi, I'm looking for a new smartphone with a good camera. My budget is around ₹30,000."

2. **Real-Time Dashboard Updates**:
    - Sentiment: Positive
    - Emotion: Curiosity
    - Purchase Intent: Immediate
    - Behavioral Intent: Product page exploration

3. **Product Recommendations**:
    - Suggestions prioritize in-stock smartphones within budget.

4. **Provide Feedback**:
    - Thumbs Up for satisfaction.
    - Thumbs Down for alternatives.

5. **Save Results**:
    - Full call transcription.
    - Sentiment, emotion, and intent analysis.
    - Performance analytics and follow-up suggestions.

---

## **API Documentation**

### **Endpoints**

### 1. GET /
**Description:** Serves the main HTML page for the application.

**Method:** GET

**Response:**
- **Content-Type:** text/html
- **Response Body:** HTML content of the application's frontend.

---

### 2. POST /get_response
**Description:** Processes user input (text or speech) and returns real-time insights, including sentiment, emotion, engagement, purchase intent, and product recommendations.

**Method:** POST

**Request Body:**
```json
{
  "user_input": "I'm looking for a new smartphone with a good camera.",
  "user_name": "John Doe",
  "email": "john.doe@example.com"
}
```
- **user_input:** The text or speech input from the user.
- **user_name:** The name of the user (optional).
- **email:** The email of the user (required for CRM tracking).

**Response:**
```json
{
  "response": "I'm looking for a new smartphone with a good camera.",
  "sentiment": "Positive",
  "emotion": "Curiosity",
  "engagement": "High",
  "purchase_intent": "Immediate purchase intent",
  "behavioral_intent": "Product page exploration",
  "advanced_intent": "High-value lead identification",
  "suggestions": [
    {
      "ProductName": "Smartphone X",
      "ProductPrice": "₹28,999",
      "Rating": "4.5",
      "StockAvailability": "In Stock",
      "Features": "48MP Camera, 128GB Storage",
      "Description": "Great performance and features"
    }
  ],
  "is_existing_user": true,
  "user_name": "John Doe",
  "last_product": "smartphones"
}
```
- **response:** The user input echoed back.
- **sentiment:** The sentiment analysis result.
- **emotion:** The detected emotional state.
- **engagement:** The level of buyer engagement.
- **purchase_intent:** The classified purchase intent.
- **behavioral_intent:** The behavioral intent signals.
- **advanced_intent:** Advanced intent detection insights.
- **suggestions:** A list of recommended products.
- **is_existing_user:** Indicates if the user exists in the CRM.
- **user_name:** The name of the user.
- **last_product:** The last product searched by the user (if available).

---

### 3. POST /handle_feedback
**Description:** Handles user feedback (thumbs_up or thumbs_down) on product recommendations and updates the CRM.

**Method:** POST

**Request Body:**
```json
{
  "user_input": "I'm looking for a new smartphone with a good camera.",
  "email": "john.doe@example.com",
  "feedback": "thumbs_up",
  "user_name": "John Doe"
}
```
- **user_input:** The original user input.
- **email:** The email of the user (required for CRM tracking).
- **feedback:** The feedback provided (thumbs_up or thumbs_down).
- **user_name:** The name of the user (optional).

**Response:**
```json
{
  "new_recommendations": [
    {
      "ProductName": "Smartphone Y",
      "ProductPrice": "₹29,999",
      "Rating": "4.7",
      "StockAvailability": "In Stock",
      "Features": "64MP Camera, 256GB Storage",
      "Description": "Excellent camera and performance"
    }
  ]
}
```
- **new_recommendations:** Updated product recommendations based on feedback.

---

### 4. POST /post_call_insights
**Description:** Generates post-call insights, including a summary, performance analytics, deal status, and follow-up suggestions.

**Method:** POST

**Request Body:**
```json
{
  "transcription": "Customer was interested in a new laptop but was concerned about the price.",
  "user_name": "John Doe",
  "email": "john.doe@example.com"
}
```
- **transcription:** The transcription of the call.
- **user_name:** The name of the user (optional).
- **email:** The email of the user (required for CRM tracking).

**Response:**
```json
{
  "user_name": "John Doe",
  "email": "john.doe@example.com",
  "sentiment": "Neutral",
  "emotion": "Hesitation",
  "purchase_intent": "Exploratory purchase intent",
  "behavioral_intent": "Website browsing intent",
  "advanced_intent": "High-value lead identification",
  "recommendations": [
    {
      "ProductName": "Laptop Z",
      "ProductPrice": "₹45,999",
      "Rating": "4.6",
      "StockAvailability": "In Stock",
      "Features": "16GB RAM, 512GB SSD",
      "Description": "Great for productivity and gaming"
    }
  ],
  "summary": "Customer is interested in a new laptop but is concerned about the price.",
  "performance_analytics": "Moderate engagement, price sensitivity detected.",
  "deal_status": "Open",
  "follow_up_suggestions": "Offer a discount or financing options.",
  "negotiation_tactics": "Highlight the long-term value of the product.",
  "objection_handling": "Address price concerns by comparing with competitors."
}
```
- **summary:** A concise summary of the call.
- **performance_analytics:** Performance metrics and insights.
- **deal_status:** Updated deal status (Open, Negotiation, Closed-Won, Closed-Lost).
- **follow_up_suggestions:** Actionable follow-up suggestions.
- **negotiation_tactics:** Negotiation strategies for the sales team.
- **objection_handling:** Suggestions for handling objections.

---

### 5. POST /negotiation_coach
**Description:** Provides negotiation tactics and objection handling strategies based on user input.

**Method:** POST

**Request Body:**
```json
{
  "user_input": "The customer is hesitant due to the price."
}
```
- **user_input:** The input describing the negotiation scenario.

**Response:**
```json
{
  "negotiation_tactics": "Highlight the long-term value and ROI of the product.",
  "objection_handling": "Offer a discount or financing options to address price concerns."
}
```
- **negotiation_tactics:** Suggested negotiation strategies.
- **objection_handling:** Strategies for handling objections.



---

## **Feedback Mechanism**

Feedback is central to Sentimind AI's adaptive learning:

1. **Thumbs Up**:
    - Prioritizes similar products in the future.
    - Updates CRM with positive feedback for improved personalization.

2. **Thumbs Down**:
    - Broadens search criteria or shuffles results.
    - Avoids similar products in future recommendations.
    - Logs feedback for refining user preferences.

3. **Feedback Integration**:
    - All feedback is stored in the CRM under user profiles.
    - Helps refine recommendations and enhance user satisfaction.

---

## **License**

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

---

## **Contact**

For questions or feedback, reach out:

- **Email**: [resultyst@gmail.com](mailto:resultyst@gmail.com)
- **GitHub**: [Resultyst](https://github.com/Resultyst)
- **LinkedIn**: [Suryaa Narayanan K](https://www.linkedin.com/in/resultyst7/)

---

## **Acknowledgments**

- **Groq** for providing the AI API.
- **FAISS** for efficient similarity search and clustering.
- **Sentence Transformers** for high-quality sentence embeddings.
- **FastAPI** for building a high-performance API.

---

