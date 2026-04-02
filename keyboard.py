import tkinter as tk
import tkinter.messagebox

# Attempt to import pynput Controller; fallback to dummy if unavailable
try:
    from pynput.keyboard import Controller
except Exception as e:
    # Define a minimal dummy controller for environments where pynput cannot be imported
    class Controller:
        def __init__(self, *args, **kwargs):
            pass

        def type(self, text):
            print(f"[DummyController] Would type: {text}")

    print(f"Warning: pynput not available ({e}); using dummy Controller.")
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

        self.start_button = tk.Button(
            self, text="Start", bg="#4CAF50", fg="#FFFFFF", command=self.start_typing
        )
        self.start_button.pack(pady=5)

    def start_typing(self):
        text = self.text_entry.get("1.0", tk.END)
        self.start_button.configure(state="disabled")
        t = Thread(target=self.type_text, args=(text,))
        t.start()

    def type_text(self, text):
        # Run typing in a background thread, then safely update UI on main thread
        time.sleep(5)
        keyboard = Controller()
        try:
            keyboard.type(text)
        except Exception as e:
            # Show error dialog on the main thread
            self.after(0, lambda: tk.messagebox.showerror("Typing Error", str(e)))
        finally:
            # Ensure the button is re-enabled only if the window still exists
            if self.winfo_exists():
                self.after(0, lambda: self.start_button.configure(state="normal"))


if __name__ == "__main__":
    app = KeyboardApp()
    app.mainloop()
