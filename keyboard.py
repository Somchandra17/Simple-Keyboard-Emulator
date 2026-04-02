import tkinter as tk
from tkinter import messagebox, filedialog
import pyautogui
import time
import logging
import os
import platform
from threading import Thread

from constants import COLORS, FONTS, PAD, VERSION, APP_NAME
from config import ConfigManager
from tooltip import Tooltip


SYSTEM = platform.system()
C = COLORS
F = FONTS

logger = logging.getLogger(APP_NAME)


class KeyboardApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title(APP_NAME)
        self.configure(bg=C["bg"])
        self.resizable(False, False)

        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0

        self.is_typing = False
        self.cfg = ConfigManager(APP_NAME.replace(" ", ""))
        loaded = self.cfg.load()

        self.delay_var = tk.StringVar(value=loaded["delay"])
        self.speed_var = tk.StringVar(value=loaded["speed"])

        self._build_menu()
        self._build()
        self._bind_keys()
        self._center()

    def _build_menu(self):
        menubar = tk.Menu(self, bg=C["bg3"], fg=C["fg"], tearoff=0)
        help_menu = tk.Menu(menubar, tearoff=0, bg=C["bg3"], fg=C["fg"])
        help_menu.add_command(label="About", command=self._show_about)
        help_menu.add_command(label="Shortcuts", command=self._show_shortcuts)
        menubar.add_cascade(label="Help", menu=help_menu)
        self.config(menu=menubar)

    def _build(self):
        self._build_header()
        self._build_editor()
        self._build_char_bar()
        self._build_settings()
        self._build_buttons()
        self._build_status()

    def _build_header(self):
        frame = tk.Frame(self, bg=C["bg"])
        frame.pack(fill="x", padx=PAD, pady=(PAD, 6))
        tk.Label(
            frame, text=APP_NAME.upper(), font=F["title"], bg=C["bg"], fg=C["fg"]
        ).pack(anchor="w")

    def _build_editor(self):
        frame = tk.Frame(self, bg=C["bg"])
        frame.pack(fill="both", expand=True, padx=PAD, pady=(0, 6))

        self.text = tk.Text(
            frame,
            bg=C["bg2"],
            fg=C["fg"],
            font=F["mono"],
            insertbackground=C["accent"],
            relief="flat",
            padx=8,
            pady=8,
            wrap="word",
            height=10,
        )
        self.text.pack(side="left", fill="both", expand=True)

        sb = tk.Scrollbar(
            frame,
            bg=C["bg2"],
            troughcolor=C["bg2"],
            activebackground=C["bg3"],
            command=self.text.yview,
        )
        sb.pack(side="right", fill="y")
        self.text.config(yscrollcommand=sb.set)

    def _build_char_bar(self):
        self.char_lbl = tk.Label(
            self, text="0 chars", font=(F["body"][0], 10), bg=C["bg"], fg=C["fg2"]
        )
        self.char_lbl.pack(anchor="e", padx=PAD, pady=(0, 6))
        self.text.bind("<KeyRelease>", self._update_chars)
        self._update_chars()

    def _build_settings(self):
        frame = tk.Frame(self, bg=C["bg"])
        frame.pack(fill="x", padx=PAD, pady=(0, 6))

        rows = [
            ("Start Delay (s)", self.delay_var, 0, 30, 1),
            ("Speed (s/char)", self.speed_var, 0.01, 1.0, 0.01),
        ]
        for label_text, var, f, t, inc in rows:
            row = tk.Frame(frame, bg=C["bg"])
            row.pack(fill="x", pady=1)
            tk.Label(
                row, text=label_text, font=(F["body"][0], 11), bg=C["bg"], fg=C["fg2"]
            ).pack(side="left")
            sp = tk.Spinbox(
                row,
                from_=f,
                to=t,
                increment=inc,
                textvariable=var,
                width=5,
                font=F["body"],
                bg=C["bg3"],
                fg=C["fg"],
                relief="flat",
                highlightthickness=0,
            )
            sp.pack(side="left", padx=(8, 0))

    def _build_buttons(self):
        row1 = tk.Frame(self, bg=C["bg"])
        row1.pack(fill="x", padx=PAD, pady=(0, 6))

        self.start_btn = self._btn(
            row1, "START", self.start_typing, C["accent"], C["accent_bg"]
        )
        self.start_btn.pack(side="left", fill="x", expand=True, padx=(0, 4))
        Tooltip(
            self.start_btn,
            "Start typing after countdown — switch to your target app during the countdown",
        )

        self.paste_btn = self._btn(
            row1, "PASTE", self.paste_text, C["accent"], C["accent_bg"]
        )
        self.paste_btn.pack(side="left", fill="x", expand=True, padx=(4, 0))
        Tooltip(self.paste_btn, "Paste clipboard content into the editor")

        row2 = tk.Frame(self, bg=C["bg"])
        row2.pack(fill="x", padx=PAD, pady=(0, 6))

        clear_btn = self._btn(row2, "CLEAR", self.clear_text, C["fg2"], C["bg3"])
        clear_btn.pack(side="left", fill="x", expand=True, padx=(0, 4))
        Tooltip(clear_btn, "Clear all text from the editor")

        save_btn = self._btn(row2, "SAVE", self.save_text, C["fg2"], C["bg3"])
        save_btn.pack(side="left", fill="x", expand=True, padx=4)
        Tooltip(save_btn, "Save text to a .txt file")

        load_btn = self._btn(row2, "LOAD", self.load_text, C["fg2"], C["bg3"])
        load_btn.pack(side="left", fill="x", expand=True, padx=(4, 0))
        Tooltip(load_btn, "Load text from a .txt file into the editor")

    def _build_status(self):
        self.status = tk.Label(
            self, text="READY", font=(F["body"][0], 11), bg=C["bg"], fg=C["green"]
        )
        self.status.pack(pady=(0, PAD))

    def _btn(self, parent, text, cmd, fg, bg):
        return tk.Button(
            parent,
            text=text,
            font=(F["body"][0], 11, "bold"),
            bg=bg,
            fg=fg,
            activebackground=C["bg3"],
            activeforeground=C["fg"],
            relief="flat",
            padx=12,
            pady=8,
            command=cmd,
        )

    def _center(self):
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"+{x}+{y}")

    def _bind_keys(self):
        mod = "Command" if SYSTEM == "Darwin" else "Control"
        self.bind(f"<{mod}-Return>", lambda e: self.start_typing())
        self.bind(f"<{mod}-d>", lambda e: self.clear_text())

    def _update_chars(self, event=None):
        self.char_lbl.config(text=f"{len(self.text.get('1.0', 'end-1c'))} chars")

    def _show_about(self):
        messagebox.showinfo(
            "About",
            f"{APP_NAME} v{VERSION}\n\nA cross-platform keyboard emulator.\nBuilt with Python + Tkinter + PyAutoGUI.",
        )

    def _show_shortcuts(self):
        mod = "Cmd" if SYSTEM == "Darwin" else "Ctrl"
        messagebox.showinfo(
            "Shortcuts", f"{mod} + Enter — Start typing\n{mod} + D — Clear text"
        )

    def start_typing(self):
        text = self.text.get("1.0", "end-1c").strip()
        if not text:
            self.status.config(text="NO TEXT", fg=C["yellow"])
            return
        try:
            delay = float(self.delay_var.get())
            speed = float(self.speed_var.get())
        except ValueError:
            self.status.config(text="INVALID SETTINGS", fg=C["red"])
            return

        self.cfg.save(delay, speed)
        self.is_typing = True
        self.start_btn.config(state="disabled", text="TYPING...")
        self.paste_btn.config(state="disabled")
        self.status.config(text="WAITING...", fg=C["yellow"])
        logger.info("Starting: delay=%s speed=%s chars=%d", delay, speed, len(text))
        Thread(target=self._type, args=(text, delay, speed), daemon=True).start()

    def _type(self, text, delay, speed):
        for i in range(int(delay), 0, -1):
            if not self.is_typing:
                return
            self.after(
                0,
                lambda s=i: self.status.config(
                    text=f"STARTING IN {s}S...", fg=C["yellow"]
                ),
            )
            time.sleep(1)
        if not self.is_typing:
            return
        self.after(0, lambda: self.status.config(text="TYPING...", fg=C["red"]))
        try:
            pyautogui.write(text, interval=speed)
            self.after(0, lambda: self.status.config(text="DONE", fg=C["green"]))
            logger.info("Typing complete")
        except Exception as e:
            msg = (
                "Cancelled (mouse moved to corner)" if "Fail-safe" in str(e) else str(e)
            )
            self.after(0, lambda: self.status.config(text="ERROR", fg=C["red"]))
            self.after(0, lambda: messagebox.showerror("Error", msg))
            logger.error("Typing failed: %s", msg)
        finally:
            self.is_typing = False
            if self.winfo_exists():
                self.after(
                    0, lambda: self.start_btn.config(state="normal", text="START")
                )
                self.after(0, lambda: self.paste_btn.config(state="normal"))

    def paste_text(self):
        try:
            t = self.clipboard_get()
            cur = self.text.get("1.0", "end-1c")
            self.text.delete("1.0", "end")
            self.text.insert("1.0", cur + t if cur else t)
            self._update_chars()
            self.status.config(text="PASTED", fg=C["green"])
        except tk.TclError:
            self.status.config(text="CLIPBOARD EMPTY", fg=C["yellow"])

    def clear_text(self):
        self.text.delete("1.0", "end")
        self._update_chars()
        self.status.config(text="CLEARED", fg=C["green"])

    def save_text(self):
        t = self.text.get("1.0", "end-1c")
        if not t.strip():
            self.status.config(text="NOTHING TO SAVE", fg=C["yellow"])
            return
        p = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            title="Save",
        )
        if p:
            try:
                with open(p, "w", encoding="utf-8") as f:
                    f.write(t)
                self.status.config(text=f"SAVED: {os.path.basename(p)}", fg=C["green"])
                logger.info("Saved: %s", p)
            except Exception as e:
                messagebox.showerror("Error", str(e))
                logger.error("Save failed: %s", e)

    def load_text(self):
        p = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")], title="Load"
        )
        if p:
            try:
                with open(p, "r", encoding="utf-8") as f:
                    c = f.read()
                cur = self.text.get("1.0", "end-1c")
                self.text.delete("1.0", "end")
                self.text.insert("1.0", cur + c if cur else c)
                self._update_chars()
                self.status.config(text=f"LOADED: {os.path.basename(p)}", fg=C["green"])
                logger.info("Loaded: %s", p)
            except Exception as e:
                messagebox.showerror("Error", str(e))
                logger.error("Load failed: %s", e)

    def on_close(self):
        self.is_typing = False
        try:
            self.cfg.save(self.delay_var.get(), self.speed_var.get())
        except Exception:
            pass
        self.destroy()


def setup_logging():
    cfg = ConfigManager(APP_NAME.replace(" ", ""))
    log_path = os.path.join(os.path.dirname(cfg.path), "app.log")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.FileHandler(log_path), logging.StreamHandler()],
    )


if __name__ == "__main__":
    setup_logging()
    app = KeyboardApp()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()
