import random
from words import words

class WordGame:

    def __init__(self):
        self.points = 0
        self.target_word = ""
        self.attempts = 3
        self.generate_task()

    def generate_task(self):
        self.attempts = 3
        self.target_word = random.choice(words)
        # print(f"New target word: {self.target_word}")
        return self.target_word

    def check_input_for_word(self, string):
        if self.target_word in string.lower():
            # print(f"The player input the target word and the task was reset.")
            self.generate_task()
            self.points -= 1
            # self.update_status(message="You input the target word yourself, so you lost one point and the game reset.")
            return True

        else:
            # print(f"The player did not input the target word, so that's good.")
            return False

    def check_output_for_word(self, string):
        # print(f"Checking for '{self.target_word}' in '{string}'.")
        if self.target_word in string.lower():
            self.points += self.attempts
            # print(f"The player scored {self.attempts} points and has a total of {self.points}.")
            score_gained = self.attempts
            self.generate_task()
            return f"Success! You earned {score_gained} points!"
            # self.update_status(message=f"Success! You earned {score_gained} points!")
        else:
            # print("The response did not contain the word.")
            self.attempts -= 1
            # print(f"Remaining attempts: {self.attempts}")
            if self.attempts <= 0:
                self.generate_task()
                # print(f"The player ran out of attempts.")
                return f"You did not win in three attempts. Generating new target word."
                # self.update_status(message=f"You did not win in three attempts. Generating new target word.")
            else:
                # print(f"The player has attempts left.")
                return "That didn't quite hit the mark. Try again!"

    def update_status(self, message=""):
        return f'Current score: {self.points}\nRemaining attempts: {self.attempts}\nTarget word: "{self.target_word}"\n{message}'