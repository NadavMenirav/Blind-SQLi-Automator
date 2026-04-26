# 🕵️‍♂️ Blind SQLi Automator

A Python script developed for an academic cybersecurity assignment to automate the extraction of data using Blind SQL Injection.

## 🎯 Overview
This repository contains a single, focused Python script (`main.py`) designed to solve a Blind SQL Injection challenge. Manually guessing database parameters via the browser is exhausting and error-prone. This script automates the process by sending iterative logical queries to the server and analyzing the responses.

## ✨ Features
* **Length Detection:** Automatically calculates the exact length of hidden database elements (e.g., table names).
* **Data Extraction:** Extracts encrypted strings (like MD5 hashes) character by character.
* **Session Management:** Utilizes a `PHPSESSID` cookie to maintain an authenticated user session during the attack.

## ⚠️ Disclaimer
This script was written purely for **educational purposes** as part of a university assignment. It is designed to be run against a local, legally provided vulnerable environment (`localhost`). **Do not** use this script against any system or network you do not own or do not have explicit authorization to test.

## 🚀 Usage
1. Clone the repository.
2. Open `main.py` and replace `"INSERT_YOUR_COOKIE_HERE"` with your active `PHPSESSID` cookie.
3. Run the script:
   ```bash
   python main.py