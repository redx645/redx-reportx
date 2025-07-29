import os
import time
import json
import random
import threading
from faker import Faker
from colorama import init, Fore, Style
from termcolor import colored
import pyfiglet
from tqdm import tqdm
from datetime import datetime

# === INIT ENV ===
init(autoreset=True)
fake = Faker()
LOG_DIR = "Red-X_logs"
os.makedirs(LOG_DIR, exist_ok=True)

# === GLOBAL CONFIG ===
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (Linux; Android 11; Pixel 5)"
]

REPORT_REASONS = [
    "spam", "nudity", "harassment", "violence",
    "fake_profile", "hate_speech", "impersonation", "misinformation"
]

CUSTOM_MESSAGES = [
    "This user is violating community rules.",
    "Inappropriate content found in posts.",
    "Account involved in suspicious activities.",
    "Impersonating another individual.",
    "Spamming stories with misleading content."
]

results = []

# === ANIMATED BANNER ===
def show_banner():
    banner1 = pyfiglet.figlet_format("Red-X Report", font="slant")
    banner2 = pyfiglet.figlet_format("", font="digital")
    for _ in range(2):
        for color in [Fore.RED, Fore.YELLOW, Fore.CYAN, Fore.MAGENTA, Fore.GREEN, Fore.BLUE]:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(Style.BRIGHT + color + banner1)
            print(Fore.WHITE + banner2)
            print(Fore.LIGHTMAGENTA_EX + "     Made by RedX_64     ".center(80))
            time.sleep(0.1)
    print(Fore.LIGHTYELLOW_EX + "="*80)
    print(Fore.CYAN + "Instagram Red-X Maas Report Tool".center(80))
    print(Fore.LIGHTYELLOW_EX + "="*80 + "\n")
    time.sleep(0.5)

# === REPORT FUNCTION ===
def simulate_report(username, thread_id, custom_gmail):
    ip = fake.ipv4()
    user_agent = random.choice(USER_AGENTS)
    reason = random.choice(REPORT_REASONS)
    message = random.choice(CUSTOM_MESSAGES)
    email = custom_gmail if custom_gmail else fake.email()

    time.sleep(random.uniform(0.3, 0.9))  # Simulate latency

    report = {
        "report_id": f"{thread_id}-{random.randint(1000,9999)}",
        "target": username,
        "reason": reason,
        "message": message,
        "reporter_email": email,
        "fake_ip": ip,
        "user_agent": user_agent,
        "timestamp": datetime.now().isoformat()
    }
    results.append(report)
    print(colored(f"[#{thread_id}] Reported @{username} | Reason: {reason} | From: {email}", "green"))

# === MASS REPORT FUNCTION ===
def mass_report(username, count, gmail_list):
    threads = []
    total_mails = len(gmail_list)
    print(Fore.YELLOW + f"\nUsing {total_mails} custom Gmail addresses...")
    print(Fore.YELLOW + f"Simulating {count} reports on @{username}...\n")

    for i in tqdm(range(count), desc=colored("Reporting Progress", "cyan")):
        custom_gmail = gmail_list[i % total_mails] if gmail_list else None
        t = threading.Thread(target=simulate_report, args=(username, i+1, custom_gmail))
        threads.append(t)
        t.start()
        time.sleep(0.05)

    for t in threads:
        t.join()

    log_file = os.path.join(LOG_DIR, f"report_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(log_file, "w") as f:
        json.dump(results, f, indent=2)
    print(Fore.LIGHTGREEN_EX + f"\nAll reports complete. Logs saved to {log_file}")

# === MAIN PROGRAM ===
if __name__ == "__main__":
    show_banner()
    target = input(Fore.LIGHTMAGENTA_EX + "Enter target Instagram username: ")
    count = int(input(Fore.LIGHTMAGENTA_EX + "How many reports to simulate?: "))

    print(Fore.LIGHTBLUE_EX + "\nEnter up to 20 custom Gmail addresses separated by commas.")
    custom_input = input(Fore.LIGHTCYAN_EX + "Leave blank to auto-generate: ").strip()

    if custom_input:
        gmail_list = [x.strip() for x in custom_input.split(",") if x.strip()]
        if len(gmail_list) > 20:
            gmail_list = gmail_list[:20]
            print(Fore.YELLOW + "Trimmed to first 20 Gmail addresses.")
    else:
        gmail_list = []

    mass_report(target, count, gmail_list)