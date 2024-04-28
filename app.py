from flask import Flask, request, jsonify, render_template
import speech_recognition as sr
from googletrans import Translator
import spacy

app = Flask(__name__)
translator = Translator()
nlp = spacy.load("en_core_web_sm")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def process_message():
    user_message = request.json["user_message"]
    bot_response = generate_bot_response(user_message)
    return jsonify(bot_response)

def generate_bot_response(user_message):
    doc = nlp(user_message.lower())
    
    # Check if user wants translation
    if any(token.text in ["translate", "translation"] for token in doc) and ("in" in user_message.lower() or "into" in user_message.lower()):
        return translate_message(user_message)
    elif "how do you say" in user_message.lower():
        return translate_message(user_message)
    
    # Check if user wants to engage in conversation about countries
    if any(entity.label_ == "GPE" for entity in doc.ents):
        return engage_in_country_conversation(user_message)
    
    # Check if user wants to engage in conversation about languages
    if any(entity.label_ == "LANGUAGE" for entity in doc.ents):
        return engage_in_language_conversation(user_message)
    
    # Check if user wants to engage in conversation
    if any(token.pos_ in ["VERB", "NOUN"] for token in doc):
        return engage_in_conversation(user_message)
    
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
    
    return f"The translation of '{word_to_translate}' in {target_language} is '{translated_text}'."

def engage_in_country_conversation(user_message):
    # Simple conversation agent related to countries
    return "That's awesome! Would you like to learn some phrases in the language of that country?"

def engage_in_language_conversation(user_message):
    # Simple conversation agent related to languages
    return "That's interesting! Would you like to learn some phrases in that language?"

def engage_in_conversation(user_message):
    # Simple conversation agent
    return "That's interesting! Tell me more."

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
