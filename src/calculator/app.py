"""
Simple Calculator with a modern UI, built using tkinter.

Run with:
    uv run calculator
or:
    uv run python -m calculator.app
"""

import tkinter as tk

from calculator.logic import to_display_expression, evaluate_display_expression

# ---------- Colors ----------
BG_COLOR = "#16161e"
DISPLAY_BG = "#1e1e2e"
HISTORY_FG = "#8a8fa3"
RESULT_FG = "#ffffff"

BTN_NUM_BG = "#2b2d3d"
BTN_NUM_HOVER = "#3a3d54"
BTN_NUM_FG = "#ffffff"

BTN_OP_BG = "#f5a623"
BTN_OP_HOVER = "#ffb84d"
BTN_OP_FG = "#16161e"

BTN_EQ_BG = "#4caf50"
BTN_EQ_HOVER = "#5fd463"
BTN_EQ_FG = "#ffffff"

BTN_CLEAR_BG = "#e94560"
BTN_CLEAR_HOVER = "#ff5c7a"
BTN_CLEAR_FG = "#ffffff"

FONT_FAMILY = "Segoe UI"


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.resizable(False, False)
        self.configure(bg=BG_COLOR, padx=18, pady=18)

        self.expression = ""
        self.history = ""  # last completed expression, shown as a small line

        self._build_display()
        self._build_buttons()
        self._bind_keyboard()

    # ---------- UI construction ----------
    def _build_display(self):
        display_frame = tk.Frame(self, bg=DISPLAY_BG)
        display_frame.grid(row=0, column=0, columnspan=4, sticky="nsew", pady=(0, 18))
        display_frame.grid_columnconfigure(0, weight=1)

        self.history_var = tk.StringVar(value="")
        history_label = tk.Label(
            display_frame,
            textvariable=self.history_var,
            font=(FONT_FAMILY, 12),
            bg=DISPLAY_BG,
            fg=HISTORY_FG,
            anchor="e",
        )
        history_label.grid(row=0, column=0, sticky="nsew", padx=16, pady=(14, 0))

        self.display_var = tk.StringVar(value="0")
        result_label = tk.Label(
            display_frame,
            textvariable=self.display_var,
            font=(FONT_FAMILY, 34, "bold"),
            bg=DISPLAY_BG,
            fg=RESULT_FG,
            anchor="e",
        )
        result_label.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 14))

    def _build_buttons(self):
        buttons = [
            ("C", 1, 0, BTN_CLEAR_BG, BTN_CLEAR_FG, BTN_CLEAR_HOVER),
            ("⌫", 1, 1, BTN_CLEAR_BG, BTN_CLEAR_FG, BTN_CLEAR_HOVER),
            ("%", 1, 2, BTN_OP_BG, BTN_OP_FG, BTN_OP_HOVER),
            ("÷", 1, 3, BTN_OP_BG, BTN_OP_FG, BTN_OP_HOVER),

            ("7", 2, 0, BTN_NUM_BG, BTN_NUM_FG, BTN_NUM_HOVER),
            ("8", 2, 1, BTN_NUM_BG, BTN_NUM_FG, BTN_NUM_HOVER),
            ("9", 2, 2, BTN_NUM_BG, BTN_NUM_FG, BTN_NUM_HOVER),
            ("×", 2, 3, BTN_OP_BG, BTN_OP_FG, BTN_OP_HOVER),

            ("4", 3, 0, BTN_NUM_BG, BTN_NUM_FG, BTN_NUM_HOVER),
            ("5", 3, 1, BTN_NUM_BG, BTN_NUM_FG, BTN_NUM_HOVER),
            ("6", 3, 2, BTN_NUM_BG, BTN_NUM_FG, BTN_NUM_HOVER),
            ("−", 3, 3, BTN_OP_BG, BTN_OP_FG, BTN_OP_HOVER),

            ("1", 4, 0, BTN_NUM_BG, BTN_NUM_FG, BTN_NUM_HOVER),
            ("2", 4, 1, BTN_NUM_BG, BTN_NUM_FG, BTN_NUM_HOVER),
            ("3", 4, 2, BTN_NUM_BG, BTN_NUM_FG, BTN_NUM_HOVER),
            ("+", 4, 3, BTN_OP_BG, BTN_OP_FG, BTN_OP_HOVER),

            ("0", 5, 0, BTN_NUM_BG, BTN_NUM_FG, BTN_NUM_HOVER),
            (".", 5, 1, BTN_NUM_BG, BTN_NUM_FG, BTN_NUM_HOVER),
            ("=", 5, 2, BTN_EQ_BG, BTN_EQ_FG, BTN_EQ_HOVER),
        ]

        self.buttons = {}

        for (text, row, col, bg, fg, hover_bg) in buttons:
            colspan = 2 if text == "=" else 1
            btn = tk.Button(
                self,
                text=text,
                font=(FONT_FAMILY, 17, "bold"),
                bg=bg,
                fg=fg,
                activebackground=hover_bg,
                activeforeground=fg,
                bd=0,
                relief="flat",
                cursor="hand2",
                highlightthickness=0,
                command=lambda t=text: self.on_button_click(t),
            )
            btn.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=5, pady=5, ipady=12)
            btn.bind("<Enter>", lambda e, b=btn, h=hover_bg: b.configure(bg=h))
            btn.bind("<Leave>", lambda e, b=btn, base=bg: b.configure(bg=base))
            self.buttons[text] = btn

        for i in range(6):
            self.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

    def _bind_keyboard(self):
        for digit in "0123456789.":
            self.bind(digit, lambda e, d=digit: self.on_button_click(d))

        key_map = {
            "+": "+", "-": "−", "*": "×", "/": "÷", "%": "%",
        }
        for key, symbol in key_map.items():
            self.bind(key, lambda e, s=symbol: self.on_button_click(s))

        self.bind("<Return>", lambda e: self.on_button_click("="))
        self.bind("<KP_Enter>", lambda e: self.on_button_click("="))
        self.bind("<BackSpace>", lambda e: self.on_button_click("⌫"))
        self.bind("<Escape>", lambda e: self.on_button_click("C"))

    # ---------- Logic glue ----------
    def on_button_click(self, char):
        if char == "C":
            self.expression = ""
            self.history = ""
        elif char == "⌫":
            self.expression = self.expression[:-1]
        elif char == "=":
            if not self.expression:
                return
            self.history = to_display_expression(self.expression)
            self.expression = evaluate_display_expression(self.expression)
            self.refresh_display()
            return
        else:
            self.expression += char

        self.refresh_display()

    def refresh_display(self):
        text = self.expression if self.expression else "0"
        self.display_var.set(to_display_expression(text))
        self.history_var.set(f"{self.history} =" if self.history else "")


def main():
    app = Calculator()
    app.mainloop()


if __name__ == "__main__":
    main()