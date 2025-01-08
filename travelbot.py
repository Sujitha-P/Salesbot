from flask import Flask, request, jsonify, render_template_string, Response
from groq import Groq
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import speech_recognition as sr
import json
import logging

# Initialize Flask app
app = Flask(__name__)

# Initialize Groq client
client = Groq(
    api_key="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"
)

# Initialize VADER Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# Intent analysis
def analyze_intent(text):
    if "vehicle" in text:
        return "Enquiry about vehicle"
    elif "cost" in text:
        return "Enquiry about price"
    elif "price" in text or "discount" in text:
        return "Willing to Book"
    elif "hate" in text or "don't like" in text or "dont like" in text:
        return "Not willing to Book"
    elif "like" in text or "love" in text:
        return "Interested"
    elif "not interested" in text:
        return "Not Interested"
    else:
        return "Neutral"

# HTML Template (same as before)
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sales Assistant Chatbot</title>
    <style>
        body { 
            font-family: Arial, sans-serif; margin: 0; padding: 0; 
            background-color: #f4f4f9; display: flex; justify-content: center; align-items: center; 
            height: 100vh;
        }
        .container {
            display: flex;
            justify-content: space-between;
            width: 100%;
            max-width: 1200px;
            height: 80vh;
            margin: 20px;
        }
        .chat-container { 
            width: 60%; 
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            background: white; 
            border-radius: 10px; 
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            padding: 20px;
            position: relative;
        }
        h2 { 
            color: #333; 
            margin-bottom: 20px; 
        }
        .messages { 
            list-style: none; 
            padding: 0; 
            margin: 0; 
            overflow-y: auto; 
            max-height: 380px; 
            flex-grow: 1; 
        }
        .message { 
            margin-bottom: 10px; 
            padding: 10px; 
            border-radius: 5px; 
            text-align: left;
            word-wrap: break-word;
        }
        .bot-message { background-color: #f1f1f1; }
        .user-message { background-color: #e0ffe0; }

        .analysis-container { 
            width: 35%; 
            height: 100%; 
            background: white; 
            border-radius: 10px; 
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); 
            padding: 20px;
            display: flex;
            flex-direction: column;
            justify-content: flex-start; /* Ensure content is stacked from top */
        }

        .analysis-title {
            font-size: 20px;
            margin-bottom: 15px;
        }

        .analysis-box {
            background-color: #f1f1f1;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 10px; /* Reduced gap between boxes */
        }

        .analysis-text {
            font-size: 16px;
            color: #555;
        }

        .positive { color: green; }
        .negative { color: red; }
        .neutral { color: gray; }

        .controls {
            display: flex;
            justify-content: space-between;
        }
        .controls button {
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            border: none;
            border-radius: 5px;
            background-color: #007bff;
            color: white;
            margin: 5px;
        }
        .controls button:disabled {
            background-color: #cccccc;
            cursor: not-allowed;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="chat-container">
            <h2>Sales Assistant Chatbot</h2>
            <ul class="messages" id="messages"></ul>
            <div class="controls">
                <button id="start-bot">Start Bot</button>
                <button id="stop-bot" disabled>Stop Bot</button>
            </div>
        </div>

        <div class="analysis-container">
            <div class="analysis-box">
                <div class="analysis-title">Sentiment Analysis</div>
                <div id="sentiment-analysis" class="analysis-text">Neutral</div>
            </div>

            <div class="analysis-box">
                <div class="analysis-title">Intent Analysis</div>
                <div id="intent-analysis" class="analysis-text">Neutral</div>
            </div>
        </div>
    </div>

    <script>
    const messages = document.getElementById("messages");
    const sentimentElement = document.getElementById("sentiment-analysis");
    const intentElement = document.getElementById("intent-analysis");
    const startButton = document.getElementById("start-bot");
    const stopButton = document.getElementById("stop-bot");

    let eventSource;

    startButton.addEventListener("click", () => {
        eventSource = new EventSource('/stream');
        eventSource.onmessage = (event) => {
            const data = JSON.parse(event.data);

            if (data.role === "user") {
                messages.innerHTML += `<li class="message user-message"><b>You:</b> ${data.message}</li>`;
            } else if (data.role === "bot") {
                messages.innerHTML += `
                    <li class="message bot-message">
                        <b>Bot:</b> ${data.message}
                    </li>`;

                sentimentElement.innerText = data.sentiment;
                intentElement.innerText = data.intent;

                messages.scrollTop = messages.scrollHeight;
            }
        };

        startButton.disabled = true;
        stopButton.disabled = false;
    });

    stopButton.addEventListener("click", () => {
        eventSource.close();
        startButton.disabled = false;
        stopButton.disabled = true;
    });
</script>
</body>
</html>
"""

# Route to serve the microphone icon (placed in static folder)
@app.route('/static/mic.png')
def serve_icon():
    return app.send_static_file('mic.png')

@app.route("/", methods=["GET"])
def index():
    return render_template_string(html_template)

@app.route("/stream", methods=["GET"])
def stream():
    def generate():
        recognizer = sr.Recognizer()
        mic = sr.Microphone()

        yield f"data: {json.dumps({'role': 'system', 'message': 'Listening... Please speak.'})}\n\n"

        while True:
            try:
                audio = None
                with mic as source:
                    recognizer.adjust_for_ambient_noise(source)
                    yield f"data: {json.dumps({'role': 'system', 'message': 'Listening...'})}\n\n"
                    audio = recognizer.listen(source, timeout=5)

                if audio:
                    user_input = recognizer.recognize_google(audio)
                    yield f"data: {json.dumps({'role': 'user', 'message': user_input})}\n\n"

                    # Sentiment Analysis using VADER
                    sentiment_result = analyzer.polarity_scores(user_input)
                    if sentiment_result['compound'] >= 0.05:
                        sentiment_label = "Positive"
                    elif sentiment_result['compound'] <= -0.05:
                        sentiment_label = "Negative"
                    else:
                        sentiment_label = "Neutral"

                    intent = analyze_intent(user_input)

                    query = f"You are Navi, a sales assistant for travels and tourism business.You suggest vehicles to user based on the no. of people, hours and package(hourly or outstation) based on their request.: {user_input}"
                    chat_completion = client.chat.completions.create(
                        messages=[{"role": "user", "content": query}],
                        model="llama3-8b-8192",
                        max_tokens=150,
                        temperature=0.3
                    )
                    response = chat_completion.choices[0].message.content.strip()

                    yield f"data: {json.dumps({'role': 'bot', 'message': response, 'sentiment': sentiment_label, 'intent': intent})}\n\n"

            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                yield f"data: {json.dumps({'role': 'system', 'message': 'Service unavailable. Please try again later.'})}\n\n"

    return Response(generate(), content_type="text/event-stream")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True, host="0.0.0.0", port=5000)
