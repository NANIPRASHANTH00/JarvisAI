from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
import vosk
import sounddevice as sd
import json
import pyttsx3
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load AI Model
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Load Vosk Model for Offline Speech Recognition
vosk_model = vosk.Model("model")
recognizer = vosk.KaldiRecognizer(vosk_model, 16000)

# Text-to-Speech Engine
engine = pyttsx3.init()

def generate_response(prompt):
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    outputs = model.generate(inputs, max_length=100, temperature=0.7)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def listen():
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype="int16", channels=1, callback=lambda i, f, t, s: recognizer.AcceptWaveform(i)):
        return json.loads(recognizer.Result()).get("text", "")

def speak(text):
    engine.say(text)
    engine.runAndWait()

class AIApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        self.label = Label(text="Tap 'Listen' and speak")
        self.layout.add_widget(self.label)

        self.button = Button(text="Listen", on_press=self.get_voice_input)
        self.layout.add_widget(self.button)

        self.response_label = Label(text="AI Response will appear here")
        self.layout.add_widget(self.response_label)

        return self.layout

    def get_voice_input(self, instance):
        self.label.text = "Listening..."
        user_input = listen()
        self.label.text = f"You: {user_input}"

        if user_input:
            ai_response = generate_response(user_input)
            self.response_label.text = f"AI: {ai_response}"
            speak(ai_response)

if __name__ == "__main__":
    AIApp().run()
