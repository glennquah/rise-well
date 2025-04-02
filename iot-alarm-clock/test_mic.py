import tkinter as tk
import speech_recognition as sr

class AudioSensor:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.collected_transcripts = []
        self.stop_listening_func = None

    def start_listening(self, callback):
        self.stop_listening_func = self.recognizer.listen_in_background(self.microphone, callback)


def build_gui():
    root = tk.Tk()
    root.title("Voice Recording")

    transcript_label = tk.Label(root, text="Transcript:", wraplength=400, bg="white", font=("Arial", 12))
    transcript_label.pack(pady=10)

    sensor = AudioSensor()

    def callback(recognizer, audio):
        try:
            transcript = recognizer.recognize_google(audio)
            sensor.collected_transcripts.append(transcript)
            root.after(0, lambda: transcript_label.config(text="Transcript: " + " ".join(sensor.collected_transcripts)))
        except sr.UnknownValueError:
            root.after(0, lambda: transcript_label.config(text="Transcript: (Could not understand audio)"))
        except sr.RequestError as e:
            root.after(0, lambda: transcript_label.config(text=f"Transcript: (Request error: {e})"))

    def start_recording():
        sensor.collected_transcripts = []
        transcript_label.config(text="Recording... Speak now!")
        sensor.start_listening(callback)
        start_record_btn.config(state="disabled")
        stop_record_btn.config(state="normal")

    def stop_recording():
        # Stop background listening
        if sensor.stop_listening_func:
            sensor.stop_listening_func(wait_for_stop=False)
        start_record_btn.config(state="normal")
        stop_record_btn.config(state="disabled")
        final_transcript = " ".join(sensor.collected_transcripts)
        transcript_label.config(text="Final Transcript: " + final_transcript)

    start_record_btn = tk.Button(root, text="Start Recording", command=start_recording, bg="lightgreen", font=("Arial", 12))
    start_record_btn.pack(pady=5)

    stop_record_btn = tk.Button(root, text="Stop Recording", command=stop_recording, bg="tomato", font=("Arial", 12), state="disabled")
    stop_record_btn.pack(pady=5)

    return root


def main():
    root = build_gui()
    root.mainloop()


if __name__ == "__main__":
    main()