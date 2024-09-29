import os
import socket
from threading import Thread
from collections import Counter


def correctness_score(guess, password):
    """
    Calculate the number of letters in 'guess' that are also in 'password'.

    Args:
        guess (str): The guessed password.
        password (str): The actual password.

    Returns:
        int: The number of matching letters between the guess and the password.
    """
    password_letters = set(password)
    return sum(1 for letter in guess if letter in password_letters)


def select_best_guess(possible_passwords):
    """
    Select the best guess from the possible passwords based on letter frequency.

    Args:
        possible_passwords (list): List of possible password strings.

    Returns:
        str: The password guess with the highest cumulative letter frequency.
    """
    # Count the frequency of each letter in all possible passwords
    letter_counts = Counter()
    for pw in possible_passwords:
        letter_counts.update(pw)

    # Choose the password with the highest total letter frequency score
    max_score = -1
    best_guess = None
    for pw in possible_passwords:
        score = sum(letter_counts[letter] for letter in set(pw))
        if score > max_score:
            max_score = score
            best_guess = pw
    return best_guess


def client():
    """
    Connect to the password server and attempt to guess the password.

    Uses feedback from the server to narrow down the list of possible passwords.
    """
    # Load possible passwords from the 'passwords.txt' file
    with open('passwords.txt', 'r') as f:
        passwords = [line.strip() for line in f if line.strip()]

    possible_passwords = passwords.copy()
    guesses_made = 0

    # Create a set of all letters in the possible passwords
    letters_in_passwords = set(''.join(possible_passwords))

    # Establish a connection to the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        server_address = ('127.0.0.1', 8881)
        client_socket.connect(server_address)
        successes = []

        try:
            while True:
                # Exit if no possible passwords remain
                if not possible_passwords:
                    print("No possible passwords remaining. Exiting.")
                    break

                # If only one password remains, use it as the guess
                if len(possible_passwords) == 1:
                    guess = possible_passwords[0]
                else:
                    # Select the best guess based on letter frequencies
                    guess = select_best_guess(possible_passwords)

                # Ensure the guess contains only valid letters
                guess = ''.join([letter for letter in guess if letter in letters_in_passwords])

                # Send the guess to the server
                print(f"Guess {guesses_made} - Sending prediction: {guess}")
                client_socket.send(guess.encode('utf-8'))
                guesses_made += 1

                # Receive feedback from the server
                feedback = client_socket.recv(1024).decode('utf-8')
                print(f"Received answer from server: {feedback} correct digits")

                # Check if the password is found
                correct_digits_count = int(feedback)
                if correct_digits_count == 20:
                    print("Success: Password found:", guess)
                    successes.append(guesses_made)
                    break

                # Filter possible passwords based on the feedback
                new_possible_passwords = []
                for pw in possible_passwords:
                    score = correctness_score(guess, pw)
                    if score == correct_digits_count:
                        new_possible_passwords.append(pw)
                possible_passwords = new_possible_passwords
                print(f"Possible passwords remaining: {len(possible_passwords)}")

                # Update the set of valid letters
                letters_in_passwords = set(''.join(possible_passwords))

                # Limit the number of guesses to prevent infinite loops
                if guesses_made >= 15:
                    print("Failed to find the password within 15 guesses")
                    break
        except Exception as e:
            print(e)


def run_server():
    """
    Start the password server by running the precompiled Python 3.8 bytecode file.
    """
    os.system("password_server.cpython-38.pyc > NUL 2>&1")


if __name__ == "__main__":
    # Create threads for the server and client
    server_thread = Thread(target=run_server)
    client_thread = Thread(target=client)

    # Start the server and client threads
    server_thread.start()
    client_thread.start()

    # Wait for both threads to complete
    server_thread.join()
    client_thread.join()
