# This file is what happens during quz mode. This will output the questions from my JSON file, check they are correct and update the scoring system.
# Charlie Gibbs
# Dated 27/04/2026

import tkinter as tk
import random
from src.questions import load_questions


class QuizGUI:
    def __init__(self, root, back):
        self.root = root
        self.back = back

        data = load_questions()
        self.questions = random.sample(data["quiz"], min(5, len(data["quiz"])))

        self.index = 0
        self.score = 0

        self.label = tk.Label(root, text="", font=("Arial", 14), wraplength=300)
        self.label.pack(pady=20)

        self.entry = tk.Entry(root)
        self.entry.pack(pady=10)

        self.feedback = tk.Label(root, text="")
        self.feedback.pack()

        tk.Button(root, text="Submit", command=self.check).pack(pady=10)
        tk.Button(root, text="Back", command=self.exit).pack()

        self.load()

    def load(self):
        if self.index < len(self.questions):
            q = self.questions[self.index]
            self.label.config(text=f"Q{self.index+1}: {q['question']}")
            self.entry.delete(0, tk.END)
            self.feedback.config(text="")
        else:
            self.label.config(text=f"Finished! Score: {self.score}/{len(self.questions)}")
            self.entry.pack_forget()

    def check(self):
        user = self.entry.get().strip()

        # INPUT VALIDATION
        if user == "":
            self.feedback.config(text="Please enter an answer")
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

    def exit(self):
        self.root.destroy()
        self.back(self.root)
