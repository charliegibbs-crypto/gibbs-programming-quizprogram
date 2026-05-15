# Charlie Gibbs
# 15/05/2026
# Quiz mode GUI
# This module controls the entire quiz mode interface including question loading,
# answer checking, feedback, score checking and navigation.
# This module was designed using decomposition by separating quiz mode into its own module
# to improve maintainability and readability for future developers.

import tkinter as tk
import random
from src.questions import load_questions


class QuizGUI:
    def __init__(self, root, back):
        # stores the main Tkinter window so the widgets can be updated dynamically
        self.root = root

        # stores the callback function which is used to return users to the main menu.
        # This improves modularity because the quiz system does not need to directly control the menu system.
        self.back = back

        # Loads question data from external JSON file.
        # This improves future proofing because new questions can be added as the curriculum is updated.
        data = load_questions()

        # Randomly selects 5 questions from the question database. This improves reliability because it prevents users
        # from memorizing the answers.
        self.questions = random.sample(data["quiz"], min(5, len(data["quiz"])))

        # Tracks the current questions number.
        self.index = 0

        # Tracks the current score of the quiz.
        self.score = 0

        # Main label used to display the questions. The wrap length improves by preventing the questions from going off
        # the screen
        self.label = tk.Label(root, text="", font=("Arial", 14), wraplength=300)
        self.label.pack(pady=20)

        # INPUT VALIDATION
        # Tkinter validation is used to restrict invalid user inputs which improves reliability and prevents any
        # unexpected data
        vcmd = (root.register(self.validate_input), "%P")
        self.entry = tk.Entry(root, validate="key", validatecommand=vcmd)
        self.entry.pack(pady=10)

        # Allows the user to press enter when submitting the answer to a question.
        self.entry.bind("<Return>", self.handle_enter)

        # Displays user feed back (Correct/Incorrect).
        self.feedback = tk.Label(root, text="")
        self.feedback.pack()

        # Submit button triggers the answer checking system. This button is stored as an instance variable so it can be
        # disabled when the quiz finishes.
        self.submit_btn = tk.Button(root, text="Submit", command=self.check)
        self.submit_btn.pack(pady=10)

        # Returns the user back to the main menu.
        tk.Button(root, text="Back", command=self.exit).pack()

        # Loads the first question when the quiz starts.
        self.load()

    # INPUT VALIDATION
    def validate_input(self, new_text):

        # Restricts excessively long answers to a max of 20 characters to improve interface consistency.
        if len(new_text) > 20:
            return False

        # Character whitelist system.
        # Allows only a selects amount of characters to prevent any invalid inputs.
        allowed_chars = "0123456789./-%:$ynYN"

        # Lets users fully clear the entry box.
        if new_text == "":
            return True

        # check every character is allowed
        for char in new_text:
            if char not in allowed_chars:
                return False

        return True

    def load(self):

        # This detects when all the questions have been answered.
        # Boundary checking prevents index errors and improves reliability.
        if self.index >= len(self.questions):

            # Displays the users final score.
            self.label.config(text=f"Finished! Score: {self.score}/{len(self.questions)}")

            # Hides the input box once quiz has finished. Prevents additional answers from being entered
            self.entry.pack_forget()

            # Clears the leftover Correct/Incorrect feedback statements, improving aesthetics.
            self.feedback.config(text="")

            # Disables the submit button once quiz has been completed. This prevents the user from interacting with
            # finished assessments.
            self.submit_btn.config(state="disabled")
            return

        # Loads the current question based on the users progress.
        q = self.questions[self.index]

        # Displays question number and the text.
        self.label.config(text=f"Q{self.index + 1}: {q['question']}")

        # Clears teh old answers from the text entry field.
        self.entry.delete(0, tk.END)

        # Clears the previous questions feedback to make sure users only see feedback for the current question.
        self.feedback.config(text="")

        # This automatically puts the cursor back in the text entry box which reduces the number of un-necessary clicks.
        self.entry.focus()

    def check(self):

        # Prevents the answer checking system from running after the quiz has finished.
        if self.index >= len(self.questions):
            return

        # This retrieves and cleans the user input.
        # strip() removes any accidental spaces.
        user = self.entry.get().strip()

        # This makes sure that blank spaces cannot be entered and tells the user to do so.
        if user == "":
            self.feedback.config(text="Please enter an answer. ")
            return

        # This converts answers to lowercase so that the marking is not case-sensitive.
        # This improves fairness and usability.
        user = user.lower()
        correct = self.questions[self.index]["answer"].lower()

        # This is the core answer checking logic and updates the score if the answer is correct.
        if user == correct:
            self.score += 1
            self.feedback.config(text="Correct ✔️")
        else:
            self.feedback.config(text=f"Wrong ❌ (Ans: {correct})")

        # Moves to the next question.
        self.index += 1

        #This delays the switch slightly so the users can read the feedback that is given.
        self.root.after(800, self.load)

    def handle_enter(self, event):

        # This is the keyboard event handler which allows the enter key submissions instead of requiring mouse
        # interactions.
        self.check()

    def exit(self):

        # This removes all the widgets currently being displayed in quiz mode.
        # Gives the menu system time to load cleanly without overlapping widgets.
        for widget in self.root.winfo_children():
            widget.destroy()

        # This returns the user back to the main menu.
        self.back(self.root)
