from flask import Flask, request, jsonify, render_template
import pyaudio
import speech_recognition as sr
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def process_message():
    user_message = request.json["user_message"]
    bot_response = generate_bot_response(user_message)
    return jsonify(bot_response)

def generate_bot_response(user_message):
    if any(word in user_message.lower() for word in ["translate", "translation", "how do you say"]) and ("in" in user_message.lower() or "into" in user_message.lower()):
        return translate_message(user_message)
    else:
        return "I'm sorry, I couldn't understand your request."

def translate_message(message):
    # Extract the target language and the word/sentence to translate
    parts = message.lower().split("translate")
    if len(parts) < 2:
        parts = message.lower().split("how do you say")
    if len(parts) < 2:
        parts = message.lower().split("translation of")
    if len(parts) < 2:
        return "I'm sorry, I couldn't understand your translation request."

    parts = parts[1].split("into") if "into" in parts[1] else parts[1].split("in")
    if len(parts) < 2:
        return "I'm sorry, I couldn't understand your translation request."
    
    target_language = parts[-1].strip()
    word_to_translate = parts[0].strip()
    
    # Translate the word/sentence to the target language
    translated_text = translator.translate(word_to_translate, dest=target_language).text
    
    #return f"{translated_text}"
    return f"The translation of '{word_to_translate}' in {target_language} is '{translated_text}'."



@app.route("/voice", methods=["POST"])
def process_voice_input():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        return jsonify(text)
    except sr.UnknownValueError:
        return jsonify("Sorry, I couldn't understand what you said.")
    except sr.RequestError as e:
        return jsonify(f"Sorry, an error occurred. {e}")

if __name__ == "__main__":
    app.run(debug=True)
