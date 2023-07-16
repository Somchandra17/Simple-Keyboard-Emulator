import tkinter as tk
from pynput.keyboard import Controller
import time
from threading import Thread

class KeyboardApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Keyboard Emulator")
        self.configure(bg="#222222")  

        self.text_entry = tk.Text(self, width=40, height=10, bg="#333333", fg="#FFFFFF") 
        self.text_entry.pack(pady=10, padx=20)

        self.text_entry.bind("<Tab>", lambda e: "break")

        self.start_button = tk.Button(self, text="Start", bg="#4CAF50", fg="#FFFFFF", command=self.start_typing) 
        self.start_button.pack(pady=5)

    def start_typing(self):
        text = self.text_entry.get("1.0", tk.END)
        self.start_button.configure(state="disabled")
        t = Thread(target=self.type_text, args=(text,))
        t.start()

    def type_text(self, text):
        time.sleep(5)
        keyboard = Controller()
        keyboard.type(text)
        self.start_button.configure(state="normal")

if __name__ == "__main__":
    app = KeyboardApp()
    app.mainloop()
