import csv
import os
import random
import subprocess
import re
import time
import argparse
from concurrent.futures import ThreadPoolExecutor

def generate_usernames(base_name):
    """Generate a shuffled list of usernames with numeric suffixes from 0000 to 9999."""
    numbers = list(range(10000))
    random.shuffle(numbers)
    return [f"{base_name}{str(num).zfill(4)}" for num in numbers]

def load_checked_users(csv_filename):
    """Load previously checked usernames from a CSV file to avoid duplicates."""
    checked_users = {}
    if os.path.exists(csv_filename):
        with open(csv_filename, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header
            for row in reader:
                if len(row) >= 5:
                    checked_users[row[0]] = (row[1], row[2], row[3], row[4])  # Status, HTTP Code, Title, Timestamp
    return checked_users

def save_result(csv_filename, username, status, http_code, title):
    """Save the result of a username check to the CSV file."""
    timestamp = int(time.time())
    with open(csv_filename, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([username, status, http_code, title, timestamp])

def list_found_users(csv_filename):
    """List all usernames that returned HTTP 200 (found)."""
    if not os.path.exists(csv_filename):
        print("No data available.")
        return
    
    with open(csv_filename, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)  # Skip header
        found_users = [row[0] for row in reader if row[2] == "200"]
    
    if found_users:
        print("Found usernames:")
        for user in found_users:
            print(user)
    else:
        print("No usernames found.")

def get_http_status_and_title(username):
    """Perform a YouTube username availability check using wget."""
    url = f"https://www.youtube.com/@{username}"
    user_agent = get_random_user_agent()
    command = [
        "wget", "--spider", "--server-response", "--max-redirect=5",
        f"--user-agent={user_agent}", "--header=Cookie: CONSENT=YES+", url
    ]
    result = subprocess.run(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    output = result.stderr + result.stdout
    
    status_match = re.findall(r"HTTP/\d\.\d (\d{3})", output)
    http_code = status_match[-1] if status_match else "Unknown"
    
    title_match = re.search(r"<title>(.*?)</title>", output, re.IGNORECASE)
    title = title_match.group(1) if title_match else ""
    
    status = "available" if http_code == "404" else "not_found" if http_code == "403" else "taken"
    
    return username, status, http_code, title

def get_random_user_agent():
    """Return a randomly chosen user agent string."""
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/119.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/119.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/119.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/118.0.0.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Edge/118.0.0.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/118.0.0.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
    ]
    return random.choice(user_agents)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["scan", "list"], help="Choose mode: 'scan' to check usernames, 'list' to display found usernames.")
    parser.add_argument("username_base", help="Base username to generate variations")
    args = parser.parse_args()
    
    csv_filename = f"checked_users_{args.username_base}.csv"
    
    if args.mode == "list":
        list_found_users(csv_filename)
        return
    
    base_name = args.username_base.strip()
    checked_users = load_checked_users(csv_filename)
    usernames = generate_usernames(base_name)
    
    usernames_to_check = [user for user in usernames if user not in checked_users]
    total = len(usernames)
    completed = total - len(usernames_to_check)
    last_reported_progress = 0
    
    print(f"{completed}/{total} completed [{(completed/total)*100:.2f}%]")
    
    if not usernames_to_check:
        print("All username combinations have been checked. No more usernames to test.")
        return
    
    batch_size = 1000
    session_requests = 0  # Counter for the current session's requests
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        for i in range(0, len(usernames_to_check), 10):
            batch = usernames_to_check[i:i+10]
            results = list(executor.map(get_http_status_and_title, batch))
            
            for username, status, http_code, title in results:
                save_result(csv_filename, username, status, http_code, title)
                session_requests += 1
                completed += 1
                
                progress = (completed / total) * 100
                if progress - last_reported_progress >= 0.5:
                    print(f"Progress: {completed}/{total} [{progress:.2f}%]", flush=True)
                    last_reported_progress = progress
                
                if session_requests >= batch_size:
                    print("Reached the limit of 1000 requests for this session. Change VPN and restart the script.")
                    return
            
            time.sleep(1)  # Minimal delay to prevent blocks
    
    print("Scanning complete! All usernames have been checked.")

if __name__ == "__main__":
    main()
