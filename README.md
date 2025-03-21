# YouTube Username Checker/Fuzzer

## Overview
This tool helps perform **Open Source Intelligence (OSINT)** by checking the availability of YouTube usernames in bulk. It generates usernames using a **name + numeric suffix** pattern (e.g., `johnsmith0000` to `johnsmith9999`) and checks if they exist on YouTube. Results are saved in a CSV file for easy reference.

![Preview](ytckeck.gif)

### Why is this useful for OSINT?
- **Identify hidden YouTube profiles** linked to real identities.
- **Track username variations** used across different platforms.
- **Extract YouTube Channel IDs** for further research.
- **Analyze public subscriptions** of discovered accounts via [xxluke.de](https://xxluke.de/subscription-history/).

## Features
- **Bulk username generation** (10,000 combinations per search).
- **Randomized order** to reduce detection risks.
- **Rotating User-Agents** for stealth.
- **Session limit (1,000 requests)** to prevent IP bans.
- **Resumable execution** (skips usernames already checked).
- **Progress updates** every 0.5%.
- **List found usernames** using a separate command.

---

## Installation
### Prerequisites
- Python 3.x
- `wget` installed on your system

### Clone the Repository
```sh
git clone https://github.com/yourrepo/youtube-username-checker.git
cd youtube-username-checker
```

### Verify Python Installation
```sh
python3 --version
```

---

## Usage
### Check for YouTube Usernames
To scan usernames:
```sh
python3 ytcheck.py scan <namesurname>
```
Example:
```sh
python3 ytcheck.py scan johnsmith
```
This generates all usernames from `johnsmith0000` to `johnsmith9999` and checks their availability on YouTube.

### List Found Users
To display previously found usernames:
```sh
python3 ytcheck.py list <namesurname>
```
Example:
```sh
python3 ytcheck.py list johnsmith
```
This prints all usernames that returned an HTTP 200 response, meaning they exist on YouTube.

---

## Output
Results are saved in:
```
checked_users_<namesurname>.csv
```

### CSV Format:
```
username,status,http_code,title,timestamp
```
Example:
```
johnsmith0000,not_found,404,,1742395130
johnsmith8732,taken,200,John Smith's Channel,1742395145
```
Each entry includes:
- **username**: The tested username
- **status**: Available, not found, or taken
- **http_code**: HTTP response code
- **title**: YouTube page title (if available)
- **timestamp**: Unix timestamp of the request

---

## OSINT & Privacy Considerations
- **Extract YouTube Channel IDs**: Found pages contain a unique **YouTube Channel ID**, which can be used with [xxluke.de](https://xxluke.de/subscription-history/) to check public subscriptions (if privacy settings allow it).
- **Ethical Use Only**: This tool does **not** bypass security measures and must be used responsibly.

---

## Disclaimer
This tool is intended for **ethical research purposes only**. Use responsibly and in compliance with YouTube’s **Terms of Service** and **Privacy Policy**.
