import traceback
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from groq import Groq
from transformers import pipeline
import speech_recognition as sr
import pyttsx3
import threading

app = Flask(__name__)

# MongoDB connection
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["Salesbot"]
products = db["Products"]

# Groq client setup
client = Groq(api_key="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")
# Sentiment analysis model
sentiment_analyzer = pipeline("sentiment-analysis")

# Text-to-speech setup
tts_engine = pyttsx3.init()

# Speech recognizer setup
recognizer = sr.Recognizer()
is_listening = False  # Tracks if the bot is actively listening
bot_response = ""  # Stores the latest bot response
user_input_transcript = ""  # Stores the latest user input
bot_thread = None  # To track the bot's listening thread


def speak_text(text):
    """Convert text to speech."""
    tts_engine.say(text)
    tts_engine.runAndWait()


def listen_and_respond():
    """Continuously listen and process user input."""
    global is_listening, bot_response, user_input_transcript

    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)  # Calibrate for ambient noise
            while is_listening:
                print("Listening...")
                try:
                    audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
                    user_input = recognizer.recognize_google(audio)
                    
                    # Check if user_input is empty or None
                    if not user_input:
                        bot_response = "I'm sorry, I couldn't hear anything. Could you please repeat?"
                        continue
                    
                    user_input_transcript = user_input  # Update transcript for frontend

                    # Analyze sentiment and intent
                    sentiment = sentiment_analyzer(user_input)[0]
                    sentiment_score = sentiment["score"]
                    sentiment_label = sentiment["label"]

                    # Intent analysis
                    if "price" in user_input or "discount" in user_input:
                        intent = "Willing to Buy"
                    elif "not interested" in user_input:
                        intent = "Not Interested"
                    elif "like" in user_input or "love" in user_input:
                        intent = "Interested"
                    elif "hate" in user_input or "don't like" in user_input:
                        intent = "Not willing to buy"
                    else:
                        intent = "Neutral"

                    # MongoDB data fetching and response logic
                    if "discount" in user_input:
                        product = products.find_one({"discount": {"$exists": True}})
                        if product:
                            bot_response = f"We currently have a discount of {product['discount']} on {product['productname']}."
                        else:
                            bot_response = "Sorry, no discounts available at the moment."
                    elif "price" in user_input:
                        product = products.find_one()
                        if product:
                            bot_response = f"The price of {product['productname']} is {product['price']}."
                        else:
                            bot_response = "Sorry, I couldn't find the price."
                    elif "products" in user_input or "what products" in user_input:
                        all_products = products.find()
                        product_list = ", ".join([prod["productname"] for prod in all_products])
                        bot_response = f"We offer the following products: {product_list}."
                    else:
                        # LLM fallback for non-specific queries
                        response = client.chat.completions.create(
                            messages=[{"role": "user", "content": user_input}],
                            model="llama3-8b-8192",
                        )
                        bot_response = response.choices[0].message.content

                    # Adjust response based on sentiment and intent
                    if sentiment_label == "NEGATIVE" and intent == "Not Interested":
                        bot_response += " However, we have exciting discounts. Would you like to know more?"
                    elif sentiment_label == "NEGATIVE" and intent == "Not willing to buy":
                        bot_response += " However, we have other great products. Would you like to know more?"

                    # Speak the response
                    speak_text(bot_response)

                except sr.UnknownValueError:
                    bot_response = "I'm sorry, I couldn't understand that. Could you please repeat?"
                except sr.WaitTimeoutError:
                    print("No speech detected. Waiting for the next input...")
                    continue  # Retry listening
                except sr.RequestError as e:
                    bot_response = "Sorry, there was a problem with the speech recognition service."
                except Exception as e:
                    bot_response = f"An error occurred: {str(e)}"
                    print(f"Error occurred during speech recognition: {traceback.format_exc()}")

                # Check for ending criteria
                if "thank you" in user_input.lower():
                    is_listening = False
                    bot_response += " You're welcome! Let me know if you need further assistance."
    except Exception as e:
        bot_response = "There was an unexpected issue. Please try again later."
        print(f"Error occurred in listen_and_respond: {traceback.format_exc()}")


@app.route("/start-bot", methods=["GET"])
def start_bot():
    """Start the bot and begin listening."""
    global is_listening, bot_thread
    is_listening = True  # Set listening to True
    bot_thread = threading.Thread(target=listen_and_respond, daemon=True)  # Start listening in a separate thread
    bot_thread.start()  # Start the bot listening in the background
    speak_text("Hello, how can I assist you today?")
    bot_response = "Hello, how can I assist you today?"  # Send the message to frontend
    return jsonify({"message": bot_response})


@app.route("/stop-bot", methods=["GET"])
def stop_bot():
    """Stop the bot from listening."""
    global is_listening
    is_listening = False  # Stop the listening loop
    if bot_thread:
        bot_thread.join()  # Ensure the thread has finished
    return jsonify({"message": "The bot has stopped listening.", "is_listening": is_listening})


@app.route("/status", methods=["GET"])
def status():
    """Provide bot's current status."""
    global bot_response, user_input_transcript
    return jsonify(
        {
            "is_listening": is_listening,
            "latest_user_input": user_input_transcript,
            "latest_bot_response": bot_response,
        }
    )


@app.route("/")
def index():
    """Render the frontend."""
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
