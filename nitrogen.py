import random
import string
import requests
import time
import os
import sys
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Define the directory and file for caching generated strings and webhook URL
CACHE_DIR = "C:\\NirtoGen V3"
CACHE_FILE = os.path.join(CACHE_DIR, "cache.txt")
WEBHOOK_FILE = os.path.join(CACHE_DIR, "webhook.txt")

# Rainbow colors
RAINBOW_COLORS = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
ORANGE = "\033[38;5;214m"  # ANSI escape code for orange (approximation)

def ensure_cache_file():
    """Ensure the cache directory and files exist."""
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    if not os.path.isfile(CACHE_FILE):
        with open(CACHE_FILE, 'w') as f:
            f.write("")  # Create an empty cache file
    if not os.path.isfile(WEBHOOK_FILE):
        with open(WEBHOOK_FILE, 'w') as f:
            f.write("")  # Create an empty webhook file

def load_cache():
    """Load existing codes from the cache file."""
    try:
        with open(CACHE_FILE, 'r') as f:
            return set(line.strip() for line in f.readlines())
    except FileNotFoundError:
        return set()

def load_webhook():
    """Load the existing webhook URL from the webhook file."""
    try:
        with open(WEBHOOK_FILE, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""

def save_webhook(url):
    """Save a new webhook URL to the webhook file."""
    with open(WEBHOOK_FILE, 'w') as f:
        f.write(url)

def save_to_cache(code):
    """Save a new code to the cache file."""
    with open(CACHE_FILE, 'a') as f:
        f.write(code + "\n")

def rainbow_print(text):
    for char in text:
        color = random.choice(RAINBOW_COLORS)
        print(color + char, end='', flush=True)
    print(Style.RESET_ALL)

def green_print(text):
    print(Fore.GREEN + text + Style.RESET_ALL)

def orange_print(text):
    print(ORANGE + text + Style.RESET_ALL)

def generate_random_string(length=18):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

def check_gift_code(code):
    url = f"https://discordapp.com/api/v9/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true"
    response = requests.get(url)
    return response.status_code == 200

def send_to_webhook(code):
    data = {
        "content": f"Valid gift code found: {code}"
    }
    
    # Load the webhook URL from the file
    webhook_url = load_webhook()
    
    if webhook_url:  # Only send if a valid URL is present
        requests.post(webhook_url, json=data)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_lock_ascii():
    lock_ascii = """
      __________
     /\____;;___\\
    | /         /
    `. ())oo() .
     |\(%()*^^()^\\
    %| |-%-------|
   % \ | %  ))   |
   %  \|%________|
    """"""""""""
    """
    green_print(lock_ascii)

def print_nitrogen_ascii():
    nitrogen_ascii = """
 _   _ _ _                              __     ______  _                   _    _        
| \ | (_) |                             \ \   / /___ \| |                 | |  | |       
|  \| |_| |_ _ __ ___   __ _  ___ _ __   \ \ / /  __) | |__  _   _    __ _| | _| | _____ 
| . ` | | __| '__/ _ \ / _` |/ _ \ '_ \   \ V /  |__ <| '_ \| | | |  / _` | |/ / |/ / _ \\
| |\  | | |_| | | (_) | (_| |  __/ | | |   \ /   ___) | |_) | |_| | | (_| |   <|   <  __/
|_| \_|_|\__|_|  \___/ \__, |\___|_| |_|    \_/  |____/|_.__/ \__, |  \__,_|_|\_\_|\_\___|
                        __/ |                                  __/ |                      
                       |___/                                  |___/                       
    """
    rainbow_print(nitrogen_ascii)

def print_menu():
    orange_print("\n1. Start")
    orange_print("2. Exit")
    orange_print("\n3. Enter new Webhook URL")
    
def run_program():
    # Load existing codes from cache
    existing_codes = load_cache()
    
    while True:
        clear_screen()
        print_nitrogen_ascii()
        rainbow_print("\nRunning...\n")
        
        # Generate a unique code
        while True:
            code = generate_random_string()
            if code not in existing_codes:
                existing_codes.add(code)  # Add to set for uniqueness check
                save_to_cache(code)       # Save to cache file
                break
        
        result = check_gift_code(code)
        rainbow_print(f"Code: {code}")
        rainbow_print(f"Valid: {result}")
        
        if result:
            send_to_webhook(code)
        
        time.sleep(1)

def password_prompt():
    password = "aksus"
    attempts = 3
    while attempts > 0:
        clear_screen()
        print_lock_ascii()
        green_print("\nEnter password: ")
        user_input = input()
        if user_input == password:
            return True
        else:
            attempts -= 1
            green_print(f"\nIncorrect password. {attempts} attempts remaining.")
            time.sleep(1)
    return False

def main():
    ensure_cache_file()  # Ensure the cache directory and files exist
    
    if not password_prompt():
        green_print("Access denied. Exiting...")
        return

    while True:
        clear_screen()
        print_nitrogen_ascii()
        
        # Load existing webhook URL and prompt user for action
        current_webhook = load_webhook()
        
        if current_webhook:
            green_print(f"Current Webhook URL: {current_webhook}")
        
        print_menu()
        
        choice = input().strip()
        
        if choice == '1':
            run_program()
            
        elif choice == '2':
            rainbow_print("Exiting...")
            break
            
        elif choice == '3':
            green_print("Enter new Webhook URL:")
            new_webhook_url = input().strip()
            save_webhook(new_webhook_url)  # Save new webhook URL to file
            green_print("Webhook URL updated successfully.")
            time.sleep(2)
            
        else:
            rainbow_print("Invalid choice. Please try again.")
            time.sleep(1)

if __name__ == "__main__":
    main()