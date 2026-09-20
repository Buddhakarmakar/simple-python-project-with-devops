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
BG_COLOR = "#1e1e2e"
DISPLAY_BG = "#282a3a"
DISPLAY_FG = "#ffffff"
BTN_NUM_BG = "#3a3d54"
BTN_NUM_FG = "#ffffff"
BTN_OP_BG = "#f5a623"
BTN_OP_FG = "#1e1e2e"
BTN_EQ_BG = "#4caf50"
BTN_EQ_FG = "#ffffff"
BTN_CLEAR_BG = "#e94560"
BTN_CLEAR_FG = "#ffffff"


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.resizable(False, False)
        self.configure(bg=BG_COLOR, padx=15, pady=15)

        self.expression = ""
        self._build_display()
        self._build_buttons()

    # ---------- UI construction ----------
    def _build_display(self):
        self.display_var = tk.StringVar(value="0")
        display = tk.Entry(
            self,
            textvariable=self.display_var,
            font=("Segoe UI", 28, "bold"),
            bg=DISPLAY_BG,
            fg=DISPLAY_FG,
            bd=0,
            justify="right",
            insertbackground=DISPLAY_FG,
            state="readonly",
            readonlybackground=DISPLAY_BG,
        )
        display.grid(row=0, column=0, columnspan=4, sticky="nsew", ipady=20, pady=(0, 15))

    def _build_buttons(self):
        buttons = [
            ("C", 1, 0, BTN_CLEAR_BG, BTN_CLEAR_FG), ("⌫", 1, 1, BTN_CLEAR_BG, BTN_CLEAR_FG),
            ("%", 1, 2, BTN_OP_BG, BTN_OP_FG), ("÷", 1, 3, BTN_OP_BG, BTN_OP_FG),

            ("7", 2, 0, BTN_NUM_BG, BTN_NUM_FG), ("8", 2, 1, BTN_NUM_BG, BTN_NUM_FG),
            ("9", 2, 2, BTN_NUM_BG, BTN_NUM_FG), ("×", 2, 3, BTN_OP_BG, BTN_OP_FG),

            ("4", 3, 0, BTN_NUM_BG, BTN_NUM_FG), ("5", 3, 1, BTN_NUM_BG, BTN_NUM_FG),
            ("6", 3, 2, BTN_NUM_BG, BTN_NUM_FG), ("−", 3, 3, BTN_OP_BG, BTN_OP_FG),

            ("1", 4, 0, BTN_NUM_BG, BTN_NUM_FG), ("2", 4, 1, BTN_NUM_BG, BTN_NUM_FG),
            ("3", 4, 2, BTN_NUM_BG, BTN_NUM_FG), ("+", 4, 3, BTN_OP_BG, BTN_OP_FG),

            ("0", 5, 0, BTN_NUM_BG, BTN_NUM_FG), (".", 5, 1, BTN_NUM_BG, BTN_NUM_FG),
            ("=", 5, 2, BTN_EQ_BG, BTN_EQ_FG),
        ]

        for (text, row, col, bg, fg) in buttons:
            colspan = 2 if text == "=" else 1
            btn = tk.Button(
                self,
                text=text,
                font=("Segoe UI", 16, "bold"),
                bg=bg,
                fg=fg,
                activebackground=bg,
                activeforeground=fg,
                bd=0,
                relief="flat",
                command=lambda t=text: self.on_button_click(t),
            )
            btn.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=5, pady=5, ipady=10)

        for i in range(6):
            self.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

    # ---------- Logic glue ----------
    def on_button_click(self, char):
        if char == "C":
            self.expression = ""
        elif char == "⌫":
            self.expression = self.expression[:-1]
        elif char == "=":
            self.expression = evaluate_display_expression(self.expression)
            self.refresh_display()
            return
        else:
            self.expression += char

        self.refresh_display()

    def refresh_display(self):
        text = self.expression if self.expression else "0"
        self.display_var.set(to_display_expression(text))


def main():
    app = Calculator()
    app.mainloop()


if __name__ == "__main__":
    main()
