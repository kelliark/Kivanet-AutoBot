import requests
import hashlib
import json
import random
import time
from fake_useragent import UserAgent
from termcolor import colored

def load_proxies(file_path="proxies.txt"):
    try:
        with open(file_path, "r") as f:
            proxies = [line.strip() for line in f if line.strip()]
            return proxies if proxies else [None]  # If empty, use direct connection
    except FileNotFoundError:
        return [None]  # Proceed without proxies if file is missing

def load_accounts(file_path="accounts.txt"):
    accounts = []
    with open(file_path, "r") as f:
        for line in f:
            parts = line.strip().split(":")
            if len(parts) == 2:
                accounts.append({"email": parts[0], "password": parts[1]})
    return accounts

def save_tokens(tokens, file_path="tokens.txt"):
    with open(file_path, "w") as f:
        for token in tokens:
            if token.startswith("ey"):
                f.write(f"{token}\n")
    print(colored("All tokens saved successfully!", "green"))

def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

def get_proxy_ip(proxy):
    if not proxy:
        return "Direct Connection"
    try:
        proxies = {"http": proxy, "https": proxy}
        response = requests.get("http://ip-api.com/json", proxies=proxies, timeout=5)
        if response.status_code == 200:
            return response.json().get("query", "Unknown")
    except requests.RequestException:
        return "Unknown"
    return "Unknown"

def send_request_with_proxy(url, headers, proxies, method="GET", data=None):
    for _ in range(len(proxies)):
        proxy = random.choice(proxies)
        proxy_config = {"http": proxy, "https": proxy} if proxy else None
        try:
            if method == "POST":
                response = requests.post(url, headers=headers, json=data, proxies=proxy_config, timeout=10)
            else:
                response = requests.get(url, headers=headers, proxies=proxy_config, timeout=10)
            
            if response.status_code == 200:
                return response
        except requests.RequestException:
            if proxy:
                print(colored(f"Proxy failed: {proxy}, switching to another proxy...", "red"))
    return None

def get_bearer_token(email, password, proxies):
    url = "https://app.kivanet.com/api/user/login"
    hashed_password = hash_password(password)
    payload = {"email": email, "password": hashed_password}
    ua = UserAgent()
    headers = {"Content-Type": "application/json", "Accept": "application/json", "User-Agent": ua.random}
    response = send_request_with_proxy(url, headers, proxies, method="POST", data=payload)
    if response:
        data = response.json()
        if data.get("state") and "object" in data:
            return data["object"].replace("Bearer ", "")
    return None

def fetch_user_info(token, proxies):
    url = "https://app.kivanet.com/api/user/getUserInfo"
    headers = {"Authorization": f"Bearer {token}", "User-Agent": UserAgent().random}
    response = send_request_with_proxy(url, headers, proxies)
    if response:
        return response.json().get("object", {}).get("nickName", "Unknown")
    return "Unknown"

def fetch_balance(token, proxies):
    url = "https://app.kivanet.com/api/user/getMyAccountInfo"
    headers = {"Authorization": f"Bearer {token}", "User-Agent": UserAgent().random}
    response = send_request_with_proxy(url, headers, proxies)
    if response:
        return response.json().get("object", {}).get("balance", "0")
    return "0"

def fetch_all_tokens(accounts, proxies):
    tokens = []
    for account in accounts:
        token = get_bearer_token(account["email"], account["password"], proxies)
        if token:
            tokens.append(token)
        else:
            print(colored(f"Failed to fetch token for {account['email']}", "red"))
    save_tokens(tokens)
    return tokens

def start_mining(token, proxies):
    url = "https://app.kivanet.com/api/user/sign"
    headers = {"Authorization": f"Bearer {token}", "User-Agent": UserAgent().random, "Content-Type": "application/json"}
    response = send_request_with_proxy(url, headers, proxies, method="POST")
    if response:
        print(colored("Mining started successfully!", "green"))
    else:
        print(colored("Failed to start mining with available proxies.", "red"))

def mine_tokens(tokens, proxies):
    while True:
        print(colored("=== Starting Mining Process ===", "cyan"))
        for token in tokens:
            proxy = random.choice(proxies)
            proxy_ip = get_proxy_ip(proxy)
            nickname = fetch_user_info(token, proxies)
            balance = fetch_balance(token, proxies)
            print(colored(f"User: {nickname} | Balance: {balance} Kiva | Proxy IP: {proxy_ip}", "yellow"))
            start_mining(token, proxies)
            time.sleep(random.randint(5, 15))
        print(colored("=== Mining Cycle Completed ===", "cyan"))
        time.sleep(60)  # Update every 1 minute

if __name__ == "__main__":
    proxies = load_proxies()
    accounts = load_accounts()
    tokens = fetch_all_tokens(accounts, proxies)
    if tokens:
        mine_tokens(tokens, proxies)
