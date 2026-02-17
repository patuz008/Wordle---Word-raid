import random
from collections import Counter  # Added for accurate duplicate letter handling

game_name = "Word Raider"
word_bank = []

with open('C:/Users/patsy/Desktop/python-exercise/words.txt') as word_file:
    for line in word_file:
        stripped = line.rstrip().lower()
        if stripped:  # Skip empty lines
            word_bank.append(stripped)

selected_word = random.choice(word_bank)

# Game Information
incorrect_letters = []
misplaced_letters = []
max_turns = 6
used_turns = 0

print(f"Welcome to {game_name}!")
print(f"The word to guess has {len(selected_word)} letters")
print(f"You have {max_turns} turns to guess the word!")

# Main Game Loop
while used_turns < max_turns:
    guess = input("Guess a word (or type 'stop' to end the game): ").lower().strip()
    if guess == 'stop':
        break

    # FIXED: Dynamic length validation (was hardcoded to 5 letters)
    if len(guess) != len(selected_word) or not guess.isalpha():
        print(f'Please enter a {len(selected_word)}-letter word.')
        continue

    # FIXED: Accurate feedback using two-pass algorithm for duplicate letters
    remaining_letters = Counter(selected_word)
    feedback = ['_'] * len(guess)
    current_misplaced = []
    current_incorrect = []

    # First pass: exact matches
    for i, letter in enumerate(guess):
        if letter == selected_word[i]:
            feedback[i] = letter
            remaining_letters[letter] -= 1

    # Second pass: misplaced letters
    for i, letter in enumerate(guess):
        if feedback[i] == '_' and remaining_letters.get(letter, 0) > 0:
            feedback[i] = f'[{letter}]'  # FIXED: Visually show misplaced letters
            current_misplaced.append(letter)
            remaining_letters[letter] -= 1
        elif feedback[i] == '_':
            current_incorrect.append(letter)

    # Display feedback
    print(' '.join(feedback))

    # FIXED: Typo correction
    if guess == selected_word:
        print("\nCongratulations! You guessed the word!")
        break

    # Update global hint lists (only add new letters)
    for letter in current_misplaced:
        if letter not in misplaced_letters:
            misplaced_letters.append(letter)
    for letter in current_incorrect:
        if letter not in incorrect_letters:
            incorrect_letters.append(letter)

    used_turns += 1

    # Loss condition
    if used_turns == max_turns:
        print(f"\nGame Over, You Lost. The word was: {selected_word}")
        break

    print()
    print(f'Misplaced letters: {misplaced_letters}')
    print(f'Incorrect letters: {incorrect_letters}')
    print(f'You have {max_turns - used_turns} turns left')