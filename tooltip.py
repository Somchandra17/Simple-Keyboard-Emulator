import tkinter as tk


class Tooltip:
    def __init__(self, widget, text, bg="#1a1a1a", fg="#ffffff", font=None, delay_ms=300):
        self.widget = widget
        self.text = text
        self.bg = bg
        self.fg = fg
        self.font = font or ("TkDefaultFont", 10)
        self.delay_ms = delay_ms
        self.tip = None
        self._after_id = None
        self._bind()

    def _bind(self):
        self.widget.bind("<Enter>", self._on_enter, add="+")
        self.widget.bind("<Leave>", self._on_leave, add="+")
        self.widget.bind("<ButtonPress>", self._on_leave, add="+")

    def _on_enter(self, event=None):
        self._after_id = self.widget.after(self.delay_ms, self._show)

    def _on_leave(self, event=None):
        if self._after_id:
            self.widget.after_cancel(self._after_id)
            self._after_id = None
        self._hide()

    def _show(self):
        if self.tip:
            return
        x = self.widget.winfo_rootx() + 12
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 4
        self.tip = tk.Toplevel(self.widget)
        self.tip.wm_overrideredirect(True)
        self.tip.wm_geometry(f"+{x}+{y}")
        self.tip.attributes("-topmost", True)
        lbl = tk.Label(
            self.tip,
            text=self.text,
            bg=self.bg,
            fg=self.fg,
            font=self.font,
            relief="flat",
            padx=8,
            pady=4,
            wraplength=250,
        )
        lbl.pack()

    def _hide(self):
        if self.tip:
            self.tip.destroy()
            self.tip = None
