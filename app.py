from flask import Flask, render_template, request
import spacy
from googletrans import Translator

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")
translator = Translator()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['user_message']
    bot_response = process_message(user_message)
    return bot_response

def process_message(message):
    # Process user message using spaCy
    doc = nlp(message)
    
    # Extract verbs and nouns
    verbs = [token.text for token in doc if token.pos_ == "VERB"]
    nouns = [token.text for token in doc if token.pos_ == "NOUN"]
    
     # Check if the user is asking for translation
    if any(word in message.lower() for word in ["translate", "translation", "how do you say"]) and ("in" in message.lower() or "into" in message.lower()):
        return translate_message(message)
    
    # Generate bot response based on the user's message
    bot_response = generate_response(verbs, nouns)
    return "Bot: " + bot_response








def generate_response(verbs, nouns):
    # Generate bot response based on the extracted verbs and nouns
    if verbs and nouns:
        return f"You mentioned {', '.join(verbs)} and {', '.join(nouns)}."
    elif verbs:
        return f"You mentioned {', '.join(verbs)}."
    elif nouns:
        return f"You mentioned {', '.join(nouns)}."
    else:
        return "I'm sorry, I couldn't understand your message."

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











if __name__ == '__main__':
    app.run(debug=True)
