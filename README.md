# KivaNet Auto Bot

This script automates the process of logging into KivaNet, retrieving Bearer tokens, and performing mining operations while rotating proxies for anonymity.

# Register Here
 - [Kivanet](https://kivanet.com/register.html?code=E2MIIX)
 - Use my code **E2MIIX**

## Features
- Supports **multiple accounts** from `accounts.txt`
- Automatic fetches **Bearer tokens** and stores them in `tokens.txt`
- Uses **rotating proxies** from `proxies.txt`
- Periodically fetches **user balance and nickname**
- Automatically **switches proxies** if a failure occurs
- Supports **mining automation**

## Installation
1. **Install Python if not already installed.**
2. **Clone this repository:**
   ```bash
   git clone https://github.com/kelliark/Kivanet-AutoBot
   cd Kivanet-AutoBot
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

## Usage
1. Add account credentials in `accounts.txt` (Format: `email:password`, one per line).
2. Add proxies in `proxies.txt` (Format: `protocol://username:password@host:port`, one per line).
3. Run the script:
   ```sh
   python main.py
   ```

## File Descriptions
- `main.py` - The core script that handles authentication, token retrieval, and mining.
- `requirements.txt` - Lists dependencies required to run the script.
- `tokens.txt` - Stores active Bearer tokens.
- `accounts.txt` - Stores account credentials.
- `proxies.txt` - Stores proxy list for rotating connections.

## Notes
- Ensure that `accounts.txt` and `proxies.txt` are properly formatted.
- This script automatically switches proxies when failures occur.
- The balance and nickname are updated **every minute**.

## Disclaimer
This script is for educational purposes only. Use at your own risk!
