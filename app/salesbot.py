from flask import Flask, request, jsonify, render_template_string, Response
from groq import Groq
from transformers import pipeline
import speech_recognition as sr
import pyttsx3
import threading
import json
import random
import os

app = Flask(__name__)

# Initialize Groq client
client = Groq(
    api_key="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"
)

# Load BERT sentiment analysis pipeline
sentiment_analyzer = pipeline("sentiment-analysis")

# Tone analysis (dummy tones for demo)
def analyze_tone(text):
    tones = ["Calm", "Excited", "Serious", "Happy"]
    return random.choice(tones)

# Intent analysis
def analyze_intent(text):
    if "price" in text or "discount" in text:
        return "Willing to Buy"
    elif "not interested" in text:
        return "Not Interested"
    elif "like" in text or "love" in text:
        return "Interested"
    elif "hate" in text or "don't like" in text:
        return "Not willing to buy"
    else:
        return "Neutral"

# Text-to-Speech setup
tts_engine = pyttsx3.init()

# HTML Template
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
        /* Left container (Chat) */
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
        /* Messages Section */
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

        /* Right container (Sentiment Graph and Analysis) */
        .analysis-container { 
            width: 35%; 
            height: 100%; 
            background: white; 
            border-radius: 10px; 
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); 
            padding: 20px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        .analysis-title {
            font-size: 20px;
            margin-bottom: 15px;
        }

        .analysis-box {
            background-color: #f1f1f1;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
        }

        .analysis-text {
            font-size: 16px;
            color: #555;
        }

        .positive { color: green; }
        .negative { color: red; }
        .neutral { color: gray; }

        /* Sentiment Graph */
        .sentiment-graph {
            width: 100%;
            height: 300px;
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Left side (Chat) -->
        <div class="chat-container">
            <h2>Sales Assistant Chatbot</h2>
            <ul class="messages" id="messages"></ul>
        </div>

        <!-- Right side (Sentiment Graph and Analysis) -->
        <div class="analysis-container">
            <div class="analysis-box">
                <div class="analysis-title">Sentiment Analysis Over Time</div>
                <canvas id="sentiment-graph" class="sentiment-graph"></canvas>
            </div>

            <div class="analysis-box">
                <div class="analysis-title">Tone Analysis</div>
                <div id="tone-analysis" class="analysis-text">Neutral</div>
            </div>

            <div class="analysis-box">
                <div class="analysis-title">Intent Analysis</div>
                <div id="intent-analysis" class="analysis-text">Neutral</div>
            </div>
        </div>
    </div>

    <!-- Include Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <script>
    const messages = document.getElementById("messages");
    const toneElement = document.getElementById("tone-analysis");
    const intentElement = document.getElementById("intent-analysis");

    // Initialize the sentiment graph
    const ctx = document.getElementById('sentiment-graph').getContext('2d');
    const sentimentData = {
        labels: [],
        datasets: [{
            label: 'Sentiment over Time',
            data: [],
            borderColor: 'rgba(0, 123, 255, 1)',
            backgroundColor: 'rgba(0, 123, 255, 0.2)',
            fill: true,
            tension: 0.4
        }]
    };

    const sentimentChart = new Chart(ctx, {
        type: 'line',
        data: sentimentData,
        options: {
            scales: {
                y: {
                    min: -1,
                    max: 1,
                    ticks: {
                        callback: function(value) {
                            if (value === 1) return 'Positive';
                            if (value === -1) return 'Negative';
                            return 'Neutral';
                        }
                    }
                },
                x: {
                    type: 'linear',
                    position: 'bottom',
                    title: {
                        display: true,
                        text: 'Prompt Number'
                    }
                }
            }
        }
    });

    const eventSource = new EventSource('/stream');

    eventSource.onmessage = (event) => {
        const data = JSON.parse(event.data);

        if (data.role === "user") {
            messages.innerHTML += `<li class="message user-message"><b>You:</b> ${data.message}</li>`;
        } else if (data.role === "bot") {
            messages.innerHTML += `
                <li class="message bot-message">
                    <b>Bot:</b> ${data.message}
                </li>`;

            // Update tone and intent analysis
            toneElement.innerText = data.tone;
            intentElement.innerText = data.intent;

            // Log received sentiment for debugging
            console.log("Sentiment received:", data.sentiment);

            // Map sentiment to numerical value
            let sentimentValue = 0;  // Default neutral

            if (data.sentiment === "positive") {
                sentimentValue = 1;
            } else if (data.sentiment === "negative") {
                sentimentValue = -1;
            }

            // Log sentiment value before updating the chart
            console.log("Mapped sentiment value:", sentimentValue);

            // Update sentiment chart with new data
            sentimentData.labels.push(sentimentData.labels.length + 1);  // Add prompt number
            sentimentData.datasets[0].data.push(sentimentValue);  // Add sentiment value
            sentimentChart.update();

            // Scroll messages to the latest message
            messages.scrollTop = messages.scrollHeight;
        }
    };
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

        yield f"data: {json.dumps({'role': 'system', 'message': 'Click the mic button to start speaking.'})}\n\n"

        while True:
            try:
                # Wait for frontend to trigger audio input
                audio = None
                with mic as source:
                    recognizer.adjust_for_ambient_noise(source)
                    yield f"data: {json.dumps({'role': 'system', 'message': 'Listening...'})}\n\n"
                    audio = recognizer.listen(source, timeout=5)

                if audio:
                    # Recognize speech
                    user_input = recognizer.recognize_google(audio)
                    yield f"data: {json.dumps({'role': 'user', 'message': user_input})}\n\n"

                    # Sentiment analysis
                    sentiment_result = sentiment_analyzer(user_input)[0]
                    sentiment_label = sentiment_result["label"]

                    # Tone analysis
                    tone = analyze_tone(user_input)

                    # Intent analysis
                    intent = analyze_intent(user_input)

                    # Generate response
                    query = f"You are a sales assistant who assists customers with their queries and negotiates with customers to make successful deals which benefits the company and also makes the customers happy with a positive sentiment. Provide a concise and complete response in a professional way: {user_input}"
                    chat_completion = client.chat.completions.create(
                        messages=[{"role": "user", "content": query}],
                        model="llama3-8b-8192",
                        max_tokens=150,
                        temperature=0.8
                    )
                    response = chat_completion.choices[0].message.content.strip()

                    # Send response back
                    yield f"data: {json.dumps({'role': 'bot', 'message': response, 'sentiment': sentiment_label, 'tone': tone, 'intent': intent})}\n\n"

                    # Run TTS in a separate thread to prevent blocking
                    threading.Thread(target=tts_engine.say, args=(response,)).start()
                    tts_engine.runAndWait()

            except sr.UnknownValueError:
                yield f"data: {json.dumps({'role': 'system', 'message': 'Could not understand. Click the mic again.'})}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'role': 'system', 'message': f'Error: {str(e)}'})}\n\n"

    return Response(generate(), content_type="text/event-stream")

@app.route("/start-listening", methods=["GET"])
def start_listening():
    threading.Thread(target=stream).start()
    return jsonify({"status": "Listening started."})

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
