import base64
from gtts import gTTS
import tempfile

def speak_in_browser(text):
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        audio_bytes = open(fp.name, "rb").read()
        b64 = base64.b64encode(audio_bytes).decode()
        audio_html = f"""
            <audio autoplay controls style='width: 100%;'>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
        """
        return audio_html
