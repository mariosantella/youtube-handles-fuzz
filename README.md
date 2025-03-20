# YouTube names Checker/Fuzzer

## Overview

This tool allows you to bulk-check the availability of YouTube usernames by simulating web requests for **Open Source Intelligence (OSINT)** purposes. The script scans through a range of possible usernames based on a given base name and records their status in a CSV file.

### Why is this useful for OSINT?

Many users create YouTube accounts using their real **name and surname** (e.g., `johnsmith0001`). By fuzzing different numeric variations, this tool helps uncover:

- **Hidden or lesser-known profiles** linked to a real-world identity.
- **Aliases used across different platforms**, assisting in digital footprint mapping.
- **YouTube Channel IDs**, which can be used to analyze user activity.
- **Potential connections through public subscription data**.

### Features

- **Bulk username checking:** Tests up to 10000 variations of a base username (e.g., `username0000` to `username9999`).
- **Randomized checks:** Usernames are checked in a shuffled order to prevent detection.
- **Automated session limits:** Stops after 1000 requests to allow VPN/IP rotation.
- **Resumable execution:** Avoids re-checking usernames already stored in the CSV.
- **Rotating User-Agents:** Uses different browser fingerprints to avoid detection.
- **Progress updates:** Displays progress every 0.5% of completion.
- **Listing mode:** View all previously found usernames that exist on YouTube.
- **Extracting YouTube Channel ID:** The username’s page contains the **YouTube Channel ID**, which can be used with [this tool](https://xxluke.de/subscription-history/) to check all public subscriptions of the user (if privacy settings allow it).

## OSINT Use Cases

This tool is particularly valuable for **Open Source Intelligence (OSINT)** investigations, as it helps:

- **Identify YouTube accounts linked to real identities.**
- **Extract and track YouTube Channel IDs for further analysis.**
- **Uncover username variations used on other platforms.**
- **Cross-reference YouTube profiles with other social media or leaked databases.**
- **Leverage public subscription data to map a user’s interests and connections.**

## Installation

## Usage

### Scan Mode

To start scanning usernames:

This will generate all usernames from `namesurname0000` to `namesurname9999` and check their availability on YouTube.

### List Found Users

To display previously found usernames:

This will print all usernames that returned an HTTP 200 response, indicating that they exist on YouTube.

## Output

Results are saved in a CSV file named:

The format is:

Example:

## Privacy Considerations

- The tool does not bypass any security or authentication.
- The YouTube usernames found may contain a **YouTube Channel ID**, which can be used with [xxluke.de](https://xxluke.de/subscription-history/) to see all publicly visible subscriptions of that user (if allowed by YouTube’s privacy policy).

## Disclaimer

This tool is intended for **ethical research purposes only**. Use responsibly and in compliance with YouTube’s **Terms of Service** and **Privacy Policy**.
