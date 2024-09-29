# Password Hunter

**Password Hunter** is a project that implements a password-guessing client communicating with a server to find a secret password. The client uses a letter frequency analysis algorithm to efficiently guess the password by narrowing down possible options based on feedback from the server.

**Note:** This project requires **Python 3.8** due to the use of a precompiled server bytecode file specific to Python 3.8.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Exercise Rules](#exercise-rules)
- [How It Works](#how-it-works)
- [Notes](#notes)
- [Troubleshooting](#troubleshooting)

## Features

- Client and server communication using TCP sockets.
- Efficient password guessing using letter frequency analysis.
- Multi-threaded execution to run the client and server simultaneously.
- Adheres to specific exercise rules for password changes.

## Requirements

- Python 3.8
- The `passwords.txt` file (included in the repository).
- The precompiled server bytecode file `password_server.cpython-38.pyc` (included in the repository).

## Setup

1. **Ensure Python 3.8 is installed** on your system. You can download it from the [official Python website](https://www.python.org/downloads/release/python-380/).

2. **Clone the Repository:**

   ```bash
   git clone https://github.com/Itay01/Password-Hunter.git
   cd Password-Hunter
   ```

3. **Verify the Files:**

   - Confirm that `main.py`, `passwords.txt`, and `password_server.cpython-38.pyc` are present in the root directory of the cloned repository.
   - `main.py` is the main script to run the client and server.
   - `passwords.txt` contains the list of possible passwords.
   - `password_server.cpython-38.pyc` is the precompiled server file required for the server to run.

## Usage

Run the script using Python 3.8:

```bash
python main.py
```

The client will attempt to guess the password by communicating with the server. It will output its guesses and feedback from the server until it finds the correct password or reaches the maximum number of allowed guesses.

## Exercise Rules

- **Password Rotation:**
  - The server changes the password every **30 seconds**.
  - After **15 incorrect guesses**, the password changes.
  - If you guess a password that is **not in `passwords.txt`**, the password changes immediately.

- **Guessing Constraints:**
  - You have a maximum of **15 guesses** to find the correct password before it changes.
  - Ensure that all guesses are passwords listed in `passwords.txt`.

- **Feedback Mechanism:**
  - The server provides feedback by indicating the number of correct characters in your guess.
  - **If the server returns that there are **20 correct digits**, it means your guess is **correct**.**
  - Use this feedback to refine your next guess.

## How It Works

- **Client (`main.py`):**
  - Reads possible passwords from `passwords.txt`.
  - Uses a letter frequency algorithm to select the best guess.
  - Sends the guess to the server and receives feedback on the number of correct characters.
  - Narrows down the list of possible passwords based on the feedback.
  - Repeats the process until the password is found or the guess limit is reached.

- **Server (`password_server.cpython-38.pyc`):**
  - Runs in a separate thread initiated by `main.py`.
  - Selects a secret password from `passwords.txt` and changes it based on the exercise rules.
  - Receives password guesses from the client.
  - Compares the guess to the secret password.
  - Sends back the number of correct characters.

## Notes

- The server runs a precompiled bytecode file specific to Python 3.8. This is why the script must be run with Python 3.8.
- The script uses multi-threading to run the client and server simultaneously.

## Troubleshooting

- **Python Version Error:** If you receive errors related to Python versions, ensure that you're using Python 3.8.
- **Missing Files:** Make sure that `main.py`, `passwords.txt`, and `password_server.cpython-38.pyc` are present in the script's directory.
- **Permissions:** Ensure you have the necessary permissions to execute the script and the server file.
- **Network Issues:** If the client cannot connect to the server, check that no other processes are using port `8881` and that your firewall settings allow for local socket connections.
- **Password Not Found:** If the client fails to find the password within the allowed guesses or time, it may be due to the password changing. Restart the script and try again.
