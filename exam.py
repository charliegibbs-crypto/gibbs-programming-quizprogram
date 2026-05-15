# Charlie Gibbs
# 15/05/2026
# Exam mode GUI
# This module handles my timed exam function for assessment practice.
# This is designed to simulate test conditions and add extra pressure with the timer with no feedback, and only shows
# the final score at the end.

import tkinter as tk
import random
import time
from src.questions import load_questions


class ExamGUI:
    def __init__(self, root, back):

        # Main Tkinter window reference.
        self.root = root

        # Callback function which returns the user to the main menu. This improves modularity and avoids tightly coupling
        # modules together.
        self.back = back

        # Loads questions from questions JSON file. This supports future proofing as questions can be added and removed
        # over time without code changes.
        data = load_questions()

        # This randomly selects 10 questions from the JSON file which ensures variation between attempts.
        self.questions = random.sample(data["exam"], min(10, len(data["exam"])))

        # Tracks the current question number
        self.index = 0

        # Tracks the current score.
        self.score = 0

        # TIME LIMIT SYSTEM
        # This sets the time limit to 300 seconds.
        self.time_limit = 300

        # This records the time for countdown calculations.
        self.start_time = time.time()

        # Timer display label
        self.timer = tk.Label(root, text="")
        self.timer.pack()

        # Question display label.
        self.label = tk.Label(root, text="", font=("Arial", 14), wraplength=300)
        self.label.pack(pady=20)

        # INPUT VALIDATION
        # This restricts invalid characters and inputs while allowing numerical symbols.
        vcmd = (root.register(self.validate_input), "%P")
        self.entry = tk.Entry(root, validate="key", validatecommand=vcmd)
        self.entry.pack(pady=10)

        # Allows the enter key to submit answers which improves reliability and usability.
        self.entry.bind("<Return>", self.handle_enter)

        # Submit button used to confirm answers.
        # This is stored as an instance variable so it can be disabled at the end of the exam.
        self.submit_btn = tk.Button(root, text="Submit", command=self.check)
        self.submit_btn.pack(pady=10)

        # Back button to return the user to the main menu.
        tk.Button(root, text="Back", command=self.exit).pack()

        # Starts the timer loop and loads the first question.
        self.update_timer()
        self.load()

    # INPUT VALIDATION SYSTEM
    def validate_input(self, new_text):

        # Limits maximum input length to 20 characters to prevent overflow and invalid inputs.
        if len(new_text) > 20:
            return False

        # Allowed characters for numerical responses.
        # This includes: Numerical symbols, numbers and Y/N for true and false questions.
        allowed_chars = "0123456789./-%:$ynYN"

        # Allows user to clear the input field.
        if new_text == "":
            return True

        # Makes sure every character is valid.
        for char in new_text:
            if char not in allowed_chars:
                return False

        return True

    # TIMER SYSTEM
    def update_timer(self):

        # Calculates the remaining time based on the start time.
        remaining = int(self.time_limit - (time.time() - self.start_time))

        # Ends the exam if the timer runs out.
        if remaining <= 0:
            self.timer.config(text="Time's up!")
            self.timer.pack_forget()
            self.finish()
            return

        # Formats the time into minutes and seconds for readability
        mins = remaining // 60
        secs = remaining % 60

        # Updates the timer display every second.
        self.timer.config(text=f"Time Left: {mins}:{secs:02}")
        self.root.after(1000, self.update_timer)

    # LOAD QUESTION SYSTEM
    def load(self):

        # This checks if all the questions are finished.
        # Prevents any index errors and makes sure the termination is smooth.
        if self.index >= len(self.questions):
            self.finish()
            return

        # Retrieves the current question.
        q = self.questions[self.index]

        # Displays question with numbering for clarity.
        self.label.config(text=f"Q{self.index + 1}: {q['question']}")

        # Clears the previous answer input
        self.entry.delete(0, tk.END)

        # Automatically focuses input field for faster interaction.
        self.entry.focus()

    # ANSWER CHECKING SYSTEM
    def check(self):

        # Prevents processing after exam is finished.
        if self.index >= len(self.questions):
            return

        # Gets and cleans the user input
        user = self.entry.get().strip()

        # Prevents empty submissions
        if user == "":
            return

        # Normalizes input for comparison.
        user = user.lower()
        correct = self.questions[self.index]["answer"].lower()

        # Updates the score if the answer is correct (Won't display to the user until exam is finished.
        if user == correct:
            self.score += 1

        # Moves to the next question.
        self.index += 1

        # Ends exam if there are no questions left.
        if self.index >= len(self.questions):
            self.finish()
        else:
            self.load()

    # ENTER KEY HANDLER
    def handle_enter(self, event):
        self.check()

    # FINISH SCREEN
    def finish(self):

        # Displays final score only (no feedback to be given to the user)
        self.label.config(
            text=f"Exam Finished!\nScore: {self.score}/{len(self.questions)}"
        )

        # Removes input field to prevent any further answers.
        self.entry.pack_forget()

        # Disables enter key to lock the exam state.
        self.submit_btn.config(state="disabled")

    # EXIT SYSTEM
    def exit(self):

        # Clears all widgets before returning to the main menu.
        for widget in self.root.winfo_children():
            widget.destroy()

        # Returns user to the main menu via callback.
        self.back(self.root)
