from flask import Flask, request, render_template, jsonify
import speech_recognition as speech
from googletrans import Translator, LANGUAGES

speech_flask = Flask(__name__)

language = {value: key for key, value in LANGUAGES.items()}
key_lang = {key: value for key, value in LANGUAGES.items()}

recording = False
audio_text = ""

@speech_flask.route("/")
def speech():
    return render_template("speech.html")


@speech_flask.route("/translate", methods=["POST"])
def translate_text():
    global audio_text

    try:
        # Parse the JSON data from the request
        data = request.get_json()
        recorded_text = data.get("audio_text")
        target_language = data.get("target_language")

        if not recorded_text:
            return jsonify({"error": "No recorded audio to translate"})

        trans = Translator()
        lang = trans.detect(recorded_text)
        print("Source Language used:", key_lang[lang.lang])
        gn_lang = key_lang[lang.lang]
        txt = trans.translate(recorded_text, dest=gn_lang)
        print("Your speech in text:", txt.text)
        t_text = trans.translate(recorded_text, dest=target_language)
        print("Translated text:", t_text.text)

        return jsonify({"src_lang": key_lang[lang.lang], "sp_text": txt.text, "trans_txt": t_text.text})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    speech_flask.run(debug=True)
