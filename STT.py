import tkinter as tk
from tkinter import filedialog, messagebox
import speech_recognition as sr
import threading

# Function to recognize speech from an audio file
def recognize_from_file():
    file_path = filedialog.askopenfilename(
        title="Select an Audio File",
        filetypes=[("Audio Files", "*.wav *.flac *.mp3")]
    )
    if not file_path:
        output_text.set("No file selected.")
        return

    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(file_path) as source:
            output_text.set("Processing audio file...")
            audio = recognizer.record(source)  # Read the entire audio file
            text = recognizer.recognize_google(audio)
            output_text.set(f"File Transcription:\n{text}")
    except sr.UnknownValueError:
        output_text.set("Could not understand the audio in the file.")
    except Exception as e:
        output_text.set(f"An error occurred: {str(e)}")

# Function to handle live speech recognition
def recognize_speech_live():
    recognizer = sr.Recognizer()
    stop_listening = False

    def listen():
        nonlocal stop_listening
        output_text.set("Listening... (say 'stop' to end)")
        while not stop_listening:
            try:
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = recognizer.listen(source)
                    text = recognizer.recognize_google(audio).lower()

                    if text == "stop":
                        stop_listening = True
                        output_text.set("Listening stopped.")
                        return
                    else:
                        output_text.set(f"You said: {text}")
            except sr.UnknownValueError:
                output_text.set("Could not understand the audio. Please try again.")
            except Exception as e:
                output_text.set(f"An error occurred: {str(e)}")
                stop_listening = True

    # Run the listening loop in a separate thread
    threading.Thread(target=listen, daemon=True).start()

# Exit the application
def exit_application():
    if messagebox.askokcancel("Quit", "Do you really want to quit?"):
        root.destroy()

# Initialize the main window
root = tk.Tk()
root.title("Speech-to-Text Converter")
root.geometry("500x400")
root.resizable(False, False)

# GUI components
title_label = tk.Label(root, text="Speech-to-Text Converter", font=("Arial", 16), pady=10)
title_label.pack()

output_text = tk.StringVar()
output_label = tk.Label(root, textvariable=output_text, font=("Arial", 12), wraplength=450, pady=20, justify="left")
output_label.pack()

live_button = tk.Button(root, text="Start Live Listening", font=("Arial", 14), command=recognize_speech_live)
live_button.pack(pady=10)

file_button = tk.Button(root, text="Transcribe Audio File", font=("Arial", 14), command=recognize_from_file)
file_button.pack(pady=10)

exit_button = tk.Button(root, text="Exit", font=("Arial", 14), command=exit_application)
exit_button.pack(pady=10)

# Run the application
root.protocol("WM_DELETE_WINDOW", exit_application)
root.mainloop()
