import random
import json

def load_words_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        words = json.load(file)
    return words

def filter_5_letter_words(words):
    return [word for word in words if len(word) == 5]

file_path = 'svenska-ord.json'
all_words = load_words_from_json(file_path)
swedish_words = filter_5_letter_words(all_words)

def select_random_word(word_list):
    return random.choice(word_list)

def get_letter_feedback(current_guess):
    feedback = []
    for i, letter in enumerate(current_guess, start=1):
        print(f"Bokstav {i} ({letter}):")
        user_input = input("Var bokstaven, (1) korrekt och korrekt plats. (2) korrekt men fel plats. (3) Inte med i ordet? Skriv 4 om ingen bokstav var korrekt: ")
        if user_input == '1':
            feedback.append((letter, 'right'))
        elif user_input == '2':
            feedback.append((letter, 'wrong_place'))
        elif user_input == '3':
            feedback.append((letter, 'wrong'))
        elif user_input == '4':
            break
        else:
            print("Fel input, Byter till nsta bokstav.")
    return feedback

def refine_word_list_based_on_feedback(current_guess, feedback, word_list):
    refined_list = word_list[:]
    letter_counts = {}

    for i, (letter, status) in enumerate(feedback):
        if status in ['right', 'wrong_place']:
            if letter in letter_counts:
                letter_counts[letter]['count'] += 1
            else:
                letter_counts[letter] = {'count': 1, 'positions': []}
            if status == 'right':
                letter_counts[letter]['positions'].append(i)

    for letter, info in letter_counts.items():
        if info['positions']:
            for position in info['positions']:
                refined_list = [word for word in refined_list if word[position] == letter]
        refined_list = [word for word in refined_list if word.count(letter) >= info['count']]

    for i, (letter, status) in enumerate(feedback):
        if status == 'wrong':
            refined_list = [word for word in refined_list if letter not in word or (word[i] != letter and i not in letter_counts.get(letter, {}).get('positions', []))]

    return refined_list

def wordle_bot(swedish_words):
    possible_words = swedish_words[:]
    attempts = 0

    while attempts < 6:
        current_guess = select_random_word(possible_words)
        print(f"Test {attempts + 1}: Boten gissar '{current_guess}'.")

        feedback = get_letter_feedback(current_guess)
        
        if not feedback:
            print("Ingen bokstav var korrekt, nytt test")
        elif all(status == 'right' for _, status in feedback):
            print(f"korrekt! order var '{current_guess}'.")
            return
        else:
            possible_words = refine_word_list_based_on_feedback(current_guess, feedback, possible_words)
            if not possible_words:
                print("inga fler ord..")
                return

        attempts += 1

    print("max försök... break")

wordle_bot(swedish_words)
