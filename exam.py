# This file is what happens during exam mode. However, in exam mode it is timed, answers aren't shown and your score is added up at the end to test students if they are ready.
# Charlie Gibbs
# Dated 27/04/2026

import tkinter as tk
import random
import time
from src.questions import load_questions


class ExamGUI:
    def __init__(self, root, back):
        self.root = root
        self.back = back

        data = load_questions()
        self.questions = random.sample(data["exam"], min(10, len(data["exam"])))

        self.index = 0
        self.score = 0

        self.time_limit = 300
        self.start_time = time.time()

        self.timer = tk.Label(root, text="")
        self.timer.pack()

        self.label = tk.Label(root, text="", font=("Arial", 14), wraplength=300)
        self.label.pack(pady=20)

        self.entry = tk.Entry(root)
        self.entry.pack(pady=10)

        tk.Button(root, text="Submit", command=self.check).pack(pady=10)
        tk.Button(root, text="Back", command=self.exit).pack()

        self.update_timer()
        self.load()

    def update_timer(self):
        remaining = int(self.time_limit - (time.time() - self.start_time))

        if remaining <= 0:
            self.finish()
            return

        self.timer.config(text=f"Time Left: {remaining}s")
        self.root.after(1000, self.update_timer)

    def load(self):
        if self.index < len(self.questions):
            q = self.questions[self.index]
            self.label.config(text=f"Q{self.index+1}: {q['question']}")
            self.entry.delete(0, tk.END)
        else:
            self.finish()

    def check(self):
        user = self.entry.get().strip()

        # INPUT VALIDATION
        if user == "":
            return  # ignore empty answers (silent in exam mode)

        user = user.lower()
        correct = self.questions[self.index]["answer"].lower()

        if user == correct:
            self.score += 1

        self.index += 1
        self.load()

    def finish(self):
        self.label.config(text=f"Finished! Score: {self.score}/{len(self.questions)}")
        self.entry.pack_forget()

    def exit(self):
        self.root.destroy()
        self.back(self.root)
