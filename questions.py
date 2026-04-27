# 27/04/2026
# Charlie Gibbs
# Questions program. This section communicates with my JSON file to load in my questions.

import json

def load_questions():
    try:
        with open("data/questions.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: questions.json not found.")
        return {"quiz": [], "exam": []}
    except json.JSONDecodeError:
        print("Error: JSON file is corrupted.")
        return {"quiz": [], "exam": []}
