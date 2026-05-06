import tkinter as tk
import random
from src.questions import load_questions


class QuizGUI:
    def __init__(self, root, back):
        self.root = root
        self.back = back

        data = load_questions()
        self.questions = random.sample(data["quiz"], min(10, len(data["quiz"])))

        self.index = 0
        self.score = 0

        self.label = tk.Label(root, text="", font=("Arial", 14), wraplength=300)
        self.label.pack(pady=20)

        # VALIDATION
        vcmd = (root.register(self.validate_input), "%P")
        self.entry = tk.Entry(root, validate="key", validatecommand=vcmd)
        self.entry.pack(pady=10)

        self.entry.bind("<Return>", self.handle_enter)

        self.feedback = tk.Label(root, text="")
        self.feedback.pack()

        self.submit_btn = tk.Button(root, text="Submit", command=self.check)
        self.submit_btn.pack(pady=10)
        tk.Button(root, text="Back", command=self.exit).pack()

        self.load()

    # INPUT VALIDATION
    def validate_input(self, new_text):
        if len(new_text) > 20:
            return False

        allowed_chars = "0123456789./-%:$yn"

        # allow empty input
        if new_text == "":
            return True

        # check every character is allowed
        for char in new_text:
            if char not in allowed_chars:
                return False

        return True

    def load(self):
        if self.index >= len(self.questions):
            self.label.config(text=f"Finished! Score: {self.score}/{len(self.questions)}")

            self.entry.pack_forget()
            self.feedback.config(text="")

            self.submit_btn.config(state="disabled")
            return

        q = self.questions[self.index]
        self.label.config(text=f"Q{self.index + 1}: {q['question']}")
        self.entry.delete(0, tk.END)
        self.feedback.config(text="")
        self.entry.focus()

    def check(self):
        if self.index >= len(self.questions):
            return

        user = self.entry.get().strip()

        if user == "":
            self.feedback.config(text="Please enter an answer ❗")
            return

        user = user.lower()
        correct = self.questions[self.index]["answer"].lower()

        if user == correct:
            self.score += 1
            self.feedback.config(text="Correct ✔️")
        else:
            self.feedback.config(text=f"Wrong ❌ (Ans: {correct})")

        self.index += 1
        self.root.after(800, self.load)

    def handle_enter(self, event):
        self.check()

    def exit(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.back(self.root)
